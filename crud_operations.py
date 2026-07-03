import streamlit as st
import mysql.connector
import pandas as pd



# DATABASE CONNECTION

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



# CRUD FUNCTIONS

def read_players():
    conn = get_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql("SELECT * FROM players ORDER BY player_id;", conn)
        return df
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None
    finally:
        conn.close()


def create_player(player_name, country, role, batting_style, bowling_style):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO players (player_name, country, role, batting_style, bowling_style)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (player_name, country, role, batting_style, bowling_style))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False
    finally:
        conn.close()


def update_player(player_id, player_name, country, role, batting_style, bowling_style):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = """
            UPDATE players
            SET player_name=%s, country=%s, role=%s,
                batting_style=%s, bowling_style=%s
            WHERE player_id=%s
        """
        cursor.execute(query, (player_name, country, role, batting_style, bowling_style, player_id))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False
    finally:
        conn.close()


def delete_player(player_id):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False
    finally:
        conn.close()



# PAGE LAYOUT

def show():
    st.title("🔧 CRUD Operations")
    st.subheader("📝 Create, Read, Update, Delete Player Records")
    st.markdown("---")

    operation = st.selectbox(
        "Choose an operation:",
        [
            "📋 Read (View Players)",
            "➕ Create (Add Player)",
            "✏️ Update (Edit Player)",
            "🗑️ Delete (Remove Player)"
        ]
    )

    # READ 
    if operation == "📋 Read (View Players)":
        st.subheader("📋 All Players")

        df = read_players()
        if df is not None:
            if df.empty:
                st.warning("No players found in database.")
            else:
                st.success(f"✅ {len(df)} players found.")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name="players.csv",
                    mime="text/csv"
                )

    # CREATE 
    elif operation == "➕ Create (Add Player)":
        st.subheader("➕ Add New Player")

        with st.form("create_form"):
            player_name   = st.text_input("Player Name")
            country       = st.text_input("Country")
            role          = st.selectbox("Role", [
                                "Batsman", "Bowler",
                                "All-rounder", "Wicket-keeper"
                            ])
            batting_style = st.selectbox("Batting Style", [
                                "Right-hand bat", "Left-hand bat"
                            ])
            bowling_style = st.text_input("Bowling Style (e.g. Right-arm fast)")

            submitted = st.form_submit_button("➕ Add Player")

            if submitted:
                if not player_name or not country:
                    st.warning("⚠️ Player Name and Country are required!")
                else:
                    success = create_player(
                        player_name, country, role,
                        batting_style, bowling_style
                    )
                    if success:
                        st.success(f"✅ Player '{player_name}' added successfully!")
                        st.balloons()

    # UPDATE 
    elif operation == "✏️ Update (Edit Player)":
        st.subheader("✏️ Edit Existing Player")

        df = read_players()
        if df is not None and not df.empty:

            player_names = df["player_name"].tolist()
            selected_name = st.selectbox("Select Player to Edit:", player_names)

            selected_row = df[df["player_name"] == selected_name].iloc[0]

            with st.form("update_form"):
                player_name   = st.text_input("Player Name",   value=selected_row["player_name"])
                country       = st.text_input("Country",       value=selected_row["country"])
                role          = st.selectbox("Role", [
                                    "Batsman", "Bowler",
                                    "All-rounder", "Wicket-keeper"
                                ],
                                index=["Batsman","Bowler","All-rounder","Wicket-keeper"].index(
                                    selected_row["role"]
                                ) if selected_row["role"] in
                                    ["Batsman","Bowler","All-rounder","Wicket-keeper"] else 0
                                )
                batting_style = st.selectbox("Batting Style", [
                                    "Right-hand bat", "Left-hand bat"
                                ],
                                index=0 if selected_row["batting_style"] == "Right-hand bat" else 1
                                )
                bowling_style = st.text_input("Bowling Style", value=selected_row["bowling_style"])

                submitted = st.form_submit_button("✏️ Update Player")

                if submitted:
                    success = update_player(
                        int(selected_row["player_id"]),
                        player_name, country, role,
                        batting_style, bowling_style
                    )
                    if success:
                        st.success(f"✅ Player '{player_name}' updated successfully!")

    # DELETE 
    elif operation == "🗑️ Delete (Remove Player)":
        st.subheader("🗑️ Remove Player")

        df = read_players()
        if df is not None and not df.empty:

            player_names  = df["player_name"].tolist()
            selected_name = st.selectbox("Select Player to Delete:", player_names)
            selected_row  = df[df["player_name"] == selected_name].iloc[0]

            st.warning(f"⚠️ You are about to delete **{selected_name}**. This cannot be undone!")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🗑️ Yes, Delete"):
                    success = delete_player(int(selected_row["player_id"]))
                    if success:
                        st.success(f"✅ Player '{selected_name}' deleted successfully!")
                        st.rerun()

            with col2:
                if st.button("❌ Cancel"):
                    st.info("Deletion cancelled.")


if __name__ == "__main__":
    show()
