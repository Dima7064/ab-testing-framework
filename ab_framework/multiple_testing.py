
"""Модуль для корректировки p-value при множественном тестировании (Multiple Testing)."""

import numpy as np
from statsmodels.stats.multitest import multipletests


def apply_bonferroni(p_values: list[float], alpha: float = 0.05) -> dict:
    """Применяет поправку Бонферрони (самую строгую)."""
    rejected, pvals_corrected, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')
    
    return {
        "method": "bonferroni",
        "original_p_values": p_values,
        "corrected_p_values": [float(x) for x in pvals_corrected],
        "is_significant": [bool(x) for x in rejected]  # Приводим к обычному bool
    }


def apply_fdr(p_values: list[float], alpha: float = 0.05) -> dict:
    """Применяет поправку FDR (False Discovery Rate) через метод Бенджамини-Хохберга."""
    rejected, pvals_corrected, _, _ = multipletests(p_values, alpha=alpha, method='fdr_bh')
    
    return {
        "method": "fdr_bh",
        "original_p_values": p_values,
        "corrected_p_values": [float(x) for x in pvals_corrected],
        "is_significant": [bool(x) for x in rejected]  # Приводим к обычному bool
    }