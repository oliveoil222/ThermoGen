import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
import numpy as np

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0", min_val=-60, max_val=60)
    task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai1", min_val=-60, max_val=60)
    task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai2", min_val=-60, max_val=60)

    task.timing.cfg_samp_clk_timing(rate=8, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=100)

    reader = AnalogMultiChannelReader(task.in_stream)
    data = np.empty((3,))  # 2 channels, 100 samples per read

    task.start()
    try:
        while True:
            reader.read_one_sample(data, timeout=10.0)
            print(data)
            # Add your processing code here
    except KeyboardInterrupt:
        pass
