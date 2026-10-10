# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

An interactive, multi-page **Streamlit** dashboard that combines live data from the **Cricbuzz Cricket API** with a **SQL database** to deliver real-time match updates, player statistics, SQL-driven analytics, and full CRUD management.

> Built as part of the **GUVI × HCL** Data Science program · Domain: **Sports Analytics**

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Database Schema](#-database-schema)
- [SQL Analytics](#-sql-analytics-25-queries)
- [Usage](#-usage)
- [Business Use Cases](#-business-use-cases)
- [Coding Standards](#-coding-standards)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## ✨ Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, tools used, usage instructions, and navigation |
| ⚡ **Live Matches** | Ongoing matches from the Cricbuzz API with scorecards, batsmen/bowler info, match status, and venue details |
| 📊 **Top Player Stats** | Top batting and bowling charts (most runs, highest score, most wickets, etc.) fetched via the API |
| 🔍 **SQL Queries & Analytics** | 25 SQL queries (beginner → advanced) run on the database, with results shown as interactive tables |
| 🛠 **CRUD Operations** | Add, view, update, and delete player records through a form-based UI |

---

## 🧰 Tech Stack

- **Language:** Python 3.9+
- **Web Framework:** Streamlit
- **Data Handling:** pandas, JSON
- **API Access:** `requests` (REST)
- **Database:** SQL (database-agnostic: SQLite / MySQL / PostgreSQL)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
cricbuzz_livestats/
│
├── app.py                  # Main entry point for the Streamlit app
├── requirements.txt        # Required Python packages
├── README.md               # Project overview and setup instructions
│
├── pages/                  # Individual Streamlit pages
│   ├── home.py             # Overview and About the Project page
│   ├── live_matches.py     # Live match data from the Cricbuzz API
│   ├── top_stats.py        # Top batting/bowling stats
│   ├── sql_queries.py      # SQL query interface and analytics
│   └── crud_operations.py  # CRUD on player stats
│
├── utils/
│   └── db_connection.py    # Centralized SQL database connection logic
│
└── notebooks/
    └── data_fetching.ipynb # Testing API calls and loading data into the DB
```

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/cricbuzz_livestats.git
cd cricbuzz_livestats
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Core dependencies: `streamlit`, `pandas`, `requests`, and your database connector (e.g. `mysql-connector-python`, `psycopg2`, or the built-in `sqlite3`).

### 4. Configure credentials

See [Configuration](#-configuration) below.

### 5. Load the data

Run `notebooks/data_fetching.ipynb` to fetch data from the Cricbuzz API and populate your database tables.

### 6. Launch the app

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

---

## 🔐 Configuration

API keys and database credentials are **never hard-coded**. Store them in a `.env` file (or Streamlit's `secrets.toml`) in the project root:

```env
# Cricbuzz API (e.g. via RapidAPI)
RAPIDAPI_KEY=your_api_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com

# Database
DB_TYPE=mysql          # sqlite | mysql | postgresql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cricbuzz_db
DB_USER=your_username
DB_PASSWORD=your_password
```

> ⚠️ Add `.env` to your `.gitignore` so secrets are never pushed to GitHub.

All database access goes through `utils/db_connection.py`, so switching databases only requires changing the configuration.

---

## 🗄 Database Schema

The database stores players, teams, venues, series, matches, and batting/bowling performance data. Typical tables:

| Table | Purpose |
|-------|---------|
| `players` | Player name, team, role, batting style, bowling style |
| `teams` | Team names and countries |
| `venues` | Venue name, city, country, capacity |
| `series` | Series name, host country, match type, start date, matches planned |
| `matches` | Match description, teams, venue, date, toss, result, victory margin/type |
| `batting_stats` / `bowling_stats` | Runs, balls, strike rate, wickets, economy, by format |

> Update this table to match your final schema. Table definitions and sample data are available in the schema file / notebook.

---

## 🧮 SQL Analytics (25 Queries)

The **SQL Queries & Analytics** page runs 25 queries across three difficulty levels.

**🟢 Beginner (Q1–Q8)** — `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`
Indian players, recent matches, top ODI run scorers, large venues, team wins, players per role, highest score per format, series started in 2024.

**🟡 Intermediate (Q9–Q16)** — JOINs, subqueries, aggregates
All-rounders (1000+ runs & 50+ wickets), last 20 completed matches, cross-format comparison, home vs away record, 100+ run partnerships, bowling at venues, close-match performers, yearly batting trends since 2020.

**🔴 Advanced (Q17–Q25)** — window functions, CTEs, complex analytics
Toss advantage, most economical bowlers, batting consistency (std. deviation), format-wise averages, weighted player ranking, head-to-head prediction, player form & momentum, best partnerships, quarterly time-series trajectory.

**Performance & quality:** indexes on frequently queried columns, plus NULL checks and data validation in queries.

---

## 💻 Usage

1. **Home** – read the overview and use the sidebar to navigate.
2. **Live Matches** – pick a match to see its scorecard, status, and venue.
3. **Top Stats** – choose a category (runs, wickets, highest score) to view the leaderboard.
4. **SQL Analytics** – select a question from the dropdown and run it to see the result table.
5. **CRUD Operations** – use the forms to create, update, or delete player records and view the changes instantly.

---

## 💼 Business Use Cases

- 📺 **Sports media & broadcasting** – live updates and pre-match player analysis
- 🎮 **Fantasy cricket platforms** – player form and head-to-head insights
- 📈 **Cricket analytics firms** – performance modeling and trend analysis
- 🎓 **Education** – hands-on SQL and API integration practice
- 🎲 **Sports prediction** – historical, form-based, and venue-specific insights

---

## 📏 Coding Standards

- Follows **PEP 8** style guidelines
- Proper **exception handling** for API calls and database operations
- **Modular** functions for each operation
- Clear **comments and docstrings** throughout
- Secure handling of **credentials and API keys**
- **Git** for version control

---

## 🔮 Future Improvements

- Auto-refresh for live scorecards
- Interactive charts (Plotly / Altair) for player trends
- User authentication for CRUD access
- Cloud deployment (Streamlit Community Cloud)

---

## 👤 Author

**Jp**
Computer Science Student · GUVI × HCL Data Science Program
🔗 GitHub: `<your-github-link>` · LinkedIn: `<your-linkedin-link>`

---

⭐ If you found this project useful, consider giving the repo a star!
