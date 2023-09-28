from datetime import datetime

now = datetime.now()
date = now.strftime("%Y/%m/%d")
time = now.strftime("%H:%M:%S")
print("Current date and time: ", date, time)
