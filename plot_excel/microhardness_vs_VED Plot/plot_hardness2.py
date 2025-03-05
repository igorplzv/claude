import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator

# Read data from Excel file
df = pd.read_excel('harndess_Ti13Nb13Zr5Cu.xlsx', skiprows=2)

# Define process parameters for each regime
regimes = {
    'C1': {'energy': 50.0, 'strategy': 'Chess'},
    'C2': {'energy': 37.5, 'strategy': 'Chess'},
    'C3': {'energy': 62.5, 'strategy': 'Chess'},
    'C4': {'energy': 66.7, 'strategy': 'Chess'},
    'C5': {'energy': 40.0, 'strategy': 'Chess'},
    'C6': {'energy': 83.3, 'strategy': 'Chess'},
    'C7': {'energy': 30.0, 'strategy': 'Chess'},
    'C8': {'energy': 80.0, 'strategy': 'Chess'},
    'L1': {'energy': 40.0, 'strategy': 'Linear'},
    'L2': {'energy': 80.0, 'strategy': 'Linear'},
    'L3': {'energy': 62.5, 'strategy': 'Linear'},
    'L4': {'energy': 78.1, 'strategy': 'Linear'},
    'L5': {'energy': 50.0, 'strategy': 'Linear'}
}

# Process data using mean values and deviations from the file
processed_data = {}

# Get unique regimes and their statistics
unique_regimes = df.dropna(subset=['Режим', 'Среднее значение', 'Отклонение']).drop_duplicates(subset=['Режим'])

for _, row in unique_regimes.iterrows():
    regime = row['Режим']
    if regime in regimes:
        mean_hardness = row['Среднее значение']
        std_hardness = row['Отклонение']
        strategy = regimes[regime]['strategy']
        energy = regimes[regime]['energy']
        
        if strategy not in processed_data:
            processed_data[strategy] = {'energies': [], 'means': [], 'stds': []}
            
        processed_data[strategy]['energies'].append(energy)
        processed_data[strategy]['means'].append(mean_hardness)
        processed_data[strategy]['stds'].append(std_hardness)

# Create figure
plt.figure(figsize=(8, 6), dpi=300)

# Set style parameters
plt.style.use('seaborn-v0_8-whitegrid')
markers = {'Chess': 'o', 'Linear': 's'}
colors = {'Chess': '#2E86C1', 'Linear': '#E74C3C'}

# Plot data for each strategy
for strategy, data in processed_data.items():
    # Plot error bars without label
    plt.errorbar(data['energies'],
                data['means'],
                yerr=data['stds'],
                fmt='none',  # No markers
                color=colors[strategy],
                capsize=4,
                capthick=1.5,
                elinewidth=1.5,
                zorder=2)
    
    # Plot markers with label
    plt.scatter(data['energies'],
               data['means'],
               marker=markers[strategy],
               s=100,  # Marker size
               color=colors[strategy],
               label=f'{strategy} pattern',
               zorder=3)

# Customize plot appearance
plt.xlabel('Energy density (J/mm³)', fontsize=12, fontweight='bold')
plt.ylabel('Microhardness (HV$_{0.5}$)', fontsize=12, fontweight='bold')

# Set axis limits and ticks
plt.xlim(25, 90)
plt.ylim(250, 500)
ax = plt.gca()
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# Customize grid
plt.grid(True, which='major', linestyle='-', alpha=0.3, zorder=1)
plt.grid(True, which='minor', linestyle=':', alpha=0.1, zorder=1)

# Add legend
plt.legend(frameon=True, fontsize=10, loc='upper right')

# Adjust layout
plt.tight_layout()

# Print processed data for verification
print("\nProcessed data:")
for strategy, data in processed_data.items():
    print(f"\n{strategy} pattern:")
    for i in range(len(data['energies'])):
        print(f"Energy: {data['energies'][i]}, "
              f"Mean hardness: {data['means'][i]:.1f} ± "
              f"{data['stds'][i]:.1f}")

# Save figure
plt.savefig('microhardness_plot.png', dpi=300, bbox_inches='tight')
plt.savefig('microhardness_plot.svg', format='svg', bbox_inches='tight')
plt.close()