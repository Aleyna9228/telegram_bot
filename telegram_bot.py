import os
import json
import telebot
from telebot.apihelper import ApiTelegramException

TOKEN = "8382352529:AAGAQoh1m-OzxTnJtGSzzW0oE_L6E-IZuuQ" 
bot = telebot.TeleBot(TOKEN)

hospital_id = -1003399670514 

patients = {}


class Patient:
    def __init__(self, id):
        self.id = id
        self.sugar = None
        self.pressure = None
        self.fever = None

    def update_sugar(self, value):
        self.sugar = float(value)

    def update_pressure(self, value):
        self.pressure = float(value)

    def update_fever(self, value):
        self.fever = float(value)


class PatientDatabase:
    def __init__(self, filename):
        self.filename = filename

    def save(self, patient: Patient):
        record = {
            "id": patient.id,
            "sugar": patient.sugar,
            "pressure": patient.pressure,
            "fever": patient.fever,
        }
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def load_all(self):
        records = []
        if not os.path.exists(self.filename):
            return records

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))
        return records

    def get_patient_history(self, patient_id):
        return [r for r in self.load_all() if r["id"] == patient_id]


db = PatientDatabase("patients.ndjson")


def safe_send(chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except ApiTelegramException as e:
        if e.error_code == 403:
            print(f"[403] Messages cannot be sent to this chat.: {chat_id}")
            patients.pop(chat_id, None)
            return
        raise


def ensure_patient(user_id):
    if user_id not in patients:
        print(f"Creating a new patient: {user_id}")
        patients[user_id] = Patient(user_id)
    return patients[user_id]


def notify_hospital(text, source_chat_id):
    if hospital_id is not None and source_chat_id != hospital_id:
        safe_send(hospital_id, text)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    patient = ensure_patient(user_id)

    text = (
        "Welcome!\n"
        "You can enter your vital signs using the following commands.:\n"
        "/Sugar 90\n"
        "/Pressure 120\n"
        "/Fever 38\n"
        "/Status  → shows your last values.\n"
    )
    safe_send(user_id, text)

    notify_hospital(
        f" New patient/chat log:\n"
        f"ID: {patient.id}",
        source_chat_id=user_id
    )


@bot.message_handler(commands=['sugar'])
def sugar(message):
    user_id = message.chat.id
    parts = message.text.split()

    if len(parts) < 2:
        safe_send(user_id, "Usage: /sugar 90")
        return

    value_str = parts[1]

    try:
        value = float(value_str)
    except ValueError:
        safe_send(user_id, "Please enter a numerical value. Example: /sugar 90")
        return

    patient = ensure_patient(user_id)
    patient.update_sugar(value)
    db.save(patient)

    safe_send(user_id, f"Sugar Updated: {value}")

    notify_hospital(
        f"New sugar record:\n"
        f"Patient/Chat ID: {user_id}\n"
        f"Sugar: {value}",
        source_chat_id=user_id
    )


@bot.message_handler(commands=['pressure'])
def pressure(message):
    user_id = message.chat.id
    parts = message.text.split()

    if len(parts) < 2:
        safe_send(user_id, "Usage: /pressure 120")
        return

    value_str = parts[1]

    try:
        value = float(value_str)
    except ValueError:
        safe_send(user_id, "Please enter a numerical value. Example: /pressure 120")
        return

    patient = ensure_patient(user_id)
    patient.update_pressure(value)
    db.save(patient)

    safe_send(user_id, f"Pressure updated: {value}")

    notify_hospital(
        f"New pressure record:\n"
        f"Patient/Chat ID: {user_id}\n"
        f"Pressure: {value}",
        source_chat_id=user_id
    )


@bot.message_handler(commands=['fever'])
def fever(message):
    user_id = message.chat.id
    parts = message.text.split()

    if len(parts) < 2:
        safe_send(user_id, "Usage: /fever 38")
        return

    value_str = parts[1]

    try:
        value = float(value_str)
    except ValueError:
        safe_send(user_id, "Please enter a numerical value. Example: /fever 38")
        return

    patient = ensure_patient(user_id)
    patient.update_fever(value)
    db.save(patient)

    safe_send(user_id, f"Fever Updated: {value}")

    notify_hospital(
        f"New fever record:\n"
        f"Patient/Chat ID: {user_id}\n"
        f"Fever: {value}",
        source_chat_id=user_id
    )


@bot.message_handler(commands=['status'])
def status(message):
    """Show the patient's latest values."""
    user_id = message.chat.id
    if user_id not in patients:
        safe_send(user_id, "You don't have any measurements saved yet. Start with /start..")
        return

    p = patients[user_id]
    text = (
        f"ID: {p.id}\n"
        f"Sugar: {p.sugar}\n"
        f"Pressure: {p.pressure}\n"
        f"Fever: {p.fever}\n"
    )
    safe_send(user_id, text)

    notify_hospital(
        f"STATUS request:\n"
        f"Patient/Chat ID: {user_id}\n"
        f"Sugar: {p.sugar}\n"
        f"Pressure: {p.pressure}\n"
        f"Fever: {p.fever}",
        source_chat_id=user_id
    )


@bot.message_handler(func=lambda m: True)
def debug_all(message):
    print("CHAT INFO → id:", message.chat.id, 
          "| type:", message.chat.type, 
          "| title:", getattr(message.chat, 'title', None))


if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling(skip_pending=True)
