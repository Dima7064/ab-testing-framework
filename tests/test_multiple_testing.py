import pytest
from ab_framework.multiple_testing import apply_bonferroni, apply_fdr

def test_bonferroni_correction():
    # 10 метрик. Одна случайно показала p=0.04, остальные - большие.
    p_values = [0.04, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
    
    res = apply_bonferroni(p_values, alpha=0.05)
    
    # Скорректированный порог: 0.05 / 10 = 0.005
    # 0.04 > 0.005, значит, значимых метрик быть не должно
    assert sum(res["is_significant"]) == 0
    # Скорректированное p-value должно стать больше (0.04 * 10 = 0.40)
    assert res["corrected_p_values"][0] == pytest.approx(0.40)

def test_fdr_correction():
    # 10 метрик
    p_values = [0.001, 0.005, 0.01, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70]
    
    res = apply_fdr(p_values, alpha=0.05)
    
    # FDR мягче. Метрики с очень маленькими p-value должны остаться значимыми
    assert res["is_significant"][0] is True
    assert res["is_significant"][1] is True
