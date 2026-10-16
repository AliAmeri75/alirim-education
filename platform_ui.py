"""Shared visual components for the research platform."""

from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
ASSET_DIR = APP_DIR / "assets"
CONTENT_DIR = APP_DIR / "content"
MOHAMMADALI_PROFILE_URL = "https://www.linkedin.com/in/mohammad-ali-ameri"
YONG_LI_PROFILE_URL = "https://apps.ualberta.ca/directory/person/yong9"


def data_uri(path: Path) -> str:
    """Encode a local image so it renders reliably on Community Cloud."""

    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def editable_markdown(filename: str, fallback: str) -> str:
    """Load public page copy from a Markdown content file."""

    path = CONTENT_DIR / filename
    return path.read_text(encoding="utf-8") if path.exists() else fallback


def apply_global_style() -> None:
    engineering_pattern = """<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
      <defs>
        <pattern id="grid" width="56" height="56" patternUnits="userSpaceOnUse">
          <path d="M56 0H0V56" fill="none" stroke="#155987" stroke-width="0.7" opacity="0.18"/>
        </pattern>
      </defs>
      <rect width="1400" height="900" fill="url(#grid)" opacity="0.34"/>
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M-80 180C180 40 360 310 620 170S1030 60 1480 250" stroke="#155987" stroke-width="3" opacity="0.10"/>
        <path d="M-80 194C180 54 360 324 620 184S1030 74 1480 264" stroke="#275d38" stroke-width="1.4" opacity="0.09"/>
        <path d="M90 720C310 470 510 820 760 610S1120 440 1450 660" stroke="#275d38" stroke-width="4" opacity="0.08"/>
        <path d="M90 736C310 486 510 836 760 626S1120 456 1450 676" stroke="#155987" stroke-width="1.5" opacity="0.08"/>
        <path d="M170 120L410 320 660 210 930 390 1210 220" stroke="#155987" stroke-width="1.2" opacity="0.10"/>
        <path d="M250 590L510 430 780 690 1080 520 1320 590" stroke="#275d38" stroke-width="1.2" opacity="0.09"/>
      </g>
      <g fill="#ffffff" stroke="#155987" stroke-width="2" opacity="0.13">
        <circle cx="170" cy="120" r="8"/><circle cx="410" cy="320" r="8"/><circle cx="660" cy="210" r="8"/>
        <circle cx="930" cy="390" r="8"/><circle cx="1210" cy="220" r="8"/><circle cx="250" cy="590" r="8"/>
        <circle cx="510" cy="430" r="8"/><circle cx="780" cy="690" r="8"/><circle cx="1080" cy="520" r="8"/>
      </g>
      <g fill="#155987" opacity="0.055" font-family="Georgia,serif" font-size="31">
        <text x="85" y="410">σₕ = pD / 2t</text><text x="1050" y="470">g(X) = R − S</text>
        <text x="740" y="115">Pᶠ ≈ n(g≤0) / N</text><text x="410" y="820">Risk = Likelihood × Consequence</text>
      </g>
    </svg>"""
    engineering_pattern_uri = base64.b64encode(
        engineering_pattern.encode("utf-8")
    ).decode("ascii")
    style = """
        <style>
        :root {
            --ua-green: #275d38; --ua-dark: #173d27; --ua-gold: #ffdb05;
            --alirim-blue: #155987; --alirim-navy: #0f426d;
            --ink: #14251c; --muted: #5b6961; --line: #d8e2da;
        }
        .stApp {
            background-color: #f7faf8;
            background-image:
                radial-gradient(circle at 88% 8%, rgba(21,89,135,.10), transparent 29rem),
                radial-gradient(circle at 7% 36%, rgba(255,219,5,.08), transparent 24rem),
                radial-gradient(circle at 78% 80%, rgba(39,93,56,.08), transparent 28rem),
                url("data:image/svg+xml;base64,__ENGINEERING_PATTERN__");
            background-size: auto, auto, auto, 1400px 900px;
            background-attachment: fixed;
        }
        [data-testid="stHeader"] { background: rgba(247,250,248,.78);
            backdrop-filter: blur(13px); border-bottom: 1px solid rgba(39,93,56,.08); }
        [data-testid="stSidebar"] { background: rgba(242,247,243,.93);
            backdrop-filter: blur(14px); border-right: 1px solid rgba(39,93,56,.12);
            box-shadow: 8px 0 30px rgba(20,49,32,.035); }
        .block-container { max-width: 1200px; padding-top: 1.35rem; padding-bottom: 4rem; }
        .platform-hero, .project-hero {
            position: relative; overflow: hidden; padding: 1.55rem 1.75rem 1.7rem;
            background: linear-gradient(118deg,rgba(255,255,255,.97),rgba(243,249,246,.91));
            border: 1px solid rgba(39,93,56,.18);
            border-top: 7px solid var(--ua-green); border-radius: 20px;
            box-shadow: 0 18px 46px rgba(20,49,32,.10);
            backdrop-filter: blur(10px);
        }
        .platform-hero::before, .project-hero::before {
            content: ""; position: absolute; inset: 0; pointer-events: none;
            background-image: linear-gradient(rgba(21,89,135,.045) 1px,transparent 1px),
                linear-gradient(90deg,rgba(21,89,135,.045) 1px,transparent 1px);
            background-size: 34px 34px;
            mask-image: linear-gradient(90deg,transparent 36%,#000 100%);
        }
        .platform-hero::after, .project-hero::after {
            content: ""; position: absolute; width: 190px; height: 190px;
            right: -72px; top: -92px; border-radius: 50%;
            background: radial-gradient(circle,rgba(255,219,5,.34) 0 38%,transparent 39% 58%,rgba(21,89,135,.11) 59% 61%,transparent 62%);
            opacity: .78;
        }
        .platform-hero > *, .project-hero > * { position: relative; z-index: 1; }
        .brand-logo-ua, .brand-logo-alirim { box-sizing: border-box; display: inline-block;
            vertical-align: middle; height: 112px; object-fit: contain; margin-bottom: 1.15rem;
            padding: .65rem 1rem; background: #fff;
            border: 1px solid #dce5df; border-radius: 14px;
            box-shadow: 0 5px 16px rgba(20,49,32,.06); }
        .brand-logo-ua { width: 360px; }
        .brand-logo-alirim { width: 180px; margin-left: 1rem; padding: .15rem;
            object-fit: cover; object-position: center; }
        .brand-logo-compact { height: 84px; margin-bottom: .9rem; }
        .brand-logo-ua.brand-logo-compact { width: 285px; }
        .brand-logo-alirim.brand-logo-compact { width: 135px; margin-left: .75rem; padding: .1rem; }
        .eyebrow { color: var(--ua-green); font-weight: 900; letter-spacing: .11em;
            text-transform: uppercase; font-size: .76rem; }
        .platform-hero h1, .project-hero h1 { color: var(--ink); font-family: Georgia, serif;
            font-weight: 500; font-size: clamp(2rem,4vw,3.35rem); line-height: 1.06;
            margin: .38rem 0 .66rem; max-width: 900px; }
        .project-hero h1 { color: transparent;
            background: linear-gradient(90deg,var(--ink) 0%,var(--alirim-blue) 52%,var(--ua-green) 100%);
            background-clip: text; -webkit-background-clip: text; }
        .platform-hero h1 { color: var(--alirim-navy); font-weight: 800;
            letter-spacing: .025em; margin-bottom: .15rem; }
        .platform-name { color: var(--ink); font-family: Georgia, serif; font-weight: 700;
            font-size: clamp(1.18rem,2.2vw,1.65rem); line-height: 1.25;
            margin: 0 0 .8rem; max-width: 850px; }
        .platform-hero p, .project-hero p { color: var(--muted); font-size: 1.02rem;
            max-width: 850px; margin: 0; }
        .credit-line { color: var(--ink); font-size: .92rem; font-weight: 800; margin-top: 1rem; }
        .credit-line a { color: var(--ua-green); text-decoration: none; }
        .credit-line a:hover { text-decoration: underline; }
        .people-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr));
            gap: 1rem; margin: 1.1rem 0 1.7rem; }
        .person-card { display: flex; align-items: center; gap: 1rem; padding: 1rem;
            background: #fff; border: 1px solid var(--line); border-radius: 16px;
            box-shadow: 0 6px 18px rgba(20,49,32,.05); }
        .person-card img { width: 100px; height: 100px; flex: 0 0 100px; object-fit: cover;
            border-radius: 50%; border: 4px solid #fff; outline: 3px solid var(--ua-green); }
        .person-card h3 { color: var(--ink); font-size: 1.13rem; margin: 0 0 .25rem; }
        .person-card p { color: var(--muted); margin: 0; font-size: .9rem; line-height: 1.38; }
        .person-card .person-contact { margin-top: .45rem; }
        .person-card a { color: var(--ua-green); font-weight: 800; text-decoration: none; }
        .person-card a:hover { text-decoration: underline; }
        .section-label { color: var(--ua-green); font-size: .78rem; font-weight: 900;
            letter-spacing: .1em; text-transform: uppercase; margin-top: 1.5rem; }
        .app-grid { display: grid; grid-template-columns: repeat(3,minmax(0,1fr));
            gap: 1rem; margin: 1rem 0 1.8rem; }
        .learning-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr));
            margin: 1rem 0 1.8rem; }
        .learning-card { min-height: 0; border-top-color: var(--alirim-blue);
            background: linear-gradient(135deg,#fff 0%,#edf6fb 100%); }
        .learning-card .app-number { width: auto; padding: 0 .8rem;
            color: #fff; background: var(--alirim-blue); }
        .app-card { display: flex; flex-direction: column; min-height: 265px; padding: 1.2rem;
            color: var(--ink); background: #fff;
            border: 1px solid var(--line); border-top: 5px solid var(--ua-green);
            border-radius: 17px; box-shadow: 0 8px 24px rgba(20,49,32,.07);
            transition: transform .18s ease, box-shadow .18s ease; }
        .app-card:hover { transform: translateY(-4px); box-shadow: 0 15px 32px rgba(20,49,32,.14); }
        .app-card-main { display: flex; flex: 1; flex-direction: column;
            color: var(--ink) !important; text-decoration: none !important; }
        .app-number { display: inline-grid; place-items: center; width: 46px; height: 46px;
            color: var(--ua-dark); background: var(--ua-gold); border-radius: 13px;
            font-weight: 950; font-size: 1.05rem; }
        .app-card h3 { font-size: 1.25rem; line-height: 1.2; margin: 1rem 0 .55rem; }
        .app-card p { color: var(--muted); font-size: .9rem; line-height: 1.48; margin: 0; }
        .app-link { margin-top: auto; padding-top: 1rem; color: var(--ua-green);
            font-weight: 900; font-size: .92rem; }
        .publication-link { width: fit-content; text-decoration: none !important; }
        .publication-link:hover { text-decoration: underline !important; }
        .app-status { color: var(--muted); }
        .external-cta {
            display: flex; align-items: center; justify-content: space-between; gap: 1rem;
            margin: 1.25rem 0; padding: 1.15rem 1.3rem; color: #fff !important;
            text-decoration: none !important; background: linear-gradient(120deg,#1f4d30,#173d27);
            border: 3px solid var(--ua-gold); border-radius: 17px;
            box-shadow: 0 12px 28px rgba(20,49,32,.18); }
        .external-cta strong { display: block; color: #fff; font-size: 1.32rem; }
        .external-cta span { color: #dfece2; font-size: .9rem; }
        .external-cta-copy { display: block; flex: 1; }
        .external-cta-detail { display: block; margin-top: .2rem; }
        .external-cta b { color: var(--ua-gold); font-size: 1.8rem; }
        .inspection-cta, .illustrated-cta {
            display: grid; grid-template-columns: 86px minmax(0,1fr) 260px;
            align-items: center; gap: 1.25rem; margin: 1.45rem 0 1.2rem;
            padding: 1.15rem 1.3rem; color: #fff !important;
            text-decoration: none !important;
            background: linear-gradient(120deg,#1f4d30 0%,var(--ua-green) 58%,#173d27 100%);
            border: 3px solid var(--ua-gold); border-radius: 18px;
            box-shadow: 0 14px 30px rgba(20,49,32,.2);
            transition: transform .18s ease, box-shadow .18s ease;
        }
        .inspection-cta:hover, .illustrated-cta:hover { transform: translateY(-3px);
            box-shadow: 0 18px 38px rgba(20,49,32,.28); }
        .calendar-icon { display: grid; place-items: center; width: 76px; height: 76px;
            color: var(--ua-green); background: var(--ua-gold); border-radius: 18px;
            box-shadow: inset 0 0 0 3px rgba(255,255,255,.55); }
        .calendar-icon svg { width: 46px; height: 46px; }
        .cta-kicker { display: block; color: #fff3a1; font-size: .76rem; font-weight: 900;
            letter-spacing: .12em; text-transform: uppercase; margin-bottom: .18rem; }
        .cta-title { display: block; color: #fff; font-size: clamp(1.25rem,2.5vw,1.72rem);
            font-weight: 900; line-height: 1.13; }
        .cta-detail { display: block; color: #e2eee5; font-size: .92rem; margin-top: .36rem; }
        .cta-arrow { color: var(--ua-gold); font-size: 1.35em; padding-left: .25rem; }
        .ili-picture { width: 100%; max-height: 118px; object-fit: contain; }
        .notice { margin: 1rem 0; padding: .9rem 1rem; color: #405047; background: #eef4ef;
            border-left: 4px solid var(--ua-green); border-radius: 6px; }
        [data-testid="stMetric"] { padding: .8rem 1rem; background: rgba(255,255,255,.86);
            border: 1px solid rgba(39,93,56,.12); border-radius: 14px;
            box-shadow: 0 7px 20px rgba(20,49,32,.045); backdrop-filter: blur(7px); }
        [data-testid="stAlert"] { border-radius: 13px; box-shadow: 0 7px 20px rgba(20,49,32,.04); }
        [data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"],
        [data-testid="stDataFrame"] { overflow: hidden; border: 1px solid rgba(39,93,56,.11);
            border-radius: 15px; background: rgba(255,255,255,.88);
            box-shadow: 0 9px 24px rgba(20,49,32,.055); }
        .stButton > button, .stLinkButton > a { border-radius: 11px;
            transition: transform .16s ease, box-shadow .16s ease; }
        .stButton > button:hover, .stLinkButton > a:hover { transform: translateY(-1px);
            box-shadow: 0 7px 18px rgba(20,49,32,.11); }
        h2, h3 { letter-spacing: -.015em; }
        @media (max-width: 850px) { .app-grid, .learning-grid { grid-template-columns: 1fr; } }
        @media (max-width: 700px) {
            .people-grid { grid-template-columns: 1fr; }
            .person-card img { width: 84px; height: 84px; flex-basis: 84px; }
            .platform-hero, .project-hero { padding: 1.2rem; }
            .brand-logo-ua, .brand-logo-ua.brand-logo-compact {
                width: calc(100% - 128px); height: 88px; padding: .45rem .6rem; }
            .brand-logo-alirim, .brand-logo-alirim.brand-logo-compact {
                width: 118px; height: 88px; margin-left: .5rem; padding: .1rem;
                object-fit: cover; object-position: center; }
            .inspection-cta, .illustrated-cta {
                grid-template-columns: 64px minmax(0,1fr); gap: .85rem;
                padding: 1rem; }
            .calendar-icon { width: 58px; height: 58px; border-radius: 14px; }
            .calendar-icon svg { width: 34px; height: 34px; }
            .ili-picture { grid-column: 1 / -1; max-height: 90px; }
        }
        </style>
        """
    st.markdown(
        style.replace("__ENGINEERING_PATTERN__", engineering_pattern_uri),
        unsafe_allow_html=True,
    )


def brand_logos(*, compact: bool = False) -> str:
    """Return the paired ALIRIM and University of Alberta brand marks."""

    ua_logo = data_uri(ASSET_DIR / "university_of_alberta_logo.svg")
    alirim_logo = data_uri(ASSET_DIR / "alirim_logo.jpeg")
    compact_class = " brand-logo-compact" if compact else ""
    return (
        f'<img class="brand-logo-ua{compact_class}" src="{ua_logo}" '
        'alt="University of Alberta">'
        f'<img class="brand-logo-alirim{compact_class}" src="{alirim_logo}" '
        'alt="ALIRIM">'
    )


def render_platform_hero() -> None:
    logos = brand_logos()
    hero = (
        '<section class="platform-hero">'
        f'{logos}'
        '<div class="eyebrow">Pipeline Integrity Research Platform</div>'
        '<h1>ALIRIM</h1>'
        '<div class="platform-name">Asset Lifecycle Intelligence for Risk &amp; '
        'Integrity Management</div>'
        '<p>A unified gateway to reliability, inspection, maintenance, and '
        'value-of-information tools developed from doctoral research.</p>'
        '<div class="credit-line">Developed by '
        f'<a href="{MOHAMMADALI_PROFILE_URL}" target="_blank" rel="noopener noreferrer">'
        'Mohammadali Ameri</a> and '
        f'<a href="{YONG_LI_PROFILE_URL}" target="_blank" rel="noopener noreferrer">'
        'Dr. Yong Li</a></div>'
        '</section>'
    )
    st.markdown(hero, unsafe_allow_html=True)


def render_team(show_contacts: bool = False) -> None:
    mohammadali = data_uri(ASSET_DIR / "mohammadali_ameri.png")
    yong = data_uri(ASSET_DIR / "yong_li.png")
    mohammadali_contact = (
        '<p class="person-contact"><a href="mailto:amerifar@ualberta.ca">'
        'amerifar@ualberta.ca</a><br>'
        f'<a href="{MOHAMMADALI_PROFILE_URL}" target="_blank" '
        'rel="noopener noreferrer">LinkedIn profile</a></p>'
        if show_contacts
        else ""
    )
    yong_contact = (
        '<p class="person-contact"><a href="mailto:yong9@ualberta.ca">'
        'yong9@ualberta.ca</a><br>'
        f'<a href="{YONG_LI_PROFILE_URL}" '
        'target="_blank" rel="noopener noreferrer">University profile</a></p>'
        if show_contacts
        else ""
    )
    st.markdown(
        f"""
        <section class="people-grid" aria-label="Platform developers">
          <article class="person-card">
            <img src="{mohammadali}" alt="Mohammadali Ameri">
            <div><h3><a href="{MOHAMMADALI_PROFILE_URL}" target="_blank" rel="noopener noreferrer">Mohammadali Ameri</a></h3><p>PhD researcher and developer<br>University of Alberta</p>{mohammadali_contact}</div>
          </article>
          <article class="person-card">
            <img src="{yong}" alt="Yong Li">
            <div><h3><a href="{YONG_LI_PROFILE_URL}" target="_blank" rel="noopener noreferrer">Dr. Yong Li</a></h3><p>Associate Professor and co-developer<br>University of Alberta</p>{yong_contact}</div>
          </article>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_project_hero(kicker: str, title: str, description: str) -> None:
    logos = brand_logos(compact=True)
    hero = (
        '<section class="project-hero">'
        f'{logos}'
        f'<div class="eyebrow">{html.escape(kicker)}</div>'
        f'<h1>{html.escape(title)}</h1>'
        f'<p>{html.escape(description)}</p>'
        '</section>'
    )
    st.markdown(hero, unsafe_allow_html=True)


def render_external_cta(
    url: str,
    title: str,
    detail: str,
    *,
    illustration: str,
    illustration_alt: str,
    feature_icon: str = "calendar",
) -> None:
    """Render one illustrated link to an independently deployed application."""

    safe_url = html.escape(url, quote=True)
    safe_title = html.escape(title)
    safe_detail = html.escape(detail)
    safe_alt = html.escape(illustration_alt, quote=True)
    aria_label = html.escape(f"{title} (opens in a new tab)", quote=True)
    illustration_uri = data_uri(ASSET_DIR / illustration)
    if feature_icon == "ai":
        feature_svg = (
            '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M15 18c0-7 5-12 12-12 5 0 9 3 11 7 5 1 8 5 8 10 0 4-2 8-6 10v8H18v-7c-5-2-8-6-8-11 0-2 1-4 2-6Z" '
            'fill="white" stroke="currentColor" stroke-width="3"/>'
            '<circle cx="24" cy="22" r="3" fill="currentColor"/>'
            '<circle cx="34" cy="22" r="3" fill="currentColor"/>'
            '<path d="M24 31c3 3 7 3 10 0M28 6V2M15 12l-4-3M40 12l4-3" '
            'stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
        )
    else:
        feature_svg = (
            '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="7" y="10" width="34" height="31" rx="5" fill="white" '
            'stroke="currentColor" stroke-width="3"/>'
            '<path d="M7 19h34M16 6v8M32 6v8" stroke="currentColor" '
            'stroke-width="3.5" stroke-linecap="round"/>'
            '<path d="m16 30 5 5 11-12" stroke="currentColor" stroke-width="3.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>'
        )
    cta = (
        f'<a class="illustrated-cta" href="{safe_url}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="{aria_label}">'
        f'<span class="calendar-icon" aria-hidden="true">{feature_svg}</span>'
        f'<span><span class="cta-kicker">Start your analysis</span>'
        f'<strong class="cta-title">{safe_title}<span class="cta-arrow">↗</span></strong>'
        f'<span class="cta-detail">{safe_detail}</span></span>'
        f'<img class="ili-picture" src="{illustration_uri}" alt="{safe_alt}"></a>'
    )
    st.markdown(cta, unsafe_allow_html=True)


def render_inspection_cta(url: str) -> None:
    """Render the illustrated launch card used by the inspection introduction."""

    ili_illustration = data_uri(ASSET_DIR / "ili_pipeline.svg")
    safe_url = html.escape(url, quote=True)
    st.markdown(
        f"""
        <a class="inspection-cta" href="{safe_url}" target="_blank"
           rel="noopener noreferrer"
           aria-label="Open the inspection, excavation, and VoI simulation in a new tab">
          <span class="calendar-icon" aria-hidden="true">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="7" y="10" width="34" height="31" rx="5" fill="white"
                    stroke="currentColor" stroke-width="3"/>
              <path d="M7 19h34M16 6v8M32 6v8" stroke="currentColor"
                    stroke-width="3.5" stroke-linecap="round"/>
              <path d="m16 30 5 5 11-12" stroke="currentColor" stroke-width="3.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span>
            <span class="cta-kicker">Start your analysis</span>
            <strong class="cta-title">Open the Planning and VoI Simulation<span
              class="cta-arrow">↗</span></strong>
            <span class="cta-detail">Compare prior excavation and ILI-informed schedules,
              then review their lifecycle costs and VoI.</span>
          </span>
          <img class="ili-picture" src="{ili_illustration}"
               alt="Illustration of an inline inspection tool inside a pipeline">
        </a>
        """,
        unsafe_allow_html=True,
    )
