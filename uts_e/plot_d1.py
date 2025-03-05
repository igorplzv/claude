import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# Data
data = [
    {"power": 200, "speed": 800, "density": 99.08, "energy": 50.0, "strategy": "Chess", "regime": "C1"},
    {"power": 150, "speed": 800, "density": 96.77, "energy": 37.5, "strategy": "Chess", "regime": "C2"},
    {"power": 250, "speed": 800, "density": 99.18, "energy": 62.5, "strategy": "Chess", "regime": "C3"},
    {"power": 200, "speed": 600, "density": 97.66, "energy": 66.7, "strategy": "Chess", "regime": "C4"},
    {"power": 200, "speed": 1000, "density": 99.14, "energy": 40.0, "strategy": "Chess", "regime": "C5"},
    {"power": 250, "speed": 600, "density": 96.92, "energy": 83.3, "strategy": "Chess", "regime": "C6"},
    {"power": 150, "speed": 1000, "density": 95.35, "energy": 30.0, "strategy": "Chess", "regime": "C7"},
    {"power": 200, "speed": 500, "density": 96.54, "energy": 80.0, "strategy": "Chess", "regime": "C8"},
    {"power": 200, "speed": 1000, "density": 99.86, "energy": 40.0, "strategy": "Linear", "regime": "L1"},
    {"power": 200, "speed": 1000, "density": 99.85, "energy": 80.0, "strategy": "Linear", "regime": "L2"},
    {"power": 200, "speed": 800, "density": 99.79, "energy": 62.5, "strategy": "Linear", "regime": "L3"},
    {"power": 250, "speed": 800, "density": 99.67, "energy": 78.1, "strategy": "Linear", "regime": "L4"},
    {"power": 200, "speed": 1000, "density": 99.51, "energy": 50.0, "strategy": "Linear", "regime": "L5"}
]

# Separate data by strategy
chess_data = [d for d in data if d["strategy"] == "Chess"]
linear_data = [d for d in data if d["strategy"] == "Linear"]

# Extract coordinates
chess_x = [d["speed"] for d in chess_data]
chess_y = [d["power"] for d in chess_data]
linear_x = [d["speed"] for d in linear_data]
linear_y = [d["power"] for d in linear_data]

# Create figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300, sharey=True)

# --- Chess Pattern Subplot (Left) ---
# Add density regions (zorder=1 for background)
chess_good_points = [(600, 180), (1050, 180), (1050, 275), (750, 275), (600, 225)]  # C1, C3, C5
chess_good_patch = Polygon(chess_good_points, closed=True, fill=True, color="yellow", alpha=0.3, label="Density 99–99.7%", zorder=1)
ax1.add_patch(chess_good_patch)

chess_moderate_points = [(450, 140), (1050, 140), (1050, 275), (600, 275), (450, 200)]  # C2, C4, C6, C7, C8
chess_moderate_patch = Polygon(chess_moderate_points, closed=True, fill=True, color="orange", alpha=0.3, label="Density 95–99%", zorder=1)
ax1.add_patch(chess_moderate_patch)

# Plot points (zorder=2 to be above zones)
ax1.scatter(chess_x, chess_y, c="#2563eb", s=100, edgecolors="black", linewidth=0.5, zorder=2)

ax1.set_xlim(400, 1100)
ax1.set_ylim(100, 300)
ax1.set_xlabel("Scanning speed, mm/s", fontsize=15)
ax1.set_ylabel("Laser power, W", fontsize=15)
ax1.set_title("(a) Chess Pattern", fontsize=17)
ax1.grid(True, linestyle="--", alpha=0.7)
ax1.legend(fontsize=13, loc="upper right")

# --- Linear Strategy Subplot (Right) ---
# Add density regions (zorder=1 for background)
linear_optimal_points = [(750, 190), (1050, 190), (1050, 230), (750, 230)]  # L1, L2, L3
linear_optimal_patch = Polygon(linear_optimal_points, closed=True, fill=True, color="green", alpha=0.3, label="Density > 99.7%", zorder=1)
ax2.add_patch(linear_optimal_patch)

linear_good_points = [(750, 180), (1050, 180), (1050, 275), (750, 275)]  # L4, L5
linear_good_patch = Polygon(linear_good_points, closed=True, fill=True, color="yellow", alpha=0.3, label="Density 99–99.7%", zorder=1)
ax2.add_patch(linear_good_patch)

# Plot points (zorder=2 to be above zones)
ax2.scatter(linear_x, linear_y, c="#16a34a", marker="^", s=100, edgecolors="black", linewidth=0.5, zorder=2, alpha=0.9)

ax2.set_xlim(400, 1100)
ax2.set_xlabel("Scanning speed, mm/s", fontsize=15)
ax2.set_title("(b) Linear Scanning Strategy", fontsize=17)
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.legend(fontsize=13, loc="upper right")

# Adjust layout
plt.tight_layout()

# Save the figure
plt.savefig("slm_processing_window_subplots_corrected.png", dpi=300, bbox_inches="tight")
plt.savefig("slm_processing_window_subplots_corrected.pdf", dpi=300, bbox_inches="tight")
plt.show()