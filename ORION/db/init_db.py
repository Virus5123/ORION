from ORION.db.database import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. статик данные
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS instruments (
        uid TEXT PRIMARY KEY,
        ticker TEXT,
        name TEXT,
        sector TEXT,
        instrument_type TEXT
    )
    """)

    # 2. юзер данные
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        user_id INTEGER,
        account_id TEXT PRIMARY KEY
    )
    """)

    # 3. динамик данные
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios (
        account_id TEXT,
        instrument_uid TEXT,
        quantity REAL,
        avg_price REAL,
        updated_at INTEGER,
        PRIMARY KEY (account_id, instrument_uid)
    )
    """)

    # 4. ттл данные
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_cache (
        instrument_uid TEXT PRIMARY KEY,
        price REAL,
        nkd REAL,
        updated_at INTEGER
    )
    """)

    conn.commit()
    conn.close()