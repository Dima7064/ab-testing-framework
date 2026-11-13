
import pandas as pd
import numpy as np
from ab_framework.frequentist import analyze_conversion, analyze_continuous, format_report
from ab_framework.cuped import apply_cuped, format_cuped_report

# Читаем данные
path = "../ab-testing-simulator/data/ab_test_1.csv"
df = pd.read_csv(path)

# --- 1. АНАЛИЗ КОНВЕРСИИ (БЕЗ CUPED) ---
print("--- АНАЛИЗ КОНВЕРСИИ ---")
df_cart = df[df["added_to_cart"] == 1]
control = df_cart[df_cart["group"] == "control"]
treatment = df_cart[df_cart["group"] == "treatment"]

result_cr = analyze_conversion(
    control_conversions=control["ordered"].sum(),
    control_total=len(control),
    treatment_conversions=treatment["ordered"].sum(),
    treatment_total=len(treatment)
)
print(format_report(result_cr))

# --- 2. АНАЛИЗ GMV С CUPED ---
print("\n--- АНАЛИЗ GMV С CUPED ---")
# Нам нужна "предэкспериментальная" метрика. В нашем датасете её нет.
# Давай искусственно создадим её для демо (в реальности она была бы в базе).
np.random.seed(42)
# Представим, что это траты пользователя за прошлый месяц
df["pre_gmv"] = np.where(df["purchased"] == 1, df["gmv"] * 0.8 + np.random.normal(0, 50, len(df)), 0)
# Убедимся, что нет отрицательных значений
df["pre_gmv"] = df["pre_gmv"].clip(lower=0)

# Применяем CUPED
df_cuped, cuped_metrics = apply_cuped(df, pre_metric_col="pre_gmv", post_metric_col="gmv")
print(format_cuped_report(cuped_metrics))

# Сравниваем результаты t-test до и после CUPED
control_orig = df_cuped[df_cuped["group"] == "control"]["gmv"]
treatment_orig = df_cuped[df_cuped["group"] == "treatment"]["gmv"]

control_cuped = df_cuped[df_cuped["group"] == "control"]["gmv_cuped"]
treatment_cuped = df_cuped[df_cuped["group"] == "treatment"]["gmv_cuped"]

print("\nРезультаты t-test для GMV:")
print(f"Обычный GMV: p-value = {analyze_continuous(control_orig, treatment_orig)['p_value']:.4f}")
print(f"CUPED GMV:   p-value = {analyze_continuous(control_cuped, treatment_cuped)['p_value']:.4f}")