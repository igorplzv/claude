import matplotlib.pyplot as plt
import numpy as np

# Data from your study (Ti-13Nb-13Zr-5Cu, Table 2)
regimes = ['C1', 'C5', 'L2', 'L3', 'L4', 'L5']
E_yours = [96, 116, 88, 94, 91, 106]  # Elastic Modulus (GPa)
E_err_yours = [5, 3, 4, 10, 5, 4]      # Error in E (GPa)
UTS_yours = [721, 264, 871, 1001, 1450, 307]  # UTS (MPa)
UTS_err_yours = [155, 15, 105, 30, 24, 22]    # Error in UTS (MPa)

# Literature data
lit_alloys = ['Ti-6Al-4V (SLM)', 'Ti-13Nb-13Zr (SLM)', 'Ti-5Cu (SLM)', 'Ti-6Al-4V-5Cu (Cast)']
E_lit = [114, 79, 108, 115]            # Elastic Modulus (GPa)
E_err_lit = [5, 5, 5, 5]               # Error in E (GPa)
UTS_lit = [1000, 900, 850, 950]        # UTS (MPa)
UTS_err_lit = [50, 50, 30, 40]         # Error in UTS (MPa)

# Initialize the figure with larger size
plt.figure(figsize=(12, 9))

# Plot your data (Ti-13Nb-13Zr-5Cu)
plt.errorbar(E_yours, UTS_yours, yerr=UTS_err_yours, xerr=E_err_yours, fmt='o', 
             color='blue', label='Ti-13Nb-13Zr-5Cu (This Study)', capsize=6, 
             markersize=12, markerfacecolor='blue', linewidth=1.5)

# Plot literature data
plt.errorbar(E_lit[0], UTS_lit[0], yerr=UTS_err_lit[0], xerr=E_err_lit[0], fmt='s', 
             color='red', label='Ti-6Al-4V (SLM)', capsize=6, markersize=12, 
             markerfacecolor='red', linewidth=1.5)
plt.errorbar(E_lit[1], UTS_lit[1], yerr=UTS_err_lit[1], xerr=E_err_lit[1], fmt='^', 
             color='green', label='Ti-13Nb-13Zr (SLM)', capsize=6, markersize=12, 
             markerfacecolor='green', linewidth=1.5)
plt.errorbar(E_lit[2:], UTS_lit[2:], yerr=UTS_err_lit[2:], xerr=E_err_lit[2:], fmt='d', 
             color='purple', label='Ti-6Al-4V-xCu', capsize=6, markersize=12, 
             markerfacecolor='purple', linewidth=1.5)

# Add shaded regions
# Human bone modulus (10-30 GPa) - lower alpha, extend Y-range
plt.fill_betweenx([0, 1700], 10, 30, color='green', alpha=0.08, 
                  label='Human Bone Modulus (10–30 GPa)')
# Ti-6Al-4V typical range (110-120 GPa, 900-1100 MPa) - lower alpha
plt.fill_between([110, 120], 900, 1100, color='gray', alpha=0.08, 
                 label='Ti-6Al-4V Typical Range')

# Customize plot with larger fonts and improved aesthetics
plt.xlabel('Elastic Modulus (GPa)', fontsize=16)
plt.ylabel('Ultimate Tensile Strength (UTS, MPa)', fontsize=16)
plt.xlim(10, 130)
plt.ylim(0, 1700)  # Extended Y-axis for better visibility
plt.grid(True, linestyle='--', alpha=0.5)  # Reduced grid opacity
plt.legend(loc='upper left', fontsize=14, framealpha=0.8)  # Larger legend, semi-transparent background

# Add tick labels with larger font
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Add dashed lines for human bone modulus boundaries (optional for emphasis)
plt.axvline(x=10, color='green', linestyle='--', alpha=0.5, linewidth=0.5)
plt.axvline(x=30, color='green', linestyle='--', alpha=0.5, linewidth=0.5)

# Save the figure with high resolution
plt.savefig('UTS_vs_E_Comparison_Enhanced.png', dpi=600, bbox_inches='tight')
plt.show()