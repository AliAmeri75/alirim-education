"""Beginner-friendly 2D and 3D defect visualizations."""

from __future__ import annotations

import json

import numpy as np
import plotly.graph_objects as go
import streamlit as st


GREEN = "#275d38"
GOLD = "#ffdb05"
BLUE = "#155987"
RED = "#c62828"
PLOTLY_CDN_URL = "https://cdn.plot.ly/plotly-3.3.0.min.js"


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


def linked_defect_views_html(
    defect_type: str,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> str:
    """Return a linked 2D/3D Plotly explorer as one self-contained HTML view.

    Hovering either plot moves the highlighted point in both plots. Keeping the
    interaction in the browser makes the response immediate and avoids a full
    Streamlit rerun for every mouse movement.
    """

    xx, yy, depth = defect_depth_grid(defect_type, length_mm, depth_mm, width_mm)
    center_row = depth.shape[0] // 2
    center_column = depth.shape[1] // 2
    center_x = float(xx[center_row, center_column])
    center_y = float(yy[center_row, center_column])
    center_depth = float(depth[center_row, center_column])

    map_figure = defect_map_figure(defect_type, length_mm, depth_mm, width_mm)
    map_figure.add_trace(
        go.Scatter(
            x=[center_x],
            y=[center_y],
            mode="markers",
            name="Linked point",
            marker={
                "size": 14,
                "color": GOLD,
                "line": {"color": "#14251c", "width": 2},
            },
            hovertemplate=(
                "Linked point<br>Axial: %{x:.1f} mm<br>"
                "Circumferential: %{y:.1f} mm<extra></extra>"
            ),
            showlegend=False,
        )
    )
    map_figure.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fbfdfc",
        font={"family": "Inter, Arial, sans-serif", "color": "#14251c"},
        hovermode="closest",
    )

    surface_figure = flat_defect_figure(
        defect_type, length_mm, depth_mm, width_mm
    )
    surface_figure.add_trace(
        go.Scatter3d(
            x=[center_x],
            y=[center_y],
            z=[-center_depth],
            mode="markers",
            name="Linked point",
            marker={
                "size": 7,
                "color": GOLD,
                "line": {"color": "#14251c", "width": 3},
            },
            hovertemplate=(
                "Linked point<br>Axial: %{x:.1f} mm<br>"
                "Circumferential: %{y:.1f} mm<br>"
                "Surface level: %{z:.2f} mm<extra></extra>"
            ),
            showlegend=False,
        )
    )
    surface_figure.update_layout(
        height=440,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Arial, sans-serif", "color": "#14251c"},
        hovermode="closest",
    )
    surface_figure.update_scenes(
        bgcolor="#fbfdfc",
        xaxis={"showspikes": True, "spikecolor": BLUE},
        yaxis={"showspikes": True, "spikecolor": BLUE},
        zaxis={"showspikes": True, "spikecolor": BLUE},
    )

    map_json = map_figure.to_json()
    surface_json = surface_figure.to_json()
    x_json = json.dumps(xx[0].tolist())
    y_json = json.dumps(yy[:, 0].tolist())
    depth_json = json.dumps(depth.tolist())
    initial_readout = (
        f"Axial: {center_x:.1f} mm &nbsp;•&nbsp; "
        f"Circumferential: {center_y:.1f} mm &nbsp;•&nbsp; "
        f"Depth: {center_depth:.2f} mm"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="{PLOTLY_CDN_URL}"></script>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: #14251c; background: transparent;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .linked-shell {{ padding: 10px; border: 1px solid #d8e2da; border-radius: 18px;
      background: rgba(255,255,255,.93); box-shadow: 0 12px 30px rgba(20,49,32,.08); }}
    .linked-header {{ display: flex; align-items: center; justify-content: space-between;
      gap: 12px; padding: 2px 8px 8px; flex-wrap: wrap; }}
    .linked-title {{ font-weight: 850; font-size: 15px; color: #173d27; }}
    .linked-hint {{ color: #5b6961; font-size: 12px; }}
    .plot-grid {{ display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr);
      gap: 8px; }}
    .plot-panel {{ min-width: 0; border: 1px solid #e5ece7; border-radius: 14px;
      overflow: hidden; background: #fbfdfc; }}
    .plot {{ width: 100%; height: 440px; }}
    #linked-readout {{ margin: 9px 8px 3px; padding: 9px 12px; border-radius: 10px;
      color: #173d27; background: #f1f6f2; border-left: 4px solid #ffdb05;
      font-size: 13px; font-variant-numeric: tabular-nums; }}
    #linked-error {{ display: none; margin: 12px; padding: 12px; color: #8b1a1a;
      background: #fff1f1; border-radius: 10px; }}
    @media (max-width: 720px) {{
      .plot-grid {{ grid-template-columns: 1fr; }}
      .plot {{ height: 390px; }}
    }}
  </style>
</head>
<body>
  <section class="linked-shell" aria-label="Linked two-dimensional and three-dimensional defect views">
    <div class="linked-header">
      <span class="linked-title">Linked defect explorer</span>
      <span class="linked-hint">Move over either view—the gold point follows in both.</span>
    </div>
    <div id="linked-error">The interactive figures could not be loaded. Please refresh the page.</div>
    <div class="plot-grid">
      <div class="plot-panel"><div id="defect-map" class="plot"></div></div>
      <div class="plot-panel"><div id="defect-surface" class="plot"></div></div>
    </div>
    <div id="linked-readout">{initial_readout}</div>
  </section>
  <script>
  (() => {{
    const errorBox = document.getElementById("linked-error");
    if (typeof Plotly === "undefined") {{
      errorBox.style.display = "block";
      return;
    }}

    const mapFigure = {map_json};
    const surfaceFigure = {surface_json};
    const xValues = {x_json};
    const yValues = {y_json};
    const depthValues = {depth_json};
    const mapDiv = document.getElementById("defect-map");
    const surfaceDiv = document.getElementById("defect-surface");
    const readout = document.getElementById("linked-readout");
    const config = {{ responsive: true, displaylogo: false,
      modeBarButtonsToRemove: ["lasso2d", "select2d"] }};

    const nearestIndex = (values, target) => {{
      let best = 0;
      let distance = Infinity;
      for (let i = 0; i < values.length; i += 1) {{
        const candidate = Math.abs(values[i] - target);
        if (candidate < distance) {{ best = i; distance = candidate; }}
      }}
      return best;
    }};

    let pending = null;
    let animationFrame = null;
    const synchronize = (xTarget, yTarget) => {{
      const column = nearestIndex(xValues, Number(xTarget));
      const row = nearestIndex(yValues, Number(yTarget));
      const x = xValues[column];
      const y = yValues[row];
      const depth = depthValues[row][column];
      const label = `Axial: ${{x.toFixed(1)}} mm • Circumferential: ${{y.toFixed(1)}} mm • Depth: ${{depth.toFixed(2)}} mm`;

      Plotly.restyle(mapDiv, {{ x: [[x]], y: [[y]] }}, [1]);
      Plotly.restyle(surfaceDiv, {{ x: [[x]], y: [[y]], z: [[-depth]] }}, [1]);
      readout.textContent = label;
    }};

    const scheduleSynchronization = (point) => {{
      if (!point || !Number.isFinite(Number(point.x)) || !Number.isFinite(Number(point.y))) return;
      pending = {{ x: Number(point.x), y: Number(point.y) }};
      if (animationFrame !== null) return;
      animationFrame = requestAnimationFrame(() => {{
        synchronize(pending.x, pending.y);
        animationFrame = null;
      }});
    }};

    Promise.all([
      Plotly.newPlot(mapDiv, mapFigure.data, mapFigure.layout, config),
      Plotly.newPlot(surfaceDiv, surfaceFigure.data, surfaceFigure.layout, config)
    ]).then(() => {{
      mapDiv.on("plotly_hover", event => scheduleSynchronization(event.points[0]));
      surfaceDiv.on("plotly_hover", event => scheduleSynchronization(event.points[0]));
    }}).catch(() => {{ errorBox.style.display = "block"; }});
  }})();
  </script>
</body>
</html>"""


def render_linked_defect_views(
    defect_type: str,
    length_mm: float,
    depth_mm: float,
    width_mm: float | None = None,
) -> None:
    """Render the linked explorer inside Streamlit."""

    st.iframe(
        linked_defect_views_html(defect_type, length_mm, depth_mm, width_mm),
        height=550,
        width="stretch",
    )


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
