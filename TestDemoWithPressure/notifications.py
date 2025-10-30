import time
from windows_toasts import WindowsToaster, Toast

class NotificationManager:
    notifier = WindowsToaster('MainNotifier')

    newNotification = Toast()

    newNotification.title = "TechDemoTest"
    newNotification.text_fields = ["Hello World"]

    def sendNotification(self):
        self.notifier.show_toast(self.newNotification)