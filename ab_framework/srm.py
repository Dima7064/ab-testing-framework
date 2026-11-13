"""Модуль для проверки SRM (Sample Ratio Mismatch)."""

from typing import Dict
from scipy import stats


def check_srm(group_sizes: Dict[str, int], expected_ratios: Dict[str, float] = None) -> dict:
    """Проверяет, соответствует ли фактическое распределение групп ожидаемому (обычно 50/50).

    Args:
        group_sizes: Словарь с размерами групп, например {'control': 5000, 'treatment': 5050}
        expected_ratios: Ожидаемые доли групп, например {'control': 0.5, 'treatment': 0.5}
                         Если None, предполагается равномерное распределение (50/50).

    Returns:
        dict: Результаты проверки (chi2, p_value, is_srm, message).
    """
    groups = list(group_sizes.keys())
    observed = [group_sizes[g] for g in groups]
    total = sum(observed)

    if expected_ratios is None:
        expected_ratios = {g: 1.0 / len(groups) for g in groups}

    expected = [expected_ratios[g] * total for g in groups]

    chi2, p_value = stats.chisquare(f_obs=observed, f_exp=expected)

    is_srm = p_value < 0.05
    message = "SRM DETECTED! Тест невалиден." if is_srm else "SRM OK. Распределение равномерное."

    return {
        "chi2": chi2,
        "p_value": p_value,
        "is_srm": is_srm,
        "message": message,
        "observed": group_sizes,
        "expected": {g: round(e, 2) for g, e in zip(groups, expected)},
    }
