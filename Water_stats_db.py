import sqlite3
from datetime import datetime, timedelta

DB_FILE = "stats.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id        INTEGER PRIMARY KEY,
            username       TEXT,
            first_name     TEXT,
            first_seen     TEXT,
            last_seen      TEXT,
            lang           TEXT DEFAULT 'ru',
            total_requests INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            event_type  TEXT,
            detail      TEXT,
            created_at  TEXT
        )
    """)
    conn.commit()
    conn.close()

def track(user_id, username, first_name, lang, event_type, detail=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO users (user_id, username, first_name, first_seen, last_seen, lang, total_requests)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(user_id) DO UPDATE SET
            username       = excluded.username,
            first_name     = excluded.first_name,
            last_seen      = excluded.last_seen,
            lang           = excluded.lang,
            total_requests = total_requests + 1
    """, (user_id, username or "", first_name or "", now, now, lang or "ru"))
    c.execute("""
        INSERT INTO events (user_id, event_type, detail, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, event_type, detail, now))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    total_users    = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_requests = c.execute("SELECT SUM(total_requests) FROM users").fetchone()[0] or 0

    users_30 = c.execute("""
        SELECT COUNT(*) FROM users
        WHERE DATE(last_seen) >= DATE('now', '-30 days')
    """).fetchone()[0]

    new_30 = c.execute("""
        SELECT COUNT(*) FROM users
        WHERE DATE(first_seen) >= DATE('now', '-30 days')
    """).fetchone()[0]

    new_prev = c.execute("""
        SELECT COUNT(*) FROM users
        WHERE DATE(first_seen) >= DATE('now', '-60 days')
        AND DATE(first_seen) < DATE('now', '-30 days')
    """).fetchone()[0]

    requests_30 = c.execute("""
        SELECT COUNT(*) FROM events
        WHERE DATE(created_at) >= DATE('now', '-30 days')
    """).fetchone()[0]

    requests_prev = c.execute("""
        SELECT COUNT(*) FROM events
        WHERE DATE(created_at) >= DATE('now', '-60 days')
        AND DATE(created_at) < DATE('now', '-30 days')
    """).fetchone()[0]

    # Напоминания включены/выключены
    reminders_started = c.execute("""
        SELECT COUNT(*) FROM events WHERE event_type = 'reminders_on'
        AND DATE(created_at) >= DATE('now', '-30 days')
    """).fetchone()[0]

    reminders_stopped = c.execute("""
        SELECT COUNT(*) FROM events WHERE event_type = 'reminders_off'
        AND DATE(created_at) >= DATE('now', '-30 days')
    """).fetchone()[0]

    # Сколько напоминаний реально отправлено
    reminders_sent = c.execute("""
        SELECT COUNT(*) FROM events WHERE event_type = 'reminder_sent'
        AND DATE(created_at) >= DATE('now', '-30 days')
    """).fetchone()[0]

    # Расчётов нормы воды
    norm_calcs = c.execute("""
        SELECT COUNT(*) FROM events WHERE event_type = 'norm_calculated'
        AND DATE(created_at) >= DATE('now', '-30 days')
    """).fetchone()[0]

    # Популярные интервалы
    top_intervals = c.execute("""
        SELECT detail, COUNT(*) as cnt
        FROM events
        WHERE event_type = 'interval_set'
        AND DATE(created_at) >= DATE('now', '-30 days')
        GROUP BY detail
        ORDER BY cnt DESC
    """).fetchall()

    # Языки
    lang_stats = c.execute("""
        SELECT lang, COUNT(*) as cnt
        FROM users
        GROUP BY lang
        ORDER BY cnt DESC
    """).fetchall()

    # Смен языка
    lang_changes = c.execute("""
        SELECT detail, COUNT(*) as cnt
        FROM events
        WHERE event_type = 'lang_changed'
        AND DATE(created_at) >= DATE('now', '-30 days')
        GROUP BY detail
        ORDER BY cnt DESC
    """).fetchall()

    # График новых по дням
    daily_new = c.execute("""
        SELECT DATE(first_seen) as day, COUNT(*) as cnt
        FROM users
        WHERE DATE(first_seen) >= DATE('now', '-30 days')
        GROUP BY day ORDER BY day ASC
    """).fetchall()
    daily_map = {row[0]: row[1] for row in daily_new}
    today = datetime.now().date()
    daily_chart = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        daily_chart.append((day.strftime("%d.%m"), daily_map.get(day_str, 0)))

    # Последние 5 пользователей
    recent_users = c.execute("""
        SELECT first_name, username, first_seen, lang
        FROM users ORDER BY first_seen DESC LIMIT 5
    """).fetchall()

    conn.close()
    return {
        "total_users":       total_users,
        "total_requests":    total_requests,
        "users_30":          users_30,
        "new_30":            new_30,
        "new_prev":          new_prev,
        "requests_30":       requests_30,
        "requests_prev":     requests_prev,
        "reminders_started": reminders_started,
        "reminders_stopped": reminders_stopped,
        "reminders_sent":    reminders_sent,
        "norm_calcs":        norm_calcs,
        "top_intervals":     top_intervals,
        "lang_stats":        lang_stats,
        "lang_changes":      lang_changes,
        "daily_chart":       daily_chart,
        "recent_users":      recent_users,
    }