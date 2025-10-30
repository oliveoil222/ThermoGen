import time
import math
import random

try:
    import nidaqmx
    SIMULATION = False
except (ImportError, ModuleNotFoundError):
    print("[TemperatureReader] NI-DAQmx not found. Running in SIMULATION mode.")
    SIMULATION = True


class TemperatureReader:

    #reads temperature data from thermocouples via ni daq or simulates if unavailable


    def __init__(self, channel="Dev1/ai0", amplitude=10.0, base_temp=25.0):
        global SIMULATION
        self.channel = channel
        self.start_time = time.time()
        self.amplitude = amplitude
        self.base_temp = base_temp

        if not SIMULATION:
            try:
                self.task = nidaqmx.Task()
                self.task.ai_channels.add_ai_thrmcpl_chan(
                    channel,
                    min_val=-60,
                    max_val=1000
                )
                print(f"[TemperatureReader] Connected to NI DAQ channel {channel}")
            except Exception as e:
                print(f"[TemperatureReader] Could not initialize NI DAQ: {e}. Switching to simulation.")
                SIMULATION = True
                self.task = None
        else:
            self.task = None

    def read_temperature(self):
        global SIMULATION
        if SIMULATION:
            elapsed = time.time() - self.start_time
            temp = self.base_temp + self.amplitude * math.sin(2 * math.pi * (elapsed / 60))
            noise = random.uniform(-0.2, 0.2)
            simulated_temp = temp + noise
            print(f"[TemperatureReader] Simulated Temperature: {simulated_temp:.2f}°C")
            return simulated_temp
        else:
            try:
                reading = self.task.read()
                print(f"[TemperatureReader] Actual Temperature: {reading:.2f}°C")
                return reading
            except Exception as e:
                print(f"[TemperatureReader] Error reading temperature: {e}")
                return None

    def close(self):
        if self.task:
            self.task.close()
            print("[TemperatureReader] Task closed.")
