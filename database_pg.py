import os
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    return psycopg.connect(
        DATABASE_URL
    )
  if __name__ == "__main__":

    conn = get_connection()

    print("✅ PostgreSQL Connected")

    conn.close()
