
import pandas as pd
import matplotlib.pyplot as plt

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


# Печать первых нескольких строк данных
print(df.head())

# Теперь попробуйте обращаться к столбцам и выполнить другие операции
top_airports = df['dest'].value_counts().head(10).index.tolist()

# 1. Определение топ-10 аэропортов, в которые чаще всего летают из Нью-Йорка
top_airports = df['dest'].value_counts().head(10).index.tolist()

df['arr_delay'] = pd.to_numeric(df['arr_delay'], errors='coerce')

# 2. Вычисление вероятности задержки прилета для каждого из топ-10 аэропортов
delay_probabilities = []
for airport in top_airports:
    total_flights = len(df[df['dest'] == airport])
    delayed_flights = len(df[(df['dest'] == airport) & (df['arr_delay'] > 0)])
    delay_probability = delayed_flights / total_flights
    delay_probabilities.append(delay_probability)
    print(f'Аэропорт: {airport}, Вероятность задержки: {delay_probability}')

# 3. Построение столбчатой диаграммы
plt.figure(figsize=(12, 6))
plt.bar(top_airports, delay_probabilities, color='skyblue')
plt.xlabel('Аэропорт')
plt.ylabel('Вероятность задержки прилета')
plt.title('Вероятность задержки прилета в топ-10 аэропортов из Нью-Йорка')
plt.xticks(rotation=45)
plt.show()

# 4. Определение аэропорта с наибольшей и наименьшей вероятностью задержки
max_delay_airport = top_airports[delay_probabilities.index(max(delay_probabilities))]
min_delay_airport = top_airports[delay_probabilities.index(min(delay_probabilities))]

print(f'Аэропорт с наибольшей вероятностью задержки: {max_delay_airport}')
print(f'Аэропорт с наименьшей вероятностью задержки: {min_delay_airport}')
