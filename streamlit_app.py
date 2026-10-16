#!/usr/bin/env python3
"""Entrypoint for the standalone ALIRIM Education application."""

from importlib import reload

import streamlit as st

import platform_ui


# Keep shared UI components current when Streamlit Cloud hot-reloads the app.
platform_ui = reload(platform_ui)


st.set_page_config(
    page_title="ALIRIM Education | Pipeline Integrity",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
platform_ui.apply_global_style()

introduction = st.Page(
    "introduction.py",
    title="Introduction",
    icon=":material/home:",
    default=True,
)
learning_book = st.Page(
    "education/book.py",
    title="Learning Book",
    icon=":material/menu_book:",
    url_path="education",
)
analysis_lab = st.Page(
    "education/tutorial.py",
    title="Analysis Lab",
    icon=":material/science:",
    url_path="analysis-lab",
)
team = st.Page(
    "team.py",
    title="Team",
    icon=":material/groups:",
    url_path="team",
)

navigation = st.navigation(
    {
        "ALIRIM Education": [introduction, learning_book, analysis_lab],
        "About": [team],
    }
)
navigation.run()
