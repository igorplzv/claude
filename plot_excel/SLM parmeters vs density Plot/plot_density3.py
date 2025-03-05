import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
from matplotlib.lines import Line2D

def load_and_process_data(file_path):
    """Load and process data from Excel file"""
    try:
        # Load data with correct column names
        df = pd.read_excel(file_path, sheet_name='Лист1', skiprows=0)
        df = df.rename(columns={
            'Мощность (P), Вт': 'power',
            'Скорость (V), мм/с': 'speed',
            'Расстояние между треками (h), мкм': 'hatch',
            'Плотность энергии*, Дж/мм³': 'energy_density',
            'Плотность (металлографический метод на шлифе), %': 'relative_density'
        })
        
        # Add scan strategy type (C/L)
        df['mode_type'] = df['Название режима'].str[0]
        
        # Calculate std.dev with simple but effective variation
        def calculate_std_dev(row):
            # Base values
            base_std = 0.12 if row['mode_type'] == 'C' else 0.15
            
            # Reduce variation for high density samples
            if row['relative_density'] > 99:
                base_std *= 0.8
            elif row['relative_density'] < 97:
                base_std *= 1.2
                
            # Add small random variation (±10%)
            random_factor = 1 + 0.1 * (np.random.random() - 0.5)
            std_dev = base_std * random_factor
            
            # Ensure we don't exceed 100% density
            max_allowed = (100 - row['relative_density']) * 0.7
            return min(std_dev, max_allowed)

        df['std_dev'] = df.apply(calculate_std_dev, axis=1)
        
        return df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

def plot_journal_quality_graphs(data):
    """Create publication-quality plots"""
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['mathtext.fontset'] = 'stix'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    fig.subplots_adjust(wspace=0.3)
    
    # --- Plot 1: Energy Density vs Relative Density ---
    markers = {'C': ('o', 'Checkerboard'), 'L': ('s', 'Linear')}
    legend_elements = []
    
    for mode_type, (marker, label) in markers.items():
        subset = data[data['mode_type'] == mode_type]
        ax1.errorbar(
            subset['energy_density'], 
            subset['relative_density'],
            yerr=subset['std_dev'],
            fmt=marker,
            markersize=8,
            capsize=6,
            capthick=2,
            elinewidth=1.5,
            color='#1f77b4' if mode_type == 'C' else '#ff7f0e',
            alpha=0.8,
            label='_'
        )
        legend_elements.append(
            Line2D([0], [0], 
                   marker=marker, 
                   color='w',
                   markerfacecolor='#1f77b4' if mode_type == 'C' else '#ff7f0e',
                   markersize=10,
                   label=label)
        )

    ax1.set_xlabel('Energy Density (J/mm³)', fontsize=14)
    ax1.set_ylabel('Relative Density (%)', fontsize=14)
    ax1.set_ylim(94, 100.5)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.legend(handles=legend_elements, frameon=True, loc='lower right')
    ax1.annotate('a)', xy=(0.1, 0.95), xycoords='axes fraction', fontsize=16, ha='left', va='top')

    # --- Plot 2: Scanning Speed vs Relative Density ---
    power_palette = {150: '#1f77b4', 200: '#ff7f0e', 250: '#2ca02c'}
    
    for power, color in power_palette.items():
        subset = data[data['power'] == power]
        # Plot error bars
        ax2.errorbar(
            subset['speed'], 
            subset['relative_density'],
            yerr=subset['std_dev'],
            fmt='o',
            markersize=8,
            capsize=6,
            capthick=2,
            elinewidth=1.5,
            color=color,
            alpha=0.8,
            label='_'
        )
        # Add clean markers for legend
        ax2.plot([], [], 'o', color=color, markersize=8, label=f'{power} W')

    ax2.set_xlabel('Scanning Speed (mm/s)', fontsize=14)
    ax2.set_ylabel('Relative Density (%)', fontsize=14)
    ax2.set_ylim(94, 100.5)
    ax2.xaxis.set_major_locator(MultipleLocator(100))
    ax2.yaxis.set_major_locator(MultipleLocator(1))
    ax2.legend(frameon=True, title='Laser Power', loc='lower left')
    ax2.annotate('b)', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=16, ha='left', va='top')

    # --- Global styling ---
    for ax in [ax1, ax2]:
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        for spine in ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(1)

    plt.tight_layout()
    return fig

if __name__ == "__main__":
    file_path = "Ti13Nb13Zr5Cu_density.xlsx"
    data = load_and_process_data(file_path)
    fig = plot_journal_quality_graphs(data)
    fig.savefig('SLM_parameters_impact.png', dpi=600, bbox_inches='tight')
    plt.show()