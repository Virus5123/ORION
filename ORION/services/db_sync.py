import time
from decimal import Decimal
from ORION.db.database import get_connection


def upsert_account(user_id: int, account_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO accounts (user_id, account_id)
        VALUES (?, ?)
    """, (user_id, account_id))

    conn.commit()
    conn.close()


def upsert_instrument(uid, ticker, name, sector, instrument_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO instruments
        (uid, ticker, name, sector, instrument_type)
        VALUES (?, ?, ?, ?, ?)
    """, (uid, ticker, name, sector, instrument_type))

    conn.commit()
    conn.close()


def upsert_portfolio(account_id, instrument_uid, quantity, avg_price):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO portfolios
        (account_id, instrument_uid, quantity, avg_price, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(account_id, instrument_uid)
        DO UPDATE SET
            quantity = excluded.quantity,
            avg_price = excluded.avg_price,
            updated_at = excluded.updated_at
    """, (
        account_id,
        instrument_uid,
        float(quantity),
        float(avg_price),
        int(time.time())
    ))

    conn.commit()
    conn.close()