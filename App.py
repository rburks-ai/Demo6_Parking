import streamlit as st
import pydeck as pdk
import pandas as pd
from mock_data import get_cities, get_areas, filter_parking

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ParkSmart – Affordable Parking Finder",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] { background: #0f1117; border-right: 1px solid #1e2330; }
[data-testid="stSidebar"] * { color: #e0e6f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #8b9bc0 !important; font-size: 0.78rem !important;
    letter-spacing: 0.06em; text-transform: uppercase;
}

.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.hero-header {
    background: linear-gradient(135deg, #0f1117 0%, #1a2035 60%, #0d2040 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    border: 1px solid #1e3060; position: relative; overflow: hidden;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800;
    color: #ffffff; margin: 0 0 0.3rem 0; letter-spacing: -0.02em;
}
.hero-title span { color: #00c8ff; }
.hero-subtitle { font-size: 0.95rem; color: #8b9bc0; margin: 0; font-weight: 300; }

.stat-row { display: flex; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap; }
.stat-chip {
    background: rgba(0,200,255,0.08); border: 1px solid rgba(0,200,255,0.2);
    border-radius: 50px; padding: 0.35rem 1rem; font-size: 0.8rem;
    color: #00c8ff; font-weight: 500;
}

.section-label {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #00c8ff; margin: 1.5rem 0 0.7rem 0;
}

.park-card {
    background: #141824; border: 1px solid #1e2845;
    border-radius: 14px; padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem; position: relative;
}
.park-card.best-deal { border-color: #00c8ff66; }
.card-badge {
    position: absolute; top: 0.9rem; right: 1rem;
    background: #00c8ff; color: #0f1117; font-size: 0.65rem;
    font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.2rem 0.6rem; border-radius: 50px;
}
.card-name {
    font-family: 'Syne', sans-serif; font-size: 1rem;
    font-weight: 700; color: #e8edf8; margin: 0 0 0.15rem 0;
}
.card-area { font-size: 0.78rem; color: #5a6a8a; margin-bottom: 0.75rem; }
.card-meta { display: flex; gap: 1.2rem; align-items: center; flex-wrap: wrap; }
.price-tag {
    font-family: 'Syne', sans-serif; font-size: 1.5rem;
    font-weight: 800; color: #00c8ff;
}
.price-tag small { font-size: 0.65rem; font-weight: 400; color: #5a6a8a; }
.meta-item { font-size: 0.78rem; color: #8b9bc0; }
.meta-item strong { color: #c8d4ec; font-weight: 500; }
.amenity-tags { display: flex; gap: 0.4rem; margin-top: 0.75rem; flex-wrap: wrap; }
.amenity-tag {
    background: #1a2035; border: 1px solid #2a3555;
    border-radius: 6px; padding: 0.15rem 0.5rem;
    font-size: 0.68rem; color: #6a7a9a;
}
.spots-badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.72rem; font-weight: 600; }
.spots-good { background: #0d2a1a; color: #30e080; border: 1px solid #1a5030; }
.spots-low  { background: #2a1a00; color: #ff9f30; border: 1px solid #5a3a00; }
.spots-none { background: #2a0d0d; color: #ff5050; border: 1px solid #5a1a1a; }
.no-results { text-align: center; padding: 3rem; color: #5a6a8a; font-size: 0.95rem; }
.sidebar-logo {
    font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.02em;
    padding-bottom: 1.2rem; border-bottom: 1px solid #1e2330; margin-bottom: 1.2rem;
}
.sidebar-logo span { color: #00c8ff; }
.map-label {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase; color: #00c8ff; margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ── City centre fallbacks ──────────────────────────────────────────────────────
CITY_CENTERS = {
    "Atlanta":     (33.749,  -84.388),
    "New York":    (40.730,  -73.985),
    "Chicago":     (41.882,  -87.628),
    "Los Angeles": (34.052, -118.244),
    "Miami":       (25.762,  -80.197),
    "Austin":      (30.267,  -97.743),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🅿️ Park<span>Smart</span></div>', unsafe_allow_html=True)

    st.markdown("**📍 Location**")
    cities = get_cities()
    selected_city = st.selectbox("City", cities, label_visibility="collapsed")
    areas = ["All Areas"] + get_areas(selected_city)
    selected_area = st.selectbox("Neighbourhood / Area", areas)

    st.markdown("---")
    st.markdown("**🎛️ Filters**")
    max_price     = st.slider("Max price per hour ($)", 1.0, 25.0, 15.0, 0.50)
    parking_type  = st.radio("Parking type", ["All Types", "Garage", "Lot"], horizontal=True)
    available_only = st.checkbox("Available spots only", value=True)
    open_24h      = st.checkbox("Open 24 hours only", value=False)

    st.markdown("---")
    st.markdown("**↕️ Sort by**")
    sort_by = st.radio(
        "Sort",
        ["price_per_hour", "distance_mi", "rating"],
        format_func=lambda x: {"price_per_hour": "💰 Price", "distance_mi": "📍 Distance", "rating": "⭐ Rating"}[x],
        label_visibility="collapsed",
    )

# ── Filter ────────────────────────────────────────────────────────────────────
results = filter_parking(
    city=selected_city, area=selected_area, max_price=max_price,
    parking_type=parking_type, available_only=available_only,
    open_24h=open_24h, sort_by=sort_by,
)

cheapest    = results["price_per_hour"].min() if not results.empty else 0
total_spots = int(results["spots_available"].sum()) if not results.empty else 0

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Find <span>Affordable</span> Parking</p>
    <p class="hero-subtitle">Compare prices · Check availability · Navigate instantly</p>
    <div class="stat-row">
        <span class="stat-chip">📍 {selected_city}</span>
        <span class="stat-chip">🏢 {len(results)} locations found</span>
        <span class="stat-chip">💰 From ${cheapest:.2f}/hr</span>
        <span class="stat-chip">🚗 {total_spots} spots available</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_map, col_list = st.columns([1.2, 1], gap="large")

# ── Map (pydeck) ──────────────────────────────────────────────────────────────
with col_map:
    st.markdown('<div class="map-label">📡 Live Map</div>', unsafe_allow_html=True)

    clat, clon = CITY_CENTERS.get(selected_city, (33.749, -84.388))
    if not results.empty:
        clat = results["lat"].mean()
        clon = results["lon"].mean()

    def spot_color(row, idx):
        """Return RGBA based on availability; cyan for best deal."""
        if idx == 0:
            return [0, 200, 255, 230]       # cyan  – best deal
        if row["spots_available"] == 0:
            return [255, 70, 70, 220]        # red   – full
        if row["spots_available"] < 20:
            return [255, 160, 40, 220]       # orange – low
        return [60, 160, 255, 200]           # blue  – available

    if not results.empty:
        map_df = results.copy()
        map_df["color"] = [spot_color(r, i) for i, (_, r) in enumerate(results.iterrows())]
        map_df["radius"] = 40
        map_df["tooltip_text"] = map_df.apply(
            lambda r: f"{r['name']} | ${r['price_per_hour']:.2f}/hr | {r['spots_available']} spots | ⭐{r['rating']}",
            axis=1,
        )
    else:
        map_df = pd.DataFrame(columns=["lat","lon","color","radius","tooltip_text"])

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius="radius",
        radius_min_pixels=8,
        radius_max_pixels=22,
        pickable=True,
    )

    view = pdk.ViewState(latitude=clat, longitude=clon, zoom=13, pitch=0)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "{tooltip_text}"},
    )

    st.pydeck_chart(deck, use_container_width=True, height=520)

    # Colour legend
    st.markdown("""
    <div style='display:flex;gap:1.2rem;margin-top:0.5rem;font-size:0.75rem;color:#8b9bc0;flex-wrap:wrap;'>
        <span>🔵 Best deal</span>
        <span>🔵 Available</span>
        <span>🟠 Low (&lt;20 spots)</span>
        <span>🔴 Full</span>
    </div>
    """, unsafe_allow_html=True)

# ── Card list ─────────────────────────────────────────────────────────────────
with col_list:
    st.markdown('<div class="section-label">🏢 Parking Locations</div>', unsafe_allow_html=True)

    if results.empty:
        st.markdown('<div class="no-results">😕 No parking found.<br>Try widening your filters.</div>', unsafe_allow_html=True)
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            is_best = (i == 0)
            if row["spots_available"] == 0:
                sc, st_ = "spots-none", "❌ Full"
            elif row["spots_available"] < 20:
                sc, st_ = "spots-low", f"⚠️ {row['spots_available']} left"
            else:
                sc, st_ = "spots-good", f"✅ {row['spots_available']} spots"

            tags = "".join(f'<span class="amenity-tag">{a}</span>' for a in row["amenities"])
            badge = '<span class="card-badge">Best Deal</span>' if is_best else ""

            st.markdown(f"""
            <div class="park-card {'best-deal' if is_best else ''}">
                {badge}
                <div class="card-name">{row['name']}</div>
                <div class="card-area">📍 {row['area']} · {row['type']}</div>
                <div class="card-meta">
                    <div class="price-tag">${row['price_per_hour']:.2f}<small>/hr</small></div>
                    <div class="meta-item">⭐ <strong>{row['rating']}</strong></div>
                    <div class="meta-item">📐 <strong>{row['distance_mi']} mi</strong></div>
                    <div class="meta-item">🕐 <strong>{'24h' if row['open_24h'] else 'Limited'}</strong></div>
                    <span class="spots-badge {sc}">{st_}</span>
                </div>
                {f'<div class="amenity-tags">{tags}</div>' if tags else ''}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Cheapest",   f"${results['price_per_hour'].min():.2f}/hr")
        c2.metric("Avg. Price", f"${results['price_per_hour'].mean():.2f}/hr")
        c3.metric("Avg. Rating",f"⭐ {results['rating'].mean():.1f}")

st.markdown("""
<div style='text-align:center;color:#2a3555;font-size:0.75rem;margin-top:2rem;
            padding-top:1rem;border-top:1px solid #1a2035;'>
    ParkSmart · Demo data · Built with Streamlit & pydeck
</div>
""", unsafe_allow_html=True)
