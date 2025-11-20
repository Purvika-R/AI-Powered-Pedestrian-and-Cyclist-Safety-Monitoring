import importlib
m = importlib.import_module("backend.app.services.alerts")
print("alerts module loaded:", m.__name__)
print("has push_alert:", hasattr(m, "push_alert"))

m2 = importlib.import_module("backend.app.services.alert_engine")
print("alert_engine loaded:", m2.__name__)
