import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

def load_and_process_data(file_path, mode1_sheets=['Образец1', 'Образец2', 'Образец3'], 
                        mode8_sheets=['Образец4', 'Образец5', 'Образец6']):
   wb = pd.ExcelFile(file_path)
   mode1_samples = []
   mode8_samples = []
   
   # Функция для обработки отдельного листа
   def process_sheet(sheet):
       df = pd.read_excel(wb, sheet, header=8)
       df = df.iloc[:, [0, 1]].dropna()
       df.columns = ['strain', 'stress']
       # Добавляем точку (0,0) если её нет
       if df['strain'].iloc[0] > 0:
           zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
           df = pd.concat([zero_point, df]).reset_index(drop=True)
       return df
   
   # Обработка данных для каждого режима
   for sheet in mode1_sheets:
       df = process_sheet(sheet)
       mode1_samples.append(df)
       
   for sheet in mode8_sheets:
       df = process_sheet(sheet)
       mode8_samples.append(df)
               
   return mode1_samples, mode8_samples

def average_curves(samples):
   if not samples:
       return pd.DataFrame()
   
   # Убедимся, что все наборы данных начинаются с нуля
   for df in samples:
       if df['strain'].iloc[0] != 0:
           zero_point = pd.DataFrame({'strain': [0], 'stress': [0]})
           df = pd.concat([zero_point, df]).reset_index(drop=True)
   
   max_strain = max(df['strain'].max() for df in samples)
   # Создаем больше точек в начале для лучшей интерполяции
   strain_points = np.concatenate(([0], np.linspace(0.001, 0.1, 100), np.linspace(0.1, max_strain, 900)))
   
   interpolated_stress = []
   for df in samples:
       interpolated = np.interp(strain_points, df['strain'], df['stress'])
       interpolated_stress.append(interpolated)
   
   avg_stress = np.mean(interpolated_stress, axis=0)
   std_stress = np.std(interpolated_stress, axis=0)
   
   return pd.DataFrame({
       'strain': strain_points,
       'stress': avg_stress,
       'stress_std': std_stress
   })

def plot_curves(mode1_avg, mode8_avg):
    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_theme(style="white")
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(plt.MultipleLocator(100))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(50))
    ax.xaxis.set_major_locator(plt.MultipleLocator(5))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.grid(True, which='major', linestyle='--', alpha=0.7)
    
    # Параметры для сглаживания
    elastic_limit = 1.5  # % strain
    transition_zone = 0.5  # размер переходной зоны
    window = 50
    
    for mode_avg in [mode1_avg, mode8_avg]:
        # Разделяем на зоны с разными весами сглаживания
        elastic_mask = mode_avg['strain'] <= (elastic_limit - transition_zone)
        transition_mask = (mode_avg['strain'] > (elastic_limit - transition_zone)) & (mode_avg['strain'] <= (elastic_limit + transition_zone))
        plastic_mask = mode_avg['strain'] > (elastic_limit + transition_zone)
        
        # Вычисляем сглаженные значения для всей кривой
        smoothed = mode_avg['stress'].rolling(window=window, min_periods=1, center=True).mean()
        
        # Применяем разные веса сглаживания для разных зон
        mode_avg['stress_smooth'] = mode_avg['stress'].copy()
        mode_avg.loc[elastic_mask, 'stress_smooth'] = mode_avg.loc[elastic_mask, 'stress']
        mode_avg.loc[plastic_mask, 'stress_smooth'] = smoothed[plastic_mask]
        
        # Для переходной зоны используем линейную интерполяцию
        transition_points = mode_avg[transition_mask].index
        for i in transition_points:
            strain = mode_avg.loc[i, 'strain']
            weight = (strain - (elastic_limit - transition_zone)) / (2 * transition_zone)
            mode_avg.loc[i, 'stress_smooth'] = (1 - weight) * mode_avg.loc[i, 'stress'] + weight * smoothed[i]
        
        # Сглаживание стандартного отклонения
        mode_avg['stress_std_smooth'] = mode_avg['stress_std'].rolling(window=window, min_periods=1, center=True).mean()
    
    # Построение графиков
    plt.plot(mode1_avg['strain'], mode1_avg['stress_smooth'], 
            label='Regime 1', color='blue', linewidth=2)
    plt.fill_between(mode1_avg['strain'],
                    mode1_avg['stress_smooth'] - mode1_avg['stress_std_smooth'],
                    mode1_avg['stress_smooth'] + mode1_avg['stress_std_smooth'],
                    color='blue', alpha=0.2)
    
    plt.plot(mode8_avg['strain'], mode8_avg['stress_smooth'], 
            label='Regime 8', color='red', linewidth=2)
    plt.fill_between(mode8_avg['strain'],
                    mode8_avg['stress_smooth'] - mode8_avg['stress_std_smooth'],
                    mode8_avg['stress_smooth'] + mode8_avg['stress_std_smooth'],
                    color='red', alpha=0.2)
    
    plt.xlabel('Strain, %', fontsize=16, fontname='Arial')
    plt.ylabel('Stress, MPa', fontsize=16, fontname='Arial')
    plt.title('Stress-strain curves for Ti15Ta SLM samples', fontsize=18, fontname='Arial', pad=20)
    plt.legend(fontsize=14, frameon=True)
    
    plt.xticks(fontsize=14, fontname='Arial')
    plt.yticks(fontsize=14, fontname='Arial')
    
    plt.tick_params(which='both', direction='in', width=1)
    plt.tick_params(which='major', length=7)
    plt.tick_params(which='minor', length=4)
    
    plt.xlim(0, max(mode1_avg['strain'].max(), mode8_avg['strain'].max()))
    plt.ylim(0, max(mode1_avg['stress'].max(), mode8_avg['stress'].max()) * 1.05)
    
    plt.tight_layout()
    
    return plt.gcf()  # перенес return в конец функцииplt.yticks(fontsize=14, fontname='Arial')
    
    plt.tick_params(which='both', direction='in', width=1)
    plt.tick_params(which='major', length=7)
    plt.tick_params(which='minor', length=4)
    
    plt.xlim(0, max(mode1_avg['strain'].max(), mode8_avg['strain'].max()))
    plt.ylim(0, max(mode1_avg['stress'].max(), mode8_avg['stress'].max()) * 1.05)
    
    plt.tight_layout()
    return plt.gcf()

if __name__ == "__main__":
   file_path = input("Enter the path to Excel file (.xlsx): ")
   
   if not os.path.exists(file_path):
       print(f"Error: File {file_path} not found")
       exit()
       
   mode1_samples, mode8_samples = load_and_process_data(file_path)
   mode1_avg = average_curves(mode1_samples)
   mode8_avg = average_curves(mode8_samples)

   fig = plot_curves(mode1_avg, mode8_avg)
   plt.savefig('stress_strain_curves.png', dpi=300, bbox_inches='tight')
   plt.show()