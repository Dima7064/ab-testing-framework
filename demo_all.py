"""Демонстрация работы всех модулей A/B Testing Framework."""

import numpy as np
import pandas as pd
from ab_framework.srm import check_srm
from ab_framework.sample_size import calculate_sample_size, calculate_mde
from ab_framework.frequentist import analyze_conversion, analyze_continuous, format_report
from ab_framework.cuped import apply_cuped, format_cuped_report
from ab_framework.multiple_testing import apply_bonferroni, apply_fdr

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

# --- 1. SRM CHECK ---
print_header("1. Проверка SRM (Sample Ratio Mismatch)")
srm_ok = check_srm({"control": 10000, "treatment": 10050})
srm_bad = check_srm({"control": 10000, "treatment": 11000})
print(f"Норма: p-value={srm_ok['p_value']:.4f} | {srm_ok['message']}")
print(f"Сломан: p-value={srm_bad['p_value']:.4f} | {srm_bad['message']}")

# --- 2. SAMPLE SIZE & MDE ---
print_header("2. Расчет Sample Size и MDE")
ss = calculate_sample_size(baseline_rate=0.10, mde_relative=0.05)
print(f"Выборка для MDE 5%: {ss['sample_size_per_group']:,} юзеров на группу")

mde = calculate_mde(baseline_rate=0.10, sample_size_per_group=20000)
print(f"MDE при выборке 20k: {mde['mde_relative']:.2%}")

# --- 3. FREQUENTIST ANALYSIS ---
print_header("3. Анализ конверсии (Z-test)")
conv = analyze_conversion(control_conversions=1000, control_total=10000, 
                          treatment_conversions=1150, treatment_total=10000)
print(format_report(conv))

print("\n--- Анализ непрерывной метрики (T-test) ---")
np.random.seed(42)
c_data = np.random.normal(1000, 200, 5000)
t_data = np.random.normal(1050, 200, 5000)
cont = analyze_continuous(c_data, t_data)
print(format_report(cont))

# --- 4. CUPED ---
print_header("4. CUPED (Снижение дисперсии)")
n = 10000
pre = np.random.normal(100, 20, n)
post = pre * 0.8 + np.random.normal(20, 10, n)
df = pd.DataFrame({"group": np.random.choice(["control", "treatment"], n), "pre": pre, "post": post})
_, cuped_metrics = apply_cuped(df, "pre", "post")
print(format_cuped_report(cuped_metrics))

# --- 5. MULTIPLE TESTING ---
print_header("5. Multiple Testing (Защита от p-hacking)")
p_vals = [0.001, 0.04, 0.05, 0.10, 0.20] # 0.04 и 0.05 - случайные всплески
print(f"Оригинальные p-value: {p_vals}")

bonf = apply_bonferroni(p_vals)
print(f"После Бонферрони: {[round(p, 4) for p in bonf['corrected_p_values']]}")
print(f"Значимые: {bonf['is_significant']}")

fdr = apply_fdr(p_vals)
print(f"После FDR (Benjamini-Hochberg): {[round(p, 4) for p in fdr['corrected_p_values']]}")
print(f"Значимые: {fdr['is_significant']}")

print("\nДемонстрация завершена!")
