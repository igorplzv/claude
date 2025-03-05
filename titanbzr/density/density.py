import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Пример данных (замените на свои, если они отличаются)
data = {
    'Sample': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'P (W)': [250, 280, 280, 250, 250, 280, 280, 250, 280],
    'V (mm/s)': [800, 500, 800, 600, 1000, 600, 600, 800, 800],
    'E (J/mm³)': [62.5, 112, 70, 83.3, 50, 93.3, 116.7, 78.1, 87.5],
    'Relative Density Hydrostatic (%)': [99.90, 99.65, 99.96, 99.68, 99.66, 99.78, 99.56, 99.67, 99.76],
    'Relative Density Metallographic (%)': [99.87, 99.71, 99.85, 99.96, 99.87, 99.77, 99.93, 99.90, 99.89]
}

df = pd.DataFrame(data)

# Реальные стандартные отклонения для гидростатической плотности (в % от теоретической плотности 4.936 г/см³)
std_hydro_percent = np.array([0.425, 0.270, 0.157, 0.232, 0.172, 0.241, 0.220, 0.292, 0.271])  # Пересчитанные из г/см³ в %

# Для металлографической плотности предполагаем меньшие отклонения (можно уточнить)
std_metallo_percent = np.random.uniform(0.03, 0.08, size=len(df))  # Пример, замените реальными данными

# Настройка шрифта для профессионального вида
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12  # Базовый размер для подписей осей

# Создание двух графиков рядом
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# График 1 (a): Relative Density vs. Energy Density with error bars
for i, row in df.iterrows():
    # Hydrostatic density
    hydro_value = row['Relative Density Hydrostatic (%)']
    hydro_std = std_hydro_percent[i]
    hydro_upper = min(hydro_value + hydro_std, 99.9)  # Ограничение сверху до 99.9%
    hydro_lower = max(hydro_value - hydro_std, 99.0)  # Ограничение снизу
    # Убедимся, что yerr неотрицательный
    yerr_hydro = [[max(0, hydro_value - hydro_lower)], [max(0, hydro_upper - hydro_value)]]
    ax1.errorbar(row['E (J/mm³)'], hydro_value, yerr=yerr_hydro, 
                 fmt='o', color='blue', capsize=4, markersize=6, label='Hydrostatic' if i == 0 else "")
    
    # Metallographic density
    metallo_value = row['Relative Density Metallographic (%)']
    metallo_std = std_metallo_percent[i]
    metallo_upper = min(metallo_value + metallo_std, 99.9)  # Ограничение сверху до 99.9%
    metallo_lower = max(metallo_value - metallo_std, 99.0)  # Ограничение снизу
    # Убедимся, что yerr неотрицательный
    yerr_metallo = [[max(0, metallo_value - metallo_lower)], [max(0, metallo_upper - metallo_value)]]
    ax1.errorbar(row['E (J/mm³)'], metallo_value, yerr=yerr_metallo, 
                 fmt='o', color='red', capsize=4, markersize=6, label='Metallographic' if i == 0 else "")

ax1.set_xlabel('Volumetric Energy Density (J/mm³)', fontsize=12)
ax1.set_ylabel('Relative Density (%)', fontsize=12)
ax1.set_title('(a) Relative Density vs. Energy Density', fontsize=16)
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)  # Более тонкая и менее заметная сетка
ax1.set_ylim(99.0, 100.2)  # Увеличенный диапазон по оси Y

# График 2 (b): Relative Density vs. Scanning Speed with error bars
# Используем отдельные вызовы errorbar для каждой группы с уникальной меткой
p250_data = df[df['P (W)'] == 250]
p280_data = df[df['P (W)'] == 280]

# Для P = 250 W (синий) — одна метка для всей группы
x_250 = p250_data['V (mm/s)']
y_250 = p250_data['Relative Density Hydrostatic (%)']
std_250 = std_hydro_percent[p250_data.index]
upper_250 = np.minimum(y_250 + std_250, 99.9)
lower_250 = np.maximum(y_250 - std_250, 99.0)
yerr_250 = np.array([[max(0, y - l) for y, l in zip(y_250, lower_250)], 
                     [max(0, u - y) for y, u in zip(y_250, upper_250)]])

ax2.errorbar(x_250, y_250, yerr=yerr_250, 
             fmt='o', color='blue', capsize=4, markersize=6, label='P = 250 W')

# Для P = 280 W (красный) — одна метка для всей группы
x_280 = p280_data['V (mm/s)']
y_280 = p280_data['Relative Density Hydrostatic (%)']
std_280 = std_hydro_percent[p280_data.index]
upper_280 = np.minimum(y_280 + std_280, 99.9)
lower_280 = np.maximum(y_280 - std_280, 99.0)
yerr_280 = np.array([[max(0, y - l) for y, l in zip(y_280, lower_280)], 
                     [max(0, u - y) for y, u in zip(y_280, upper_280)]])

ax2.errorbar(x_280, y_280, yerr=yerr_280, 
             fmt='o', color='red', capsize=4, markersize=6, label='P = 280 W')

ax2.set_xlabel('Scanning Speed (mm/s)', fontsize=12)
ax2.set_ylabel('Relative Density (%)', fontsize=12)
ax2.set_title('(b) Relative Density vs. Scanning Speed', fontsize=16)
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)  # Более тонкая и менее заметная сетка
ax2.set_ylim(99.0, 100.2)  # Увеличенный диапазон по оси Y

# Общий заголовок
fig.suptitle('Effect of SLM Processing Parameters on the Relative Density of Ti-10Ta-2Nb-2Zr Alloy', fontsize=16)

# Оптимизация расположения
plt.tight_layout()

# Сохранение графика
plt.savefig('density_plots_with_errorbars_english_optimized_final_fixed_legend.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()