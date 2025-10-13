import pyvisa
import pyvisa_sim

class TemperatureWriter:
    def __init__(self):
        self.rm = pyvisa.ResourceManager('default.yaml@sim')
        print(self.rm.list_resources())
        self.instrument = self.rm.open_resource('ASRL1::INSTR')
        print(self.instrument.query("*IDN?"))
        print(self.instrument.query("MEAS:CURR?"))
        print(self.instrument.query("MEAS:VOLT?"))
        print(self.instrument.query("SOUR:CURR 10.00"))
        print(self.instrument.query("SOUR:VOLT 5.00"))
        print(self.instrument.query("MEAS:CURR?"))
        print(self.instrument.query("MEAS:VOLT?"))