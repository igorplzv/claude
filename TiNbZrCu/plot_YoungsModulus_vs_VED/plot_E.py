import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.ticker as ticker

# Data for chess pattern strategy
chess_energy = np.array([50.0, 50.0, 40.0])  # Energy density values
chess_modulus = np.array([91.41, 100.96, 116.04])  # Elastic modulus values

# Data for linear pattern strategy
linear_energy = np.array([80.0, 80.0, 80.0, 62.5, 62.5, 78.1, 78.1, 78.1, 50.0])
linear_modulus = np.array([83.95, 91.20, 87.25, 104.24, 83.76, 89.32, 97.89, 86.48, 106.50])

# Create the figure with specified size and DPI for publication quality
plt.figure(figsize=(9, 7), dpi=300)

# Customize the plot style
plt.rcParams['axes.linewidth'] = 0.8  # Тоньше рамка
plt.grid(True, linestyle='--', alpha=0.4, which='major')  # Более светлая основная сетка
plt.grid(True, linestyle=':', alpha=0.2, which='minor')  # Добавляем минорную сетку

# Plot individual points with slightly smaller markers
plt.scatter(chess_energy, chess_modulus, color='#2563eb', s=80, label='Chess pattern')
plt.scatter(linear_energy, linear_modulus, color='#16a34a', s=80, marker='s', label='Linear pattern')

# Customize axes
plt.xlabel('Energy Density (J/mm³)', fontsize=14, fontweight='bold')
plt.ylabel('Elastic Modulus (GPa)', fontsize=14, fontweight='bold')

# Set axis ranges and ticks
plt.xlim(30, 90)
plt.ylim(80, 120)

# Add minor ticks
ax = plt.gca()
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

# Customize tick parameters
plt.tick_params(axis='both', which='major', labelsize=12, length=6)
plt.tick_params(axis='both', which='minor', length=3)

# Reference area for Ti-6Al-4V with more transparency
ti64_region = plt.axhspan(110, 120, color='gray', alpha=0.15)
plt.annotate('Ti-6Al-4V range', 
             xy=(35, 115),
             xytext=(35, 105),
             fontsize=12,
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8),
             arrowprops=dict(arrowstyle='->', linewidth=0.8))

# Optimal processing window with lighter color
opt_region = plt.axvspan(60, 80, color='green', alpha=0.08)
plt.annotate('Optimal processing\nwindow',
             xy=(70, 95),
             xytext=(43, 95),
             fontsize=12,
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.8),
             arrowprops=dict(arrowstyle='->', linewidth=0.8))

# Add legend with border
legend = plt.legend(fontsize=12, frameon=True, loc='upper right',
                   edgecolor='black', framealpha=1.0)
legend.get_frame().set_linewidth(0.8)

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig('elastic_modulus_vs_energy_improved.png', dpi=300, bbox_inches='tight')
plt.savefig('elastic_modulus_vs_energy_improved.pdf', bbox_inches='tight')

# Show the plot
plt.show()