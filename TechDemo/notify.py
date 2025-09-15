import time

from PySide6.QtCore import QThread, Signal

# def get_float_input(prompt):
#     while True:
#         try:
#             return round(float(input(prompt)), 1)
#         except ValueError:
#             print("Please enter a valid number (up to one decimal place).")

class Worker(QThread):

    finished = Signal(str)

    def __init__(self, currentTemp, currentPres, desiredTemp, desiredPres):
        super().__init__()
        self.currentTemp = currentTemp
        self.currentPres = currentPres
        self.desiredTemp = desiredTemp
        self.desiredPres = desiredPres

    def run(self):
        self.check_condition(self.currentTemp, self.currentPres, self.desiredTemp, self.desiredPres)

    def adjust_value(self, current, desired):
        diff = abs(current - desired)

        step = 10

        if diff > 100:
            step = 10
        elif diff > 10:
            step = 1
        elif diff > 1:
            step = 0.1
        elif diff == 0:
            step = 0


        if current < desired:
            current += step
            if current > desired:
                current = desired
        elif current > desired:
            current -= step
            if current < desired:
                current = desired

        return round(current, 1)

    def check_condition(self, start_temp, start_pres, desired_temp, desired_pres):
        current_temp = start_temp
        current_pres = start_pres
        max_iterations = 1000
        iterations = 0

        while (current_temp != desired_temp or current_pres != desired_pres) and iterations < max_iterations:
            current_temp = self.adjust_value(current_temp, desired_temp)
            current_pres = self.adjust_value(current_pres, desired_pres)
            iterations += 1

            print(f"[Step {iterations}] Temperature: {current_temp}, Pressure: {current_pres}, Desired: {desired_temp}, {desired_pres}")

            # Unsafe environment check
            if current_temp > 1000 or current_pres > 1000:
                self.finished.emit("unsafe")
            time.sleep(0.1)

        if current_temp == desired_temp and current_pres == desired_pres:
            self.finished.emit("success")
        else:
            self.finished.emit("timeout")

# Prompt user input
# start_temp = get_float_input("Enter starting temperature: ")
# start_pres = get_float_input("Enter starting pressure: ")
# desired_temp = get_float_input("Enter desired temperature: ")
# desired_pres = get_float_input("Enter desired pressure: ")

# Create a toast notifier
# notifier = win10toast.ToastNotifier()
#
# Check the condition and show the correct notification
# result = check_condition(start_temp, start_pres, desired_temp, desired_pres)
#
# if result == "success":
#     notifier.show_toast("SUCCESS", "Temperature and pressure reached.")
# elif result == "unsafe":
#     notifier.show_toast("FAILURE", "Unsafe environment: Temperature or pressure exceeded 1000.")
# else:
#     notifier.show_toast("FAILURE", "Failed to reach temperature or pressure in safe time.")
