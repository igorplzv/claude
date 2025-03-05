import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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

# Read data for all three samples
angles_9, intensities_9 = read_xrd_data('TiNbZrCu_9.txt')    # L1
angles_11, intensities_11 = read_xrd_data('TiNbZrCu_11.txt') # L3
angles_12, intensities_12 = read_xrd_data('TiNbZrCu_12.txt') # L4

# Create the figure with larger size
plt.figure(figsize=(14, 8), dpi=300)

# Увеличиваем отступы между графиками
offset1 = 25000  # Increased offset
offset2 = 50000  # Increased offset

# Plot with different colors
plt.plot(angles_9, intensities_9, '-', color='#1f77b4', linewidth=1.2, label='L1 (40.0 J/mm³)')
plt.plot(angles_11, intensities_11 + offset1, '-', color='#2ca02c', linewidth=1.2, label='L3 (62.5 J/mm³)')
plt.plot(angles_12, intensities_12 + offset2, '-', color='#ff7f0e', linewidth=1.2, label='L4 (78.1 J/mm³)')

# Set plot limits and labels
plt.xlim(30, 100)
plt.ylim(-2000, max(intensities_12) + offset2 + 15000)
plt.xlabel('2θ (degrees)', fontsize=14, fontweight='bold')
plt.ylabel('Intensity (a.u.)', fontsize=14, fontweight='bold')

# Add grid
plt.grid(True, linestyle='--', alpha=0.3)

# Remove y-axis numbers but keep the ticks
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.NullFormatter())

# Defining all peaks with their phases and indices
peaks = {
    38.5: ('β-Ti', '(110)'),
    55.6: ('β-Ti', '(200)'),
    69.8: ('β-Ti', '(211)'),
    78.5: ('β-Ti', '(220)'),
    82.5: ('β-Ti', '(310)'),
    95.6: ('β-Ti', '(321)')
}

# Function to find y-value at specific x-value
def find_y_at_x(x_target, x_data, y_data):
    idx = np.abs(x_data - x_target).argmin()
    return y_data[idx]

# Add vertical lines and annotations for each peak
for angle, (phase, index) in peaks.items():
    # Add vertical dashed line
    plt.axvline(x=angle, color='gray', linestyle=':', alpha=0.3)
    
    # Find peak heights for each pattern
    y1 = find_y_at_x(angle, angles_9, intensities_9)
    y2 = find_y_at_x(angle, angles_11, intensities_11) + offset1
    y3 = find_y_at_x(angle, angles_12, intensities_12) + offset2
    
    # Use maximum height for annotation
    y_max = max(y1, y2, y3)
    
    # Calculate text position to avoid overlap
    text_offset = 7000  # Increased offset for text
    if angle == 38.5:  # Special case for the highest peak
        text_y = y_max + text_offset * 2
        ha = 'right'
        x_shift = -1
    elif angle == 82.5:  # Special case for overlapping peaks
        text_y = y_max + text_offset * 1.5
        ha = 'right'
        x_shift = -1
    else:
        text_y = y_max + text_offset
        ha = 'center'
        x_shift = 0
    
    plt.annotate(f'{phase} {index}', 
                xy=(angle, y_max), 
                xytext=(angle + x_shift, text_y),
                ha=ha, va='bottom', 
                fontsize=12,
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.2, ls='-'))

# Customize ticks
plt.tick_params(axis='both', which='major', labelsize=12)
ax.xaxis.set_minor_locator(MultipleLocator(2))

# Add legend with larger font
plt.legend(frameon=True, loc='upper right', fontsize=12, 
          bbox_to_anchor=(0.98, 0.98))

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Make remaining spines thicker
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

# Adjust layout
plt.tight_layout()

# Save plot as PNG
plt.savefig('xrd_patterns.png', dpi=300, bbox_inches='tight')
plt.close()