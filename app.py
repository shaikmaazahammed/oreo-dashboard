import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="The Great Oreo Takeover",
    page_icon="🍪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0a;
    color: #f5f0e8;
}

.block-container { padding: 2rem 2.5rem; max-width: 1400px; }

h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #1a0a00 0%, #3d1a00 40%, #000000 100%);
    border: 1px solid #c8a96e44;
    border-radius: 12px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●';
    position: absolute; top: 0; left: 0; right: 0;
    font-size: 8px; color: #c8a96e11; letter-spacing: 4px;
    line-height: 1.8; padding: 1rem; word-break: break-all;
    pointer-events: none;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem; letter-spacing: 6px;
    background: linear-gradient(90deg, #ffffff, #c8a96e, #ffffff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1;
}
.hero-subtitle { color: #c8a96e; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.5rem; }
.hero-tags { display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap; }
.hero-tag {
    background: #c8a96e22; border: 1px solid #c8a96e55;
    color: #c8a96e; padding: 0.3rem 0.9rem; border-radius: 4px;
    font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase;
}

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: #111111; border: 1px solid #2a2a2a;
    border-radius: 10px; padding: 1.2rem 1.5rem;
    flex: 1; min-width: 150px;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #c8a96e66; }
.metric-label { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #666; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: #c8a96e; line-height: 1; }
.metric-sub { font-size: 0.72rem; color: #555; margin-top: 0.3rem; }

/* Section headers */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem; letter-spacing: 3px; color: #ffffff;
    border-left: 4px solid #c8a96e; padding-left: 1rem;
    margin: 2rem 0 1rem;
}

/* Platform badge colors */
.badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:600; letter-spacing:0.5px; }
.badge-tiktok    { background:#1a1a2e; color:#69c9d0; border:1px solid #69c9d055; }
.badge-instagram { background:#2a0a1f; color:#e1306c; border:1px solid #e1306c55; }
.badge-facebook  { background:#0a1a2e; color:#4267b2; border:1px solid #4267b255; }
.badge-youtube   { background:#1a0a0a; color:#ff0000; border:1px solid #ff000055; }
.badge-ugc       { background:#1a1a0a; color:#f0c040; border:1px solid #f0c04055; }
.badge-boost     { background:#0a1a0a; color:#4caf50; border:1px solid #4caf5055; }

/* Phase pill */
.phase-pill {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase; font-weight: 600;
}
.phase-1 { background:#c8a96e22; color:#c8a96e; border:1px solid #c8a96e44; }
.phase-2 { background:#69c9d022; color:#69c9d0; border:1px solid #69c9d044; }
.phase-3 { background:#e1306c22; color:#e1306c; border:1px solid #e1306c44; }

/* Status badge */
.status-planned  { color: #888; font-size: 0.72rem; }
.status-analysis { color: #c8a96e; font-size: 0.72rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid #1f1f1f;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #222; border-radius: 8px; overflow: hidden; }

/* Divider */
hr { border-color: #1f1f1f !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #111; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #666; border-radius: 6px; padding: 6px 20px; font-size:0.8rem; letter-spacing:1px; text-transform:uppercase; }
.stTabs [aria-selected="true"] { background: #c8a96e !important; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = "oreo_content_calendar.xlsx"
    raw = pd.read_excel(path, sheet_name=None, header=None)

    # ── Content Calendar ─────────────────────────────────────────────────────
    cc = raw["Content Calendar"]
    df = cc.iloc[2:].copy()
    df.columns = ["Phase","Week","Day","Day of Week","Platform","Format","Content Description","Message Hook","Hashtag CTA","Budget Note","KPI Focus","Status"]
    df = df.reset_index(drop=True)
    df = df[df["Day"].notna()].copy()

    # forward-fill Phase and Week
    df["Phase"] = df["Phase"].fillna(method="ffill")
    df["Week"]  = df["Week"].fillna(method="ffill")

    # Clean Phase labels
    df["Phase"] = df["Phase"].astype(str).str.replace(r"\\n", " ", regex=True).str.strip()
    df["Week"]  = df["Week"].astype(str).str.replace(r"\\n", " ", regex=True).str.strip()
    df["Day"]   = df["Day"].astype(int)

    # ── KPI Tracker ──────────────────────────────────────────────────────────
    kk = raw["KPI Tracker"]
    kpi_df = kk.iloc[2:].copy()
    kpi_df.columns = ["KPI","Target","Week 1","Week 2","Week 3","Week 4","Week 5"]
    kpi_df = kpi_df[kpi_df["KPI"].notna() & ~kpi_df["KPI"].isin(["KPI","PRIMARY KPIs","SECONDARY KPIs"])].copy()
    kpi_df = kpi_df.reset_index(drop=True)

    # ── Budget Breakdown ─────────────────────────────────────────────────────
    bb = raw["Budget Breakdown"]
    # Platform rows: rows 8–12 (0-indexed)
    platform_df = pd.DataFrame({
        "Platform": ["TikTok","Instagram","Facebook + YouTube","Boosting / Creator Amplification"],
        "HUF":      [8_000_000, 7_000_000, 3_000_000, 2_000_000],
        "Share":    [40, 35, 15, 10],
    })
    funnel_df = pd.DataFrame({
        "Funnel":  ["Prospecting","Retargeting"],
        "HUF":     [18_000_000, 2_000_000],
        "Share":   [90, 10],
    })

    return df, kpi_df, platform_df, funnel_df

df, kpi_df, platform_df, funnel_df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:3px;color:#c8a96e;margin-bottom:1rem;'>🍪 OREO TAKEOVER</div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["📅 Content Calendar", "📊 KPI Tracker", "💰 Budget Breakdown"], label_visibility="collapsed")
    st.markdown("---")

    # Filters (only relevant on calendar page)
    if page == "📅 Content Calendar":
        st.markdown("<div style='font-size:0.7rem;letter-spacing:2px;color:#555;text-transform:uppercase;margin-bottom:0.5rem;'>Filters</div>", unsafe_allow_html=True)
        platforms = ["All"] + sorted(df["Platform"].dropna().unique().tolist())
        sel_platform = st.selectbox("Platform", platforms)

        phases = ["All"] + df["Phase"].dropna().unique().tolist()
        sel_phase = st.selectbox("Phase", phases)

        weeks = ["All"] + df["Week"].dropna().unique().tolist()
        sel_week = st.selectbox("Week", weeks)

        formats = ["All"] + sorted(df["Format"].dropna().unique().tolist())
        sel_format = st.selectbox("Format", formats)
    else:
        sel_platform = sel_phase = sel_week = sel_format = "All"

    st.markdown("---")
    st.markdown("<div style='font-size:0.65rem;color:#333;'>Hungary · 5 Weeks · 20M HUF</div>", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">THE GREAT OREO TAKEOVER</div>
  <div class="hero-subtitle">Content Calendar &amp; Campaign Dashboard</div>
  <div class="hero-tags">
    <span class="hero-tag">📍 Hungary</span>
    <span class="hero-tag">🎯 14–34 Year Olds</span>
    <span class="hero-tag">📅 5 Weeks</span>
    <span class="hero-tag">💰 20,000,000 HUF</span>
    <span class="hero-tag">🏷 Brand Awareness</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Page: Content Calendar ────────────────────────────────────────────────────
if page == "📅 Content Calendar":
    # Metrics row
    total_posts = len(df)
    paid_posts  = df["Budget Note"].str.contains("Paid", na=False).sum()
    organic     = df["Budget Note"].str.contains("Organic", na=False).sum()
    platforms_n = df["Platform"].nunique()

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="metric-label">Total Posts</div><div class="metric-value">{total_posts}</div><div class="metric-sub">Across 5 weeks</div></div>
      <div class="metric-card"><div class="metric-label">Paid Posts</div><div class="metric-value">{paid_posts}</div><div class="metric-sub">Paid distribution</div></div>
      <div class="metric-card"><div class="metric-label">Organic</div><div class="metric-value">{organic}</div><div class="metric-sub">Organic reach</div></div>
      <div class="metric-card"><div class="metric-label">Platforms</div><div class="metric-value">{platforms_n}</div><div class="metric-sub">TikTok, IG, FB, YT</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Apply filters
    filtered = df.copy()
    if sel_platform != "All": filtered = filtered[filtered["Platform"] == sel_platform]
    if sel_phase    != "All": filtered = filtered[filtered["Phase"] == sel_phase]
    if sel_week     != "All": filtered = filtered[filtered["Week"] == sel_week]
    if sel_format   != "All": filtered = filtered[filtered["Format"] == sel_format]

    tab1, tab2 = st.tabs(["📋  CALENDAR VIEW", "📈  PLATFORM ANALYSIS"])

    with tab1:
        st.markdown(f"<div style='font-size:0.78rem;color:#555;margin-bottom:1rem;'>Showing <b style='color:#c8a96e'>{len(filtered)}</b> posts</div>", unsafe_allow_html=True)

        PLATFORM_COLORS = {
            "TikTok": "badge-tiktok", "Instagram": "badge-instagram",
            "Facebook": "badge-facebook", "YouTube": "badge-youtube",
            "UGC/Creator": "badge-ugc", "Boost": "badge-boost",
        }
        PHASE_CLASSES = {
            "Phase 1 Teaser & Launch": "phase-1",
            "Phase 2 Scale & Amplify":  "phase-2",
            "Phase 3 Recap & Sustain":  "phase-3",
        }

        def phase_class(p):
            for k, v in PHASE_CLASSES.items():
                if "1" in p: return "phase-1"
                if "2" in p: return "phase-2"
                if "3" in p: return "phase-3"
            return "phase-1"

        def platform_badge(p):
            cls = PLATFORM_COLORS.get(str(p).strip(), "badge-boost")
            return f'<span class="badge {cls}">{p}</span>'

        current_week = None
        for _, row in filtered.iterrows():
            if row["Week"] != current_week:
                current_week = row["Week"]
                wlabel = str(current_week).replace("\\n", " ")
                st.markdown(f"<div class='section-header'>{wlabel}</div>", unsafe_allow_html=True)

            phase_lbl = str(row["Phase"]).replace("\\n"," ")
            pc = phase_class(phase_lbl)
            plat = platform_badge(row["Platform"])
            status_cls = "status-analysis" if str(row.get("Status","")).lower()=="analysis" else "status-planned"

            st.markdown(f"""
            <div style="background:#111;border:1px solid #222;border-radius:8px;padding:1rem 1.4rem;margin-bottom:0.6rem;display:flex;gap:1.5rem;align-items:flex-start;flex-wrap:wrap;">
              <div style="min-width:40px;text-align:center;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#c8a96e;line-height:1;">{row['Day']}</div>
                <div style="font-size:0.65rem;color:#555;text-transform:uppercase;">{row['Day of Week']}</div>
              </div>
              <div style="flex:1;min-width:200px;">
                <div style="margin-bottom:0.4rem;display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap;">
                  {plat}
                  <span style="font-size:0.72rem;color:#555;">{row['Format']}</span>
                  <span class="phase-pill {pc}">{phase_lbl}</span>
                </div>
                <div style="font-size:0.92rem;color:#e8e0d0;font-weight:500;margin-bottom:0.3rem;">{row['Content Description']}</div>
                <div style="font-size:0.8rem;color:#888;font-style:italic;">"{row['Message Hook']}"</div>
              </div>
              <div style="min-width:160px;text-align:right;">
                <div style="font-size:0.72rem;color:#c8a96e;margin-bottom:0.2rem;">{row['Hashtag CTA'] if pd.notna(row['Hashtag CTA']) else ''}</div>
                <div style="font-size:0.7rem;color:#555;margin-bottom:0.2rem;">{row['Budget Note'] if pd.notna(row['Budget Note']) else ''}</div>
                <div style="font-size:0.7rem;color:#444;">{row['KPI Focus'] if pd.notna(row['KPI Focus']) else ''}</div>
                <div class="{status_cls}">{row['Status'] if pd.notna(row['Status']) else ''}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            platform_counts = df["Platform"].value_counts().reset_index()
            platform_counts.columns = ["Platform", "Posts"]
            fig = px.bar(platform_counts, x="Platform", y="Posts",
                         color="Platform",
                         color_discrete_map={
                             "TikTok":"#69c9d0","Instagram":"#e1306c",
                             "Facebook":"#4267b2","YouTube":"#ff0000",
                             "UGC/Creator":"#f0c040","Boost":"#4caf50",
                         },
                         title="Posts by Platform")
            fig.update_layout(
                paper_bgcolor="#111", plot_bgcolor="#111",
                font_color="#888", title_font_color="#c8a96e",
                showlegend=False, margin=dict(t=40,b=0,l=0,r=0)
            )
            fig.update_xaxes(color="#555"); fig.update_yaxes(color="#555", gridcolor="#1f1f1f")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fmt_counts = df["Format"].value_counts().reset_index()
            fmt_counts.columns = ["Format", "Count"]
            fig2 = px.pie(fmt_counts, names="Format", values="Count",
                          title="Content Format Mix",
                          color_discrete_sequence=["#c8a96e","#69c9d0","#e1306c","#4267b2","#4caf50","#ff0000","#f0c040","#9c27b0"])
            fig2.update_layout(
                paper_bgcolor="#111", font_color="#888",
                title_font_color="#c8a96e", margin=dict(t=40,b=0,l=0,r=0)
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Budget type breakdown
        df["BudgetType"] = df["Budget Note"].apply(
            lambda x: "Paid" if "Paid" in str(x) else ("Creator" if "Creator" in str(x) else ("Boost" if "Boost" in str(x) else "Organic"))
        )
        bt = df["BudgetType"].value_counts().reset_index()
        bt.columns = ["Type","Count"]
        fig3 = px.bar(bt, x="Type", y="Count", title="Posts by Budget Type",
                      color="Type",
                      color_discrete_map={"Paid":"#c8a96e","Organic":"#4caf50","Creator":"#69c9d0","Boost":"#e1306c"})
        fig3.update_layout(
            paper_bgcolor="#111", plot_bgcolor="#111",
            font_color="#888", title_font_color="#c8a96e",
            showlegend=False, margin=dict(t=40,b=0,l=0,r=0)
        )
        fig3.update_xaxes(color="#555"); fig3.update_yaxes(color="#555", gridcolor="#1f1f1f")
        st.plotly_chart(fig3, use_container_width=True)

# ── Page: KPI Tracker ─────────────────────────────────────────────────────────
elif page == "📊 KPI Tracker":
    st.markdown("<div class='section-header'>KPI Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.82rem;color:#555;margin-bottom:1.5rem;'>Track weekly performance against campaign targets</div>", unsafe_allow_html=True)

    primary_kpis = ["Reach","Impressions","Frequency","Video Views","View-Through Rate (VTR)","CPM","Ad Recall Lift"]
    secondary_kpis = [k for k in kpi_df["KPI"].tolist() if k not in primary_kpis]

    st.markdown("**Primary KPIs**")
    primary_df = kpi_df[kpi_df["KPI"].isin(primary_kpis)].copy()
    st.dataframe(
        primary_df.style.set_properties(**{"background-color":"#111","color":"#e8e0d0","border-color":"#222"}),
        use_container_width=True, hide_index=True
    )

    st.markdown("<br>**Secondary KPIs**", unsafe_allow_html=True)
    secondary_df = kpi_df[kpi_df["KPI"].isin(secondary_kpis)].copy()
    st.dataframe(
        secondary_df.style.set_properties(**{"background-color":"#111","color":"#e8e0d0","border-color":"#222"}),
        use_container_width=True, hide_index=True
    )

    st.markdown("<div class='section-header'>Progress Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#555;font-size:0.8rem;'>Enter actual weekly data below to track progress against targets.</div>", unsafe_allow_html=True)

    kpi_display = kpi_df[["KPI","Target"]].copy()
    for w in ["Week 1","Week 2","Week 3","Week 4","Week 5"]:
        kpi_display[w] = ""

    edited = st.data_editor(kpi_display, use_container_width=True, hide_index=True)

# ── Page: Budget Breakdown ────────────────────────────────────────────────────
elif page == "💰 Budget Breakdown":
    st.markdown("<div class='section-header'>Budget Breakdown</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-label">Total Budget</div>
          <div class="metric-value">20M</div>
          <div class="metric-sub">Hungarian Forint (HUF)</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-label">Prospecting</div>
          <div class="metric-value">18M</div>
          <div class="metric-sub">90% of total budget</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
          <div class="metric-label">Retargeting</div>
          <div class="metric-value">2M</div>
          <div class="metric-sub">10% of total budget</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("<div class='section-header' style='font-size:1.2rem;'>Platform Allocation</div>", unsafe_allow_html=True)
        fig_plat = px.pie(platform_df, names="Platform", values="HUF",
                          title="Budget by Platform",
                          color="Platform",
                          color_discrete_map={
                              "TikTok":"#69c9d0","Instagram":"#e1306c",
                              "Facebook + YouTube":"#4267b2",
                              "Boosting / Creator Amplification":"#c8a96e"
                          })
        fig_plat.update_traces(textposition="inside", textinfo="percent+label")
        fig_plat.update_layout(
            paper_bgcolor="#111", font_color="#888",
            title_font_color="#c8a96e", margin=dict(t=40,b=0,l=0,r=0),
            showlegend=False
        )
        st.plotly_chart(fig_plat, use_container_width=True)

        for _, r in platform_df.iterrows():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.6rem 1rem;background:#111;border:1px solid #1f1f1f;
                        border-radius:6px;margin-bottom:0.4rem;">
              <span style="font-size:0.85rem;">{r['Platform']}</span>
              <span style="font-family:'Bebas Neue',sans-serif;color:#c8a96e;font-size:1.1rem;">
                {r['HUF']:,} HUF &nbsp;<span style="font-size:0.75rem;color:#555;">({r['Share']}%)</span>
              </span>
            </div>""", unsafe_allow_html=True)

    with col5:
        st.markdown("<div class='section-header' style='font-size:1.2rem;'>Funnel Split</div>", unsafe_allow_html=True)
        fig_funnel = px.bar(funnel_df, x="Funnel", y="HUF",
                            color="Funnel",
                            color_discrete_map={"Prospecting":"#c8a96e","Retargeting":"#69c9d0"},
                            title="Funnel Budget Split")
        fig_funnel.update_layout(
            paper_bgcolor="#111", plot_bgcolor="#111",
            font_color="#888", title_font_color="#c8a96e",
            showlegend=False, margin=dict(t=40,b=0,l=0,r=0)
        )
        fig_funnel.update_xaxes(color="#555"); fig_funnel.update_yaxes(color="#555", gridcolor="#1f1f1f")
        st.plotly_chart(fig_funnel, use_container_width=True)

        # Budget notes legend
        st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
        notes = [
            ("TikTok (Paid)", "40% of paid media"),
            ("Instagram (Paid)", "35% of paid media"),
            ("YouTube / Facebook (Paid)", "15% of paid media"),
            ("Boost Budget", "10% flex for best content"),
            ("Creator Budget", "Per-creator flat fee"),
        ]
        for label, note in notes:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:0.5rem 1rem;
                        background:#111;border:1px solid #1f1f1f;border-radius:6px;margin-bottom:0.3rem;">
              <span style="font-size:0.8rem;color:#aaa;">{label}</span>
              <span style="font-size:0.75rem;color:#555;">{note}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
