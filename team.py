"""Team page for the standalone ALIRIM Education application."""

import streamlit as st

from platform_ui import render_project_hero, render_team


render_project_hero(
    "About the project",
    "Team",
    "ALIRIM Education is developed at the University of Alberta as a teaching-focused extension of pipeline integrity research.",
)

st.markdown("## Project team")
render_team(show_contacts=True)

st.markdown(
    """
    ### Purpose

    We are developing this app step by step with feedback from university lecturers,
    pipeline-integrity experts, students, and early-career learners.
    """
)
