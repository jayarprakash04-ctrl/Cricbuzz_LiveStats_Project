import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import requests

from player_status import show_player_status
import sql_queries
import crud_operations



conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="cricket_db"
)


st.title("🏏 Cricbuzz LiveStats Dashboard")


menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Live Scores",
        "Player Status",
        "SQL Analytics",
        "CRUD Operations"
    ]
)

st.write("Selected Menu:", menu)
st.sidebar.markdown("---")
st.sidebar.info("""
### Live Scores Page
- Real-time match data
- Detailed scorecards
- Series information
- Interactive match selection
""")

show_debug = st.sidebar.checkbox("Show Debug Info")


if menu == "Live Scores":


    st.subheader("🎯 Select a Match")

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
        "x-rapidapi-key": "25c333010emsh22065893cf170c6p1b9c33jsnea916aef0083",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            matches_list = []
            matches_data = []

            for match_type in data.get("typeMatches", []):
                if "seriesMatches" not in match_type:
                    continue
                for series in match_type["seriesMatches"]:
                    if "seriesAdWrapper" not in series:
                        continue
                    for match in series["seriesAdWrapper"].get("matches", []):
                        if "matchInfo" not in match:
                            continue
                        info = match["matchInfo"]
                        match_name = (
                            f"{info['team1']['teamName']} vs "
                            f"{info['team2']['teamName']} - "
                            f"{info['matchDesc']}"
                        )
                        matches_list.append(match_name)
                        matches_data.append(match)

            if len(matches_list) > 0:
                selected_match = st.selectbox("Available Matches", matches_list)
                selected_index = matches_list.index(selected_match)
                match = matches_data[selected_index]
                info = match["matchInfo"]

                st.write("Match ID:", info["matchId"])
                team1 = info["team1"]["teamName"]
                team2 = info["team2"]["teamName"]

                st.markdown("---")
                st.header(f"🏏 {team1} vs {team2}")

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"📄 Match: {info.get('matchDesc','')}")
                    st.write(f"🏆 Format: {info.get('matchFormat','')}")
                    st.write(f"📢 Status: {info.get('status','')}")
                with col2:
                    st.write(f"🏟 Venue: {info['venueInfo'].get('ground','')}")
                    st.write(f"📍 City: {info['venueInfo'].get('city','')}")
                    st.write(f"📅 Series: {info.get('seriesName','')}")

                st.markdown("---")
                st.subheader("📊 Current Score")

                if "matchScore" in match:
                    score = match["matchScore"]
                    c1, c2 = st.columns(2)

                    if "team1Score" in score:
                        innings1 = score["team1Score"].get("inngs1", {})
                        c1.success(
                            f"{team1}\n\n"
                            f"{innings1.get('runs',0)}/"
                            f"{innings1.get('wickets',0)} "
                            f"({innings1.get('overs',0)} overs)"
                        )

                    if "team2Score" in score:
                        innings2 = score["team2Score"].get("inngs1", {})
                        c2.success(
                            f"{team2}\n\n"
                            f"{innings2.get('runs',0)}/"
                            f"{innings2.get('wickets',0)} "
                            f"({innings2.get('overs',0)} overs)"
                        )

                st.markdown("---")
                st.subheader("📋 Detailed Scorecard")

                if st.button("Load Full Scorecard"):
                    match_id = info["matchId"]
                    score_url = (
                        f"https://cricbuzz-cricket.p.rapidapi.com/"
                        f"mcenter/v1/{match_id}/scard"
                    )
                    score_response = requests.get(score_url, headers=headers)
                    st.write("Scorecard Status:", score_response.status_code)

                    if score_response.status_code == 200:
                        score_data = score_response.json()
                        st.success("Scorecard Loaded!")
                        scorecard = score_data.get("scorecard", [])

                        for innings in scorecard:
                            st.markdown("---")

                            
                            innings_id = innings.get("inningsId", "")
                            st.subheader(f"🏏 Innings {innings_id}")

                            
                            batsmen = innings.get("batsman", [])
                            if batsmen:
                                st.markdown("**🏏 Batting**")
                                bat_data = []
                                for b in batsmen:
                                    bat_data.append({
                                        "Player":      b.get("name", ""),
                                        "Runs":        b.get("runs", 0),
                                        "Balls":       b.get("balls", 0),
                                        "Fours":       b.get("fours", 0),
                                        "Sixes":       b.get("sixes", 0),
                                        "Strike Rate": b.get("strkrate", ""),
                                        "Dismissal":   b.get("outdec", "")
                                    })
                                st.dataframe(
                                    pd.DataFrame(bat_data),
                                    use_container_width=True
                                )

                            # ── Bowling Table ──
                            bowlers = innings.get("bowler", [])
                            if bowlers:
                                st.markdown("**🎳 Bowling**")
                                bowl_data = []
                                for b in bowlers:
                                    bowl_data.append({
                                        "Player":  b.get("name", ""),
                                        "Overs":   b.get("overs", 0),
                                        "Maidens": b.get("maidens", 0),
                                        "Runs":    b.get("runs", 0),
                                        "Wickets": b.get("wickets", 0),
                                        "Economy": b.get("economy", "")
                                    })
                                st.dataframe(
                                    pd.DataFrame(bowl_data),
                                    use_container_width=True
                                )

                            
                            extras = innings.get("extras", {})
                            if extras:
                                st.markdown(
                                    f"**Extras:** {extras.get('r', 0)} "
                                    f"(b {extras.get('b', 0)}, "
                                    f"lb {extras.get('lb', 0)}, "
                                    f"wd {extras.get('wd', 0)}, "
                                    f"nb {extras.get('nb', 0)})"
                                )

                            total   = innings.get("score", "")
                            wickets = innings.get("wickets", "")
                            overs   = innings.get("overs", "")
                            if total:
                                st.markdown(
                                    f"**Total: {total}/{wickets} ({overs} overs)**"
                                )
                    else:
                        st.error(f"Scorecard API Error: {score_response.status_code}")
            else:
                st.warning("No live matches found.")
        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {e}")


elif menu == "Player Status":
    show_player_status()


elif menu == "SQL Analytics":
    sql_queries.show()


elif menu == "CRUD Operations":
    crud_operations.show()
