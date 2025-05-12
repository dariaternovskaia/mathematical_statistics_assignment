import csv
import math
import matplotlib.pyplot as plt  # Импортируем matplotlib для построения графиков

# Путь к вашему CSV-файлу
csv_file_path = 'C:\\Users\\Dasha\\Downloads\\flights_NY.csv'  # Замените на фактический путь к вашему файлу

# Инициализация структур данных
# Создаем списки для подсчета количества вылетов и суммарных задержек по каждому часу
hours_count = [0] * 24  # Индексы 0-23 соответствуют часам
hours_delay = [0] * 24

# Функция для проверки наличия пропущенных значений в строке
def has_missing_values(row):
    for value in row:
        if value.strip() == '' or value.strip().upper() == 'NA':
            return True
    return False

# Функция для извлечения часа из времени в формате HHMM или HMM
def extract_hour(time_str):
    if len(time_str) == 3:
        return int(time_str[0])
    elif len(time_str) == 4:
        return int(time_str[:2])
    else:
        raise ValueError(f"Неправильный формат времени: {time_str}")

# Чтение и обработка CSV-файла
try:
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Извлечение заголовков
        headers = next(reader)
        headers = [header.strip().lower() for header in headers]  # Приводим заголовки к нижнему регистру для удобства
        
        # Создаем словарь для доступа по имени столбца
        header_indices = {header: index for index, header in enumerate(headers)}
        
        # Проверяем, что все необходимые столбцы присутствуют
        required_columns = ['year', 'month', 'day', 'dep_time', 'arr_time', 'dep_delay', 'arr_delay',
                            'carrier', 'flight', 'tailnum', 'origin', 'dest', 'air_time', 'distance']
        missing_columns = [col for col in required_columns if col not in header_indices]
        if missing_columns:
            print(f"Отсутствуют необходимые столбцы: {missing_columns}")
            exit(1)
        
        total_rows = 0
        processed_rows = 0
        
        for row in reader:
            total_rows += 1
            
            # Проверяем наличие пропущенных значений
            if has_missing_values(row):
                continue  # Пропускаем строку с пропущенными значениями
            
            # Фильтрация по аэропорту отправления JFK
            origin = row[header_indices['origin']].strip().upper()
            if origin != 'JFK':
                continue  # Пропускаем строки, где отправление не из JFK
            
            # Извлекаем время вылета и задержку
            dep_time_str = row[header_indices['dep_time']].strip()
            dep_delay_str = row[header_indices['dep_delay']].strip()
            
            # Проверяем, что время и задержка не пустые
            if not dep_time_str or not dep_delay_str:
                continue  # Пропускаем строку, если отсутствуют данные
            
            try:
                dep_hour = extract_hour(dep_time_str)
                dep_delay = float(dep_delay_str)
            except ValueError:
                continue  # Пропускаем строку с неверным форматом данных
            
            # Обновляем счетчики
            if 0 <= dep_hour < 24:
                hours_count[dep_hour] += 1
                hours_delay[dep_hour] += dep_delay
                processed_rows += 1
            else:
                continue  # Пропускаем строки с недопустимым часом
    
    print(f"Всего строк в файле: {total_rows}")
    print(f"Обработано строк: {processed_rows}")
    
    # Нахождение двух пиковых часов: один до полудня, другой после
    # Определяем максимальное количество вылетов до 12 часов и после
    am_peak_hour = -1
    pm_peak_hour = -1
    max_am = -1
    max_pm = -1
    
    for hour in range(24):
        if hour < 12:
            if hours_count[hour] > max_am:
                max_am = hours_count[hour]
                am_peak_hour = hour
        else:
            if hours_count[hour] > max_pm:
                max_pm = hours_count[hour]
                pm_peak_hour = hour
    
    if am_peak_hour == -1 or pm_peak_hour == -1:
        print("Не удалось найти пиковые часы для утренних или дневных вылетов.")
        exit(1)
    
    # Вычисление среднего времени задержки для найденных пиковых часов
    avg_delay_am = hours_delay[am_peak_hour] / hours_count[am_peak_hour] if hours_count[am_peak_hour] else 0
    avg_delay_pm = hours_delay[pm_peak_hour] / hours_count[pm_peak_hour] if hours_count[pm_peak_hour] else 0
    
    print(f"\nПиковый час до полудня: {am_peak_hour}:00 - Вылетов: {max_am}")
    print(f"Средняя задержка в этот час: {avg_delay_am:.2f} минут")
    
    print(f"\nПиковый час после полудня: {pm_peak_hour}:00 - Вылетов: {max_pm}")
    print(f"Средняя задержка в этот час: {avg_delay_pm:.2f} минут")
    
    # Определение, в каком из часов средняя задержка больше
    if avg_delay_am > avg_delay_pm:
        print("\nСредняя задержка больше в утренний пиковый час.")
    elif avg_delay_pm > avg_delay_am:
        print("\nСредняя задержка больше в дневной пиковый час.")
    else:
        print("\nСредние задержки в оба пиковых часа равны.")
    
    # Проверка статистической значимости различий в средних задержках
    # Используем простую проверку различия средних с использованием стандартных ошибок
    # Предположим независимость выборок и известную дисперсию, что не совсем корректно,
    # но для простоты мы применим простой Z-тест.
    
    # Вычисление стандартных отклонений для каждого часа
    # Нам необходимо пройтись по данным снова, чтобы собрать индивидуальные задержки
    am_delays = []
    pm_delays = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if has_missing_values(row):
                continue
            origin = row[header_indices['origin']].strip().upper()
            if origin != 'JFK':
                continue
            dep_time_str = row[header_indices['dep_time']].strip()
            dep_delay_str = row[header_indices['dep_delay']].strip()
            if not dep_time_str or not dep_delay_str:
                continue
            try:
                dep_hour = extract_hour(dep_time_str)
                dep_delay = float(dep_delay_str)
            except ValueError:
                continue
            if dep_hour == am_peak_hour:
                am_delays.append(dep_delay)
            elif dep_hour == pm_peak_hour:
                pm_delays.append(dep_delay)
    
    # Функция для вычисления среднего и стандартного отклонения
    def calculate_stats(delays):
        n = len(delays)
        if n == 0:
            return 0, 0
        mean = sum(delays) / n
        variance = sum((x - mean) ** 2 for x in delays) / (n - 1) if n > 1 else 0
        std_dev = math.sqrt(variance)
        return mean, std_dev
    
    mean_am, std_dev_am = calculate_stats(am_delays)
    mean_pm, std_dev_pm = calculate_stats(pm_delays)
    
    # Вычисление Z-статистики
    if std_dev_am == 0 or std_dev_pm == 0:
        print("\nНевозможно провести статистическую проверку из-за отсутствия вариаций в данных.")
    else:
        z = (mean_am - mean_pm) / math.sqrt((std_dev_am ** 2) / len(am_delays) + (std_dev_pm ** 2) / len(pm_delays))
        # Для простоты принимаем порог Z-статистики 1.96 (для 95% доверия)
        if abs(z) > 1.96:
            print("Различие в средних значениях задержек статистически значимо (p < 0.05).")
        else:
            print("Различие в средних значениях задержек не является статистически значимым (p >= 0.05).")
    
    # -------------- Добавление графика распределения вылетов по часам --------------
    # Настройка данных для графика
    hours = list(range(24))
    counts = hours_count
    
    # Создание фигуры и оси
    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts, color='skyblue')
    
    # Добавление заголовка и меток осей
    plt.title('Распределение количества вылетов по часам из аэропорта JFK')
    plt.xlabel('Час дня (0-23)')
    plt.ylabel('Количество вылетов')
    
    # Добавление отметок пиковых часов
    plt.axvline(x=am_peak_hour, color='red', linestyle='--', label=f'Пик до полудня ({am_peak_hour}:00)')
    plt.axvline(x=pm_peak_hour, color='green', linestyle='--', label=f'Пик после полудня ({pm_peak_hour}:00)')
    
    # Добавление легенды
    plt.legend()
    
    # Отображение графика
    plt.xticks(hours)  # Установка отметок оси X на каждый час
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    # --------------------------------------------------------------------------------

except FileNotFoundError:
    print(f"Файл по пути {csv_file_path} не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
