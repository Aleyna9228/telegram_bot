# 🏥 Telegram Patient Monitoring Bot

A **console-free Telegram bot application** built using **Python** and **Object-Oriented Programming (OOP)** principles.  
The bot allows users to enter basic vital signs (blood sugar, blood pressure, fever) via Telegram commands, stores the data persistently, and notifies a hospital/admin chat in real time.

---

## 🚀 Features

✔ Object-Oriented design (Patient, PatientDatabase classes)  
✔ Telegram bot integration  
✔ Multiple patient support (each chat represents one patient)  
✔ Persistent data storage using NDJSON format  
✔ Automatic hospital/admin notifications  
✔ Input validation with `try/except`  
✔ Latest patient status display  
✔ Safe message handling for blocked users  

---

## 🧠 How It Works

### 📡 Telegram Bot Interaction

- The application runs as a **Telegram bot**
- Users interact with the system via Telegram commands
- Each chat ID uniquely represents a patient

### 🔄 Workflow

1. User starts the bot using `/start`
2. A new patient object is created if the user is new
3. Vital signs are entered using commands:
   - `/sugar`
   - `/pressure`
   - `/fever`
4. Inputs are validated and stored in a file
5. Hospital/admin chat receives notifications
6. User can check their latest data using `/status`

---

## 🗂 Data Storage

All patient records are stored in the file:

patients.ndjson
Each line represents one patient record:

json
{
  "id": 123456789,
  "sugar": 90,
  "pressure": 120,
  "fever": 38
}

🏗️ Class Overview

🔹 Patient Class

Represents a single patient.

Attributes:
	•	id
	•	sugar
	•	pressure
	•	fever

Methods:
	•	update_sugar(value)
	•	update_pressure(value)
	•	update_fever(value)

⸻

🔹 PatientDatabase Class

Manages persistent storage of patient data.

Responsibilities:
	•	Saving patient records
	•	Loading stored data
	•	Retrieving patient history by ID

⸻

📸 Example Program Output (Telegram Chat)
Welcome!
You can enter your vital signs using the following commands:
/Sugar 90
/Pressure 120
/Fever 38
/Status


===== Patient Status =====
ID: 123456789
Sugar: 90
Pressure: 120
Fever: 38
=========================

Technologies Used
	•	Programming Language: Python
	•	Development Environment: Visual Studio Code
	•	Libraries:
	•	os
	•	json
	•	telebot
	•	ApiTelegramException


👥 Group Members ( coder)
Aleyna Başar 20232892 / Mustafa Çiçek 20231391 / Kerem Aykaç 20231425 / Emine Öz 20243033

📄 Course Information
	•	Course: AII108 Object Oriented Programming
	•	Instructor: AMR ABDELBARI
	•	Date: 17.12.2025

Conclusion

This project demonstrates the effective use of Object-Oriented Programming principles combined with Telegram bot development in Python.
By managing real-time user interaction, persistent data storage, and automated notifications, the system provides a practical solution for basic patient monitoring.







