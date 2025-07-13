import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client

load_dotenv()

def get_theme_for_today(conn):
    today = datetime.now().strftime('%A')
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM foodthemes WHERE theme_day = %s", (today,))
        row = cur.fetchone()
        return row[0] if row else None

def send_sms(theme_name):
    try:
        client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        client.messages.create(
            from_=os.getenv("TWILIO_PHONE_FROM"),
            to=os.getenv("TWILIO_PHONE_TO"),
            body=f"Today's theme is: {theme_name}"
        )
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def main():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT"))
        )
        theme = get_theme_for_today(conn)
        if theme:
            send_sms(theme)
        else:
            print("No theme found for today.")
    except Exception as e:
        print(f"Database connection or query failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    main()
