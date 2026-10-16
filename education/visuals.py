"""Beginner-friendly 2D and 3D defect visualizations."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go


GREEN = "#275d38"
GOLD = "#ffdb05"
BLUE = "#155987"
RED = "#c62828"


def defect_depth_grid(
    defect_type: str,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return an exaggerated teaching surface for a crack or corrosion patch."""

    width = float(width_mm or max(2.0, 0.05 * length_mm))
    x_limit = max(1.15 * length_mm, 80.0)
    y_limit = max(1.25 * width, 40.0)
    x = np.linspace(-x_limit / 2.0, x_limit / 2.0, 121)
    y = np.linspace(-y_limit / 2.0, y_limit / 2.0, 81)
    xx, yy = np.meshgrid(x, y)

    axial_scale = max(0.42 * length_mm, 1.0)
    if defect_type == "Crack":
        # Crack width is not an engineering input here. A narrow band is used only
        # to make the crack visible in the teaching figure.
        display_half_width = max(0.018 * length_mm, 0.6)
        shape = np.exp(-((xx / axial_scale) ** 4)) * np.exp(
            -((yy / display_half_width) ** 2)
        )
    else:
        circumferential_scale = max(0.42 * width, 1.0)
        shape = np.exp(
            -0.5
            * (
                (xx / axial_scale) ** 4
                + (yy / circumferential_scale) ** 4
            )
        )
    return xx, yy, depth_mm * shape


def defect_map_figure(
    defect_type: str,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> go.Figure:
    """Create a top-view depth map."""

    xx, yy, depth = defect_depth_grid(defect_type, length_mm, depth_mm, width_mm)
    figure = go.Figure(
        go.Heatmap(
            x=xx[0],
            y=yy[:, 0],
            z=depth,
            colorscale="YlOrRd",
            colorbar={"title": "Depth<br>(mm)"},
            hovertemplate="Axial: %{x:.1f} mm<br>Circumferential: %{y:.1f} mm<br>Depth: %{z:.2f} mm<extra></extra>",
        )
    )
    figure.update_layout(
        title=f"2D depth map: {defect_type.lower()}",
        xaxis_title="Axial direction (mm)",
        yaxis_title="Circumferential direction (mm)",
        height=380,
        margin={"l": 45, "r": 20, "t": 55, "b": 45},
    )
    return figure


def flat_defect_figure(
    defect_type: str,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> go.Figure:
    """Create a 3D wall-patch view of a defect."""

    xx, yy, depth = defect_depth_grid(defect_type, length_mm, depth_mm, width_mm)
    figure = go.Figure(
        go.Surface(
            x=xx,
            y=yy,
            z=-depth,
            surfacecolor=depth,
            colorscale="YlOrRd",
            colorbar={"title": "Depth<br>(mm)"},
            hovertemplate="Axial: %{x:.1f} mm<br>Circumferential: %{y:.1f} mm<br>Depth below surface: %{surfacecolor:.2f} mm<extra></extra>",
        )
    )
    figure.update_layout(
        title=f"3D wall view: {defect_type.lower()}",
        scene={
            "xaxis_title": "Axial (mm)",
            "yaxis_title": "Circumferential (mm)",
            "zaxis_title": "Surface level (mm)",
            "camera": {"eye": {"x": 1.45, "y": -1.55, "z": 0.9}},
            "aspectratio": {"x": 1.5, "y": 1.0, "z": 0.45},
        },
        height=430,
        margin={"l": 0, "r": 0, "t": 55, "b": 0},
    )
    return figure


def pipe_defect_figure(
    defect_type: str,
    diameter_mm: float,
    wall_thickness_mm: float,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> go.Figure:
    """Place an exaggerated defect on a cylindrical pipe surface."""

    width = float(width_mm or max(2.0, 0.05 * length_mm))
    pipe_view_length = max(2.2 * length_mm, 260.0)
    axial = np.linspace(-pipe_view_length / 2.0, pipe_view_length / 2.0, 121)
    theta = np.linspace(-np.pi, np.pi, 101)
    xx, tt = np.meshgrid(axial, theta)
    circumferential_mm = tt * diameter_mm / 2.0

    axial_scale = max(0.42 * length_mm, 1.0)
    if defect_type == "Crack":
        display_half_width = max(0.018 * length_mm, 0.6)
        defect_shape = np.exp(-((xx / axial_scale) ** 4)) * np.exp(
            -((circumferential_mm / display_half_width) ** 2)
        )
    else:
        circumferential_scale = max(0.42 * width, 1.0)
        defect_shape = np.exp(
            -0.5
            * (
                (xx / axial_scale) ** 4
                + (circumferential_mm / circumferential_scale) ** 4
            )
        )

    # The real depth-to-radius ratio is too small to see clearly on screen.
    # A capped visual exaggeration is used, while the colour shows real depth.
    real_depth = depth_mm * defect_shape
    depth_ratio = min(depth_mm / wall_thickness_mm, 1.0)
    display_depression = 0.22 * depth_ratio * defect_shape
    radius = 1.0 - display_depression
    yy = radius * np.cos(tt)
    zz = radius * np.sin(tt)

    figure = go.Figure(
        go.Surface(
            x=xx,
            y=yy,
            z=zz,
            surfacecolor=real_depth,
            colorscale="YlOrRd",
            cmin=0,
            cmax=max(depth_mm, 0.01),
            colorbar={"title": "Depth<br>(mm)"},
            hovertemplate="Axial: %{x:.1f} mm<br>Depth: %{surfacecolor:.2f} mm<extra></extra>",
        )
    )
    figure.update_layout(
        title=f"{defect_type} on the pipe surface",
        scene={
            "xaxis_title": "Pipe axis (mm)",
            "yaxis_title": "",
            "zaxis_title": "",
            "camera": {"eye": {"x": 1.5, "y": -1.6, "z": 0.9}},
            "aspectratio": {"x": 2.2, "y": 1.0, "z": 1.0},
        },
        height=500,
        margin={"l": 0, "r": 0, "t": 55, "b": 0},
    )
    return figure
