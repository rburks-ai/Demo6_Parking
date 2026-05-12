import streamlit as st
import folium
from streamlit_folium import st_folium
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

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2330;
}
[data-testid="stSidebar"] * { color: #e0e6f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stRadio label { color: #8b9bc0 !important; font-size: 0.78rem !important; letter-spacing: 0.06em; text-transform: uppercase; }

/* ── Main background ── */
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #0f1117 0%, #1a2035 60%, #0d2040 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #1e3060;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,200,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.02em;
}
.hero-title span { color: #00c8ff; }
.hero-subtitle {
    font-size: 0.95rem;
    color: #8b9bc0;
    margin: 0;
    font-weight: 300;
}

/* ── Stat chips ── */
.stat-row { display: flex; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap; }
.stat-chip {
    background: rgba(0,200,255,0.08);
    border: 1px solid rgba(0,200,255,0.2);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    color: #00c8ff;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

/* ── Section label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #00c8ff;
    margin: 1.5rem 0 0.7rem 0;
}

/* ── Parking card ── */
.park-card {
    background: #141824;
    border: 1px solid #1e2845;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    position: relative;
    transition: border-color 0.2s;
}
.park-card:hover { border-color: #00c8ff44; }
.park-card.best-deal { border-color: #00c8ff66; }

.card-badge {
    position: absolute;
    top: 0.9rem; right: 1rem;
    background: #00c8ff;
    color: #0f1117;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 50px;
}

.card-name {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8edf8;
    margin: 0 0 0.15rem 0;
}
.card-area {
    font-size: 0.78rem;
    color: #5a6a8a;
    margin-bottom: 0.75rem;
}
.card-meta { display: flex; gap: 1.2rem; align-items: center; flex-wrap: wrap; }
.price-tag {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #00c8ff;
}
.price-tag small { font-size: 0.65rem; font-weight: 400; color: #5a6a8a; }

.meta-item { font-size: 0.78rem; color: #8b9bc0; }
.meta-item strong { color: #c8d4ec; font-weight: 500; }

.amenity-tags { display: flex; gap: 0.4rem; margin-top: 0.75rem; flex-wrap: wrap; }
.amenity-tag {
    background: #1a2035;
    border: 1px solid #2a3555;
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
    font-size: 0.68rem;
    color: #6a7a9a;
}

.spots-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
}
.spots-good { background: #0d2a1a; color: #30e080; border: 1px solid #1a5030; }
.spots-low  { background: #2a1a00; color: #ff9f30; border: 1px solid #5a3a00; }
.spots-none { background: #2a0d0d; color: #ff5050; border: 1px solid #5a1a1a; }

/* ── Sort / filter row ── */
.stRadio [role="radiogroup"] { flex-direction: row !important; gap: 0.5rem; }

/* ── Map container ── */
.map-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #00c8ff;
    margin-bottom: 0.5rem;
}

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 3rem;
    color: #5a6a8a;
    font-size: 0.95rem;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a3555; border-radius: 3px; }

/* ── Sidebar logo ── */
.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #1e2330;
    margin-bottom: 1.2rem;
}
.sidebar-logo span { color: #00c8ff; }
</style>
""", unsafe_allow_html=True)

# ── State init ────────────────────────────────────────────────────────────────
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

# ── Sidebar – Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🅿️ Park<span>Smart</span></div>', unsafe_allow_html=True)

    st.markdown("**📍 Location**")
    cities = get_cities()
    selected_city = st.selectbox("City", cities, label_visibility="collapsed")

    areas = ["All Areas"] + get_areas(selected_city)
    selected_area = st.selectbox("Neighbourhood / Area", areas)

    st.markdown("---")
    st.markdown("**🎛️ Filters**")

    max_price = st.slider("Max price per hour ($)", 1.0, 25.0, 15.0, 0.50)
    parking_type = st.radio("Parking type", ["All Types", "Garage", "Lot"], horizontal=True)
    available_only = st.checkbox("Available spots only", value=True)
    open_24h = st.checkbox("Open 24 hours only", value=False)

    st.markdown("---")
    st.markdown("**↕️ Sort by**")
    sort_by = st.radio(
        "Sort",
        ["price_per_hour", "distance_mi", "rating"],
        format_func=lambda x: {"price_per_hour": "💰 Price", "distance_mi": "📍 Distance", "rating": "⭐ Rating"}[x],
        label_visibility="collapsed",
    )

# ── Filter data ───────────────────────────────────────────────────────────────
results = filter_parking(
    city=selected_city,
    area=selected_area,
    max_price=max_price,
    parking_type=parking_type,
    available_only=available_only,
    open_24h=open_24h,
    sort_by=sort_by,
)

# ── Hero header ───────────────────────────────────────────────────────────────
avg_price = results["price_per_hour"].mean() if not results.empty else 0
total_spots = results["spots_available"].sum() if not results.empty else 0
cheapest = results["price_per_hour"].min() if not results.empty else 0

st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Find <span>Affordable</span> Parking</p>
    <p class="hero-subtitle">Real-time spot availability · Compare prices · Navigate instantly</p>
    <div class="stat-row">
        <span class="stat-chip">📍 {selected_city}</span>
        <span class="stat-chip">🏢 {len(results)} locations found</span>
        <span class="stat-chip">💰 From ${cheapest:.2f}/hr</span>
        <span class="stat-chip">🚗 {total_spots} spots available</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: Map | Cards ───────────────────────────────────────────────────────
col_map, col_list = st.columns([1.2, 1], gap="large")

# ────────────────────────────────── MAP ──────────────────────────────────────
with col_map:
    st.markdown('<div class="map-label">📡 Live Map</div>', unsafe_allow_html=True)

    if not results.empty:
        center_lat = results["lat"].mean()
        center_lon = results["lon"].mean()
    else:
        # City fallback centres
        city_centers = {
            "Atlanta": (33.749, -84.388),
            "New York": (40.730, -73.985),
            "Chicago": (41.882, -87.628),
            "Los Angeles": (34.052, -118.244),
            "Miami": (25.762, -80.197),
            "Austin": (30.267, -97.743),
        }
        center_lat, center_lon = city_centers.get(selected_city, (33.749, -84.388))

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="CartoDB dark_matter",
    )

    for _, row in results.iterrows():
        is_best = row["id"] == (results.iloc[0]["id"] if not results.empty else -1)

        if row["spots_available"] == 0:
            icon_color = "red"
        elif row["spots_available"] < 20:
            icon_color = "orange"
        else:
            icon_color = "blue" if not is_best else "green"

        popup_html = f"""
        <div style='font-family:sans-serif;min-width:180px;'>
            <b style='font-size:13px;'>{row['name']}</b><br>
            <span style='color:#555;font-size:11px;'>{row['area']}</span><br><br>
            <b style='color:#00a8d4;font-size:16px;'>${row['price_per_hour']:.2f}/hr</b><br>
            ⭐ {row['rating']} &nbsp;|&nbsp; 🚗 {row['spots_available']} spots<br>
            🕐 {'24h' if row['open_24h'] else 'Limited hours'}<br>
            📐 {row['distance_mi']} mi away
        </div>
        """

        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"${row['price_per_hour']:.2f}/hr – {row['name']}",
            icon=folium.Icon(color=icon_color, icon="p-sign" if icon_color == "green" else "circle", prefix="fa"),
        ).add_to(m)

    # Legend
    legend_html = """
    <div style='position:fixed;bottom:20px;left:20px;z-index:9999;
                background:#141824cc;border:1px solid #2a3555;border-radius:10px;
                padding:10px 14px;font-family:sans-serif;font-size:11px;color:#aaa;
                backdrop-filter:blur(4px);'>
        <b style='color:#fff;'>Spot Availability</b><br>
        🟢 Best deal &nbsp; 🔵 Available<br>🟠 Low (&lt;20) &nbsp; 🔴 Full
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    map_data = st_folium(m, height=540, use_container_width=True)

    # Capture clicked marker
    if map_data and map_data.get("last_object_clicked_tooltip"):
        tooltip = map_data["last_object_clicked_tooltip"]
        for _, row in results.iterrows():
            if row["name"] in tooltip:
                st.session_state.selected_id = row["id"]
                break

# ─────────────────────────────── CARD LIST ───────────────────────────────────
with col_list:
    st.markdown('<div class="section-label">🏢 Parking Locations</div>', unsafe_allow_html=True)

    if results.empty:
        st.markdown('<div class="no-results">😕 No parking found with these filters.<br>Try widening your search.</div>', unsafe_allow_html=True)
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            is_best = (i == 0)

            if row["spots_available"] == 0:
                spots_class, spots_text = "spots-none", "❌ Full"
            elif row["spots_available"] < 20:
                spots_class, spots_text = "spots-low", f"⚠️ {row['spots_available']} left"
            else:
                spots_class, spots_text = "spots-good", f"✅ {row['spots_available']} spots"

            amenity_tags = "".join(
                f'<span class="amenity-tag">{a}</span>' for a in row["amenities"]
            ) if row["amenities"] else ""

            badge = '<span class="card-badge">Best Deal</span>' if is_best else ""

            st.markdown(f"""
            <div class="park-card {'best-deal' if is_best else ''}">
                {badge}
                <div class="card-name">{row['name']}</div>
                <div class="card-area">📍 {row['area']} · {row['type']}</div>
                <div class="card-meta">
                    <div class="price-tag">${row['price_per_hour']:.2f}<small>/hr</small></div>
                    <div class="meta-item">⭐ <strong>{row['rating']}</strong> rating</div>
                    <div class="meta-item">📐 <strong>{row['distance_mi']} mi</strong></div>
                    <div class="meta-item">🕐 <strong>{'24h' if row['open_24h'] else 'Limited'}</strong></div>
                    <span class="spots-badge {spots_class}">{spots_text}</span>
                </div>
                {f'<div class="amenity-tags">{amenity_tags}</div>' if amenity_tags else ''}
            </div>
            """, unsafe_allow_html=True)

        # ── Summary stats ──────────────────────────────────────────────────
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Cheapest", f"${results['price_per_hour'].min():.2f}/hr")
        with c2:
            st.metric("Avg. Price", f"${results['price_per_hour'].mean():.2f}/hr")
        with c3:
            st.metric("Avg. Rating", f"⭐ {results['rating'].mean():.1f}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;color:#2a3555;font-size:0.75rem;margin-top:2rem;padding-top:1rem;
            border-top:1px solid #1a2035;'>
    ParkSmart · Demo data for illustration purposes · Built with Streamlit
</div>
""", unsafe_allow_html=True)
