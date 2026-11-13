import pandas as pd
import numpy as np
import pytest
from ab_framework.cuped import apply_cuped, format_cuped_report


def test_cuped_variance_reduction():
    # Генерируем данные с высокой корреляцией
    np.random.seed(42)
    n = 10000
    pre_metric = np.random.normal(100, 20, n)
    # Post метрика сильно зависит от Pre метрики (корреляция ~0.8)
    post_metric = pre_metric * 0.8 + np.random.normal(20, 10, n)
    
    df = pd.DataFrame({
        "group": np.random.choice(["control", "treatment"], n),
        "pre": pre_metric,
        "post": post_metric
    })
    
    df_res, metrics = apply_cuped(df, "pre", "post")
    
    # Проверяем, что колонка создалась
    assert "post_cuped" in df_res.columns
    
    # Дисперсия должна упасть (variance_reduction > 0)
    assert metrics["variance_reduction"] > 0.3  # Ожидаем минимум 30% снижения
    assert metrics["theta"] > 0.5  # Высокая корреляция -> высокий theta


def test_cuped_no_correlation():
    # Если X и Y не коррелируют, дисперсия не должна упасть сильно
    np.random.seed(42)
    n = 5000
    pre_metric = np.random.normal(100, 20, n)
    post_metric = np.random.normal(100, 20, n)  # Полностью независимая
    
    df = pd.DataFrame({
        "group": np.random.choice(["control", "treatment"], n),
        "pre": pre_metric,
        "post": post_metric
    })
    
    df_res, metrics = apply_cuped(df, "pre", "post")
    
    # Снижение дисперсии должно быть близко к 0 (или отрицательным из-за шума)
    assert abs(metrics["variance_reduction"]) < 0.05
    assert abs(metrics["theta"]) < 0.1


def test_cuped_report():
    metrics = {
        "theta": 0.75,
        "variance_reduction": 0.40,
        "original_variance": 100.0,
        "cuped_variance": 60.0,
        "mean_pre_metric": 50.0
    }
    report = format_cuped_report(metrics)
    
    assert "theta: 0.7500" in report
    assert "Снижение дисперсии: 40.0%" in report
    assert "🚀" in report
