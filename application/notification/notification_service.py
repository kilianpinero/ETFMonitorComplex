class NotificationService:
    def __init__(self, channels):
        self.channels = channels

    def notify(self, recipient, subject, message):
        for channel in self.channels:
            channel.send(recipient, subject, message)

