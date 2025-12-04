import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
import numpy as np
import threading

class TemperatureReader:
    def __init__(self, inputDevice):
        self.task = nidaqmx.Task()
        self.inputDevice = inputDevice
        self.reader = None
        self.data = None
        self.thread = threading.Thread(target=self.start_read)
        self.thread.daemon = True
        self.thread.start()


    def start_read(self):
        with self.task as task:
            task.ai_channels.add_ai_thrmcpl_chan(self.inputDevice + "/ai0", min_val=-10, max_val=20, units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
            task.ai_channels.add_ai_thrmcpl_chan(self.inputDevice + "/ai1", min_val=-10, max_val=20, units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
            task.ai_channels.add_ai_thrmcpl_chan(self.inputDevice + "/ai2", min_val=-10, max_val=20, units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)

            task.timing.cfg_samp_clk_timing(rate=8, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=100)

            self.reader = AnalogMultiChannelReader(task.in_stream)
            self.data = np.empty((3,))  # 3 channels

            task.start()

            try:
                while True:
                    self.reader.read_one_sample(self.data, timeout=10.0)
            except KeyboardInterrupt:
                pass