from win10toast import ToastNotifier

class Notifier:
    # handles windows toast notifications for system events


    def __init__(self):
        self.toaster = ToastNotifier()
        print("[Notifier] Initialized Windows Toast notifications.")

    def notify_success(self, message="Temperature and pressure targets reached."):
        # notify user that system reached target conditions
        print(f"[Notifier] SUCCESS: {message}")
        self.toaster.show_toast("SUCCESS", message, duration=5, threaded=True)

    def notify_failure(self, message="System failed to reach target conditions."):
        # notify user that system failed to stabilize
        print(f"[Notifier] FAILURE: {message}")
        self.toaster.show_toast("FAILURE", message, duration=5, threaded=True)

    def notify_unsafe(self, message="Unsafe environment detected!"):
        # notify user that unsafe pressure or temperature levels occurred
        print(f"[Notifier] UNSAFE: {message}")
        self.toaster.show_toast("UNSAFE CONDITION", message, duration=5, threaded=True)
