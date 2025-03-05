import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.signal import savgol_filter

def load_and_process_data(file_path, manual_cutoffs=None):
    wb = pd.ExcelFile(file_path)
    
    sheet_to_regime = {
        'Образец1': 'C1', 'Образец2': 'C1',
        'Образец3': 'C5',
        'Образец4': 'L2', 'Образец5': 'L2', 'Образец6': 'L2',
        'Образец7': 'L3', 'Образец8': 'L3',
        'Образец9': 'L4', 'Образец10': 'L4', 'Образец11': 'L4',
        'Образец12': 'L5'
    }
    
    regime_params = {
        'C1': {'power': 200, 'speed': 800, 'hatch': 100, 'energy': 50.0},
        'C5': {'power': 200, 'speed': 1000, 'hatch': 100, 'energy': 40.0},
        'L2': {'power': 200, 'speed': 1000, 'hatch': 100, 'energy': 80.0, 'note': 'double scan'},
        'L3': {'power': 200, 'speed': 800, 'hatch': 80, 'energy': 62.5},
        'L4': {'power': 250, 'speed': 800, 'hatch': 80, 'energy': 78.1},
        'L5': {'power': 200, 'speed': 1000, 'hatch': 80, 'energy': 50.0}
    }
    
    samples_by_regime = {}
    
    def process_sheet(sheet, manual_cutoff=None):
        df = pd.read_excel(wb, sheet, header=8)
        df = df.iloc[:, [0, 1]].dropna()
        df.columns = ['strain', 'stress']
        
        if df['strain'].iloc[0] > 0:
            zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
            df = pd.concat([zero_point, df]).reset_index(drop=True)
        
        # Находим точку максимального напряжения
        max_stress_idx = df['stress'].idxmax()
        max_stress = df['stress'].max()
        
        if manual_cutoff is not None:
            # Проверяем, находится ли точка обрезки в пределах данных
            if manual_cutoff > df['strain'].max():
                print(f"Предупреждение: Выбранная точка обрезки {manual_cutoff} больше максимального strain {df['strain'].max()} для {sheet}")
                cutoff_idx = len(df) - 1
            elif manual_cutoff < df['strain'].min():
                print(f"Предупреждение: Выбранная точка обрезки {manual_cutoff} меньше минимального strain {df['strain'].min()} для {sheet}")
                cutoff_idx = 0
            else:
                # Находим ближайшую точку к выбранному значению strain
                cutoff_idx = (df['strain'] - manual_cutoff).abs().idxmin()
        else:
            # Автоматическое определение точки обрезки
            stress_gradient = df['stress'].diff().rolling(window=3, center=True).mean()
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
            
            if not found_drop:
                for i in range(max_stress_idx + 1, len(df)):
                    if df['stress'].iloc[i] < 0.7 * max_stress:
                        cutoff_idx = i
                        break
        
        # Обрезаем данные и применяем сглаживание
        df = df.iloc[:cutoff_idx+1]
        
        if len(df) > max_stress_idx + 5:
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
            
            # Получаем точку обрезки для данного режима, если она задана
            manual_cutoff = manual_cutoffs.get(regime) if manual_cutoffs else None
            df = process_sheet(sheet, manual_cutoff)
            samples_by_regime[regime].append(df)
    
    return samples_by_regime, regime_params

def average_curves(samples):
    if len(samples) == 1:
        return samples[0]
    
    max_strain = max(df['strain'].max() for df in samples)
    strain_points = np.linspace(0, max_strain, 1000)
    
    interpolated_stress = []
    for df in samples:
        interpolated = np.interp(strain_points, df['strain'], df['stress'])
        interpolated_stress.append(interpolated)
    
    avg_stress = np.mean(interpolated_stress, axis=0)
    
    window = min(31, len(avg_stress) - 1 if len(avg_stress) % 2 == 0 else len(avg_stress))
    if window > 3:
        avg_stress = savgol_filter(avg_stress, window, 3)
    
    return pd.DataFrame({
        'strain': strain_points,
        'stress': avg_stress
    })

def plot_sample_for_cutoff_selection(file_path, sheet_name):
    """
    Функция для отображения графика одного образца и выбора точки обрезки
    """
    wb = pd.ExcelFile(file_path)
    df = pd.read_excel(wb, sheet_name, header=8)
    df = df.iloc[:, [0, 1]].dropna()
    df.columns = ['strain', 'stress']
    
    if df['strain'].iloc[0] > 0:
        zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
        df = pd.concat([zero_point, df]).reset_index(drop=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['strain'], df['stress'])
    plt.grid(True)
    plt.xlabel('Strain, %')
    plt.ylabel('Stress, MPa')
    plt.title(f'Click to select cutoff point for {sheet_name}\nStrain range: {df["strain"].min():.2f} to {df["strain"].max():.2f}')
    
    cutoff_point = []
    def onclick(event):
        if event.xdata is not None:
            if df['strain'].min() <= event.xdata <= df['strain'].max():
                cutoff_point.append(event.xdata)
                plt.axvline(x=event.xdata, color='r', linestyle='--')
                plt.draw()
                plt.close()
            else:
                print(f"Предупреждение: Выбранная точка {event.xdata:.2f} находится вне диапазона данных ({df['strain'].min():.2f} - {df['strain'].max():.2f})")
    
    plt.connect('button_press_event', onclick)
    plt.show()
    
    return cutoff_point[0] if cutoff_point else None

def select_cutoff_points(file_path):
    """
    Функция для интерактивного выбора точек обрезки для всех режимов
    """
    wb = pd.ExcelFile(file_path)
    sheet_to_regime = {
        'Образец1': 'C1', 'Образец2': 'C1',
        'Образец3': 'C5',
        'Образец4': 'L2', 'Образец5': 'L2', 'Образец6': 'L2',
        'Образец7': 'L3', 'Образец8': 'L3',
        'Образец9': 'L4', 'Образец10': 'L4', 'Образец11': 'L4',
        'Образец12': 'L5'
    }
    
    cutoffs = {}
    processed_regimes = set()
    
    for sheet in wb.sheet_names:
        if sheet in sheet_to_regime:
            regime = sheet_to_regime[sheet]
            if regime not in processed_regimes:
                print(f"\nВыберите точку обрезки для режима {regime}")
                cutoff = plot_sample_for_cutoff_selection(file_path, sheet)
                if cutoff is not None:
                    cutoffs[regime] = cutoff
                processed_regimes.add(regime)
    
    return cutoffs

def plot_tensile_curves(samples_by_regime, regime_params):
    plt.figure(figsize=(14, 9), dpi=300)
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Arial'
    
    colors = {
        'C1': '#0066CC',  # темно-синий
        'C5': '#FF3300',  # ярко-оранжевый
        'L2': '#00CC00',  # зеленый
        'L3': '#CC0000',  # красный
        'L4': '#6600CC',  # фиолетовый
        'L5': '#FF9900'   # оранжевый
    }
    
    line_styles = {
        'C1': '-',
        'C5': '-',
        'L2': '-.',
        'L3': '-',
        'L4': '-',
        'L5': '-'
    }
    
    line_widths = {
        'C1': 2.0,
        'C5': 2.5,
        'L2': 2.0,
        'L3': 2.0,
        'L4': 2.0,
        'L5': 2.5
    }
    
    sorted_regimes = sorted(samples_by_regime.keys())
    
    for regime in sorted_regimes:
        params = regime_params[regime]
        avg_curve = average_curves(samples_by_regime[regime])
        
        # Формируем подпись с примечанием для режимов с особенностями
        label = f"{regime}: {params['power']}W, {params['speed']}mm/s,\nh={params['hatch']}µm"
        if 'note' in params:
            label += f" ({params['note']})"
        
        plt.plot(avg_curve['strain'], avg_curve['stress'],
                label=label,
                color=colors[regime],
                linestyle=line_styles[regime],
                linewidth=line_widths[regime],
                zorder=3 if regime == 'L4' else 2)

    plt.xlabel('Strain, %', fontsize=28, fontweight='bold')
    plt.ylabel('Stress, MPa', fontsize=28, fontweight='bold')
    
    plt.grid(True, linestyle=':', alpha=0.3, zorder=1)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(200))
    ax.tick_params(which='both', direction='in', width=1)
    ax.tick_params(which='major', length=6, labelsize=18)
    ax.tick_params(which='minor', length=3)
    
    plt.legend(fontsize=22, frameon=True, 
              loc='center left',
              bbox_to_anchor=(0.55, 0.5),
              borderaxespad=0,
              framealpha=0.9,
              edgecolor='none')
    
    plt.xlim(-0.1, 3.8)
    plt.ylim(-50, 1600)
    
    plt.tight_layout()
    
    return plt.gcf()

if __name__ == "__main__":
    file_path = "TiNbZrCu_m6_.xls"
    
    # Интерактивный выбор точек обрезки
    print("Выберите точки обрезки для каждого режима (кликните на графике в нужной точке)")
    manual_cutoffs = select_cutoff_points(file_path)
    
    # Загрузка и обработка данных с учетом выбранных точек обрезки
    samples_by_regime, regime_params = load_and_process_data(file_path, manual_cutoffs)
    
    # Построение итогового графика
    fig = plot_tensile_curves(samples_by_regime, regime_params)
    plt.savefig('tensile_curves_TiNbZrCu.png', dpi=300, bbox_inches='tight')
    plt.show()