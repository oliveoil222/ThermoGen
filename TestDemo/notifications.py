import platform
import sys

# Try importing Windows-specific library, ignore if not available
if platform.system() == "Windows":
    try:
        from windows_toasts import WindowsToaster, Toast
    except ImportError:
        WindowsToaster = None
        Toast = None
# from windows_toasts import WindowsToaster, Toast
import subprocess

class NotificationManager:
    def __init__(self):
        self.system = platform.system()

        if self.system == "Windows" and WindowsToaster and Toast:
            self.notifier = WindowsToaster('TechDemo')
            self.newNotification = Toast()


    def send_notification(self):
        if self.system == "Windows" and WindowsToaster and Toast:
            self.notifier.show_toast(self.newNotification)
        elif self.system == "Darwin":  # macOS
            subprocess.run([
                "osascript", "-e",
                f'display notification "{self.message}" with title "{self.title}"'
            ])
        else:
            print(f"Notifications not supported on {self.system}. Message: {self.title} - {self.message}")

    def set_message(self, title, message):
        self.newNotification.title = title
        self.newNotification.text_fields = [title, message]


if __name__ == "__main__":
    nm = NotificationManager()
    nm.send_notification()
