"""Introduction page for the standalone ALIRIM Education application."""

import streamlit as st

from platform_ui import editable_markdown, render_project_hero


render_project_hero(
    "ALIRIM Education",
    "Learn Pipeline Integrity Through Guided Examples",
    "A simple learning environment for exploring how pipeline cracks, uncertainty, and operating conditions affect integrity decisions.",
)

st.markdown(editable_markdown("INTRODUCTION.md", "Add the introduction in `content/INTRODUCTION.md`."))

st.markdown("## Start with three simple steps")
step_one, step_two, step_three = st.columns(3)
with step_one:
    st.markdown("### 1. Choose inputs")
    st.write("Set pipe, material, crack, and operating-pressure values.")
with step_two:
    st.markdown("### 2. Explore results")
    st.write("See how crack depth, crack length, and uncertainty change the result.")
with step_three:
    st.markdown("### 3. Check learning")
    st.write("Interpret the figures and answer a short knowledge-check question.")

start_col, lab_col = st.columns(2)
with start_col:
    st.page_link(
        "education/book.py",
        label="Start the Learning Book",
        icon=":material/menu_book:",
        width="stretch",
    )
with lab_col:
    st.page_link(
        "education/tutorial.py",
        label="Open the Analysis Lab",
        icon=":material/science:",
        width="stretch",
    )

st.markdown(
    """
    <div class="notice"><strong>Learning use only.</strong> This educational app is a
    teaching prototype. Its outputs do not replace engineering review, applicable
    codes, or an operator's integrity-management procedures.</div>
    """,
    unsafe_allow_html=True,
)
