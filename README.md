# 🍔 Food Order Chatbot (Dialogflow + FastAPI + MySQL)

This is an AI-powered food ordering chatbot that uses **Dialogflow** as the conversational interface, **FastAPI** for backend services, and **MySQL** as the database. The chatbot can display menu items, take orders, calculate total price, and return a unique order ID to the customer.

> 🎯 [Try the chatbot demo on Dialogflow](https://bot.dialogflow.com/db9879f0-d035-4906-9c92-537c5c5b5ae1)  
> ⚠️ Note: Real-time pricing and order ID functionality work **only** when the FastAPI backend and MySQL database are running locally. This demo shows chatbot logic but not backend integration.

---

## ✨ Features

- Conversational food ordering via Dialogflow
- Menu items and prices stored in MySQL database
- Handles item availability and confirms orders
- Generates unique order IDs for each order
- Calculates and displays total price
- Backend implemented using FastAPI
- Dialogflow trained with multiple query examples

---

## 🧰 Tech Stack

| Layer    | Technology       |
| -------- | ---------------- |
| Frontend | Dialogflow       |
| Backend  | FastAPI (Python) |
| Database | MySQL            |

---

## 📁 Project Structure

````bash
food-chatbot/
├── backend/
│ ├── main.py # FastAPI backend
│ ├── database.py # MySQL connection and queries
│ └── models.py # (Optional) data models
├── dialogflow-agent/ # Dialogflow intents and config
└── README.md
````
---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/food-chatbot.git
cd food-chatbot
````

# 🍔 FastAPI + Dialogflow Food Ordering Chatbot

An AI-powered food ordering assistant using FastAPI, Dialogflow, and MySQL.

---

## 2. Backend Setup

### ✅ Install dependencies:

```bash
pip install fastapi uvicorn mysql-connector-python
````

Configure `database.py` with your local MySQL credentials and ensure your `food_items` table is created.

### 🚀 Run the FastAPI server:

```bash
uvicorn main:app --reload
```

---

## 3. Dialogflow Setup

1. Go to [Dialogflow Console](https://dialogflow.cloud.google.com/)
2. Create or import an agent
3. Add intents and training phrases to match the provided functionality

> 📝 **Notes**
>
> - The Dialogflow demo works without the backend but won't show **total price** or **order ID** unless the backend is running locally.
> - Make sure to have **MySQL installed** and a `food_items` table containing **item names and prices**.

---

## 🔮 Future Improvements

- 🚀 Deploy backend API using services like **Heroku**, **Railway**, or **AWS**
- 🌐 Host the MySQL database in the cloud
- 🔐 Add user authentication and order history
- 💳 Integrate payment gateway and delivery tracking
- 🎨 Create a visual frontend using **React** or **Flutter**

---

## 📽️ Demo

🎯 **Live Dialogflow Chatbot Demo**  
_Coming soon or available upon request._

---

## 👨‍💻 Author

**Mehmood**  
AI Researcher & Developer | FastAPI • Dialogflow • MySQL  
🔗 [LinkedIn](https://www.linkedin.com)

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

> Let me know if you'd like a sample `.sql` file to preload food items or a badge section for GitHub (e.g., stars, license, etc.).
