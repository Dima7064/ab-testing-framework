
"""Модуль для расчета размера выборки (Sample Size) и MDE."""

import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def calculate_sample_size(
    baseline_rate: float,
    mde_relative: float,
    alpha: float = 0.05,
    power: float = 0.80
) -> dict:
    """Рассчитывает размер выборки для бинарной метрики (конверсии)."""
    treatment_rate = baseline_rate * (1 + mde_relative)
    effect_size = proportion_effectsize(treatment_rate, baseline_rate)

    analysis = NormalIndPower()
    n_per_group = analysis.solve_power(
        effect_size=effect_size, alpha=alpha, power=power, ratio=1.0
    )

    return {
        "sample_size_per_group": int(np.ceil(n_per_group)),
        "total_sample_size": int(np.ceil(n_per_group)) * 2,
    }


def calculate_mde(
    baseline_rate: float,
    sample_size_per_group: int,
    alpha: float = 0.05,
    power: float = 0.80
) -> dict:
    """Рассчитывает минимальный детектируемый эффект (MDE) при заданном размере выборки."""
    analysis = NormalIndPower()
    
    # Находим effect size (Cohen's h), который можно детектировать
    effect_size = analysis.solve_power(
        effect_size=None,
        nobs1=sample_size_per_group,
        alpha=alpha,
        power=power,
        ratio=1.0
    )
    
    # Берем модуль (NormalIndPower всегда возвращает положительный эффект)
    h = abs(effect_size)

    # Точная обратная формула для Cohen's h: p2 = sin(arcsin(sqrt(p1)) + h/2)^2
    # Используем тригонометрию, чтобы избежать ошибок поиска корней
    arcsin_val = np.arcsin(np.sqrt(baseline_rate))
    
    # Считаем верхнюю границу (treatment лучше)
    p2_upper = np.sin(arcsin_val + h / 2) ** 2
    # Считаем нижнюю границу (treatment хуже)
    p2_lower = np.sin(max(0, arcsin_val - h / 2)) ** 2
    
    # MDE - это минимальное отклонение от базовой ставки
    mde_abs_upper = abs(p2_upper - baseline_rate)
    mde_abs_lower = abs(p2_lower - baseline_rate)
    
    mde_absolute = min(mde_abs_upper, mde_abs_lower)
    mde_relative = mde_absolute / baseline_rate

    return {
        "mde_absolute": mde_absolute,
        "mde_relative": mde_relative,
        "baseline_rate": baseline_rate,
        "detectable_treatment_rate": p2_upper if mde_abs_upper < mde_abs_lower else p2_lower,
    }