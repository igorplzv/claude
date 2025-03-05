import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def load_xrd_data(filename):
    """Загрузка данных XRD из файла"""
    data = np.loadtxt(filename, skiprows=2)
    return data[:, 0], data[:, 1]

def annotate_peak(ax, x, y, label, offset_x=0, offset_y=5):
    """Аннотация пиков с ограничением по границам"""
    # Ограничение по оси X
    xlim = ax.get_xlim()
    if x + offset_x < xlim[0] or x + offset_x > xlim[1]:
        offset_x = 0  # Центрируем, если выходит за границы
    
    # Ограничение по оси Y
    ylim = ax.get_ylim()
    if y + offset_y > ylim[1]:
        offset_y = -offset_y  # Перемещаем вниз, если выходит за верхнюю границу
    
    ax.annotate(
        label,
        xy=(x, y),
        xytext=(x + offset_x, y + offset_y),
        fontsize=12,
        ha='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.95, pad=2),
        arrowprops=dict(arrowstyle='-', color='gray', alpha=0.6)
    )

def plot_xrd_patterns(regime1_file, regime8_file, output_file='xrd_final.png'):
    """Построение графиков с аннотациями над пиками"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 15), dpi=120)
    
    # Загрузка данных
    theta1, i1 = load_xrd_data(regime1_file)
    theta8, i8 = load_xrd_data(regime8_file)
    
    # Нормализация
    i1 = i1/np.max(i1)*100
    i8 = i8/np.max(i8)*100

    # Список пиков
    phases = {
        'β': {
            38.26: '(110)', 
            52.84: '(200)',
            70.50: '(211)',
            76.34: '(220)'
        },
        'α"': {
            34.92: '(110)',
            40.00: '(021)',
            62.50: '(220)',  # Пик ~62°
            63.80: '(022)'
        }
    }

    # Построение графиков
    for ax, theta, intensity, title in zip(
        [ax1, ax2], 
        [theta1, theta8], 
        [i1, i8], 
        ['(a) Regime 1 (h=100 μm, E=62.5 J/mm³)', '(b) Regime 8 (h=80 μm, E=78.1 J/mm³)']
    ):
        ax.plot(theta, intensity, 'k-', lw=1.5)
        ax.set_title(title, pad=16, fontsize=14, fontweight='semibold')
        ax.set_xlabel('2θ (degrees)', fontsize=12, labelpad=12)
        ax.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=12)
        
        # Аннотирование
        for phase in phases:
            for angle, hkl in phases[phase].items():
                idx = np.abs(theta - angle).argmin()
                if intensity[idx] > 3:
                    label = f'{phase}{hkl}'
                    offset_x = 0  # Центрируем по X
                    offset_y = 7  # Смещаем вверх
                    annotate_peak(ax, theta[idx], intensity[idx], label, offset_x, offset_y)

    # Настройка осей
    for ax in [ax1, ax2]:
        ax.set_xlim(30, 75)
        ax.set_ylim(0, 105)
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(20))
        ax.yaxis.set_minor_locator(MultipleLocator(5))
        ax.tick_params(axis='both', which='major', labelsize=11)
        
    plt.tight_layout(pad=4.5)
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_xrd_patterns("Ti15Ta-1.txt", "Ti15Ta-8.txt")