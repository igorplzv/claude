import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.ticker import AutoMinorLocator
from adjustText import adjust_text

def read_xrd_data(filename):
    """Read XRD data from .xy file"""
    angles = []
    intensities = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith("'"):
                try:
                    angle, intensity = map(float, line.strip().split())
                    angles.append(angle)
                    intensities.append(intensity)
                except ValueError:
                    continue
    return np.array(angles), np.array(intensities)

def normalize_data(intensities):
    """Normalize intensities to maximum value"""
    return intensities / np.max(intensities)

def smooth_data(intensities, window=15, polyorder=3):
    """Apply Savitzky-Golay filter for smoothing"""
    return savgol_filter(intensities, window, polyorder)

# Read and process data
angles_before, intensities_before = read_xrd_data('TiTa-7_exported non HT.xy')
angles_after, intensities_after = read_xrd_data('TiTa-7 HT.xy')

intensities_before_smooth = smooth_data(normalize_data(intensities_before))
intensities_after_smooth = smooth_data(normalize_data(intensities_after))

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300, 
                              sharex=True, gridspec_kw={'hspace': 0.12})
xlim = (30, 80)  # Ограничение до 80 градусов
ylim = (0, 1.2)

# Phase configuration (updated with 35° and 62° peaks)
phases = {
    'α-Ti': {
        'peaks': [35.0, 38.4, 40.2, 53.0, 70.6],  # Добавлен пик на 35°
        'color': '#1f77b4',
        'marker': 'v'
    },
    'β-Ti': {
        'peaks': [39.5, 56.8, 62.0, 71.3],  # Добавлен пик на 62°
        'color': '#ff7f0e',
        'marker': 's'
    },
    'Ta': {
        'peaks': [37.8, 43.2, 46.5], 
        'color': '#2ca02c',
        'marker': '^'
    }
}

def smart_annotations(ax, angles, intensities):
    texts = []
    arrows = []
    
    for phase, params in phases.items():
        for peak_angle in params['peaks']:
            if not (xlim[0] < peak_angle < xlim[1]):
                continue  # Пропускаем пики вне диапазона
            
            idx = np.abs(angles - peak_angle).argmin()
            y = intensities[idx]
            
            # Фиксированное смещение текста и стрелки
            text_offset = (10, 10)  # Смещение текста (x, y) в пунктах
            arrow_length = 15  # Длина стрелки в пунктах
            arrow_angle = 45  # Угол наклона стрелки (в градусах)
            
            # Проверка границ графика
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            
            # Если текст выходит за пределы графика, корректируем смещение
            if peak_angle + text_offset[0] / 100 * (x_max - x_min) > x_max:
                text_offset = (-10, text_offset[1])  # Смещаем влево
            if y + text_offset[1] / 100 * (y_max - y_min) > y_max:
                text_offset = (text_offset[0], -10)  # Смещаем вниз
            
            t = ax.annotate(
                phase,
                xy=(peak_angle, y),  # Точка, к которой ведет стрелка
                xytext=text_offset,  # Смещение текста
                textcoords='offset points',  # Смещение в пунктах
                fontsize=9,
                color=params['color'],
                ha='center',
                va='bottom',
                arrowprops=dict(
                    arrowstyle=f"->,head_width=0.4,head_length=0.8",  # Короткая стрелка
                    color=params['color'],
                    lw=1.0,
                    shrinkA=0,  # Стрелка начинается точно от текста
                    shrinkB=0,  # Стрелка заканчивается точно у пика
                    connectionstyle=f"angle,angleA=0,angleB={arrow_angle},rad=0"  # Фиксированный угол
                ),
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    fc="white",
                    ec=params['color'],
                    lw=0.8
                ),
                zorder=10
            )
            texts.append(t)
            
            # Вертикальная линия для пика
            ax.axvline(peak_angle, color=params['color'], 
                      lw=0.8, ls=':', alpha=0.6, zorder=5)
    
    # Автоматическое выравнивание подписей
    adjust_text(texts, ax=ax, 
               autoalign='y', 
               only_move={'points':'y', 'text':'y'},
               force_text=(0.5, 0.5),
               expand_text=(1.2, 1.5),
               ensure_inside_axes=True)  # Гарантирует, что текст останется внутри графика

# Plotting
for ax, data, title in zip([ax1, ax2], 
                          [(angles_before, intensities_before_smooth),
                           (angles_after, intensities_after_smooth)], 
                          ['Before Heat Treatment', 'After Heat Treatment']):
    ax.plot(data[0], data[1], color='#444444', linewidth=1.2, alpha=0.9)
    ax.set_title(title, fontsize=12, pad=8)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.yaxis.set_ticklabels([])
    smart_annotations(ax, data[0], data[1])

ax2.set_xlabel('2θ (degrees)', fontsize=12, labelpad=10)
fig.text(0.06, 0.5, 'Intensity (a.u.)', va='center', rotation='vertical', fontsize=12)

# Subplot labels
for label, ax in zip(['a)', 'b)'], [ax1, ax2]):
    ax.text(0.02, 0.95, label, transform=ax.transAxes, 
           fontsize=14, va='top', weight='bold')

plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.08)
plt.savefig('xrd_final_corrected.png', dpi=300, bbox_inches='tight')
plt.close()