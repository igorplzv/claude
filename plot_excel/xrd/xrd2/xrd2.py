import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import ConnectionPatch

def read_xrd_data(filename):
    angles = []
    intensities = []
    with open(filename, 'r') as f:
        next(f)
        next(f)
        for line in f:
            if line.strip():
                angle, intensity = line.strip().split('\t')
                angles.append(float(angle))
                intensities.append(float(intensity))
    return np.array(angles), np.array(intensities)

angles_9, intensities_9 = read_xrd_data('TiNbZrCu_9.txt')
angles_11, intensities_11 = read_xrd_data('TiNbZrCu_11.txt')
angles_12, intensities_12 = read_xrd_data('TiNbZrCu_12.txt')

plt.figure(figsize=(14, 8), dpi=300)

offset1 = 35000
offset2 = 70000

plt.plot(angles_9, intensities_9, '-', color='#1f77b4', linewidth=1.2, label='L1 (40.0 J/mm³)')
plt.plot(angles_11, intensities_11 + offset1, '-', color='#2ca02c', linewidth=1.2, label='L3 (62.5 J/mm³)')
plt.plot(angles_12, intensities_12 + offset2, '-', color='#ff7f0e', linewidth=1.2, label='L4 (78.1 J/mm³)')

plt.xlim(30, 100)
plt.ylim(-2000, max(intensities_12) + offset2 + 15000)
plt.xlabel('2θ (degrees)', fontsize=21, fontweight='bold')
plt.ylabel('Intensity (a.u.)', fontsize=21, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.3)

ax = plt.gca()
ax.yaxis.set_major_formatter(plt.NullFormatter())

# Определение пиков и их подписей с настройками позиционирования
peaks = {
    38.7: ('β-Ti(ss)', '(110)', 0, 1.4),  # (угол, фаза, индекс, x_offset, y_scale)
    55.8: ('β-Ti(ss)', '(200)', 0, 1.3),
    70.0: ('β-Ti(ss)', '(211)', -2.5, 1.6),  # Смещение влево
    70.4: ('α″-Ti', '(201)', 2.5, 1.3),     # Смещение вправо
    78.6: ('β-Ti(ss)', '(220)', -2, 3.0),   # Смещение влево
    82.8: ('β-Ti(ss)', '(310)', 2, 1.2),    # Смещение вправо
    95.8: ('β-Ti(ss)', '(321)', 0, 1.2)
}

def find_y_at_x(x_target, x_data, y_data):
    idx = np.abs(x_data - x_target).argmin()
    return y_data[idx]

# Добавляем вертикальные линии и подписи
for angle, (phase, index, x_offset, y_scale) in peaks.items():
    # Добавляем вертикальную линию
    plt.axvline(x=angle, color='#404040', linestyle=':', alpha=0.3)
    
    # Находим максимальную высоту для подписи
    y1 = find_y_at_x(angle, angles_9, intensities_9)
    y2 = find_y_at_x(angle, angles_11, intensities_11) + offset1
    y3 = find_y_at_x(angle, angles_12, intensities_12) + offset2
    y_max = max(y1, y2, y3)
    
    # Настраиваем положение текста
    text_offset = 8000
    text_y = y_max + text_offset * y_scale
    text_x = angle + x_offset
    
    # Добавляем подпись с белым фоном
    plt.text(text_x, text_y, f'{phase} {index}',
            ha='center', va='bottom',
            fontsize=18,
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    
    # Добавляем тонкую линию от подписи к пику
    if abs(x_offset) > 0:  # Только для смещенных подписей
        plt.plot([angle, text_x], [y_max, text_y], 
                color='#404040', linewidth=0.8, linestyle='-', alpha=0.5)

plt.tick_params(axis='both', which='major', labelsize=18)
ax.xaxis.set_minor_locator(MultipleLocator(2))

plt.legend(frameon=True, loc='upper right', fontsize=21,
          bbox_to_anchor=(0.98, 0.98))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

plt.tight_layout()
plt.savefig('xrd_patterns.png', dpi=300, bbox_inches='tight')
plt.close()