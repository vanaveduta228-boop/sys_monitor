import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from main import check_thresholds 

class TestSystemMonitor(unittest.TestCase):

    def test_cpu_alert_trigger(self):
        metrics = {"cpu": 95, "ram": 50, "disk": 100, "net_sent": 10, "net_recv": 10, "battery_percent": 80, "is_plugged": True}
        config = {"cpu_limit": 80, "ram_limit": 90, "disk_min_gb": 10, "net_limit_gb": 100, "battery_min_percent": 20}
        alert_states = {"cpu": False, "ram": False, "disk": False, "net": False, "battery": False} 
        check_thresholds(metrics, config, alert_states)
        self.assertTrue(alert_states["cpu"])

    def test_cpu_recovery(self):
        metrics = {"cpu": 50, "ram": 50, "disk": 100, "net_sent": 10, "net_recv": 10, "battery_percent": 80, "is_plugged": True}
        config = {"cpu_limit": 80, "ram_limit": 90, "disk_min_gb": 10, "net_limit_gb": 100, "battery_min_percent": 20}
        alert_states = {"cpu": True, "ram": False, "disk": False, "net": False, "battery": False}
        check_thresholds(metrics, config, alert_states)
        self.assertFalse(alert_states["cpu"])
    
    def test_ram_alert_trigger(self):
        metrics = {"cpu": 50, "ram": 95, "disk": 100, "net_sent": 10, "net_recv": 10, "battery_percent": 80, "is_plugged": True}
        config = {"cpu_limit": 80, "ram_limit": 90, "disk_min_gb": 10, "net_limit_gb": 100, "battery_min_percent": 20}
        alert_states = {"cpu": False, "ram": False, "disk": False, "net": False, "battery": False}
        check_thresholds(metrics, config, alert_states)
        self.assertTrue(alert_states["ram"])

    def test_ram_recovery(self):
        metrics = {"cpu": 50, "ram": 50, "disk": 100, "net_sent": 10, "net_recv": 10, "battery_percent": 80, "is_plugged": True}
        config = {"cpu_limit": 80, "ram_limit": 90, "disk_min_gb": 10, "net_limit_gb": 100, "battery_min_percent": 20}
        alert_states = {"cpu": True, "ram": False, "disk": False, "net": False, "battery": False}
        check_thresholds(metrics, config, alert_states)
        self.assertFalse(alert_states["ram"])