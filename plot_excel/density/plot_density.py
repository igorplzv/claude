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
        
        # Формируем результаты
        results = []
        for mode in modes_params:
            row = df[df['mode'] == mode].iloc[0]
            results.append({
                'mode': mode,
                'energy_density': modes_params[mode]['energy_density'],
                'hatch': modes_params[mode]['hatch'],
                'relative_density': row['relative_density'],
                'density': row['density'],  # Добавляем данные плотности по взвешиванию
                'std_dev': 0.1  # Пример стандартного отклонения (замените на реальные данные)
            })
        
        result_df = pd.DataFrame(results)
        print("\nProcessed data:")
        print(result_df)
        return result_df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

def plot_density_vs_energy(data):
    """Построение графика с двумя осями Y"""
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    sns.set_theme(style="white")
    
    # Разделяем данные по hatch distance
    hatch_100 = data[data['hatch'] == 100]
    hatch_80 = data[data['hatch'] == 80]
    
    # Первая ось Y: Относительная плотность
    ax1.errorbar(hatch_100['energy_density'], hatch_100['relative_density'],
                 yerr=hatch_100['std_dev'], fmt='o', color='blue', capsize=5, capthick=1.5,
                 label='h = 100 µm (Relative Density)', markersize=8)
    
    ax1.errorbar(hatch_80['energy_density'], hatch_80['relative_density'],
                 yerr=hatch_80['std_dev'], fmt='o', color='green', capsize=5, capthick=1.5,
                 label='h = 80 µm (Relative Density)', markersize=8)
    
    ax1.set_ylim(95, 100)  # Диапазон для относительной плотности
    ax1.set_xlabel('Energy density, J/mm³', fontsize=16, fontname='Arial')
    ax1.set_ylabel('Relative density, %', fontsize=16, fontname='Arial', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    
    # Вторая ось Y: Плотность по взвешиванию
    ax2 = ax1.twinx()
    ax2.plot(hatch_100['energy_density'], hatch_100['density'],
             's', color='red', label='h = 100 µm (Density)', markersize=8)
    
    ax2.plot(hatch_80['energy_density'], hatch_80['density'],
             's', color='orange', label='h = 80 µm (Density)', markersize=8)
    
    ax2.set_ylim(5.0, 5.1)  # Диапазон для плотности
    ax2.set_ylabel('Density, g/cm³', fontsize=16, fontname='Arial', color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    # Настройка осей
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(MultipleLocator(0.2))
    ax1.grid(True, which='major', linestyle='--', alpha=0.7)
    
    # Объединение легенд
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=12, frameon=True, loc='upper left')
    
    plt.tight_layout()
    
    return fig

if __name__ == "__main__":
    file_path = input("Enter the path to Excel file with density data (.xlsx): ")
    print(f"Input path: {file_path}")
    
    data = load_and_process_data(file_path)
    fig = plot_density_vs_energy(data)
    plt.savefig('density_vs_energy_with_density.png', dpi=300, bbox_inches='tight')
    plt.show()