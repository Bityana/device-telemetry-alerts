from services.worker.app.app.rules import evaluate_rules


def test_overheat_rule():
    alerts = evaluate_rules("cam-1", {"temperature_c": 80})
    assert any(a.alert_type == "OVERHEAT" for a in alerts)


def test_low_battery_rule():
    alerts = evaluate_rules("cam-1", {"battery_pct": 10})
    assert any(a.alert_type == "LOW_BATTERY" for a in alerts)


def test_no_alerts():
    alerts = evaluate_rules("cam-1", {"temperature_c": 40, "battery_pct": 90})
    assert alerts == []
