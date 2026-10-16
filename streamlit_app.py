#!/usr/bin/env python3
"""Entrypoint for the standalone ALIRIM Education application."""

import streamlit as st

from platform_ui import apply_global_style


st.set_page_config(
    page_title="ALIRIM Education | Pipeline Integrity",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_global_style()

introduction = st.Page(
    "introduction.py",
    title="Introduction",
    icon=":material/home:",
    default=True,
)
educational_module = st.Page(
    "education/tutorial.py",
    title="Educational Module",
    icon=":material/school:",
    url_path="education",
)
team = st.Page(
    "team.py",
    title="Team",
    icon=":material/groups:",
    url_path="team",
)

navigation = st.navigation(
    {
        "ALIRIM Education": [introduction, educational_module],
        "About": [team],
    }
)
navigation.run()
