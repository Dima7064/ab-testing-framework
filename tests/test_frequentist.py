
import numpy as np
import pytest
from ab_framework.frequentist import analyze_conversion, analyze_continuous, format_report


def test_analyze_conversion_positive():
    # Control: 10000 юзеров, 1000 покупок (10%)
    # Treatment: 10000 юзеров, 1200 покупок (12%). Эффект есть и он значим.
    res = analyze_conversion(1000, 10000, 1200, 10000)
    
    assert res["control_rate"] == 0.10
    assert res["treatment_rate"] == 0.12
    assert res["is_significant"] is True
    assert res["relative_lift"] == pytest.approx(0.20)
    assert res["ci_lower"] > 0


def test_analyze_conversion_zero_effect():
    # Одинаковые данные - эффекта нет
    res = analyze_conversion(100, 1000, 100, 1000)
    assert res["is_significant"] is False
    assert res["ci_lower"] < 0 < res["ci_upper"]


def test_analyze_continuous_positive():
    np.random.seed(42)
    control_data = np.random.normal(1000, 200, 5000)
    treatment_data = np.random.normal(1100, 200, 5000)
    
    res = analyze_continuous(control_data, treatment_data)
    assert res["is_significant"] is True
    assert res["relative_lift"] > 0


def test_analyze_continuous_small_sample():
    # На маленькой выборке (10 юзеров) с абсолютно ОДИНАКОВЫМИ данными эффекта не будет (p-value = 1.0)
    control_data = np.array([1000, 1100, 900, 1000, 1000, 1100, 900, 1000, 1000, 1100])
    treatment_data = np.array([1000, 1100, 900, 1000, 1000, 1100, 900, 1000, 1000, 1100])
    
    res = analyze_continuous(control_data, treatment_data)
    assert res["is_significant"] is False


def test_format_report():
    res = analyze_conversion(1000, 10000, 1200, 10000)
    report = format_report(res)
    
    assert "CR Control: 10.00%" in report
    assert "Относительный прирост (Lift): 20.00%" in report
    assert "ВЕРДИКТ" in report