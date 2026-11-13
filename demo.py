import pandas as pd
from ab_framework.frequentist import analyze_conversion, format_report

# Читаем данные из Проекта 1 (путь может отличаться, проверь)
path = "../ab-testing-simulator/data/ab_test_1.csv"
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print(f"Файл {path} не найден. Убедись, что ты создал его в Проекте 1.")
    exit()

# Берем только тех, кто дошел до корзины
df = df[df["added_to_cart"] == 1]

control = df[df["group"] == "control"]
treatment = df[df["group"] == "treatment"]

# Запускаем анализ конверсии
result = analyze_conversion(
    control_conversions=control["ordered"].sum(),
    control_total=len(control),
    treatment_conversions=treatment["ordered"].sum(),
    treatment_total=len(treatment)
)

print("=== РЕЗУЛЬТАТ АНАЛИЗА A/B ТЕСТА ===")
print(format_report(result))
