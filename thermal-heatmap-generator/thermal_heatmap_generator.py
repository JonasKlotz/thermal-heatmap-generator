import numpy as np
from scipy.ndimage import gaussian_filter
from bezier import get_random_points, get_bezier_curve


def generate_heat_source(
    heatmap: np.ndarray,
    x: int,
    y: int,
    intensity: float,
    size: int = 5,
    spread_sigma: float = 3,
) -> np.ndarray:
    """
    Generate a single heat source with a soft spread.

    Parameters:
        heatmap (np.ndarray): The base heatmap to which the heat source will be added.
        x (int): X-coordinate of the heat source's center.
        y (int): Y-coordinate of the heat source's center.
        intensity (float): Intensity of the heat source.
        size (int, optional): The size of the heat source (default is 5).
        spread_sigma (float, optional): Standard deviation for Gaussian filter to soften the heat source (default is 3).

    Returns:
        np.ndarray: The heatmap with the added heat source.
    """
    heat_source = np.zeros_like(heatmap)
    heat_source[
        y - size // 2 : y + size // 2 + 1, x - size // 2 : x + size // 2 + 1
    ] = intensity
    return gaussian_filter(heat_source, sigma=spread_sigma)


def add_random_edges(
    heatmap: np.ndarray,
    num_edges: int = 1,
    edge_intensity: int = 128,
    num_points: int = 3,
) -> np.ndarray:
    """
    Add random edges to the heatmap using Bezier curves.

    Parameters:
        heatmap (np.ndarray): The base heatmap to which the edges will be added.
        num_edges (int, optional): Number of Bezier curve edges to generate (default is 1).
        edge_intensity (int, optional): Intensity of the edges (default is 128).
        num_points (int, optional): Number of control points for generating Bezier curves (default is 5).

    Returns:
        np.ndarray: The heatmap with added Bezier curve edges.
    """
    edges_map = np.zeros_like(heatmap)

    for _ in range(num_edges):
        random_points = get_random_points(n=num_points, scale=heatmap.shape[0])
        x, y, _ = get_bezier_curve(random_points)

        for i in range(len(x)):
            xi, yi = int(x[i]), int(y[i])
            if 0 <= xi < heatmap.shape[1] and 0 <= yi < heatmap.shape[0]:
                edges_map[yi, xi] = edge_intensity

    return edges_map


def generate_thermal_heatmap(
    width: int = 256,
    height: int = 256,
    num_sources: int = 3,
    num_edges: int = 1,
    edge_sigma: float = 5,
    source_sigma: float = 50,
) -> np.ndarray:
    """
    Generate a thermal-like heatmap with random heat sources and Bezier curve edges.

    Parameters:
        width (int, optional): Width of the heatmap (default is 256).
        height (int, optional): Height of the heatmap (default is 256).
        num_sources (int, optional): Number of heat sources to generate (default is 3).
        num_edges (int, optional): Number of Bezier curve edges to generate (default is 1).
        edge_sigma (float, optional): Standard deviation for Gaussian filter applied to edges (default is 5).
        source_sigma (float, optional): Standard deviation for Gaussian filter applied to heat sources (default is 50).

    Returns:
        np.ndarray: The final thermal-like heatmap with sources and edges.
    """
    heatmap = np.zeros((height, width))

    for _ in range(num_sources):
        x = np.random.randint(10, width - 10)
        y = np.random.randint(10, height - 10)
        intensity = np.random.uniform(200, 255)
        heatmap += generate_heat_source(
            heatmap, x, y, intensity, spread_sigma=source_sigma
        )

    # Generate random edges
    edges = add_random_edges(heatmap, num_edges=num_edges, edge_intensity=128)
    edges = gaussian_filter(edges, sigma=edge_sigma)

    # Normalize the heatmap (sources) to a range of 0-1
    if heatmap.max() != 0:
        heatmap = heatmap / heatmap.max()

    # Normalize the edges to a range of 0-1
    if edges.max() != 0:
        edges = edges / edges.max()

    # Combine the normalized heatmap and edges, ensuring both are in the same range
    combined_heatmap = heatmap + edges

    # Normalize the combined heatmap to a range of 0-255 for final output
    if combined_heatmap.max() != 0:
        combined_heatmap = combined_heatmap / combined_heatmap.max() * 255
    return np.clip(combined_heatmap, 0, 255).astype(np.uint8)


import matplotlib.pyplot as plt


def main():
    # Generate a heatmap with heat sources only
    heatmap_sources = generate_thermal_heatmap(num_sources=5, num_edges=0)

    # Generate a heatmap with edges only
    heatmap_edges = generate_thermal_heatmap(num_sources=0, num_edges=3)

    # Generate a heatmap with both heat sources and edges
    heatmap_combined = generate_thermal_heatmap(num_sources=2, num_edges=3)

    # Save the heatmaps
    plt.imsave("../images/heatmap_sources.png", heatmap_sources, cmap="hot")
    plt.imsave("../images/heatmap_edges.png", heatmap_edges, cmap="hot")
    plt.imsave("../images/heatmap_combined.png", heatmap_combined, cmap="hot")


if __name__ == "__main__":
    main()
