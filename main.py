import time
from mailjet_rest import Client
import psutil
import os

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')


current_time = time.localtime()

formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

CPU_THRESHOLD = 2

RAM_THRESHOLD = 10

DISK_THRESHOLD = 50


def send_alert(subject, message):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "testmyprojects622@gmail.com",
                    "Name": "24/7 SysMon"
                },
                "To": [
                    {
                        "Email": "cojjojimmy12@gmail.com",
                        "Name": "Admin"
                    }
                ],
                "Subject": subject,
                "HTMLPart": f"<h3>{message}</h3>",
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent: {result.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")



    



if __name__ == "__main__":
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_usage}%")
        ram_usage = psutil.virtual_memory().percent
        print(f"RAM Usage: {ram_usage}%")
        disk_usage = psutil.disk_usage('/').percent
        print(f"Disk Usage: {disk_usage}%")
        alert_message = ""

        if cpu_usage > CPU_THRESHOLD:
            alert_message += f"CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"

        if ram_usage > RAM_THRESHOLD:
            alert_message += f"RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"

        if disk_usage > DISK_THRESHOLD:
            alert_message += f"Disk usage is high: {disk_usage}% (Threshold: {DISK_THRESHOLD}%)\n"

        if alert_message:
            send_alert(f"Python Monitoring Alert-{formatted_time}", alert_message)
        else:
            print("All system metrics are within normal limits.")
