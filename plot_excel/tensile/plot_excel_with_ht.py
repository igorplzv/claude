import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

def load_and_process_data(file_path, is_heat_treated=False):
    wb = pd.ExcelFile(file_path)
    mode1_samples = []
    mode8_samples = []
    
    def get_sample_areas():
        # Известные площади сечения
        sample_areas = {
            '1-1': 7.163145,
            '1-2': 7.068583,
            '8-1': 7.115786,
            '8-2': 7.068583
        }
        return sample_areas
    
    def process_sheet(sheet, sample_areas=None, sample_id=None):
        print(f"Processing sheet: {sheet}")  # Отладочная информация
        try:
            df = pd.read_excel(wb, sheet, header=8)
            df = df.iloc[:, [0, 1]].dropna()
            
            if is_heat_treated and sample_areas and sample_id:
                area = sample_areas.get(sample_id)
                if area:
                    print(f"Using area {area} for sample {sample_id}")  # Отладочная информация
                    # Пересчет в напряжение и деформацию
                    df.iloc[:, 1] = df.iloc[:, 1] / area  # Сила в напряжение
                    df.iloc[:, 0] = (df.iloc[:, 0] / 15.0) * 100  # Перемещение в деформацию
                else:
                    print(f"Warning: No area found for sample {sample_id}")
                    return None
                    
            df.columns = ['strain', 'stress']
            
            if df['strain'].iloc[0] > 0:
                zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
                df = pd.concat([zero_point, df]).reset_index(drop=True)
            
            return df
        except Exception as e:
            print(f"Error processing sheet {sheet}: {str(e)}")
            return None
    
    sample_areas = get_sample_areas() if is_heat_treated else None
    
    if is_heat_treated:
        # Для данных после Т/О
        mode1_sheets = ['Образец1', 'Образец2']  # образцы 1-1 и 1-2
        mode8_sheets = ['Образец3', 'Образец4']  # образцы 8-1 и 8-2
        
        # Соответствие листов и ID образцов
        sheet_to_sample_id = {
            'Образец1': '1-1',
            'Образец2': '1-2',
            'Образец3': '8-1',
            'Образец4': '8-2'
        }
    else:
        # Для данных до Т/О
        mode1_sheets = ['Образец1', 'Образец2', 'Образец3']
        mode8_sheets = ['Образец4', 'Образец5', 'Образец6']
        sheet_to_sample_id = None
    
    # Обработка данных для каждого режима
    for sheet in mode1_sheets:
        if sheet in wb.sheet_names:
            sample_id = sheet_to_sample_id[sheet] if is_heat_treated else None
            df = process_sheet(sheet, sample_areas, sample_id)
            if df is not None:
                mode1_samples.append(df)
                print(f"Added sample {sheet} to mode 1")  # Отладочная информация
        else:
            print(f"Sheet {sheet} not found in the workbook")
            
    for sheet in mode8_sheets:
        if sheet in wb.sheet_names:
            sample_id = sheet_to_sample_id[sheet] if is_heat_treated else None
            df = process_sheet(sheet, sample_areas, sample_id)
            if df is not None:
                mode8_samples.append(df)
                print(f"Added sample {sheet} to mode 8")  # Отладочная информация
        else:
            print(f"Sheet {sheet} not found in the workbook")
    
    print(f"\nProcessed samples:")
    print(f"Mode 1: {len(mode1_samples)} samples")
    print(f"Mode 8: {len(mode8_samples)} samples")
                
    return mode1_samples, mode8_samples

def average_curves(samples):
    if not samples:
        return pd.DataFrame()
    
    for df in samples:
        if df['strain'].iloc[0] != 0:
            zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
            df = pd.concat([zero_point, df]).reset_index(drop=True)
    
    max_strain = max(df['strain'].max() for df in samples)
    strain_points = np.concatenate(([0], np.linspace(0.001, 0.1, 100), np.linspace(0.1, max_strain, 900)))
    
    interpolated_stress = []
    for df in samples:
        interpolated = np.interp(strain_points, df['strain'], df['stress'])
        interpolated_stress.append(interpolated)
    
    avg_stress = np.mean(interpolated_stress, axis=0)
    # Рассчитываем std только если есть больше одного образца
    if len(samples) > 1:
        std_stress = np.std(interpolated_stress, axis=0)
    else:
        std_stress = np.zeros_like(avg_stress)  # Нулевое отклонение для одного образца
    
    return pd.DataFrame({
        'strain': strain_points,
        'stress': avg_stress,
        'stress_std': std_stress
    })

def plot_all_curves(before_mode1_avg, before_mode8_avg, after_mode1_avg, after_mode8_avg):
    plt.figure(figsize=(12, 8), dpi=300)
    sns.set_theme(style="white")
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(plt.MultipleLocator(100))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(50))
    ax.xaxis.set_major_locator(plt.MultipleLocator(5))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.grid(True, which='major', linestyle='--', alpha=0.7)
    
    # Параметры для сглаживания
    elastic_limit = 1.5
    transition_zone = 0.5
    window = 50
    
    # Цвета для разных режимов
    colors = {
        'before_mode1': 'blue',
        'before_mode8': 'red',
        'after_mode1': 'darkblue',
        'after_mode8': 'darkred'
    }
    
    # Линии разных стилей для до/после термообработки
    styles = {
        'before': '-',
        'after': '--'
    }
    
    # Функция для обработки и построения одной кривой
    def process_and_plot_curve(mode_avg, color, label, style='-', is_after_ht=False):
        if mode_avg.empty:
            return
            
        elastic_mask = mode_avg['strain'] <= (elastic_limit - transition_zone)
        transition_mask = (mode_avg['strain'] > (elastic_limit - transition_zone)) & (mode_avg['strain'] <= (elastic_limit + transition_zone))
        plastic_mask = mode_avg['strain'] > (elastic_limit + transition_zone)
        
        smoothed = mode_avg['stress'].rolling(window=window, min_periods=1, center=True).mean()
        
        mode_avg['stress_smooth'] = mode_avg['stress'].copy()
        mode_avg.loc[elastic_mask, 'stress_smooth'] = mode_avg.loc[elastic_mask, 'stress']
        mode_avg.loc[plastic_mask, 'stress_smooth'] = smoothed[plastic_mask]
        
        transition_points = mode_avg[transition_mask].index
        for i in transition_points:
            strain = mode_avg.loc[i, 'strain']
            weight = (strain - (elastic_limit - transition_zone)) / (2 * transition_zone)
            mode_avg.loc[i, 'stress_smooth'] = (1 - weight) * mode_avg.loc[i, 'stress'] + weight * smoothed[i]
        
        mode_avg['stress_std_smooth'] = mode_avg['stress_std'].rolling(window=window, min_periods=1, center=True).mean()
        
        plt.plot(mode_avg['strain'], mode_avg['stress_smooth'], 
                label=label, color=color, linestyle=style, linewidth=2)
        
        # Разная прозрачность для кривых до и после Т/О
        alpha_value = 0.1 if is_after_ht else 0.2
        
        plt.fill_between(mode_avg['strain'],
                        mode_avg['stress_smooth'] - mode_avg['stress_std_smooth'],
                        mode_avg['stress_smooth'] + mode_avg['stress_std_smooth'],
                        color=color, alpha=alpha_value)
    
    # Построение всех кривых
    process_and_plot_curve(before_mode1_avg, colors['before_mode1'], 'Regime 1 (Before HT)', styles['before'], is_after_ht=False)
    process_and_plot_curve(before_mode8_avg, colors['before_mode8'], 'Regime 8 (Before HT)', styles['before'], is_after_ht=False)
    process_and_plot_curve(after_mode1_avg, colors['after_mode1'], 'Regime 1 (After HT)', styles['after'], is_after_ht=True)
    process_and_plot_curve(after_mode8_avg, colors['after_mode8'], 'Regime 8 (After HT)', styles['after'], is_after_ht=True)
    
    plt.xlabel('Strain, %', fontsize=16, fontname='Arial')
    plt.ylabel('Stress, MPa', fontsize=16, fontname='Arial')
    plt.title('Stress-strain curves for Ti15Ta SLM samples\nbefore and after heat treatment', 
              fontsize=18, fontname='Arial', pad=20)
    plt.legend(fontsize=12, frameon=True)
    
    plt.xticks(fontsize=14, fontname='Arial')
    plt.yticks(fontsize=14, fontname='Arial')
    
    plt.tick_params(which='both', direction='in', width=1)
    plt.tick_params(which='major', length=7)
    plt.tick_params(which='minor', length=4)
    
    all_curves = [before_mode1_avg, before_mode8_avg, after_mode1_avg, after_mode8_avg]
    max_strain = max(df['strain'].max() for df in all_curves if not df.empty)
    max_stress = max(df['stress'].max() for df in all_curves if not df.empty)
    
    plt.xlim(0, max_strain)
    plt.ylim(0, max_stress * 1.05)
    
    plt.tight_layout()
    return plt.gcf()

if __name__ == "__main__":
    # Загрузка данных до термообработки
    file_before = "Ti15Ta_SLM_m6_.xls"
    if os.path.exists(file_before):
        before_mode1_samples, before_mode8_samples = load_and_process_data(file_before, is_heat_treated=False)
        before_mode1_avg = average_curves(before_mode1_samples)
        before_mode8_avg = average_curves(before_mode8_samples)
    else:
        print(f"Warning: File {file_before} not found")
        before_mode1_avg = pd.DataFrame()
        before_mode8_avg = pd.DataFrame()
    
    # Загрузка данных после термообработки
    file_after = "2025_01_28-TiTa_1_8_HT.xls"
    if os.path.exists(file_after):
        after_mode1_samples, after_mode8_samples = load_and_process_data(file_after, is_heat_treated=True)
        after_mode1_avg = average_curves(after_mode1_samples)
        after_mode8_avg = average_curves(after_mode8_samples)
    else:
        print(f"Warning: File {file_after} not found")
        after_mode1_avg = pd.DataFrame()
        after_mode8_avg = pd.DataFrame()
    
    # Построение графиков
    fig = plot_all_curves(before_mode1_avg, before_mode8_avg, after_mode1_avg, after_mode8_avg)
    plt.savefig('stress_strain_curves_with_ht.png', dpi=300, bbox_inches='tight')
    plt.show()