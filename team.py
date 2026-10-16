"""Team and research materials for the standalone education application."""

import streamlit as st

from platform_ui import editable_markdown, render_project_hero, render_team


render_project_hero(
    "Research record and resources",
    "Publications, Documentation and Team",
    "The same team profiles, research outputs, and supporting materials presented in the main ALIRIM platform.",
)

st.markdown("## Team")
render_team(show_contacts=True)

st.markdown(
    editable_markdown(
        "PUBLICATIONS.md",
        "Add publications in `content/PUBLICATIONS.md`.",
    )
)

st.divider()
st.markdown(
    editable_markdown(
        "DOCUMENTATION.md",
        "Add documentation in `content/DOCUMENTATION.md`.",
    )
)

st.markdown(
    """
    ## Education purpose

    We are developing this app step by step with feedback from university lecturers,
    pipeline-integrity experts, students, and early-career learners.
    """
)
