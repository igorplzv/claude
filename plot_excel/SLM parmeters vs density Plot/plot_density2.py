import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

def load_and_process_data(file_path):
    """Загрузка и обработка данных из Excel файла"""
    try:
        # Загружаем данные
        df = pd.read_excel(file_path, sheet_name='Лист1', skiprows=2)
        print("Shape of data:", df.shape)
        print("\nFirst few rows of data:")
        print(df.head())
        
        # Переименуем столбцы для удобства
        df.columns = ['mode', 'power', 'speed', 'layer_thickness', 'hatch', 'energy_density', 'density', 'relative_density']
        
        # Создаем словарь с параметрами режимов
        modes_params = {
            1: {'energy_density': 62.5, 'hatch': 100, 'speed': 800, 'power': 250},
            2: {'energy_density': 112.0, 'hatch': 100, 'speed': 500, 'power': 280},
            3: {'energy_density': 70.0, 'hatch': 100, 'speed': 800, 'power': 280},
            4: {'energy_density': 83.3, 'hatch': 100, 'speed': 600, 'power': 250},
            5: {'energy_density': 50.0, 'hatch': 100, 'speed': 1000, 'power': 250},
            6: {'energy_density': 93.3, 'hatch': 100, 'speed': 600, 'power': 280},
            7: {'energy_density': 116.7, 'hatch': 80, 'speed': 600, 'power': 280},
            8: {'energy_density': 78.1, 'hatch': 80, 'speed': 800, 'power': 250},
            9: {'energy_density': 87.5, 'hatch': 80, 'speed': 800, 'power': 280}
        }
        
        # Формируем результаты
        results = []
        for mode in modes_params:
            row = df[df['mode'] == mode].iloc[0]
            results.append({
                'mode': mode,
                'energy_density': modes_params[mode]['energy_density'],
                'hatch': modes_params[mode]['hatch'],
                'speed': modes_params[mode]['speed'],
                'power': modes_params[mode]['power'],
                'relative_density': row['relative_density'],
                'std_dev': 0.1  # Пример стандартного отклонения (замените на реальные данные)
            })
        
        result_df = pd.DataFrame(results)
        print("\nProcessed data:")
        print(result_df)
        return result_df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

def plot_double_graph(data):
    """Построение двойного графика"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12), dpi=300)  # Изменено на вертикальную ориентацию
    sns.set_theme(style="white")
    
    # Разделяем данные по hatch distance (график a)
    hatch_100 = data[data['hatch'] == 100]
    hatch_80 = data[data['hatch'] == 80]
    
    # График (a): Влияние hatch distance (относительная плотность vs плотность энергии)
    ax1.errorbar(hatch_100['energy_density'], hatch_100['relative_density'],
                 yerr=hatch_100['std_dev'], fmt='o', color='blue', capsize=5, capthick=1.5,
                 label='h = 100 µm', markersize=8)
    
    ax1.errorbar(hatch_80['energy_density'], hatch_80['relative_density'],
                 yerr=hatch_80['std_dev'], fmt='o', color='green', capsize=5, capthick=1.5,
                 label='h = 80 µm', markersize=8)
    
    ax1.set_xlabel('Energy density, J/mm³', fontsize=16, fontname='Arial')  # Увеличенный шрифт
    ax1.set_ylabel('Relative density, %', fontsize=16, fontname='Arial')  # Увеличенный шрифт
    ax1.set_ylim(95, 100)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(MultipleLocator(0.2))
    ax1.grid(True, which='major', linestyle='--', alpha=0.7)
    ax1.legend(fontsize=14, frameon=True)  # Увеличенный шрифт
    ax1.set_title('(a) Influence of hatch spacing', fontsize=18, fontname='Arial', pad=10)  # Увеличенный шрифт
    
    # Увеличение шрифта значений на осях
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.tick_params(axis='both', which='minor', labelsize=12)
    
    # Разделяем данные по мощности (график b)
    power_250 = data[data['power'] == 250]
    power_280 = data[data['power'] == 280]
    
    # График (b): Влияние скорости сканирования (относительная плотность vs скорость сканирования)
    ax2.errorbar(power_250['speed'], power_250['relative_density'],
                 yerr=power_250['std_dev'], fmt='o', color='blue', capsize=5, capthick=1.5,
                 label='250 W', markersize=8)
    
    ax2.errorbar(power_280['speed'], power_280['relative_density'],
                 yerr=power_280['std_dev'], fmt='o', color='green', capsize=5, capthick=1.5,
                 label='280 W', markersize=8)
    
    ax2.set_xlabel('Scanning speed, mm/s', fontsize=16, fontname='Arial')  # Увеличенный шрифт
    ax2.set_ylabel('Relative density, %', fontsize=16, fontname='Arial')  # Увеличенный шрифт
    ax2.set_ylim(95, 100)
    ax2.xaxis.set_major_locator(MultipleLocator(100))
    ax2.xaxis.set_minor_locator(MultipleLocator(50))
    ax2.yaxis.set_major_locator(MultipleLocator(1))
    ax2.yaxis.set_minor_locator(MultipleLocator(0.2))
    ax2.grid(True, which='major', linestyle='--', alpha=0.7)
    ax2.legend(fontsize=14, frameon=True)  # Увеличенный шрифт
    ax2.set_title('(b) Effect of scanning speed', fontsize=18, fontname='Arial', pad=10)  # Увеличенный шрифт
    
    # Увеличение шрифта значений на осях
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='both', which='minor', labelsize=12)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    file_path = input("Enter the path to Excel file with density data (.xlsx): ")
    print(f"Input path: {file_path}")
    
    data = load_and_process_data(file_path)
    fig = plot_double_graph(data)
    plt.savefig('double_graph.png', dpi=300, bbox_inches='tight')
    plt.show()