import streamlit as st
import requests
import pandas as pd

API_KEY = "25c333010emsh22065893cf170c6p1b9c33jsnea916aef0083"
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

def call_api(endpoint, params=None):
    r = requests.get(BASE_URL + endpoint, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def values_to_df(data):
    """Safely convert API response to DataFrame."""
    try:
        headers = data.get("headers", [])
        vals = data.get("values", [])

        if not headers or not vals:
            return pd.DataFrame()

        rows = []
        for v in vals:
            row_values = v.get("values", [])
            # Make sure row length matches headers length
            if len(row_values) == len(headers):
                rows.append(row_values)
            elif len(row_values) < len(headers):
                # Pad with empty strings if row is shorter
                row_values += [""] * (len(headers) - len(row_values))
                rows.append(row_values)
            else:
                # Trim if row is longer
                rows.append(row_values[:len(headers)])

        if not rows:
            return pd.DataFrame()

        return pd.DataFrame(rows, columns=headers)

    except Exception as e:
        st.warning(f"Could not parse data: {e}")
        return pd.DataFrame()


def safe_dataframe(data, title):
    """Safely display any API data as a table."""
    try:
        # Try values_to_df first
        df = values_to_df(data)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            return

        # If that fails, try direct list
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            return

        # If data is a dict with different structure
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    st.markdown(f"**{key}**")
                    try:
                        df = pd.DataFrame(value)
                        st.dataframe(df, use_container_width=True)
                    except:
                        st.write(value)
            return

        st.info(f"No data available for {title}")

    except Exception as e:
        st.warning(f"Could not display {title}: {e}")


def show_player_status():
    st.title("👤 Player Status")

    player_name = st.text_input("🔍 Search Player Name")

    if not player_name:
        st.info("Enter a player name to search.")
        return

    # ── Search Player ──────────────────────────────────────
    try:
        search = call_api("/stats/v1/player/search", {"plrN": player_name})
    except Exception as e:
        st.error(f"Search failed: {e}")
        return

    plist = search.get("player", [])
    if not plist:
        st.warning("No player found. Try a different name.")
        return

    names = [f'{p["name"]} ({p.get("teamName", "Unknown")})' for p in plist]
    selected = st.selectbox("Select Player", names)
    player = plist[names.index(selected)]
    pid = player["id"]

    # ── Player Info ────────────────────────────────────────
    try:
        info = call_api(f"/stats/v1/player/{pid}")
    except Exception as e:
        st.error(f"Unable to fetch player info: {e}")
        return

    st.markdown("---")

    # Profile
    col1, col2 = st.columns([1, 2])
    with col1:
        if info.get("image"):
            st.image(info["image"], width=160)

    with col2:
        st.header(info.get("name", ""))
        st.write(f"**Full Name:** {info.get('fullName', 'N/A')}")
        st.write(f"**Role:** {info.get('role', 'N/A')}")
        st.write(f"**Batting:** {info.get('bat', 'N/A')}")
        st.write(f"**Bowling:** {info.get('bowl', 'N/A')}")
        st.write(f"**DOB:** {info.get('DoB', 'N/A')}")
        st.write(f"**International Team:** {info.get('intlTeam', 'N/A')}")
        st.write(f"**Birth Place:** {info.get('birthPlace', 'N/A')}")

    with st.expander("📖 Biography"):
        bio = info.get("bio", "").replace("<br/>", " ").strip()
        st.write(bio if bio else "No biography available.")

    st.markdown("---")

    # ── Career Stats ───────────────────────────────────────
    st.subheader("📊 Career Statistics")
    try:
        career_data = call_api(f"/stats/v1/player/{pid}/career")
        safe_dataframe(career_data, "Career")
    except Exception as e:
        st.warning(f"Career stats not available: {e}")

    # ── Batting Stats ──────────────────────────────────────
    st.subheader("🏏 Batting Statistics")
    try:
        bat_data = call_api(f"/stats/v1/player/{pid}/batting")
        safe_dataframe(bat_data, "Batting")
    except Exception as e:
        st.warning(f"Batting stats not available: {e}")

    # ── Bowling Stats ──────────────────────────────────────
    st.subheader("🎳 Bowling Statistics")
    try:
        bowl_data = call_api(f"/stats/v1/player/{pid}/bowling")
        safe_dataframe(bowl_data, "Bowling")
    except Exception as e:
        st.warning(f"Bowling stats not available: {e}")

    # ── Recent Batting ─────────────────────────────────────
    if "recentBatting" in info:
        st.subheader("🕐 Recent Batting")
        try:
            rb = info["recentBatting"]
            headers = rb.get("headers", [])
            rows = rb.get("rows", [])
            safe_rows = []
            for r in rows:
                vals = r.get("values", [])
                # Fix column mismatch
                if len(vals) > len(headers):
                    vals = vals[:len(headers)]
                elif len(vals) < len(headers):
                    vals += [""] * (len(headers) - len(vals))
                safe_rows.append(vals)
            if safe_rows:
                df = pd.DataFrame(safe_rows, columns=headers)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.warning(f"Recent batting not available: {e}")

    # ── Recent Bowling ─────────────────────────────────────
    if "recentBowling" in info:
        st.subheader("🕐 Recent Bowling")
        try:
            rw = info["recentBowling"]
            headers = rw.get("headers", [])
            rows = rw.get("rows", [])
            safe_rows = []
            for r in rows:
                vals = r.get("values", [])
                if len(vals) > len(headers):
                    vals = vals[:len(headers)]
                elif len(vals) < len(headers):
                    vals += [""] * (len(headers) - len(vals))
                safe_rows.append(vals)
            if safe_rows:
                df = pd.DataFrame(safe_rows, columns=headers)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.warning(f"Recent bowling not available: {e}")