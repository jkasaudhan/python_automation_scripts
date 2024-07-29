from win10toast import ToastNotifier
import time

# This is only for windows machine but not for MAC
toaster = ToastNotifier()


def set_reminder():
    reminder_header = input("What would you like me to remember?\n")
    related_message = input("Related Message:\n")
    time_minutes = float(input("In how many minutes?\n"))

    time_seconds = time_minutes * 60

    print("Setting up reminder...")
    time.sleep(2)
    print("All set!")

    time.sleep(time_seconds)

    toaster.show_toast(
        title=f"{reminder_header}",
        msg=f"{related_message}",
        duration=10,
        threaded=True
    )

    while toaster.notification_active():
        time.sleep(0.005)


if __name__ == "__main__":
    set_reminder()
