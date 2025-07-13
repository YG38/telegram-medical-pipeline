from typing import List

from .database import get_conn


def get_top_products(limit: int = 10):
    sql = """
        SELECT LOWER(product) AS product, COUNT(*) AS cnt
        FROM (
            SELECT unnest(string_to_array(message, ' ')) AS product
            FROM mart.fct_messages
        ) sub
        GROUP BY product
        ORDER BY cnt DESC
        LIMIT %s;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()


def get_channel_activity(channel_id: int):
    sql = """
        SELECT date_id AS date, COUNT(*) AS message_count
        FROM mart.fct_messages
        WHERE channel_id = %s
        GROUP BY date
        ORDER BY date;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (channel_id,))
            return cur.fetchall()


def search_messages(query: str):
    sql = """
        SELECT message_id, channel_id, message
        FROM mart.fct_messages
        WHERE message ILIKE %s
        LIMIT 100;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f"%{query}%",))
            return cur.fetchall()
