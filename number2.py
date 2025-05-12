import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv(
    'C:\\Users\\Dasha\\Downloads\\flights_NY.csv',
    sep=',',  # Изменено с ';' на ','
    header=None,
    names=[
        'year', 'month', 'day',
        'dep_time', 'dep_delay',
        'arr_time', 'arr_delay',
        'carrier', 'tailnum',
        'flight', 'origin', 'dest',
        'air_time', 'distance'
    ]
)


# Преобразуйте значения в столбце 'air_time' в строки
flight_times_str = df['air_time'].astype(str).dropna()

# Постройте гистограмму с преобразованными значениями
plt.hist(flight_times_str, bins=30, density=True, alpha=0.6, color='b', edgecolor='black')

# Преобразование данных в числовой формат
flight_times = pd.to_numeric(flight_times_str, errors='coerce').dropna()
mu, std = norm.fit(flight_times)

# Оценка параметров нормального распределения
mu, std = norm.fit(flight_times)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)

# Нахождение интервала, в который с вероятностью не менее 95% попадает время полета
lower_bound = mu - 1.96 * std
upper_bound = mu + 1.96 * std

# Отображение интервала на графике
plt.axvline(lower_bound, color='r', linestyle='--', label=f'95% интервал: [{lower_bound:.2f}, {upper_bound:.2f}]')
plt.axvline(upper_bound, color='r', linestyle='--')
plt.legend()


# Добавление названий и меток на график
plt.xlabel('Время полета')
plt.ylabel('Плотность вероятности')
plt.title('Распределение времени полета из Нью-Йорка в Сан-Франциско')
plt.grid(True)

# Управление метками на оси x через интервал
x_ticks = np.arange(int(xmin), int(xmax)+1, 50)  # Определяем интервал между метками
plt.xticks(x_ticks)

plt.show()


