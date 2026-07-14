import json
import psutil
import time
from datetime import datetime

# python main.py

with open("config.json", "r") as file:
    config = json.load(file)
print(config)

def write_log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("monitor.log", "a", encoding="utf-8") as file:
        file.write(f"[{current_time}] {message}\n")

while True:
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_free_gb = psutil.disk_usage('C:\\').free / (1024**3)
    battery_info = psutil.sensors_battery()
    if battery_info is not None:
        battery_percent = battery_info.percent
        is_plugged = battery_info.power_plugged
    else:
        battery_percent = "Нет батареи (ПК)"
        is_plugged = True
    net_io = psutil.net_io_counters()
    net_sent_gb = net_io.bytes_sent / (1024**3)
    net_recv_gb = net_io.bytes_recv / (1024**3)

    if battery_info is not None:
        if battery_percent < config["battery_min_percent"] and is_plugged == False:
            print("\033[36m" + "ТРИВОГА: Низький заряд батареї! Підключіть кабель!" + "\033[0m")
            write_log("ТРИВОГА: Низький заряд батареї! Підключіть кабель!")

    if (net_sent_gb + net_recv_gb) > config["net_limit_gb"]:
        print("\033[35m" + "ТРИВОГА: Підозріло високий обіг мережевого трафіку!" + "\033[0m")
        write_log("ТРИВОГА: Підозріло високий обіг мережевого трафіку!")

    if cpu_usage > config["cpu_limit"]:
        print("\033[31m" + "УВАГА: Процесор перевантажено!" + "\033[0m")
        write_log("УВАГА! Процесор перевантажено!")

    if ram_usage > config["ram_limit"]:
        print("\033[33m" + "ТРИВОГА: Оперативна пам'ять майже забита!" + "\033[0m")
        write_log("УВАГА!: Оперативна пам'ять майже забита!")

    if disk_free_gb < config["disk_min_gb"]:
        print("\033[31m" + "КРИТИЧНО: Залишилося замало місця на системному диску!" + "\033[0m")
        write_log("КРИТИЧНО!: Залишилося замало місця на системному диску!")
        time.sleep(60)