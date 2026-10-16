import unittest

import numpy as np

from education.visuals import (
    defect_depth_grid,
    defect_map_figure,
    flat_defect_figure,
    linked_defect_views_html,
    pipe_defect_figure,
    pipe_stress_directions_figure,
)


class EducationalVisualTests(unittest.TestCase):
    def test_crack_grid_uses_length_and_depth(self):
        x, y, depth = defect_depth_grid("Crack", length_mm=80.0, depth_mm=3.0)

        self.assertEqual(x.shape, y.shape)
        self.assertEqual(x.shape, depth.shape)
        self.assertAlmostEqual(float(np.max(depth)), 3.0, places=10)
        self.assertGreater(float(np.ptp(x)), 80.0)

    def test_corrosion_grid_uses_selected_width(self):
        _, narrow_y, _ = defect_depth_grid(
            "Corrosion", length_mm=80.0, depth_mm=3.0, width_mm=20.0
        )
        _, wide_y, depth = defect_depth_grid(
            "Corrosion", length_mm=80.0, depth_mm=3.0, width_mm=60.0
        )

        self.assertGreater(float(np.ptp(wide_y)), float(np.ptp(narrow_y)))
        self.assertAlmostEqual(float(np.max(depth)), 3.0, places=10)

    def test_visual_functions_return_plotly_figures(self):
        figures = [
            defect_map_figure("Crack", 80.0, 3.0),
            flat_defect_figure("Corrosion", 80.0, 3.0, 45.0),
            pipe_defect_figure("Crack", 508.0, 8.0, 80.0, 3.0),
        ]

        for figure in figures:
            self.assertEqual(len(figure.data), 1)
            self.assertGreater(len(figure.to_json()), 100)

    def test_linked_explorer_synchronizes_hover_between_both_views(self):
        linked_html = linked_defect_views_html("Crack", 80.0, 3.0)

        self.assertIn('mapDiv.on("plotly_hover"', linked_html)
        self.assertIn('surfaceDiv.on("plotly_hover"', linked_html)
        self.assertIn("Plotly.restyle(mapDiv", linked_html)
        self.assertIn("Plotly.restyle(surfaceDiv", linked_html)
        self.assertIn("Move over either view", linked_html)

    def test_pipe_stress_figure_shows_all_three_directions(self):
        figure = pipe_stress_directions_figure()
        names = {trace.name for trace in figure.data if trace.showlegend}
        trace_types = {trace.type for trace in figure.data}

        self.assertIn("Hoop stress — around the pipe", names)
        self.assertIn("Longitudinal stress — along the pipe", names)
        self.assertIn("Internal pressure — pushes outward", names)
        self.assertIn("surface", trace_types)
        self.assertIn("cone", trace_types)


if __name__ == "__main__":
    unittest.main()
