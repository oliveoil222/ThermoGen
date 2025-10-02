# notify.py
import time
from PySide6.QtCore import QThread, Signal

# optional hardware libs - wrapped in try/except so code can simulate if not present
try:
    import pyvisa
except Exception:
    pyvisa = None

try:
    import nidaqmx
    import nidaqmx.constants as ni_consts
except Exception:
    nidaqmx = None
    ni_consts = None

try:
    import serial
except Exception:
    serial = None


class Worker(QThread):
    """
    Background worker that:
    - reads temperature from NI-DAQ if available, otherwise simulates,
    - controls Sorensen DCS80-13E via PyVISA if available, otherwise simulates,
    - simulates pressure adjustments,
    - emits a single finished signal with "success", "unsafe" or "timeout".
    """

    finished = Signal(str)

    def __init__(self, currentTemp, currentPres, desiredTemp, desiredPres,
                 sorensen_addr=None, daq_channel=None, pres_serial_port=None, parent=None):
        super().__init__(parent)
        self.currentTemp = float(currentTemp)
        self.currentPres = float(currentPres)
        self.desiredTemp = float(desiredTemp)
        self.desiredPres = float(desiredPres)

        # optional addresses / channels
        self.sorensen_addr = sorensen_addr
        self.daq_channel = daq_channel
        self.pres_serial_port = pres_serial_port

        # hardware handles
        self._visa_inst = None
        self._daq_task = None
        self._serial_handle = None

        # operational constants
        self.MAX_VOLTAGE = 10.0
        self.MIN_VOLTAGE = 0.0
        self.MAX_ITERATIONS = 2000
        self.SLEEP_INTERVAL = 0.1

        # controller gain WILL NEED TO TUNE LATER
        self.KP = 0.5

        # initialize hardware if possible
        self._try_init_hardware()

    # hardware initialization
    def _try_init_hardware(self):
        # try pyvisa for Sorensen
        if pyvisa:
            try:
                rm = pyvisa.ResourceManager()
                # if a specific address provided, try it; otherwise try to find an instrument
                if self.sorensen_addr:
                    self._visa_inst = rm.open_resource(self.sorensen_addr)
                else:
                    # try to auto detect a visa resource that looks like a power supply
                    resources = rm.list_resources()
                    # default pick first GPIB or USB resource available WILL NEED TO UPDATE ONCE KNOW ACTUAL PORT
                    chosen = None
                    for r in resources:
                        if "GPIB" in r or "USB" in r or "ASRL" in r:
                            chosen = r
                            break
                    if chosen:
                        self._visa_inst = rm.open_resource(chosen)
                # if instrument opened might want to query ID
                # if self._visa_inst:
                #     try:
                #         idn = self._visa_inst.query("*IDN?")
                #         print("Connected to:", idn)
                #     except Exception:
                #         pass
            except Exception:
                self._visa_inst = None

        # try nidaqmx for daq thermocouple reading
        if nidaqmx and self.daq_channel:
            try:
                # create and keep a short lived task on each read to be robust
                # no persistent object stored here read function will create task when needed
                pass
            except Exception:
                self._daq_task = None

        # try pyserial for pressure gauge
        if serial and self.pres_serial_port:
            try:
                self._serial_handle = serial.Serial(self.pres_serial_port, timeout=1)
            except Exception:
                self._serial_handle = None

    # utility: clamp and scale
    def _clamp(self, value, lo, hi):
        return max(lo, min(hi, value))

    # reading temperature
    def _read_temperature(self):
        """
        Try to read thermocouple temperature from DAQ; fallback to simulated reading.
        Returns float
        """
        # if nidaqmx available and a channel configured attempt a read
        if nidaqmx and self.daq_channel:
            try:
                # create a temporary task to read one sample
                with nidaqmx.Task() as task:
                    # add thermocouple channel type can be changed as needed.
                    # the exact signature may need to be tuned to the DAQ wiring & thermocouple type
                    task.ai_channels.add_ai_thrmcpl_chan(self.daq_channel, min_val=-200.0, max_val=3000.0,
                                                         thermocouple_type=ni_consts.ThermocoupleType.K,
                                                         units=ni_consts.TemperatureUnits.DEG_C)
                    # read one sample
                    temp = task.read()
                    # task context will close automatically
                    return float(temp)
            except Exception as e:
                # if any error fall through to simulation
                print("DAQ read failed or not configured, simulating temp. Error:", e)

        # simulation fallback:
        # return the last known temperature
        # in the control loop still update currentTemp based on applied voltage
        return float(self.currentTemp)

    # writing voltage to Sorensen
    def _set_sorensen_voltage(self, voltage):
        """
        Try to set the Sorensen output voltage. If hardware not present, update simulated internal state.
        WARNING: SCPI/command syntax can vary; verify commands from the instrument manual.
        This implementation uses generic VOLT <value> and turns output on.
        """
        voltage = self._clamp(voltage, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        if self._visa_inst:
            try:
                # many bench supplies respond to VOLT {value} or VOLTage {value}
                # and OUTP ON to enable the output adjust if the instrument uses different CLI
                try:
                    self._visa_inst.write(f"VOLT {voltage}")
                except Exception:
                    # try alternate command
                    self._visa_inst.write(f"VOLTage {voltage}")
                # enable output
                try:
                    self._visa_inst.write("OUTP ON")
                except Exception:
                    pass
            except Exception as e:
                print("Failed to write to Sorensen via VISA:", e)
                # fall through to simulation
                self._simulate_voltage_effect(voltage)
        else:
            # simulation update internal applied voltage state and apply thermal response later
            self._simulate_voltage_effect(voltage)


    # simulation helpers
    def _simulate_voltage_effect(self, voltage):
        """
        Simple thermal model:
        - Higher voltage => increases temperature gradually
        - Lower voltage => temperature drifts down slowly towards ambient
        This is a very rough simulation to allow testing without hardware.
        """
        # map voltage to temperature effect THIS IS ARBITRARY SCALING FOR SIMULATION ONLY
        ambient = 25.0
        max_temp_sim = 1000.0
        target_temp_from_voltage = ambient + (voltage / (self.MAX_VOLTAGE + 1e-9)) * (max_temp_sim - ambient)
        print("test temp")
        # simulate update move currentTemp fractionally toward target_temp_from_voltage
        # how fast temperature reacts to voltage
        blend = 0.05  
        self.currentTemp = round(self.currentTemp + (target_temp_from_voltage - self.currentTemp) * blend, 2)

    # Pressure simulation
    def adjust_pressure_sim(self, current, desired):
        """step based adjuster used for pressure simulation"""
        diff = abs(current - desired)
        step = 10.0
        if diff > 100:
            step = 10.0
        elif diff > 10:
            step = 1.0
        elif diff > 1:
            step = 0.1
        elif diff == 0:
            step = 0.0
        print("test pressure")
        if current < desired:
            current += step
            if current > desired:
                current = desired
        elif current > desired:
            current -= step
            if current < desired:
                current = desired

        return round(current, 2)

    # main control loop
    def check_condition(self):
        """
        Control loop:
        - read actual temperature
        - compute a simple proportional control action to move temperature toward desired
        - write voltage to Sorensen or simulate effect
        - update/simulate pressure as before
        - terminate with "success"/"unsafe"/"timeout" appropriately
        """
        iterations = 0
        applied_voltage = 0.0

        while iterations < self.MAX_ITERATIONS:
            iterations += 1

            # read temperature
            measured_temp = self._read_temperature()
            # if measuring via NI update internal record otherwise measured_temp is last known or simulated
            self.currentTemp = float(measured_temp)

            # compute control action
            error = self.desiredTemp - self.currentTemp
            voltage_delta = self.KP * error
            applied_voltage = self._clamp(applied_voltage + voltage_delta, self.MIN_VOLTAGE, self.MAX_VOLTAGE)

            # apply voltage to sorensen
            self._set_sorensen_voltage(applied_voltage)

            # if used actual DAQ read of thermocouple the measured_temp will reflect real reading
            # For simulation, _set_sorensen_voltage calls _simulate_voltage_effect which updates self.currentTemp.

            # simulate/update pressure as before
            self.currentPres = self.adjust_pressure_sim(self.currentPres, self.desiredPres)

            print(f"[Iter {iterations}] Measured Temp: {self.currentTemp} | Applied V: {applied_voltage} | Measured Pres: {self.currentPres}")

            # unsafe environment check
            if self.currentTemp > 1000.0 or self.currentPres > 1000.0:
                # emit unsafe and stop
                self.finished.emit("unsafe")
                return

            # check success condition
            temp_close = abs(self.currentTemp - self.desiredTemp) <= max(0.01, 0.01 * abs(self.desiredTemp))
            pres_close = abs(self.currentPres - self.desiredPres) <= max(0.01, 0.01 * abs(self.desiredPres))

            if temp_close and pres_close:
                self.finished.emit("success")
                return

            time.sleep(self.SLEEP_INTERVAL)

        # if loop exits due to iterations
        self.finished.emit("timeout")

    # QThread run override
    def run(self):
        try:
            self.check_condition()
        except Exception as e:
            print("Worker encountered an exception:", e)
            # in case of unexpected exception signal timeout/failure
            self.finished.emit("timeout")
