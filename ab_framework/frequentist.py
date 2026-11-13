
"""Модуль для частотного анализа A/B-тестов (Frequentist approach)."""

import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def analyze_conversion(
    control_conversions: int,
    control_total: int,
    treatment_conversions: int,
    treatment_total: int,
    alpha: float = 0.05
) -> dict:
    """Анализирует бинарную метрику (конверсию) с помощью Z-теста."""
    cr_control = control_conversions / control_total
    cr_treatment = treatment_conversions / treatment_total

    abs_lift = cr_treatment - cr_control
    rel_lift = abs_lift / cr_control if cr_control > 0 else 0.0

    counts = np.array([treatment_conversions, control_conversions])
    nobs = np.array([treatment_total, control_total])
    z_stat, p_value = proportions_ztest(counts, nobs)

    se_diff = np.sqrt(
        (cr_control * (1 - cr_control) / control_total) +
        (cr_treatment * (1 - cr_treatment) / treatment_total)
    )
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = abs_lift - z_crit * se_diff
    ci_upper = abs_lift + z_crit * se_diff

    return {
        "metric_type": "conversion",
        "control_rate": cr_control,
        "treatment_rate": cr_treatment,
        "absolute_lift": abs_lift,
        "relative_lift": rel_lift,
        "z_stat": z_stat,
        "p_value": p_value,
        "is_significant": bool(p_value < alpha),  # <-- ИСПРАВЛЕНИЕ: bool()
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }


def analyze_continuous(
    control_data: np.ndarray,
    treatment_data: np.ndarray,
    alpha: float = 0.05
) -> dict:
    """Анализирует непрерывную метрику с помощью t-теста Уэлча."""
    mean_control = np.mean(control_data)
    mean_treatment = np.mean(treatment_data)

    abs_lift = mean_treatment - mean_control
    rel_lift = abs_lift / mean_control if mean_control != 0 else 0.0

    t_stat, p_value = stats.ttest_ind(treatment_data, control_data, equal_var=False)

    n1 = len(control_data)
    n2 = len(treatment_data)
    s1 = np.var(control_data, ddof=1)
    s2 = np.var(treatment_data, ddof=1)

    se_diff = np.sqrt((s1 / n1) + (s2 / n2))

    df = ((s1 / n1 + s2 / n2) ** 2) / (
        ((s1 / n1) ** 2) / (n1 - 1) + ((s2 / n2) ** 2) / (n2 - 1)
    )
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    ci_lower = abs_lift - t_crit * se_diff
    ci_upper = abs_lift + t_crit * se_diff

    return {
        "metric_type": "continuous",
        "control_mean": mean_control,
        "treatment_mean": mean_treatment,
        "absolute_lift": abs_lift,
        "relative_lift": rel_lift,
        "t_stat": t_stat,
        "p_value": p_value,
        "is_significant": bool(p_value < alpha),  # <-- ИСПРАВЛЕНИЕ: bool()
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }


def format_report(result: dict) -> str:
    """Превращает словарь с результатами в красивый текстовый отчет."""
    if result["metric_type"] == "conversion":
        base = f"CR Control: {result['control_rate']:.2%}\n"
        base += f"CR Treatment: {result['treatment_rate']:.2%}\n"
    else:
        base = f"Mean Control: {result['control_mean']:.2f}\n"
        base += f"Mean Treatment: {result['treatment_mean']:.2f}\n"

    base += f"Относительный прирост (Lift): {result['relative_lift']:.2%}\n"
    base += f"p-value: {result['p_value']:.4f}\n"
    base += f"95% CI: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]\n"

    if result["is_significant"]:
        base += "✅ ВЕРДИКТ: Эффект статистически значим. Можно катить."
    else:
        base += "❌ ВЕРДИКТ: Эффект НЕ значим. Недостаточно данных или эффекта нет."

    return base