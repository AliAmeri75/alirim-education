"""Introduction page for the standalone ALIRIM Education application."""

import streamlit as st

from platform_ui import (
    editable_markdown,
    render_education_module_choices,
    render_learning_cards,
    render_project_hero,
)


render_project_hero(
    "ALIRIM Education",
    "Learn Pipeline Integrity Through Guided Examples",
    "A simple learning environment for exploring how pipeline cracks, uncertainty, and operating conditions affect integrity decisions.",
)

st.markdown(editable_markdown("INTRODUCTION.md", "Add the introduction in `content/INTRODUCTION.md`."))

st.markdown("## Start with three simple steps")
render_learning_cards(
    [
        ("Learn one idea", "Begin with a short explanation and a simple engineering example."),
        ("Explore the model", "Change the inputs and observe how the visual result responds."),
        ("Check understanding", "Answer a quick question before moving to the next concept."),
    ],
    label="Step",
)

st.markdown("## Choose your learning mode")
render_education_module_choices()

st.markdown(
    """
    <div class="notice"><strong>Learning use only.</strong> This educational app is a
    teaching prototype. Its outputs do not replace engineering review, applicable
    codes, or an operator's integrity-management procedures.</div>
    """,
    unsafe_allow_html=True,
)
