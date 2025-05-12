import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Шаг 1: Загрузка данных
file_path = r'C:\Users\Dasha\Downloads\flights_NY.csv'

# Чтение CSV файла с разделителем запятая и заголовками из первой строки
df = pd.read_csv(file_path, delimiter=',', header=0)

# Шаг 2: Преобразование типов данных
# Преобразуем столбцы, которые должны быть числовыми
numeric_columns = ['year', 'month', 'day', 'dep_time', 'arr_time',
                   'dep_delay', 'arr_delay', 'air_time', 'distance']

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Столбцы 'carrier', 'flight', 'tailnum', 'origin', 'dest' остаются строковыми

# Шаг 3: Удаление строк с пропущенными значениями в ключевых столбцах
# Опционально: можно указать конкретные столбцы для удаления NaN
df_clean = df.dropna(subset=['dest', 'air_time', 'distance'])

# Шаг 4: Вычисление стандартного отклонения времени перелета для каждого аэропорта прилета
std_dev_air_time = df_clean.groupby('dest')['air_time'].std().reset_index()
std_dev_air_time.rename(columns={'air_time': 'std_dev_air_time'}, inplace=True)

# Шаг 5: Вычисление среднего расстояния для каждого аэропорта прилета
avg_distance = df_clean.groupby('dest')['distance'].mean().reset_index()
avg_distance.rename(columns={'distance': 'avg_distance'}, inplace=True)

# Объединение данных по аэропорту прилета
merged_df = pd.merge(std_dev_air_time, avg_distance, on='dest')

# Шаг 6: Удаление строк с NaN после вычисления стандартного отклонения
merged_df = merged_df.dropna(subset=['std_dev_air_time', 'avg_distance'])

# Шаг 7: Построение точечной диаграммы зависимости стандартного отклонения от расстояния
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['avg_distance'], merged_df['std_dev_air_time'], color='blue', label='Данные')

# Шаг 8: Аппроксимация линейной регрессией на основе расстояния
X = merged_df[['avg_distance']]
y = merged_df['std_dev_air_time']

linear_model = LinearRegression()
linear_model.fit(X, y)
y_pred_linear = linear_model.predict(X)

# Добавление линии линейной регрессии на график
plt.plot(merged_df['avg_distance'], y_pred_linear, color='red', label='Линейная регрессия')

# Шаг 9: Уточнение модели с дополнительными признаками (например, квадрат расстояния)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

poly_model = LinearRegression()
poly_model.fit(X_poly, y)
y_pred_poly = poly_model.predict(X_poly)

# Добавление линии уточненной модели на график
# Для корректного отображения полиномиальной регрессии сортируем данные по x
sorted_indices = merged_df['avg_distance'].argsort()
plt.plot(merged_df['avg_distance'].iloc[sorted_indices], y_pred_poly[sorted_indices], color='green', label='Полиномиальная регрессия (степень 2)')

# Шаг 10: Сравнение точности моделей
r2_linear = r2_score(y, y_pred_linear)
r2_poly = r2_score(y, y_pred_poly)

print(f"Коэффициент детерминации для линейной регрессии: {r2_linear:.4f}")
print(f"Коэффициент детерминации для полиномиальной регрессии: {r2_poly:.4f}")

# Шаг 11: Финальная настройка графика
plt.title('Зависимость стандартного отклонения времени перелета от расстояния до аэропорта')
plt.xlabel('Среднее расстояние до аэропорта (мили)')
plt.ylabel('Стандартное отклонение времени перелета (минуты)')
plt.legend()
plt.grid(True)
plt.show()
