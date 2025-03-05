import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

def load_and_process_data(file_path):
    try:
        # Загружаем данные микротвердости без заголовков
        df_hardness = pd.read_excel(file_path, header=None)
        print("Shape of data:", df_hardness.shape)
        print("\nFirst few rows of data:")
        print(df_hardness.head())
        
        # Создаем словарь с параметрами режимов
        modes_params = {
            1: {'energy_density': 62.5, 'hatch': 100},
            2: {'energy_density': 112.0, 'hatch': 100},
            3: {'energy_density': 70.0, 'hatch': 100},
            4: {'energy_density': 83.3, 'hatch': 100},
            5: {'energy_density': 50.0, 'hatch': 100},
            6: {'energy_density': 93.3, 'hatch': 100},
            7: {'energy_density': 116.7, 'hatch': 80},
            8: {'energy_density': 78.1, 'hatch': 80},
            9: {'energy_density': 87.5, 'hatch': 80}
        }
        
        # Структура для сбора данных по каждому режиму
        hardness_data = {}
        
        # Собираем данные по режимам
        current_mode = None
        for _, row in df_hardness.iterrows():
            if not pd.isna(row[0]):  # Если есть номер режима
                current_mode = int(row[0])
                if current_mode not in hardness_data:
                    hardness_data[current_mode] = []
            if current_mode is not None and not pd.isna(row[1]):  # Если есть значение твердости
                hardness_data[current_mode].append(row[1])
        
        # Формируем результаты
        results = []
        for mode in sorted(hardness_data.keys()):
            if mode in modes_params:
                values = hardness_data[mode]
                results.append({
                    'mode': mode,
                    'energy_density': modes_params[mode]['energy_density'],
                    'hatch': modes_params[mode]['hatch'],
                    'hardness_mean': np.mean(values),
                    'hardness_std': np.std(values)
                })
        
        result_df = pd.DataFrame(results)
        print("\nProcessed data:")
        print(result_df)
        return result_df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise
def plot_hardness_vs_energy(data):
   plt.figure(figsize=(10, 6), dpi=300)
   sns.set_theme(style="white")
   
   # Разделяем данные по hatch distance
   hatch_100 = data[data['hatch'] == 100]
   hatch_80 = data[data['hatch'] == 80]
   
   # Построение точек и error bars
   plt.errorbar(hatch_100['energy_density'], hatch_100['hardness_mean'],
               yerr=hatch_100['hardness_std'],
               fmt='o', color='blue', capsize=5, capthick=1.5,
               label='h = 100 µm', markersize=8)
   
   plt.errorbar(hatch_80['energy_density'], hatch_80['hardness_mean'],
               yerr=hatch_80['hardness_std'],
               fmt='o', color='green', capsize=5, capthick=1.5,
               label='h = 80 µm', markersize=8)
   
   # Настройка осей
   ax = plt.gca()
   plt.ylim(150, 250)  # Диапазон от 150 до 250
   ax.yaxis.set_major_locator(plt.MultipleLocator(25))  # Основные деления каждые 25 единиц
   ax.yaxis.set_minor_locator(plt.MultipleLocator(5))  # Вспомогательные деления каждые 5 единиц
   ax.xaxis.set_major_locator(plt.MultipleLocator(10))
   ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
   ax.grid(True, which='major', linestyle='--', alpha=0.7)
   
   plt.xlabel('Energy density, J/mm³', fontsize=16, fontname='Arial')
   plt.ylabel('Microhardness, HV$_{0.5}$', fontsize=16, fontname='Arial')
   plt.title('Correlation between microhardness and energy density in Ti-15Ta alloy',
            fontsize=18, fontname='Arial', pad=20)
   
   plt.legend(fontsize=14, frameon=True)
   
   plt.xticks(fontsize=14, fontname='Arial')
   plt.yticks(fontsize=14, fontname='Arial')
   
   plt.tick_params(which='both', direction='in', width=1)
   plt.tick_params(which='major', length=7)
   plt.tick_params(which='minor', length=4)
   
   plt.tight_layout()
   
   return plt.gcf()

if __name__ == "__main__":
    file_path = input("Enter the path to Excel file with microhardness data (.xlsx): ")
    print(f"Input path: {file_path}")
    
    data = load_and_process_data(file_path)
    fig = plot_hardness_vs_energy(data)
    plt.savefig('microhardness_vs_energy.png', dpi=300, bbox_inches='tight')
    plt.show()