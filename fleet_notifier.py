import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class FleetNotifier:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.db_connection.cursor(dictionary=True)

    def check_expiring(self):
        today = datetime.now().date()
        self.cursor.execute("""
            SELECT * FROM vehicles 
            WHERE is_active = TRUE AND (
                DATEDIFF(tech_inspection_expiry, %s) IN (3, 7, 30) OR
                DATEDIFF(oc_insurance_expiry, %s) IN (3, 7, 30)
            )
        """, (today, today))
        return self.cursor.fetchall()

    def send_email(self, vehicle, expiry_type, days_left):
        expiry_date = vehicle[f"{expiry_type}_expiry"]

        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_USER')
        msg['To'] = os.getenv('NOTIFICATION_RECIPIENT')
        msg['Subject'] = f"Przypomnienie: {expiry_type.upper()} kończy się za {days_left} dni"

        body = f"""
Pojazd: {vehicle['brand']} {vehicle['model']} ({vehicle['registration_number']})
{expiry_type.upper()} ważne do: {expiry_date}
Pozostało dni: {days_left}
"""
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as server:
                server.starttls()
                server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)
            print(f"Wysłano powiadomienie dla {vehicle['registration_number']}")
        except Exception as e:
            print(f"Błąd wysyłania: {e}")

    def run(self):
        vehicles = self.check_expiring()
        today = datetime.now().date()

        for vehicle in vehicles:
            for expiry_type in ['tech_inspection', 'oc_insurance']:
                expiry_date = vehicle[f"{expiry_type}_expiry"]
                days_left = (expiry_date - today).days

                if days_left in (3, 7, 30):
                    self.send_email(vehicle, expiry_type, days_left)

        self.db_connection.close()

if __name__ == "__main__":
    notifier = FleetNotifier()
    notifier.run()
