import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from matplotlib.ticker import AutoMinorLocator

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

intensities_before_norm = normalize_data(intensities_before)
intensities_after_norm = normalize_data(intensities_after)

intensities_before_smooth = smooth_data(intensities_before_norm)
intensities_after_smooth = smooth_data(intensities_after_norm)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300, 
                              sharex=True, gridspec_kw={'hspace': 0.1})

# Common parameters
xlim = (30, 80)
ylim = (0, 1.2)
plot_params = {
    'linewidth': 1.2,
    'alpha': 0.9,
    'zorder': 1
}

# Phase markers parameters
phases = {
    'α-Ti': {'peaks': [35.0, 38.4, 40.2, 53.0, 62.0, 70.6], 'color': '#1f77b4', 'offset': (0, 5)},
    'β-Ti': {'peaks': [39.5, 43.0, 56.8, 71.3], 'color': '#2ca02c', 'offset': (0, 5)},
    'Ta': {'peaks': [37.8, 43.2, 46.5], 'color': '#9467bd', 'offset': (0, -15)}
}

# Function to add phase annotations
def add_phase_annotations(ax, angles, intensities, y_offset=0):
    for phase, params in phases.items():
        for peak_angle in params['peaks']:
            # Find nearest data point
            idx = np.abs(angles - peak_angle).argmin()
            peak_intensity = intensities[idx] + 0.05
            
            # Adjust y_offset for peaks in the range 37-40 degrees
            if 37 <= peak_angle <= 40:
                y_offset_adjusted = y_offset + 10  # Increase y_offset for this range
            else:
                y_offset_adjusted = y_offset
            
            ax.annotate(
                phase,
                xy=(peak_angle, peak_intensity),
                xytext=(params['offset'][0], params['offset'][1] + y_offset_adjusted),
                textcoords='offset points',
                fontsize=9,
                color=params['color'],
                arrowprops=dict(
                    arrowstyle="->",
                    color=params['color'],
                    lw=0.8,
                    connectionstyle="arc3,rad=-0.2"
                ),
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    fc="white",
                    ec=params['color'],
                    lw=0.5
                ),
                zorder=3
            )
            ax.axvline(peak_angle, color=params['color'], 
                      lw=0.8, ls=':', alpha=0.6, zorder=2)

# Plot before HT
ax1.plot(angles_before, intensities_before_smooth, 'b-', label='Before HT', **plot_params)
ax1.set_title('Before Heat Treatment', fontsize=12, pad=10)
ax1.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=10)
ax1.set_ylim(ylim)
add_phase_annotations(ax1, angles_before, intensities_before_smooth)

# Plot after HT
ax2.plot(angles_after, intensities_after_smooth, 'r-', label='After HT', **plot_params)
ax2.set_title('After Heat Treatment', fontsize=12, pad=10)
ax2.set_xlabel('2θ (degrees)', fontsize=12, labelpad=10)
ax2.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=10)
ax2.set_ylim(ylim)
add_phase_annotations(ax2, angles_after, intensities_after_smooth)

# Configure axes
for ax in [ax1, ax2]:
    ax.set_xlim(xlim)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='major', direction='in', length=6, width=1.2)
    ax.tick_params(which='minor', direction='in', length=3, width=1.0)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.yaxis.set_ticklabels([])

# Add subplot labels
ax1.text(0.02, 0.95, 'a)', transform=ax1.transAxes, fontsize=14, va='top')
ax2.text(0.02, 0.95, 'b)', transform=ax2.transAxes, fontsize=14, va='top')

plt.tight_layout()
plt.savefig('xrd_phase_analysis.png', dpi=300, bbox_inches='tight')
plt.close()