# Thermal Heatmap Generator

`thermal-heatmap-generator` is a Python package for generating thermal-like heatmaps with customizable heat sources and Bezier curve-based edges. This package allows you to create dynamic heatmaps for use in simulations, visualizations, and artistic renderings.

## Features

- **Heat Sources**: Create thermal heatmaps with customizable heat sources that radiate heat.
- **Bezier Curve Edges**: Add natural, flowing edges based on Bezier curves to represent boundaries or object contours.

## Example Heatmaps

### Heatmap with Heat Sources
![Heatmap with Heat Sources](images/heatmap_sources.png)

### Heatmap with Bezier Edges
![Heatmap with Bezier Edges](images/heatmap_edges.png)

### Heatmap with Heat Sources and Bezier Edges
![Heatmap with Both Heat Sources and Edges](images/heatmap_combined.png)

## Installation

To install the package, use `conda`:

```bash
conda install -c your-conda-channel thermal-heatmap-generator
```

Alternatively, you can install the package via pip:

```bash
pip install git+https://github.com/yourusername/thermal-heatmap-generator.git
```

## Usage

Here’s a simple example of how to generate and save a thermal heatmap using the generate_thermal_heatmap function.

```python

from thermal_heatmap_generator import generate_thermal_heatmap
import matplotlib.pyplot as plt

# Generate a heatmap with heat sources only
heatmap_sources = generate_thermal_heatmap(num_sources=5, num_edges=0)

# Generate a heatmap with edges only
heatmap_edges = generate_thermal_heatmap(num_sources=0, num_edges=3)

# Generate a heatmap with both heat sources and edges
heatmap_combined = generate_thermal_heatmap(num_sources=5, num_edges=3)

# Save the heatmaps
plt.imsave('images/heatmap_sources.png', heatmap_sources, cmap='hot')
plt.imsave('images/heatmap_edges.png', heatmap_edges, cmap='hot')
plt.imsave('images/heatmap_combined.png', heatmap_combined, cmap='hot')
```