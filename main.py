import json
import psutil
import time
from datetime import datetime
import socket  
import os      




def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    return config



# python main.py

def write_log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("monitor.log", "a", encoding="utf-8") as file:
        file.write(f"[{current_time}] {message}\n")


def collect_metrics():
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
    return {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "disk": disk_free_gb,
        "battery_percent": battery_percent,
        "is_plugged": is_plugged,
        "net_sent": net_sent_gb,
        "net_recv": net_recv_gb
    }

def check_thresholds(metrics, config, alert_states):
    if (metrics["net_sent"] + metrics["net_recv"]) > config["net_limit_gb"]:
        if not alert_states["net"]:
            print("ТРЕВОГА: Високий мережевий трафік!")
            write_log("ТРЕВОГА: Високий мережевий трафік!")
            alert_states["net"] = True
    else:
        if alert_states["net"]:
            print("Все ок: Мережевий трафік нормалізувався")
            write_log("Все ок: Мережевий трафік нормалізувався")
            alert_states["net"] = False

    if metrics["cpu"] > config["cpu_limit"]:
        if not alert_states["cpu"]: 
            print("ТРЕВОГА: Процессор перегружен!")
            write_log("ТРЕВОГА: Процессор перегружен!")
            alert_states["cpu"] = True 
    else:
        if alert_states["cpu"]: 
            print("Всё ок: Процессор вернулся в норму")
            write_log("Всё ок: Процессор вернулся в норму")
            alert_states["cpu"] = False 

    if metrics["ram"] > config["ram_limit"]:
        if not alert_states["ram"]:
            print("ТРЕВОГА: Оперативна пам'ять перевантажена!")
            write_log("ТРЕВОГА: Оперативна пам'ять перевантажена!")
            alert_states["ram"] = True
        else:
            if alert_states["ram"]:
                print("Все ок: Оперативна пам'ять в нормі")
                write_log("Все ок: Оперативна пам'ять в нормі")
                alert_states["ram"] = False


    if metrics["disk"] < config["disk_min_gb"]:
        if not alert_states["disk"]:
            print("КРИТИЧНО: Залишилося замало місця на диску!")
            write_log("КРИТИЧНО: Залишилося замало місця на диску!")
            alert_states["disk"] = True
    else:
        if alert_states["disk"]:
            print("Все ок: Місце на диску в нормі")
            write_log("Все ок: Місце на диску в нормі")
            alert_states["disk"] = False
    if metrics["battery_percent"] != "Нет батареи (ПК)" and metrics["battery_percent"] < config["battery_min_percent"] and metrics["is_plugged"] == False:
        if not alert_states["battery"]:
            print("ТРЕВОГА: Низький заряд батареї! Підключіть кабель!")
            write_log("ТРЕВОГА: Низький заряд батареї! Підключіть кабель!")
            alert_states["battery"] = True
    else:
        if alert_states["battery"]:
            print("Все ок: Заряд батареї в нормі")
            write_log("Все ок: Заряд батареї в нормі")
            alert_states["battery"] = False
    # Проверка порта
    target = config["server_to_check"]
    if not check_network_port(target):
        if not alert_states["net_port"]:
            print(f"ТРЕВОГА: Сервер {target} недоступний!")
            write_log(f"ТРЕВОГА: Сервер {target} недоступний!")
            alert_states["net_port"] = True
    else:
        if alert_states["net_port"]:
            print(f"Все ок: Сервер {target} знову доступний")
            write_log(f"Все ок: Сервер {target} знову доступний")
            alert_states["net_port"] = False

def validate_config(config):
    required_keys = ["cpu_limit", "ram_limit", "disk_min_gb", "net_limit_gb", "battery_min_percent", "check_interval_seconds", "server_to_check"]
    for f in required_keys:
        if f not in config:
            print(f"ПОМИЛКА: В конфігу відсутній параметр {f}")
            exit(1)

def check_network_port(target):
    try:
        host, port = target.split(":")
        socket.create_connection((host, int(port)), timeout=3)
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def main():
    config = load_config()
    validate_config(config)
    alert_states = {"cpu": False, "ram": False, "disk": False, "net": False, "battery": False,"net_port": False}
    try:
        while True:
            metrics = collect_metrics()
            check_thresholds(metrics, config, alert_states)
            time.sleep(config["check_interval_seconds"])
    except KeyboardInterrupt:
        print("Ви коректно завершили програму за допомогою: Ctrl+C")
if __name__ == "__main__":
    main()