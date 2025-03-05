import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def load_xrd_data(filename):
    """Load XRD data from file"""
    data = np.loadtxt(filename, skiprows=1)
    return data[:, 0], data[:, 1]

def annotate_peak(ax, x, y, label, offset_y=15, color='k', side='center'):
    """Create draggable peak annotation"""
    ha = {'left': 'right', 'right': 'left', 'center': 'center'}[side]
    x_offset = {'left': -1, 'right': 1, 'center': 0}[side] * 2
    
    ann = ax.annotate(
        label,
        xy=(x, y),
        xytext=(x + x_offset, y + offset_y),
        fontsize=15,
        ha=ha,
        va='bottom',
        color=color,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.95, pad=1),
        arrowprops=dict(arrowstyle='-', color=color, alpha=0.7, linewidth=1.2)
    )
    ann.draggable()
    return ann

def plot_xrd_patterns(sample1_file, sample8_file):
    """Create interactive XRD pattern plot with draggable labels"""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
    
    # Load data
    theta1, i1 = load_xrd_data(sample1_file)
    theta8, i8 = load_xrd_data(sample8_file)
    
    # Normalize and add vertical offset
    i1 = i1/np.max(i1)*100
    i8 = i8/np.max(i8)*100 + 120

    # Define peaks with their positions and annotation parameters
    peaks = [
        {'pos': 35.4, 'label': 'α(100)', 'offset': 25, 'side': 'center'},
        {'pos': 38.4, 'label': 'α(002)', 'offset': 35, 'side': 'left'},
        {'pos': 39.0, 'label': 'β(110)', 'offset': 45, 'side': 'right'},
        {'pos': 40.4, 'label': 'α(101)', 'offset': 25, 'side': 'center'},
        {'pos': 53.2, 'label': 'α(102)', 'offset': 25, 'side': 'center'},
        {'pos': 55.6, 'label': 'β(200)', 'offset': 35, 'side': 'center'},
        {'pos': 63.2, 'label': 'α(110)', 'offset': 25, 'side': 'center'},
        {'pos': 70.2, 'label': 'β(211)', 'offset': 25, 'side': 'center'}
    ]

    # Plot patterns
    ax.plot(theta1, i1, 'b-', lw=1.2, label='Sample 1')
    ax.plot(theta8, i8, 'r-', lw=1.2, label='Sample 8')

    # Store annotations for both patterns
    annotations = []
    
    # Annotate peaks for both patterns
    for theta, intensity, color, base_y in [(theta1, i1, 'blue', 0), (theta8, i8, 'red', 120)]:
        for peak in peaks:
            # Find nearest point to peak position
            idx = np.abs(theta - peak['pos']).argmin()
            # Check if there's a significant peak
            if intensity[idx] - base_y > 3:
                # Find local maximum in ±0.5° window
                window = 20  # Approximate points in 0.5° window
                start = max(0, idx - window)
                end = min(len(intensity), idx + window)
                local_max_idx = start + np.argmax(intensity[start:end])
                
                # Create draggable annotation
                ann = annotate_peak(ax, theta[local_max_idx], intensity[local_max_idx],
                                  peak['label'], peak['offset'], color, peak['side'])
                annotations.append(ann)

    # Configure axes
    ax.set_xlim(30, 75)
    ax.set_ylim(-5, 245)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(40))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    
    # Labels and title
    ax.set_xlabel('2θ (degrees)', fontsize=17, labelpad=10)
    ax.set_ylabel('Intensity (a.u.)', fontsize=17, labelpad=10)
    ax.set_title('XRD Patterns of Ti-15Ta Samples after Heat Treatment (950°C)', 
                pad=25, fontsize=16)
    
    # Add legend with increased font size
    ax.legend(loc='upper right', fontsize=17, frameon=True, 
             edgecolor='none', fancybox=True)
    
    # Remove right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Adjust tick parameters
    ax.tick_params(axis='both', which='major', labelsize=15)
    
    plt.tight_layout()
    
    # Add instruction text
    plt.figtext(0.02, 0.02, "Click and drag annotations to move them\nClose window to save", 
                fontsize=10, color='gray')
    
    # Show the plot and wait for user to close it
    plt.show()
    
    # After window is closed, save the final version
    plt.savefig('xrd_heat_treated.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_xrd_patterns("Ti15Ta_1.xy", "Ti15Ta_8.xy")