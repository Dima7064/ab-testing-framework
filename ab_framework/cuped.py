"""Модуль для применения метода CUPED (Controlled-experiment Using Pre-Experiment Data).

CUPED позволяет снизить дисперсию целевой метрики, используя данные до эксперимента.
Это позволяет проводить A/B-тесты быстрее (на меньшей выборке).
"""

import pandas as pd
import numpy as np


def apply_cuped(
    df: pd.DataFrame,
    pre_metric_col: str,
    post_metric_col: str,
    group_col: str = "group"
) -> tuple[pd.DataFrame, dict]:
    """Применяет CUPED-корректировку к датафрейму.

    Args:
        df: DataFrame с данными эксперимента.
        pre_metric_col: Название колонки с предэкспериментальной метрикой (X).
        post_metric_col: Название колонки с метрикой во время эксперимента (Y).
        group_col: Название колонки с группой (control/treatment).

    Returns:
        tuple: (DataFrame с новой колонкой '{post_metric_col}_cuped', dict с параметрами).
    """
    # 1. Убираем строки с пропусками в нужных колонках
    df_clean = df.dropna(subset=[pre_metric_col, post_metric_col, group_col]).copy()

    # 2. Считаем математическое ожидание X (по всей выборке)
    mean_x = df_clean[pre_metric_col].mean()

    # 3. Считаем коэффициент theta
    # theta = Cov(X, Y) / Var(X)
    cov_matrix = np.cov(df_clean[post_metric_col], df_clean[pre_metric_col])
    cov_xy = cov_matrix[0, 1]
    var_x = cov_matrix[1, 1]

    theta = cov_xy / var_x if var_x != 0 else 0.0

    # 4. Создаем CUPED-метрику: Y_cuped = Y - theta * (X - mean_x)
    cuped_col_name = f"{post_metric_col}_cuped"
    df_clean[cuped_col_name] = df_clean[post_metric_col] - theta * (df_clean[pre_metric_col] - mean_x)

    # 5. Считаем, насколько снизилась дисперсия
    var_original = df_clean[post_metric_col].var()
    var_cuped = df_clean[cuped_col_name].var()
    variance_reduction = (var_original - var_cuped) / var_original if var_original > 0 else 0.0

    metrics = {
        "theta": theta,
        "mean_pre_metric": mean_x,
        "variance_reduction": variance_reduction,
        "original_variance": var_original,
        "cuped_variance": var_cuped
    }

    return df_clean, metrics


def format_cuped_report(metrics: dict) -> str:
    """Формирует текстовый отчет о применении CUPED."""
    reduction_pct = metrics["variance_reduction"] * 100
    report = f"=== CUPED Результаты ===\n"
    report += f"Коэффициент theta: {metrics['theta']:.4f}\n"
    report += f"Снижение дисперсии: {reduction_pct:.1f}%\n"
    
    # Интерпретация
    if reduction_pct > 0:
        report += f"🚀 Благодаря CUPED, мы можем найти эффект на меньшей выборке (эквивалентно увеличению выборки на {reduction_pct:.1f}%).\n"
    else:
        report += f"⚠️ CUPED не дал снижения дисперсии (метрики слабо коррелируют).\n"
        
    return report
