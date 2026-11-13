import numpy as np
import pytest
from ab_framework.frequentist import analyze_conversion, analyze_continuous, format_report


def test_analyze_conversion_positive():
    # Control: 1000 юзеров, 100 покупок (10%)
    # Treatment: 1000 юзеров, 120 покупок (12%). Эффект есть.
    res = analyze_conversion(100, 1000, 120, 1000)
    
    assert res["control_rate"] == 0.10
    assert res["treatment_rate"] == 0.12
    assert res["is_significant"] is True
    assert res["relative_lift"] == pytest.approx(0.20) # +20% относительно
    # Доверительный интервал не должен включать 0
    assert res["ci_lower"] > 0
    assert res["ci_upper"] > res["ci_lower"]


def test_analyze_conversion_zero_effect():
    # Control: 10%, Treatment: 10%. Эффекта нет.
    res = analyze_conversion(100, 1000, 100, 1000)
    
    assert res["is_significant"] is False
    # CI должен включать 0 (то есть разница может быть нулевой)
    assert res["ci_lower"] < 0 < res["ci_upper"]


def test_analyze_continuous_positive():
    np.random.seed(42)
    # Control: средний чек 1000 руб.
    control_data = np.random.normal(1000, 200, 5000)
    # Treatment: средний чек 1100 руб. (+10%). Эффект есть.
    treatment_data = np.random.normal(1100, 200, 5000)
    
    res = analyze_continuous(control_data, treatment_data)
    
    assert res["is_significant"] is True
    assert res["relative_lift"] > 0
    assert res["ci_lower"] > 0


def test_analyze_continuous_small_sample():
    # Маленькая выборка (по 10 юзеров), эффект может быть не найден
    np.random.seed(42)
    control_data = np.random.normal(1000, 500, 10)
    treatment_data = np.random.normal(1100, 500, 10)
    
    res = analyze_continuous(control_data, treatment_data)
    
    # На маленькой выборке p-value почти наверняка будет > 0.05
    assert res["is_significant"] is False


def test_format_report():
    res = analyze_conversion(100, 1000, 120, 1000)
    report = format_report(res)
    
    assert "CR Control: 10.00%" in report
    assert "Lift: 20.00%" in report
    assert "ВЕРДИКТ" in report
