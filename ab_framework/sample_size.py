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
    """Рассчитывает размер выборки для бинарной метрики (конверсия).

    Args:
        baseline_rate: Текущая конверсия (например, 0.10 для 10%).
        mde_relative: Ожидаемый относительный прирост (например, 0.05 для +5%).
        alpha: Уровень значимости (по умолчанию 0.05).
        power: Статистическая мощность (по умолчанию 0.80).

    Returns:
        dict: Размер выборки на группу и общий размер.
    """
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
    """Рассчитывает минимальный детектируемый эффект (MDE) при заданном размере выборки.

    Args:
        baseline_rate: Текущая конверсия.
        sample_size_per_group: Количество пользователей в одной группе.
        alpha: Уровень значимости.
        power: Статистическая мощность.

    Returns:
        dict: Абсолютный и относительный MDE.
    """
    analysis = NormalIndPower()
    # Находим effect size, который можно детектировать
    effect_size = analysis.solve_power(
        effect_size=None,
        nobs1=sample_size_per_group,
        alpha=alpha,
        power=power,
        ratio=1.0
    )

    # Переводим effect size обратно в конверсию (приближенно)
    # Используем формулу Cohen's h: h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))
    # Нам нужно найти p2 (treatment_rate), зная h и p1
    # Решаем через поиск (так как функция arcsin нелинейна)
    from scipy.optimize import brentq

    def func(p2):
        return abs(proportion_effectsize(p2, baseline_rate) - effect_size)

    # Ищем p2 в диапазоне от baseline_rate до 1.0 (если эффект положительный)
    # или от 0 до baseline_rate (если отрицательный)
    try:
        if effect_size > 0:
            treatment_rate = brentq(func, baseline_rate + 1e-6, 1.0 - 1e-6)
        else:
            treatment_rate = brentq(func, 1e-6, baseline_rate - 1e-6)
    except ValueError:
        # Если не удалось найти, возвращаем None
        treatment_rate = None

    if treatment_rate is None:
        return {"error": "Не удалось рассчитать MDE. Проверьте параметры."}

    mde_absolute = abs(treatment_rate - baseline_rate)
    mde_relative = mde_absolute / baseline_rate

    return {
        "mde_absolute": mde_absolute,
        "mde_relative": mde_relative,
        "baseline_rate": baseline_rate,
        "detectable_treatment_rate": treatment_rate,
    }
