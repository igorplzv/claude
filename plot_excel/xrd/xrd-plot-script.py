import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def load_xrd_data(filename):
    """
    Загружает данные XRD из текстового файла
    """
    data = np.loadtxt(filename, skiprows=2)
    return data[:, 0], data[:, 1]  # 2theta, intensity

def annotate_peak(ax, x, y, label, offset_x=0, offset_y=5):
    """
    Добавляет аннотацию пика с линией
    """
    ax.annotate(
        label,
        xy=(x, y),
        xytext=(x + offset_x, y + offset_y),
        fontsize=10,
        ha='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1),
        arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5)
    )

def plot_xrd_patterns(regime1_file, regime8_file, output_file='xrd_patterns.png'):
    """
    Строит XRD-графики для двух режимов
    """
    # Создаем фигуру с двумя графиками
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), height_ratios=[1, 1])
    fig.suptitle('XRD Patterns of Ti-15Ta Alloy', fontsize=16, fontweight='bold', y=0.95)

    # Загружаем данные
    theta1, intensity1 = load_xrd_data(regime1_file)
    theta8, intensity8 = load_xrd_data(regime8_file)

    # Нормализуем интенсивности
    intensity1 = intensity1 / np.max(intensity1) * 100
    intensity8 = intensity8 / np.max(intensity8) * 100

    # График для Режима 1
    ax1.plot(theta1, intensity1, 'k-', linewidth=1)
    ax1.set_title('(a) Regime 1 (h=100 μm, E=62.5 J/mm³)', pad=10)

    # График для Режима 8
    ax2.plot(theta8, intensity8, 'k-', linewidth=1)
    ax2.set_title('(b) Regime 8 (h=80 μm, E=78.1 J/mm³)', pad=10)

    # Отмечаем важные пики для Режима 1
    beta_peaks_1 = {
        38.26: 'β(110)',
        52.84: 'β(200)',
        70.50: 'β(211)'
    }
    
    # Отмечаем важные пики для Режима 8
    peaks_8 = {
        34.92: 'α"(110)',
        38.26: 'β(110)',
        40.00: 'α"(021)',
        52.84: 'β(200)',
        70.50: 'β(211)'
    }

    # Добавляем аннотации пиков
    for theta, label in beta_peaks_1.items():
        idx = np.abs(theta1 - theta).argmin()
        annotate_peak(ax1, theta1[idx], intensity1[idx], label)

    for theta, label in peaks_8.items():
        idx = np.abs(theta8 - theta).argmin()
        annotate_peak(ax2, theta8[idx], intensity8[idx], label)

    # Настраиваем оси и подписи
    for ax in [ax1, ax2]:
        ax.set_xlabel('2θ (degrees)', fontsize=12)
        ax.set_ylabel('Intensity (a.u.)', fontsize=12)
        ax.set_xlim(30, 90)
        ax.set_ylim(0, 105)
        
        # Настраиваем сетку и деления
        ax.grid(True, which='major', linestyle='--', alpha=0.3)
        ax.grid(True, which='minor', linestyle=':', alpha=0.1)
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(20))
        ax.yaxis.set_minor_locator(MultipleLocator(5))

    # Настраиваем общий вид
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)

    # Сохраняем график
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Файлы с данными
    regime1_file = "Ti15Ta-1.txt"
    regime8_file = "Ti15Ta-8.txt"
    
    plot_xrd_patterns(regime1_file, regime8_file)
    print("XRD patterns have been plotted and saved.")