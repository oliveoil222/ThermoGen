import pyvisa
import pyvisa_sim

class TemperatureWriter:
    def __init__(self):
        self.rm = pyvisa.ResourceManager('default.yaml@sim')
        # print(self.rm.list_resources())
        self.instrument = self.rm.open_resource('ASRL1::INSTR')
        # print(self.instrument.query("*IDN?"))
        # print(self.instrument.query("MEAS:CURR?"))
        # print(self.instrument.query("MEAS:VOLT?"))
        # print(self.instrument.query("SOUR:CURR 10.00"))
        # print(self.instrument.query("SOUR:VOLT 5.00"))
        # print(self.instrument.query("MEAS:CURR?"))
        # print(self.instrument.query("MEAS:VOLT?"))

    def temp_to_volt(self, temp):
        # 0V ~= 25C
        # 80V ~= 1000C (assumption, need to confirm)
        volt = ((80.0 * temp) /1000.0) - 2.0
        volt = round(volt, 2)

        if volt < 0:
            return 0
        elif volt > 80:
            return 80

        return volt

    def write_volt(self, volt):
        return self.instrument.query("SOUR:VOLT " + str(volt))

    def read_volt(self):
        volt_str = self.instrument.query("MEAS:VOLT?")
        volt_float = float(volt_str)
        return volt_float
