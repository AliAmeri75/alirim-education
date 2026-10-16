"""Step-by-step undergraduate learning book for pipeline integrity."""

from __future__ import annotations

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from education.pof_model import (
    DistributionSpec,
    POFInputs,
    corlas_failure_pressure,
    simulate_probability_of_failure,
)
from education.visuals import (
    pipe_defect_figure,
    pipe_stress_directions_figure,
    render_linked_defect_views,
)
from platform_ui import render_learning_cards, render_learning_path, render_project_hero


STATICS_URL = "https://engcourses-uofa.ca/books/statics/"
SOLID_MECHANICS_URL = (
    "https://engcourses-uofa.ca/books/introduction-to-solid-mechanics/"
)
PHMSA_RISK_URL = (
    "https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/2020-03/"
    "Pipeline-Risk-Modeling-Technical-Information-Document-02-01-2020-Final_0.pdf"
)
CANADA_VSL_URL = (
    "https://www.canada.ca/en/government/system/laws/developing-improving-"
    "federal-regulations/requirements-developing-managing-reviewing-regulations/"
    "policy-cost-benefit-analysis.html"
)
CORLAS_REVIEW_URL = "https://doi.org/10.1061/JPSEA2.PSENG-1849"
CORLAS_IMPROVEMENT_URL = "https://doi.org/10.1016/j.iintel.2023.100043"

CHAPTERS = (
    "Welcome and learning path",
    "Forces, equilibrium, stress and strain",
    "Pressure stresses in a pipe",
    "Crack and corrosion shapes",
    "Defects on a pipe",
    "Simple limit states: leakage and rupture",
    "Consequences of failure",
    "Failure pressure and the CorLAS model",
    "Probability of failure",
    "Knowledge check",
)


def _go_to_chapter(index: int) -> None:
    st.session_state.book_chapter_selector = int(
        np.clip(index, 0, len(CHAPTERS) - 1)
    )


def _concept_cards(cards: list[tuple[str, str]]) -> None:
    render_learning_cards(cards, label="Key idea")


def _checkpoint(question: str, options: list[str], correct: str, key: str) -> None:
    st.markdown("#### Quick check")
    answer = st.radio(question, options, index=None, key=key)
    if answer == correct:
        st.success("Correct — you are ready to continue.")
    elif answer is not None:
        st.info("Not quite. Re-read the short explanation and try once more.")


def chapter_welcome() -> None:
    st.header("Welcome to pipeline integrity")
    st.write(
        "This book starts with basic mechanics and builds one idea at a time. "
        "You do not need previous pipeline experience."
    )

    st.subheader("What will you be able to do?")
    _concept_cards(
        [
            ("Describe", "Explain what pressure, stress, cracks, corrosion, leakage, and rupture mean."),
            ("Calculate", "Use simple formulas for pipe stress, limit states, failure pressure, and probability."),
            ("Interpret", "Connect probability and consequences to a basic integrity decision."),
        ]
    )

    st.subheader("The learning story")
    render_learning_path(
        [
            "Pressure produces forces and stresses in the pipe wall.",
            "Cracks and corrosion damage or remove material.",
            "A limit state separates margin from failure.",
            "Uncertain inputs make failure uncertain.",
            "Risk combines likelihood with consequences.",
        ]
    )

    st.info(
        "Use the chapter list on the left. Each chapter contains a short explanation, "
        "an interactive example, and a quick check."
    )

    st.subheader("Optional mechanics preparation")
    left, right = st.columns(2)
    with left:
        st.link_button(
            "University of Alberta: Engineering Mechanics—Statics",
            STATICS_URL,
            width="stretch",
        )
    with right:
        st.link_button(
            "University of Alberta: Introduction to Solid Mechanics",
            SOLID_MECHANICS_URL,
            width="stretch",
        )


def chapter_mechanics() -> None:
    st.header("Forces, equilibrium, stress and strain")
    st.write(
        "Mechanics asks a simple question: **how do loads act on an object, and how "
        "does the object respond?** A pressurized pipe must remain in equilibrium while "
        "its wall carries the pressure load."
    )

    _concept_cards(
        [
            ("Force", "A push or pull, measured in newtons (N)."),
            ("Stress", "Force distributed over an area. Stress = Force ÷ Area."),
            ("Strain", "Change in length divided by the original length."),
        ]
    )

    st.subheader("Try a simple stress calculation")
    force_kn = st.slider("Axial force (kN)", 1.0, 500.0, 100.0, 1.0)
    area_mm2 = st.slider("Load-carrying area (mm²)", 50.0, 5000.0, 1000.0, 50.0)
    stress_mpa = force_kn * 1000.0 / area_mm2
    st.metric("Average normal stress", f"{stress_mpa:,.1f} MPa")
    st.latex(r"\sigma = \frac{F}{A}")
    st.caption(
        "Because 1 MPa equals 1 N/mm², using newtons and mm² gives stress directly in MPa."
    )

    st.subheader("Equilibrium comes first")
    st.write(
        "If an object is not accelerating, its forces and moments balance. We can cut "
        "the pipe conceptually, draw a free-body diagram, and balance pressure forces "
        "against forces carried by the wall. That balance produces the pipe-stress formulas."
    )
    st.link_button("Review free-body diagrams and equilibrium", STATICS_URL)

    _checkpoint(
        "If the same force acts over a smaller area, what happens to stress?",
        ["Stress decreases", "Stress stays the same", "Stress increases"],
        "Stress increases",
        "book_check_mechanics",
    )


def chapter_pipe_stress() -> None:
    st.header("Pressure stresses in a pipe")
    st.write(
        "Internal pressure pushes outward on the pipe wall. For a thin-walled closed "
        "cylinder, two membrane stresses are especially important."
    )

    st.latex(r"\sigma_h = \frac{pD}{2t} \qquad \sigma_L = \frac{pD}{4t}")
    st.markdown(
        "- **Hoop stress, $\\sigma_h$:** acts around the circumference.\n"
        "- **Longitudinal stress, $\\sigma_L$:** acts along the pipe axis.\n"
        "- $p$ is internal pressure, $D$ is diameter, and $t$ is wall thickness."
    )

    st.subheader("See the directions in 3D")
    st.plotly_chart(
        pipe_stress_directions_figure(),
        width="stretch",
        config={"displaylogo": False},
    )
    st.caption(
        "Rotate the cutaway pipe with your mouse. Orange arrows follow the curved "
        "wall (hoop stress), green arrows run along the pipe (longitudinal stress), "
        "and blue arrows show internal pressure pushing outward."
    )

    st.subheader("Interactive pipe-stress calculator")
    p_col, d_col, t_col = st.columns(3)
    with p_col:
        pressure_psi = st.number_input(
            "Internal pressure (psi)", 0.0, 3000.0, 936.0, 10.0, key="book_pressure"
        )
    with d_col:
        diameter_mm = st.number_input(
            "Outside diameter (mm)", 100.0, 1500.0, 508.0, 10.0, key="book_diameter"
        )
    with t_col:
        wall_mm = st.number_input(
            "Wall thickness (mm)", 2.0, 40.0, 6.35, 0.05, key="book_wall"
        )

    pressure_mpa = pressure_psi * 0.006894757
    hoop_mpa = pressure_mpa * diameter_mm / (2.0 * wall_mm)
    longitudinal_mpa = pressure_mpa * diameter_mm / (4.0 * wall_mm)
    hoop_col, long_col, ratio_col = st.columns(3)
    hoop_col.metric("Hoop stress", f"{hoop_mpa:,.1f} MPa")
    long_col.metric("Longitudinal stress", f"{longitudinal_mpa:,.1f} MPa")
    ratio_col.metric("Hoop ÷ longitudinal", f"{hoop_mpa / max(longitudinal_mpa, 1e-9):.1f}")

    stress_data = pd.DataFrame(
        {
            "Stress": ["Hoop", "Longitudinal"],
            "Value (MPa)": [hoop_mpa, longitudinal_mpa],
        }
    )
    chart = (
        alt.Chart(stress_data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Stress:N", title=None),
            y=alt.Y("Value (MPa):Q", title="Stress (MPa)"),
            color=alt.Color(
                "Stress:N",
                scale=alt.Scale(domain=["Hoop", "Longitudinal"], range=["#155987", "#275d38"]),
                legend=None,
            ),
            tooltip=["Stress:N", alt.Tooltip("Value (MPa):Q", format=".1f")],
        )
        .properties(height=280)
    )
    st.altair_chart(chart, width="stretch")

    st.warning(
        "These are introductory thin-wall formulas. Real assessments may also consider "
        "temperature, residual stress, external loads, material behaviour, geometry, "
        "and applicable codes."
    )

    _checkpoint(
        "For the same pressure and diameter, what happens when wall thickness increases?",
        ["Pipe stress increases", "Pipe stress decreases", "Pipe stress is unchanged"],
        "Pipe stress decreases",
        "book_check_pipe_stress",
    )


def _defect_controls(prefix: str) -> tuple[str, float, float, float | None]:
    defect_type = st.radio(
        "Defect type",
        ["Crack", "Corrosion"],
        horizontal=True,
        key=f"{prefix}_type",
    )
    length_col, depth_col = st.columns(2)
    with length_col:
        length_mm = st.slider(
            "Defect length (mm)", 10.0, 200.0, 80.0, 5.0, key=f"{prefix}_length"
        )
    with depth_col:
        depth_mm = st.slider(
            "Maximum depth (mm)", 0.2, 8.0, 3.0, 0.1, key=f"{prefix}_depth"
        )
    width_mm = None
    if defect_type == "Corrosion":
        width_mm = st.slider(
            "Corrosion width (mm)", 5.0, 150.0, 45.0, 5.0, key=f"{prefix}_width"
        )
    else:
        st.caption(
            "A crack is represented by its length and depth. The thin line in the "
            "figure is only used to make it visible."
        )
    return defect_type, length_mm, depth_mm, width_mm


def chapter_defect_shapes() -> None:
    st.header("Crack and corrosion shapes")
    st.write(
        "Cracks and corrosion both reduce integrity, but their shapes are different. "
        "A crack is narrow and sharp. Corrosion is usually a broader area of metal loss."
    )

    comparison = pd.DataFrame(
        [
            {
                "Defect": "Crack",
                "Simple dimensions": "Length and depth",
                "Typical teaching shape": "Narrow, sharp, often semi-elliptical",
                "Important behaviour": "Stress concentration and fracture",
            },
            {
                "Defect": "Corrosion",
                "Simple dimensions": "Length, width, and depth",
                "Typical teaching shape": "Broad patch or pit",
                "Important behaviour": "Wall thinning and plastic collapse",
            },
        ]
    )
    st.dataframe(comparison, hide_index=True, width="stretch")

    defect_type, length_mm, depth_mm, width_mm = _defect_controls("shape")
    render_linked_defect_views(defect_type, length_mm, depth_mm, width_mm)
    st.caption(
        "Move over either figure to follow the same location in both views. "
        "The shapes are smooth teaching illustrations, not inspection measurements."
    )

    _checkpoint(
        "Which dimensions are normally used for a simple corrosion patch?",
        ["Length only", "Length and depth", "Length, width, and depth"],
        "Length, width, and depth",
        "book_check_shapes",
    )


def chapter_defects_on_pipe() -> None:
    st.header("Defects on a pipe")
    st.write(
        "A flat defect map helps us measure the anomaly. Placing the same defect on a "
        "pipe helps us understand its orientation and how much wall remains."
    )

    defect_type, length_mm, depth_mm, width_mm = _defect_controls("pipe")
    diameter_mm = st.slider("Pipe diameter (mm)", 200.0, 1000.0, 508.0, 10.0)
    wall_mm = st.slider("Pipe wall thickness (mm)", 3.0, 20.0, 8.0, 0.25)
    depth_percent = 100.0 * depth_mm / wall_mm

    if depth_mm >= wall_mm:
        st.error("The selected depth reaches or exceeds the wall thickness. This represents leakage in the simple model.")
    else:
        st.metric("Defect depth", f"{depth_percent:.1f}% of wall thickness")

    st.plotly_chart(
        pipe_defect_figure(
            defect_type,
            diameter_mm,
            wall_mm,
            length_mm,
            depth_mm,
            width_mm,
        ),
        width="stretch",
        config={"displaylogo": False},
    )
    st.caption(
        "The surface depression is exaggerated so it can be seen. Colour shows the "
        "selected defect depth. The first crack example is longitudinal, along the pipe axis."
    )

    st.markdown(
        """
        #### Questions an integrity engineer asks

        - Is the defect inside or outside the pipe?
        - Is a crack longitudinal, circumferential, or inclined?
        - How deep and long is it, and how reliable are those measurements?
        - Are several nearby defects likely to interact?
        """
    )


def chapter_limit_states() -> None:
    st.header("Simple limit states: leakage and rupture")
    st.write(
        "A **limit state** is a boundary between two conditions. We write it as "
        "$g(\\mathbf{X})$. In this book, $g>0$ means the modelled condition has margin, "
        "and $g\\leq0$ means the limit state has been reached."
    )

    st.subheader("1. Leakage: has the defect reached through the wall?")
    wall_mm = st.slider("Wall thickness, t (mm)", 3.0, 20.0, 8.0, 0.25, key="limit_wall")
    defect_depth_mm = st.slider(
        "Defect depth, d (mm)", 0.0, 22.0, 5.0, 0.25, key="limit_depth"
    )
    leakage_margin = wall_mm - defect_depth_mm
    st.latex(r"g_{leak}=t-d")
    st.metric("Remaining-wall margin", f"{leakage_margin:,.2f} mm")
    if leakage_margin > 0:
        st.success("Simple leakage limit state not reached: some wall remains.")
    else:
        st.error("Simple leakage limit state reached: the defect is through-wall.")

    st.subheader("2. Rupture: can predicted resistance carry the pressure?")
    operating_pressure = st.slider(
        "Operating pressure (psi)", 100.0, 3000.0, 936.0, 10.0, key="limit_operation"
    )
    predicted_failure_pressure = st.slider(
        "Predicted failure pressure (psi)",
        100.0,
        4000.0,
        1500.0,
        10.0,
        key="limit_failure",
    )
    burst_margin = predicted_failure_pressure - operating_pressure
    st.latex(r"g_{rupture}=P_f-P_{operating}")
    st.metric("Pressure margin", f"{burst_margin:,.0f} psi")
    if burst_margin > 0:
        st.success("Operating pressure is below the modelled failure pressure.")
    else:
        st.error("Operating pressure reaches or exceeds the modelled failure pressure.")

    st.warning(
        "These two equations teach the idea of a limit state. They are not complete "
        "acceptance criteria and must not be used to operate a pipeline."
    )

    _checkpoint(
        "In this book, what does g ≤ 0 mean?",
        ["The limit state is reached", "The pipe has extra margin", "The input is deterministic"],
        "The limit state is reached",
        "book_check_limit_state",
    )


def chapter_consequences() -> None:
    st.header("Consequences of failure")
    st.write(
        "Likelihood answers **how likely?** Consequence answers **what could happen?** "
        "Pipeline risk considers both."
    )
    st.latex(r"Risk = Likelihood \times Consequence")

    _concept_cards(
        [
            ("People", "Possible injuries or fatalities from fire, explosion, exposure, or other hazards."),
            ("Environment", "Possible impacts to water, soil, air, wildlife, habitat, and cleanup needs."),
            ("Economic", "Repair, product loss, service interruption, property damage, and business impacts."),
            ("Social", "Community disruption, evacuation, loss of confidence, and effects on critical services."),
        ]
    )

    st.subheader("Build a simple consequence profile")
    st.caption("Use 0–5 classroom scores. These are not regulatory consequence values.")
    categories = ["People", "Environment", "Economic", "Social"]
    defaults = [4, 3, 3, 2]
    scores: list[int] = []
    columns = st.columns(4)
    for column, category, default in zip(columns, categories, defaults):
        with column:
            scores.append(
                st.slider(category, 0, 5, default, key=f"consequence_{category.lower()}")
            )

    consequence_data = pd.DataFrame({"Category": categories, "Relative score": scores})
    chart = (
        alt.Chart(consequence_data)
        .mark_bar(cornerRadiusEnd=5, color="#155987")
        .encode(
            x=alt.X("Relative score:Q", scale=alt.Scale(domain=[0, 5])),
            y=alt.Y("Category:N", sort=categories),
            tooltip=["Category:N", "Relative score:Q"],
        )
        .properties(height=230)
    )
    st.altair_chart(chart, width="stretch")

    annual_pof = st.number_input(
        "Illustrative annual probability of failure",
        min_value=0.0,
        max_value=1.0,
        value=0.001,
        step=0.001,
        format="%.4f",
    )
    relative_index = annual_pof * sum(scores)
    st.metric("Illustrative relative-risk index", f"{relative_index:.4f}")
    st.caption(
        "This index is only for seeing how likelihood and consequence interact. "
        "Real categories may have different units and require a documented method."
    )

    with st.expander("What does ‘value of statistical life’ mean?"):
        st.write(
            "Value of Statistical Life (VSL) is a policy tool for valuing small "
            "reductions in mortality risk across a population. It does **not** assign "
            "a price to an identifiable person. Real analyses must use the value, "
            "price year, and guidance required by the relevant authority."
        )
        st.link_button("Government of Canada explanation of VSL", CANADA_VSL_URL)

    st.link_button("PHMSA technical information on pipeline risk modelling", PHMSA_RISK_URL)

    _checkpoint(
        "Which statement best describes pipeline risk?",
        [
            "Failure probability only",
            "Repair cost only",
            "Likelihood considered together with consequences",
        ],
        "Likelihood considered together with consequences",
        "book_check_consequence",
    )


def chapter_corlas() -> None:
    st.header("Failure pressure and the CorLAS model")
    st.write(
        "A failure-pressure model estimates the internal pressure at which a cracked "
        "pipe could fail under the model assumptions. CorLAS is a pipeline-specific "
        "model for longitudinal crack-like flaws."
    )

    st.subheader("The main idea")
    _concept_cards(
        [
            ("Flow check", "Could the remaining section fail by plastic collapse?"),
            ("Fracture check", "Could the crack grow because fracture resistance is exceeded?"),
            ("Prediction", "The lower pressure from the two checks controls the prediction."),
        ]
    )
    st.latex(r"P_f=\min(P_{flow},\;P_{fracture})")

    st.subheader("Try a simplified CorLAS classroom case")
    length_col, depth_col, pressure_col = st.columns(3)
    with length_col:
        crack_length = st.slider("Crack length (mm)", 5.0, 250.0, 40.0, 5.0)
    with depth_col:
        crack_depth = st.slider("Crack depth (mm)", 0.2, 6.0, 4.0, 0.1)
    with pressure_col:
        operating_pressure = st.slider("Operating pressure (psi)", 100.0, 2000.0, 936.0, 10.0)

    inputs = POFInputs(
        flaw_length_mm=crack_length,
        flaw_depth_mm=crack_depth,
        operating_pressure_psi=operating_pressure,
    )
    result = corlas_failure_pressure(inputs)
    flow_pressure = result["flow_pressure_psi"]
    toughness_pressure = result["toughness_pressure_psi"]
    failure_pressure = result["failure_pressure_psi"]
    fpr = failure_pressure / operating_pressure

    flow_col, fracture_col, final_col, fpr_col = st.columns(4)
    flow_col.metric("Flow check", f"{flow_pressure:,.0f} psi")
    fracture_col.metric("Fracture check", f"{toughness_pressure:,.0f} psi")
    final_col.metric("Predicted failure pressure", f"{failure_pressure:,.0f} psi")
    fpr_col.metric("FPR", f"{fpr:.3f}")

    pressures = pd.DataFrame(
        {
            "Quantity": ["Operating", "Flow check", "Fracture check", "Prediction"],
            "Pressure (psi)": [
                operating_pressure,
                flow_pressure,
                toughness_pressure,
                failure_pressure,
            ],
        }
    )
    pressure_chart = (
        alt.Chart(pressures)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Quantity:N", sort=None, title=None),
            y=alt.Y("Pressure (psi):Q"),
            color=alt.Color(
                "Quantity:N",
                scale=alt.Scale(
                    domain=["Operating", "Flow check", "Fracture check", "Prediction"],
                    range=["#c62828", "#155987", "#7b5ea7", "#275d38"],
                ),
                legend=None,
            ),
            tooltip=["Quantity:N", alt.Tooltip("Pressure (psi):Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(pressure_chart, width="stretch")

    st.info(
        "This classroom implementation uses fixed default pipe and material properties "
        "while you vary crack size and pressure. Open the Analysis Lab for all parameters."
    )
    st.warning(
        "CorLAS predictions depend on geometry, material data, fracture toughness, model "
        "form, and applicability limits. Engineering validation and applicable standards are required."
    )

    st.subheader("Suggested publications")
    st.markdown(
        f"""
        - [ANN and XFEM-Driven Predictive Framework for Axial Crack Failure in Pipelines: Advancing beyond CorLAS]({CORLAS_REVIEW_URL})
        - [Improvement of burst capacity model for pipelines containing surface cracks and its implication for reliability analysis]({CORLAS_IMPROVEMENT_URL})
        """
    )

    _checkpoint(
        "If the flow check is 1,600 psi and the fracture check is 1,300 psi, which controls?",
        ["1,600 psi", "1,300 psi", "Their average"],
        "1,300 psi",
        "book_check_corlas",
    )


def chapter_probability() -> None:
    st.header("Probability of failure")
    st.write(
        "Pipe properties, defect measurements, loads, and models are uncertain. "
        "Instead of one input set, we can simulate many plausible sets and count how "
        "often the limit state is reached."
    )
    st.latex(r"P_f \approx \frac{\text{number of simulations with }g\leq0}{\text{total simulations}}")

    st.subheader("Monte Carlo experiment")
    mean_col, sd_col = st.columns(2)
    with mean_col:
        mean_depth = st.slider("Mean crack depth (mm)", 1.0, 6.0, 5.0, 0.1)
        mean_length = st.slider("Mean crack length (mm)", 10.0, 200.0, 80.0, 5.0)
    with sd_col:
        depth_sd = st.slider("Depth standard deviation (mm)", 0.05, 1.2, 0.45, 0.05)
        length_sd = st.slider("Length standard deviation (mm)", 1.0, 40.0, 12.0, 1.0)
    operating_pressure = st.slider(
        "Operating pressure (psi)", 500.0, 1800.0, 1100.0, 10.0, key="pof_operating"
    )
    samples = st.select_slider(
        "Number of simulations",
        options=[250, 500, 1000, 2000],
        value=500,
    )

    inputs = POFInputs(
        flaw_depth_mm=mean_depth,
        flaw_length_mm=mean_length,
        operating_pressure_psi=operating_pressure,
    )
    specs = {name: DistributionSpec() for name in inputs.__dict__}
    specs["flaw_depth_mm"] = DistributionSpec("Normal", standard_deviation=depth_sd)
    specs["flaw_length_mm"] = DistributionSpec("Normal", standard_deviation=length_sd)
    result = simulate_probability_of_failure(
        inputs,
        variable_specs=specs,
        samples=int(samples),
        seed=12,
    )
    probability = float(result["probability_of_failure"])
    failures = int(result["failures"])
    margins = np.asarray(result["margins_psi"], dtype=float)

    pof_col, failure_col, safe_col = st.columns(3)
    pof_col.metric("Estimated POF", f"{probability:.4f}")
    failure_col.metric("Failed simulations", f"{failures} of {samples}")
    safe_col.metric("Other simulations", f"{samples - failures} of {samples}")

    margin_data = pd.DataFrame(
        {
            "Limit-state margin (psi)": margins,
            "Outcome": np.where(margins <= 0.0, "Failure: g ≤ 0", "Margin: g > 0"),
        }
    )
    margin_chart = (
        alt.Chart(margin_data)
        .mark_bar(opacity=0.82)
        .encode(
            x=alt.X("Limit-state margin (psi):Q", bin=alt.Bin(maxbins=35)),
            y=alt.Y("count():Q", title="Simulated cases"),
            color=alt.Color(
                "Outcome:N",
                scale=alt.Scale(
                    domain=["Failure: g ≤ 0", "Margin: g > 0"],
                    range=["#c62828", "#275d38"],
                ),
            ),
            tooltip=["Outcome:N", "count():Q"],
        )
        .properties(height=320)
    )
    zero_line = (
        alt.Chart(pd.DataFrame({"g": [0.0]}))
        .mark_rule(color="#111111", strokeDash=[5, 4], strokeWidth=2)
        .encode(x="g:Q")
    )
    st.altair_chart(margin_chart + zero_line, width="stretch")
    st.caption(
        "Red simulations are on the failure side of the simple limit state. Change the "
        "mean, uncertainty, pressure, or sample count and observe the result."
    )

    st.link_button(
        "Continue to the full Analysis Lab",
        "/analysis-lab",
        icon=":material/science:",
        width="stretch",
    )

    _checkpoint(
        "If 5 of 1,000 simulations have g ≤ 0, what is the estimated POF?",
        ["0.0005", "0.005", "0.05"],
        "0.005",
        "book_check_probability",
    )


def chapter_quiz() -> None:
    st.header("Knowledge check")
    st.write("Answer all six questions, then check your score.")

    questions = [
        (
            "1. What is stress?",
            ["Force divided by area", "Area divided by force", "Pressure multiplied by volume"],
            "Force divided by area",
        ),
        (
            "2. In a simple thin-walled pipe, which pressure stress is larger?",
            ["Hoop stress", "Longitudinal stress", "They are always equal"],
            "Hoop stress",
        ),
        (
            "3. Which simple dimensions describe a crack in this book?",
            ["Length and depth", "Length, width, and depth", "Diameter only"],
            "Length and depth",
        ),
        (
            "4. What does g ≤ 0 mean in the learning model?",
            ["The limit state is reached", "Uncertainty is zero", "The model is invalid"],
            "The limit state is reached",
        ),
        (
            "5. What does CorLAS compare in the simple explanation?",
            ["Flow and fracture checks", "Cost and revenue", "Length and width only"],
            "Flow and fracture checks",
        ),
        (
            "6. What is a Monte Carlo POF estimate?",
            [
                "Failed simulations divided by all simulations",
                "Mean crack depth divided by wall thickness",
                "Failure pressure divided by operating pressure",
            ],
            "Failed simulations divided by all simulations",
        ),
    ]

    answers: list[str | None] = []
    for index, (question, options, _) in enumerate(questions):
        answers.append(st.radio(question, options, index=None, key=f"book_final_{index}"))

    if st.button("Check my answers", type="primary", width="stretch"):
        score = sum(
            answer == correct
            for answer, (_, _, correct) in zip(answers, questions)
        )
        if any(answer is None for answer in answers):
            st.warning("Please answer every question before checking the final score.")
        elif score >= 5:
            st.success(f"Score: {score}/6 — strong foundation. You are ready for the Analysis Lab.")
        elif score >= 3:
            st.info(f"Score: {score}/6 — good start. Review the chapters you found difficult.")
        else:
            st.info(f"Score: {score}/6 — return to the first chapters and take one concept at a time.")

    st.link_button(
        "Open the Analysis Lab",
        "/analysis-lab",
        icon=":material/science:",
        width="stretch",
    )


CHAPTER_RENDERERS = (
    chapter_welcome,
    chapter_mechanics,
    chapter_pipe_stress,
    chapter_defect_shapes,
    chapter_defects_on_pipe,
    chapter_limit_states,
    chapter_consequences,
    chapter_corlas,
    chapter_probability,
    chapter_quiz,
)


render_project_hero(
    "Undergraduate learning book",
    "Pipeline Mechanics, Defects, Failure and Risk",
    "A step-by-step path from basic mechanics to probability of failure, with interactive examples and short checks.",
)

if "book_chapter_selector" not in st.session_state:
    st.session_state.book_chapter_selector = 0

with st.sidebar:
    st.header("Learning Book")
    chapter_index = st.radio(
        "Chapters",
        options=list(range(len(CHAPTERS))),
        format_func=lambda index: f"{index + 1}. {CHAPTERS[index]}",
        key="book_chapter_selector",
    )
    st.progress(
        (chapter_index + 1) / len(CHAPTERS),
        text=f"Chapter {chapter_index + 1} of {len(CHAPTERS)}",
    )
    st.caption("External mechanics resources")
    st.link_button("Statics book ↗", STATICS_URL, width="stretch")
    st.link_button("Solid mechanics book ↗", SOLID_MECHANICS_URL, width="stretch")

st.markdown(
    """
    <div class="notice"><strong>Learning use only.</strong> Equations, scores, and
    visualizations in this book introduce concepts. They are not operating criteria
    and do not replace engineering review, validated models, standards, or regulations.</div>
    """,
    unsafe_allow_html=True,
)

CHAPTER_RENDERERS[chapter_index]()

st.divider()
previous_col, position_col, next_col = st.columns([1, 2, 1])
with previous_col:
    st.button(
        "← Previous",
        disabled=chapter_index == 0,
        on_click=_go_to_chapter,
        args=(chapter_index - 1,),
        width="stretch",
    )
with position_col:
    st.markdown(
        f"<p style='text-align:center'><strong>{chapter_index + 1} / {len(CHAPTERS)}</strong><br>"
        f"{CHAPTERS[chapter_index]}</p>",
        unsafe_allow_html=True,
    )
with next_col:
    st.button(
        "Next →",
        disabled=chapter_index == len(CHAPTERS) - 1,
        on_click=_go_to_chapter,
        args=(chapter_index + 1,),
        width="stretch",
    )
