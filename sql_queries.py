import streamlit as st
import mysql.connector
import pandas as pd


# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="cricket_db"
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"❌ Database Connection Failed: {e}")
        return None


def run_query(query):
    conn = get_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ Query Error: {e}")
        return None
    finally:
        conn.close()


# ─────────────────────────────────────────────
# ALL 25 SQL QUERIES
# ─────────────────────────────────────────────
QUERIES = {

    "1. List all Indian players": {
        "level": "🟢 Beginner",
        "description": "Find all players who represent India.",
        "sql": """
SELECT player_name, role, batting_style, bowling_style
FROM players
WHERE country = 'India'
ORDER BY player_name;
        """
    },

    "2. Recent cricket matches": {
        "level": "🟢 Beginner",
        "description": "Show all matches sorted by most recent date.",
        "sql": """
SELECT team1, team2, winner, venue, match_date
FROM matches
ORDER BY match_date DESC;
        """
    },

    "3. Top ODI run scorers": {
        "level": "🟢 Beginner",
        "description": "Top run scorers in ODI cricket.",
        "sql": """
SELECT player_name, runs, batting_average, strike_rate
FROM player_stats
WHERE format = 'ODI'
ORDER BY runs DESC
LIMIT 10;
        """
    },

    "4. Venues with capacity > 25,000": {
        "level": "🟢 Beginner",
        "description": "Venues with seating capacity more than 25,000.",
        "sql": """
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 25000
ORDER BY capacity DESC;
        """
    },

    "5. Team win counts": {
        "level": "🟢 Beginner",
        "description": "How many matches each team has won.",
        "sql": """
SELECT winner AS team_name, COUNT(*) AS total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC;
        """
    },

    "6. Players count by role": {
        "level": "🟢 Beginner",
        "description": "Count of players for each playing role.",
        "sql": """
SELECT role AS playing_role, COUNT(*) AS player_count
FROM players
GROUP BY role
ORDER BY player_count DESC;
        """
    },

    "7. Highest runs by format": {
        "level": "🟢 Beginner",
        "description": "Highest runs scored in each cricket format.",
        "sql": """
SELECT format, MAX(runs) AS highest_runs
FROM player_stats
GROUP BY format
ORDER BY highest_runs DESC;
        """
    },

    "8. All matches in 2025": {
        "level": "🟢 Beginner",
        "description": "All cricket matches played in 2025.",
        "sql": """
SELECT team1, team2, winner, venue, match_date
FROM matches
WHERE YEAR(match_date) = 2025
ORDER BY match_date;
        """
    },

    "9. Players with 100+ wickets": {
        "level": "🟡 Intermediate",
        "description": "Players who have taken 100 or more wickets.",
        "sql": """
SELECT player_name, format, wickets, batting_average
FROM player_stats
WHERE wickets >= 100
ORDER BY wickets DESC;
        """
    },

    "10. All-rounders with runs and wickets": {
        "level": "🟡 Intermediate",
        "description": "Players with both 500+ runs and 50+ wickets.",
        "sql": """
SELECT player_name, format, runs, wickets, batting_average, strike_rate
FROM player_stats
WHERE runs > 500 AND wickets > 50
ORDER BY runs DESC;
        """
    },

    "11. Player performance across formats": {
        "level": "🟡 Intermediate",
        "description": "Each player's runs across different formats.",
        "sql": """
SELECT player_name,
       MAX(CASE WHEN format = 'Test' THEN runs END) AS test_runs,
       MAX(CASE WHEN format = 'ODI'  THEN runs END) AS odi_runs,
       MAX(CASE WHEN format = 'T20I' THEN runs END) AS t20i_runs
FROM player_stats
GROUP BY player_name
ORDER BY player_name;
        """
    },

    "12. Average runs per format": {
        "level": "🟡 Intermediate",
        "description": "Average batting stats grouped by format.",
        "sql": """
SELECT format,
       ROUND(AVG(runs), 2)            AS avg_runs,
       ROUND(AVG(batting_average), 2) AS avg_batting_average,
       ROUND(AVG(strike_rate), 2)     AS avg_strike_rate,
       COUNT(*)                        AS player_count
FROM player_stats
GROUP BY format
ORDER BY avg_runs DESC;
        """
    },

    "13. Teams and their countries": {
        "level": "🟡 Intermediate",
        "description": "All registered teams with their country.",
        "sql": """
SELECT team_name, country
FROM teams
ORDER BY country;
        """
    },

    "14. Matches won by each team": {
        "level": "🟡 Intermediate",
        "description": "Total match wins grouped by winning team.",
        "sql": """
SELECT winner, COUNT(*) AS wins
FROM matches
WHERE winner IS NOT NULL AND winner != ''
GROUP BY winner
ORDER BY wins DESC;
        """
    },

    "15. Players from each country": {
        "level": "🟡 Intermediate",
        "description": "Count of players representing each country.",
        "sql": """
SELECT country, COUNT(*) AS player_count
FROM players
GROUP BY country
ORDER BY player_count DESC;
        """
    },

    "16. Strike rate above 90 in ODI": {
        "level": "🟡 Intermediate",
        "description": "Players with strike rate above 90 in ODI format.",
        "sql": """
SELECT player_name, runs, batting_average, strike_rate
FROM player_stats
WHERE format = 'ODI' AND strike_rate > 90
ORDER BY strike_rate DESC;
        """
    },

    "17. Best batting average by format": {
        "level": "🔴 Advanced",
        "description": "Top batting average player in each format.",
        "sql": """
SELECT format, player_name, batting_average
FROM player_stats ps1
WHERE batting_average = (
    SELECT MAX(batting_average)
    FROM player_stats ps2
    WHERE ps2.format = ps1.format
)
ORDER BY batting_average DESC;
        """
    },

    "18. Players with above average runs": {
        "level": "🔴 Advanced",
        "description": "Players who scored above the overall average runs.",
        "sql": """
SELECT player_name, format, runs, batting_average
FROM player_stats
WHERE runs > (SELECT AVG(runs) FROM player_stats)
ORDER BY runs DESC;
        """
    },

    "19. Player stats joined with player info": {
        "level": "🔴 Advanced",
        "description": "Full player details joined with their stats.",
        "sql": """
SELECT p.player_name, p.country, p.role,
       ps.format, ps.runs, ps.wickets,
       ps.batting_average, ps.strike_rate
FROM players p
JOIN player_stats ps ON p.player_name = ps.player_name
ORDER BY ps.runs DESC;
        """
    },

    "20. Top scorer per country": {
        "level": "🔴 Advanced",
        "description": "Highest run scorer from each country.",
        "sql": """
SELECT p.country, ps.player_name, MAX(ps.runs) AS max_runs
FROM player_stats ps
JOIN players p ON ps.player_name = p.player_name
GROUP BY p.country, ps.player_name
ORDER BY max_runs DESC;
        """
    },

    "21. Ranked players by runs in ODI": {
        "level": "🔴 Advanced",
        "description": "Players ranked by ODI runs using RANK().",
        "sql": """
SELECT player_name, runs, batting_average,
       RANK() OVER (ORDER BY runs DESC) AS run_rank
FROM player_stats
WHERE format = 'ODI';
        """
    },

    "22. Cumulative runs by player": {
        "level": "🔴 Advanced",
        "description": "Total runs across all formats per player.",
        "sql": """
SELECT player_name,
       SUM(runs)                      AS total_runs,
       SUM(wickets)                   AS total_wickets,
       ROUND(AVG(batting_average), 2) AS avg_batting,
       ROUND(AVG(strike_rate), 2)     AS avg_strike_rate
FROM player_stats
GROUP BY player_name
ORDER BY total_runs DESC;
        """
    },

    "23. Matches played at each venue": {
        "level": "🔴 Advanced",
        "description": "How many matches were played at each venue.",
        "sql": """
SELECT venue, COUNT(*) AS matches_played
FROM matches
GROUP BY venue
ORDER BY matches_played DESC;
        """
    },

    "24. Players with 1000+ runs and 5+ wickets": {
        "level": "🔴 Advanced",
        "description": "Players who have runs > 1000 AND wickets > 5.",
        "sql": """
SELECT player_name, format, runs, wickets,
       batting_average, strike_rate
FROM player_stats
WHERE runs > 1000 AND wickets > 5
ORDER BY runs DESC;
        """
    },

    "25. Overall player performance summary": {
        "level": "🔴 Advanced",
        "description": "Complete summary ranking all players by total contribution.",
        "sql": """
SELECT ps.player_name, p.country, p.role,
       SUM(ps.runs)                      AS total_runs,
       SUM(ps.wickets)                   AS total_wickets,
       ROUND(AVG(ps.batting_average), 2) AS avg_batting,
       ROUND(AVG(ps.strike_rate), 2)     AS avg_strike_rate,
       RANK() OVER (ORDER BY SUM(ps.runs) DESC) AS overall_rank
FROM player_stats ps
JOIN players p ON ps.player_name = p.player_name
GROUP BY ps.player_name, p.country, p.role
ORDER BY total_runs DESC;
        """
    },
}


# ─────────────────────────────────────────────
# PAGE LAYOUT
# ─────────────────────────────────────────────
def show():
    st.title("📊 Cricket SQL Analytics")
    st.markdown("---")

    st.subheader("🔍 Database Query Questions")

    question_list = list(QUERIES.keys())
    selected = st.selectbox("📋 Select a question to analyze:", question_list)

    query_info = QUERIES[selected]

    st.markdown(f"### {selected}")
    st.markdown(f"**Level:** {query_info['level']}")
    st.markdown(f"**Description:** {query_info['description']}")

    with st.expander("🔎 View SQL Query"):
        st.code(query_info["sql"], language="sql")

    if st.button("🚀 Execute Query"):
        with st.spinner("Running query..."):
            df = run_query(query_info["sql"])

        if df is not None:
            if df.empty:
                st.warning("⚠️ Query ran successfully but returned no results.")
            else:
                st.success(f"✅ {len(df)} row(s) returned.")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name=f"{selected[:30].replace(' ', '_')}.csv",
                    mime="text/csv"
                )

    with st.expander("🗄️ Database Information"):
        st.markdown("""
**Your Tables in `cricket_db`:**
| Table | Columns |
|-------|---------|
| `players` | player_id, player_name, country, role, batting_style, bowling_style |
| `teams` | team_id, team_name, country |
| `venues` | venue_id, venue_name, city, country, capacity |
| `matches` | match_id, team1, team2, winner, venue, match_date |
| `player_stats` | stat_id, player_name, format, runs, wickets, batting_average, strike_rate |
        """)


if __name__ == "__main__":
    show()