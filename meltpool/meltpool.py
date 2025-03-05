import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# Data for melt pool measurements including standard deviations
chess_data = {
    'energy': [37.5, 40.0, 50.0, 62.5, 66.7, 83.3, 30.0, 80.0],  # Energy density (J/mm³)
    'width': [92, 98, 95, 102, 100, 104, 88, 103],               # Melt pool width (μm)
    'std_dev': [3.2, 2.3, 2.7, 3.1, 3.0, 3.3, 3.8, 3.2],        # Standard deviation (μm)
    'regime': ['C2', 'C5', 'C1', 'C3', 'C4', 'C6', 'C7', 'C8'],
}

linear_data = {
    'energy': [40.0, 80.0, 62.5, 78.1, 50.0],  # Energy density (J/mm³)
    'width': [101, 110, 108, 115, 102],        # Melt pool width (μm)
    'std_dev': [2.5, 2.2, 2.7, 2.4, 2.6],      # Standard deviation (μm)
    'regime': ['L1', 'L2', 'L3', 'L4', 'L5'],
}

# Create figure with specified size (in inches)
plt.figure(figsize=(10, 8))

# Plot data points with error bars (without labels)
plt.errorbar(chess_data['energy'], chess_data['width'], 
            yerr=chess_data['std_dev'],
            c='#2563eb', marker='o', markersize=12, 
            capsize=6, capthick=1.5, elinewidth=1.5,
            ls='none', label='_nolegend_')

plt.errorbar(linear_data['energy'], linear_data['width'], 
            yerr=linear_data['std_dev'],
            c='#16a34a', marker='s', markersize=12,
            capsize=6, capthick=1.5, elinewidth=1.5,
            ls='none', label='_nolegend_')

# Add separate scatter plots for legend
plt.scatter([], [], c='#2563eb', marker='o', s=144, label='Chess pattern')  # markersize^2 = s
plt.scatter([], [], c='#16a34a', marker='s', s=144, label='Linear strategy')

# Add regime labels
for i, regime in enumerate(chess_data['regime']):
    plt.annotate(regime, 
                (chess_data['energy'][i], chess_data['width'][i]),
                xytext=(7, 7), textcoords='offset points',
                fontsize=14, fontweight='bold')

for i, regime in enumerate(linear_data['regime']):
    plt.annotate(regime, 
                (linear_data['energy'][i], linear_data['width'][i]),
                xytext=(7, 7), textcoords='offset points',
                fontsize=14, fontweight='bold')

# Configure axes
plt.xlabel('Energy density (J/mm³)', fontsize=18, fontweight='bold')
plt.ylabel('Melt pool width (μm)', fontsize=18, fontweight='bold')

# Set axis limits with some padding
plt.xlim(25, 85)
plt.ylim(80, 125)

# Add grid
plt.grid(True, linestyle='--', alpha=0.3)

# Add minor ticks
ax = plt.gca()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# Increase tick label size
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# Add legend with frame
plt.legend(loc='upper right', fontsize=16, frameon=True, framealpha=1, edgecolor='black')

# Adjust layout to prevent label clipping
plt.tight_layout()

# Save figure
plt.savefig('melt_pool_width.png', dpi=300, bbox_inches='tight')
plt.savefig('melt_pool_width.eps', format='eps', bbox_inches='tight')