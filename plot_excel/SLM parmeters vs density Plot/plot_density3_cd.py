import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

def load_and_process_data(file_path='Ti13Nb13Zr5Cu_density.csv'):
    """Load and process density data from CSV file"""
    # Читаем CSV файл с указанием разделителя и кодировки
    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    
    # Очищаем названия столбцов от пробелов
    df.columns = df.columns.str.strip()
    
    # Преобразуем названия столбцов для удобства
    column_mapping = {
        'Название режима': 'Режим',
        'Мощность (P), Вт': 'Мощность',
        'Скорость (V), мм/с': 'Скорость',
        'Расстояние между треками (h), мкм': 'Расстояние',
        'Плотность энергии*, Дж/мм³': 'Энергия',
        'Плотность (металлографический метод на шлифе), %': 'Плотность',
    }
    df = df.rename(columns=column_mapping)
    
    # Преобразуем числовые значения, заменяя запятые на точки
    numeric_columns = ['Энергия', 'Плотность']
    for col in numeric_columns:
        df[col] = df[col].str.replace(',', '.').astype(float)
    
    # Определяем стратегию сканирования
    df['Strategy'] = df['Режим'].apply(
        lambda x: 'Linear pattern' if any(c.isalpha() for c in str(x)) else 'Chess pattern'
    )
    
    # Добавляем стандартные отклонения (можно настроить значения)
    df['Отклонение'] = np.where(df['Strategy'] == 'Chess pattern', 0.15, 0.08)
    
    print("Loaded data:")
    print(df[['Режим', 'Strategy', 'Энергия', 'Плотность', 'Отклонение']])
    
    return df

def set_style_params():
    """Set up the plotting style parameters"""
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.size': 16,
        'axes.labelsize': 18,
        'axes.titlesize': 18,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'legend.fontsize': 16,
        'figure.dpi': 300,
        'axes.grid': True,
        'grid.linestyle': '--',
        'grid.alpha': 0.7
    })

def create_plots(data):
    """Create two publication-quality plots"""
    set_style_params()
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot 1: Energy Density vs Relative Density
    for strategy, props in [('Chess pattern', ('o', '#2563eb')), 
                          ('Linear pattern', ('s', '#16a34a'))]:
        marker, color = props
        group = data[data['Strategy'] == strategy]
        
        ax1.errorbar(group['Энергия'], 
                    group['Плотность'],
                    yerr=group['Отклонение'],
                    fmt=marker,
                    color=color,
                    markersize=12,
                    capsize=8,
                    capthick=2,
                    elinewidth=2,
                    label=strategy,
                    zorder=3)

    # Customize first plot
    ax1.set_xlabel('Energy Density (J/mm³)', fontsize=18, fontweight='bold')
    ax1.set_ylabel('Relative Density (%)', fontsize=18, fontweight='bold')
    ax1.set_xlim(25, 85)
    ax1.set_ylim(95, 100.5)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax1.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)
    ax1.legend(frameon=True, fancybox=True, shadow=True, fontsize=16, loc='lower right')
    ax1.text(0.05, 0.95, 'a)', transform=ax1.transAxes, fontsize=20, fontweight='bold')
    
    # Plot 2: Scanning Speed vs Relative Density
    power_colors = {150: '#1f77b4', 200: '#ff7f0e', 250: '#2ca02c'}
    for power in sorted(data['Мощность'].unique()):
        group = data[data['Мощность'] == power]
        ax2.errorbar(group['Скорость'],
                    group['Плотность'],
                    yerr=group['Отклонение'],
                    fmt='o',
                    color=power_colors[power],
                    markersize=12,
                    capsize=8,
                    capthick=2,
                    elinewidth=2,
                    label=f'{power} W',
                    zorder=3)

    # Customize second plot
    ax2.set_xlabel('Scanning Speed (mm/s)', fontsize=18, fontweight='bold')
    ax2.set_ylabel('Relative Density (%)', fontsize=18, fontweight='bold')
    ax2.set_xlim(400, 1100)
    ax2.set_ylim(95, 100.5)
    ax2.xaxis.set_major_locator(MultipleLocator(200))
    ax2.xaxis.set_minor_locator(MultipleLocator(100))
    ax2.yaxis.set_major_locator(MultipleLocator(1))
    ax2.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax2.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)
    leg = ax2.legend(frameon=True, fancybox=True, shadow=True, fontsize=16, title='Laser Power')
    leg.get_title().set_fontsize(16)
    ax2.text(0.05, 0.95, 'b)', transform=ax2.transAxes, fontsize=20, fontweight='bold')

    # Customize spines for both plots
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_linewidth(2)

    plt.tight_layout()
    return fig

def main():
    # Load and process data from CSV
    data = load_and_process_data()
    
    # Create plots
    fig = create_plots(data)
    
    # Save figures with high resolution
    fig.savefig('density_analysis.png', dpi=600, bbox_inches='tight', format='png')
    fig.savefig('density_analysis.pdf', bbox_inches='tight', format='pdf')
    
    plt.show()

if __name__ == "__main__":
    main()