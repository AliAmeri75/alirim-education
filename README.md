# ALIRIM Education

A standalone Streamlit application for teaching introductory pipeline-integrity
concepts through guided examples.

## Pages

- **Introduction** — purpose, audience, and learning path.
- **Educational Module** — deterministic failure-pressure-ratio and probabilistic
  probability-of-failure exercises.
- **Team** — project team, profiles, and contact information.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

Create a Streamlit Community Cloud app using:

- Repository: `AliAmeri75/alirim-education`
- Branch: `main`
- Main file: `streamlit_app.py`

The educational exercises are classroom demonstrations. They do not replace
applicable codes, validated engineering models, or professional review.
