"""Модуль для корректировки p-value при множественном тестировании (Multiple Testing).

Зачем это нужно: если мы проверяем 20 метрик одновременно, с вероятностью 64% 
хотя бы одна из них покажет p-value < 0.05 просто случайно. Чтобы избежать 
"p-hacking", мы применяем поправки.
"""

import numpy as np
from statsmodels.stats.multitest import multipletests


def apply_bonferroni(p_values: list[float], alpha: float = 0.05) -> dict:
    """Применяет поправку Бонферрони (самую строгую).

    Делит порог alpha на количество тестов. Если тестов много, ни один не пройдет.

    Args:
        p_values: Список p-value из разных тестов.
        alpha: Исходный уровень значимости (обычно 0.05).

    Returns:
        dict: Скорректированные p-value и массив значимости.
    """
    rejected, pvals_corrected, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    
    return {
        "method": "bonferroni",
        "original_p_values": p_values,
        "corrected_p_values": list(pvals_corrected),
        "is_significant": list(rejected)
    }


def apply_fdr(p_values: list[float], alpha: float = 0.05) -> dict:
    """Применяет поправку FDR (False Discovery Rate) через метод Бенджамини-Хохберга.

    Этот метод мягче, чем Бонферрони, и часто используется в бигтехе. 
    Он контролирует долю ложноположительных результатов среди всех "значимых".

    Args:
        p_values: Список p-value.
        alpha: Уровень значимости.

    Returns:
        dict: Скорректированные p-value и массив значимости.
    """
    rejected, pvals_corrected, _, _ = multipletests(p_values, alpha=alpha, method='fdr_bh')
    
    return {
        "method": "fdr_bh",
        "original_p_values": p_values,
        "corrected_p_values": list(pvals_corrected),
        "is_significant": list(rejected)
    }
