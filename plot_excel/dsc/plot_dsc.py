import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.signal import savgol_filter

def load_dsc_data(file_path):
    """
    Загружает данные ДСК из Excel файла
    """
    try:
        df = pd.read_excel(file_path, header=None)
        header_row = df[df[0].astype(str).str.contains('#Temp|Temperature', na=False)].index[0]
        data = df.iloc[header_row + 1:].copy()
        data.columns = ['Temperature', 'Time', 'Heat_Flow', 'Sample']
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.dropna()
        data = data[['Temperature', 'Heat_Flow']]
        return data
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {str(e)}")
        return None

def plot_dsc_curves(mode1_heat, mode1_cool, mode8_heat, mode8_cool, output_path='dsc_curves.png'):
    """
    Строит график ДСК с кривыми нагрева и охлаждения для обоих режимов
    """
    plt.figure(figsize=(12, 8), dpi=300)
    
    # Настройка стиля
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 14  # Увеличиваем базовый размер шрифта
    
    # Настройка фона
    plt.gca().set_facecolor('white')
    plt.gcf().patch.set_facecolor('white')
    
    # Построение кривых
    plt.plot(mode1_heat['Temperature'], mode1_heat['Heat_Flow'], 
             'r-', label='Mode 1 (Heating)', linewidth=1.5)
    plt.plot(mode1_cool['Temperature'], mode1_cool['Heat_Flow'], 
             'b-', label='Mode 1 (Cooling)', linewidth=1.5)
    plt.plot(mode8_heat['Temperature'], mode8_heat['Heat_Flow'], 
             'r--', label='Mode 8 (Heating)', linewidth=1.5)
    plt.plot(mode8_cool['Temperature'], mode8_cool['Heat_Flow'], 
             'b--', label='Mode 8 (Cooling)', linewidth=1.5)

    # Добавляем известные температуры пиков с разнесенными позициями
    peak_annotations = [
        # Режим 1
        (842, 0.14, 'Mode 1\n842°C', 'red', (-50, 20)),    # нагрев
        (764, 0.0, 'Mode 1\n764°C', 'blue', (-20, -40)),   # охлаждение
        # Режим 8
        (844, 0.14, 'Mode 8\n844°C', 'red', (20, 20)),     # нагрев
        (767, -0.04, 'Mode 8\n767°C', 'blue', (15, -13)),  # охлаждение
    ]

    for temp, heat_flow, text, color, offset in peak_annotations:
        plt.annotate(text, 
                    xy=(temp, heat_flow),
                    xytext=offset,
                    textcoords='offset points',
                    color=color,
                    fontsize=12,
                    bbox=dict(facecolor='white', edgecolor='grey', alpha=0.8),
                    arrowprops=dict(arrowstyle='->',
                                  color=color,
                                  alpha=0.7))
    
    # Настройка графика с увеличенными шрифтами
    plt.xlabel('Temperature (°C)', fontsize=16, fontweight='bold')
    plt.ylabel('Heat Flow (mW/mg)', fontsize=16, fontweight='bold')
    plt.title('DSC Curves for Ti-15Ta Alloy\nModes 1 and 8, Heating/Cooling 20 K/min', 
              fontsize=18, fontweight='bold', pad=20)
    
    # Настройка осей
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.xaxis.set_minor_locator(MultipleLocator(50))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.01))
    
    # Увеличиваем размер подписей на осях
    ax.tick_params(axis='both', which='major', labelsize=14)
    
    # Устанавливаем пределы осей
    plt.xlim(600, 1000)
    plt.ylim(-0.05, 0.2)
    
    # Настраиваем сетку
    plt.grid(True, which='major', linestyle='-', alpha=0.2)
    plt.grid(True, which='minor', linestyle=':', alpha=0.1)
    
    # Легенда с увеличенным шрифтом
    plt.legend(loc='upper right', fontsize=14, frameon=True)
    
    # Стрелка экзо с увеличенным шрифтом
    plt.annotate(
        'exo ↓',
        xy=(610, 0.19),
        xytext=(610, 0.19),
        fontsize=16,  # Увеличиваем размер шрифта
        fontweight='bold',
        bbox=dict(
            facecolor='white',
            edgecolor='none',
            alpha=0.8
        )
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("DSC Analysis Program")
    print("-" * 50)
    
    files = {
        'mode1_heat': 'Ti15Ta 1 heat1.xlsx',
        'mode1_cool': 'Ti15Ta 1 cool1.xlsx',
        'mode8_heat': 'Ti15Ta 8 heat1.xlsx',
        'mode8_cool': 'Ti15Ta 8 cool1.xlsx'
    }
    
    data = {}
    for key, file_path in files.items():
        data[key] = load_dsc_data(file_path)
        if data[key] is None:
            print(f"Error loading {key} data")
            return
    
    plot_dsc_curves(
        data['mode1_heat'],
        data['mode1_cool'],
        data['mode8_heat'],
        data['mode8_cool'],
        'dsc_curves.png'
    )
    print(f"\nГрафик сохранен как dsc_curves.png")

if __name__ == "__main__":
    main()