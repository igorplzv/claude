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
# Note: despite the filenames, 'non HT' is after heat treatment and 'HT' is before
angles_after_ht, intensities_after_ht = read_xrd_data('TiTa-7_exported non HT.xy')  # после T/O
angles_before_ht, intensities_before_ht = read_xrd_data('TiTa-7 HT.xy')  # до T/O

intensities_after_ht_norm = normalize_data(intensities_after_ht)
intensities_before_ht_norm = normalize_data(intensities_before_ht)

intensities_after_ht_smooth = smooth_data(intensities_after_ht_norm)
intensities_before_ht_smooth = smooth_data(intensities_before_ht_norm)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300, 
                              sharex=True, gridspec_kw={'hspace': 0.1})

# Common parameters
xlim = (30, 90)
ylim = (0, 1.2)
plot_params = {
    'linewidth': 1.2,
    'alpha': 0.9,
    'zorder': 1
}

# Phase markers for before heat treatment (includes Ta)
phases_before = {
    'α-Ti': {
        'peaks': [35.2, 38.5, 40.3, 53.1, 63.0, 70.7, 76.3, 78.0, 82.4],
        'color': '#1f77b4',
        'offsets': [(0, 20), (-10, 15), (10, 10), (-15, 10), (10, 15), (-10, 10), (10, 15), (-10, 10), (10, 15)]
    },
    'β-Ti': {
        'peaks': [39.3, 56.3, 69.8, 83.6],
        'color': '#2ca02c',
        'offsets': [(15, 20), (-10, 20), (15, 15), (-10, 15)]
    },
    'Ta': {
        'peaks': [38.0, 43.5, 46.5, 55.8, 69.0, 82.0],
        'color': '#9467bd',
        'offsets': [(-15, -15), (10, -15), (-10, -15), (10, -15), (-10, -15), (10, -15)]
    }
}

# Phase markers for after heat treatment (Ta dissolved)
phases_after = {
    'α-Ti': {
        'peaks': [35.2, 38.5, 40.3, 53.1, 63.0, 70.7, 76.3, 78.0, 82.4],
        'color': '#1f77b4',
        'offsets': [(0, 20), (-10, 15), (10, 10), (-15, 10), (10, 15), (-10, 10), (10, 15), (-10, 10), (10, 15)]
    },
    'β-Ti': {
        'peaks': [39.3, 56.3, 69.8, 83.6],
        'color': '#2ca02c',
        'offsets': [(15, 20), (-10, 20), (15, 15), (-10, 15)]
    }
}

def add_phase_annotations(ax, angles, intensities, phases_dict):
    for phase, params in phases_dict.items():
        for peak_angle, offset in zip(params['peaks'], params['offsets']):
            # Find actual peak within a window around theoretical position
            window = 1.0  # ±1 градус вокруг теоретического положения
            mask = (angles >= peak_angle - window) & (angles <= peak_angle + window)
            if any(mask):
                window_intensities = intensities[mask]
                window_angles = angles[mask]
                max_idx = np.argmax(window_intensities)
                actual_angle = window_angles[max_idx]
                peak_intensity = window_intensities[max_idx] + 0.05
            else:
                actual_angle = peak_angle
                idx = np.abs(angles - peak_angle).argmin()
                peak_intensity = intensities[idx] + 0.05
            
            ax.annotate(
                phase,
                xy=(actual_angle, peak_intensity),
                xytext=offset,
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
            ax.axvline(actual_angle, color=params['color'], 
                      lw=0.8, ls=':', alpha=0.6, zorder=2)

# Plot before HT (using 'HT' file)
ax1.plot(angles_before_ht, intensities_before_ht_smooth, 'b-', label='Before HT', **plot_params)
ax1.set_title('Before Heat Treatment', fontsize=12, pad=10)
ax1.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=10)
ax1.set_ylim(ylim)
add_phase_annotations(ax1, angles_before_ht, intensities_before_ht_smooth, phases_before)  # включая Ta

# Plot after HT (using 'non HT' file)
ax2.plot(angles_after_ht, intensities_after_ht_smooth, 'r-', label='After HT', **plot_params)
ax2.set_title('After Heat Treatment', fontsize=12, pad=10)
ax2.set_xlabel('2θ (degrees)', fontsize=12, labelpad=10)
ax2.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=10)
ax2.set_ylim(ylim)
add_phase_annotations(ax2, angles_after_ht, intensities_after_ht_smooth, phases_after)  # без Ta

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