import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.signal import savgol_filter

def load_and_process_data(file_path):
    wb = pd.ExcelFile(file_path)
    
    sheet_to_regime = {
        'Образец1': 1, 'Образец2': 1,
        'Образец3': 5,
        'Образец4': 9, 'Образец5': 9, 'Образец6': 9,
        'Образец7': 10, 'Образец8': 10,
        'Образец9': 11, 'Образец10': 11, 'Образец11': 11,
        'Образец12': 12
    }
    
    regime_params = {
        1: {'power': 200, 'speed': 800, 'hatch': 100, 'energy': 50.0, 'strategy': 'chess'},
        5: {'power': 200, 'speed': 1000, 'hatch': 100, 'energy': 40.0, 'strategy': 'chess'},
        9: {'power': 200, 'speed': 1000, 'hatch': 100, 'energy': 80.0, 'strategy': 'linear'},
        10: {'power': 200, 'speed': 800, 'hatch': 80, 'energy': 62.5, 'strategy': 'linear'},
        11: {'power': 250, 'speed': 800, 'hatch': 80, 'energy': 78.1, 'strategy': 'linear'},
        12: {'power': 200, 'speed': 1000, 'hatch': 80, 'energy': 50.0, 'strategy': 'linear'}
    }
    
    samples_by_regime = {}
    
    def process_sheet(sheet):
        df = pd.read_excel(wb, sheet, header=8)
        df = df.iloc[:, [0, 1]].dropna()
        df.columns = ['strain', 'stress']
        
        if df['strain'].iloc[0] > 0:
            zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
            df = pd.concat([zero_point, df]).reset_index(drop=True)
        
        # Находим точку максимального напряжения
        max_stress_idx = df['stress'].idxmax()
        max_stress = df['stress'].max()
        
        # Вычисляем градиент напряжения с использованием скользящего среднего
        stress_gradient = df['stress'].diff().rolling(window=3, center=True).mean()
        
        # Ищем основное падение напряжения
        steep_drop_threshold = -50
        cutoff_idx = max_stress_idx
        found_drop = False
        drop_start_idx = max_stress_idx
        
        for i in range(max_stress_idx + 1, len(df)):
            if stress_gradient.iloc[i] < steep_drop_threshold and not found_drop:
                found_drop = True
                drop_start_idx = i
            elif found_drop and abs(stress_gradient.iloc[i]) < abs(steep_drop_threshold/5):
                cutoff_idx = i
                break
        
        # Если не нашли явного падения, используем порог по напряжению
        if not found_drop:
            for i in range(max_stress_idx + 1, len(df)):
                if df['stress'].iloc[i] < 0.7 * max_stress:
                    cutoff_idx = i
                    break
        
        # Обрезаем данные и применяем сглаживание к конечному участку
        df = df.iloc[:cutoff_idx+1]
        
        if len(df) > max_stress_idx + 5:
            # Сглаживаем только участок после максимума
            post_max_data = df.iloc[max_stress_idx:]
            window = min(11, len(post_max_data) - 1 if len(post_max_data) % 2 == 0 else len(post_max_data))
            if window > 3:
                smoothed_stress = savgol_filter(post_max_data['stress'], window, 2)
                df.loc[df.index >= max_stress_idx, 'stress'] = smoothed_stress
        
        return df
    
    for sheet in wb.sheet_names:
        if sheet in sheet_to_regime:
            regime = sheet_to_regime[sheet]
            if regime not in samples_by_regime:
                samples_by_regime[regime] = []
            df = process_sheet(sheet)
            samples_by_regime[regime].append(df)
    
    return samples_by_regime, regime_params

def average_curves(samples):
    if len(samples) == 1:
        return samples[0]
    
    # Создаем единую сетку точек
    max_strain = max(df['strain'].max() for df in samples)
    strain_points = np.linspace(0, max_strain, 1000)
    
    # Интерполяция всех кривых на общую сетку
    interpolated = np.array([np.interp(strain_points, df['strain'], df['stress']) 
                           for df in samples])
    
    # Усреднение
    avg_stress = np.mean(interpolated, axis=0)
    
    # Дополнительное сглаживание среднего значения
    window = min(31, len(avg_stress) - 1 if len(avg_stress) % 2 == 0 else len(avg_stress))
    if window > 3:
        avg_stress = savgol_filter(avg_stress, window, 3)
    
    return pd.DataFrame({
        'strain': strain_points,
        'stress': avg_stress
    })

def plot_tensile_curves(samples_by_regime, regime_params):
    plt.figure(figsize=(14, 9), dpi=300)
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Arial'
    
    colors = {
        1: '#0066CC',  # темно-синий
        5: '#FF3300',  # ярко-оранжевый
        9: '#00CC00',  # зеленый
        10: '#CC0000', # красный
        11: '#6600CC', # фиолетовый
        12: '#FF9900'  # оранжевый
    }
    
    line_styles = {
        1: '-',
        5: '-',
        9: '-.',
        10: '-',
        11: '-',
        12: '-'
    }
    
    line_widths = {
        1: 2.0,
        5: 2.5,
        9: 2.0,
        10: 2.0,
        11: 2.0,
        12: 2.5
    }
    
    for regime in sorted(samples_by_regime.keys()):
        params = regime_params[regime]
        avg_curve = average_curves(samples_by_regime[regime])
        
        label = f"R{regime}: {params['power']}W, {params['speed']}mm/s,\nh={params['hatch']}µm ({params['energy']}J/mm³)"
        
        plt.plot(avg_curve['strain'], avg_curve['stress'],
                label=label,
                color=colors[regime],
                linestyle=line_styles[regime],
                linewidth=line_widths[regime],
                zorder=3 if regime == 11 else 2)

    plt.xlabel('Strain, %', fontsize=20, fontweight='bold')
    plt.ylabel('Stress, MPa', fontsize=20, fontweight='bold')
    
    plt.grid(True, linestyle=':', alpha=0.3, zorder=1)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(200))
    ax.tick_params(which='both', direction='in', width=1)
    ax.tick_params(which='major', length=6, labelsize=18)
    ax.tick_params(which='minor', length=3)
    
    plt.legend(fontsize=16, frameon=True, 
              loc='center left',
              bbox_to_anchor=(0.65, 0.5),
              borderaxespad=0,
              framealpha=0.9,
              edgecolor='none')
    
    plt.xlim(-0.1, 3.8)
    plt.ylim(-50, 1600)
    
    plt.text(0.02, 0.98, 'Chess strategy: R1, R5\nLinear strategy: R9-R12',
             transform=ax.transAxes,
             fontsize=16,
             verticalalignment='top',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.tight_layout()
    
    return plt.gcf()

if __name__ == "__main__":
    file_path = "TiNbZrCu_m6_.xls"
    samples_by_regime, regime_params = load_and_process_data(file_path)
    
    fig = plot_tensile_curves(samples_by_regime, regime_params)
    plt.savefig('tensile_curves_TiNbZrCu.png', dpi=300, bbox_inches='tight')
    plt.show()