# Safe City Hub 🚨

A Django-based emergency reporting system that allows users to report incidents, view reports, and interact with administrators. Integrated with MongoDB, SQLite, and supports file uploads and Google social authentication.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Fusbydev/Safe_City_Hub.git
cd Safe_City_Hub
```

---

### 2. Create & Configure `.env` File

Inside the `Safe_City_Hub/` directory, create a `.env` file:

```bash
touch .env
```
**OR** manually create a `.env` file inside the `Safe_City_Hub` folder.

Add the following environment variables:

```
MONGO_URI=HINGIN NYO SAKIN
GEMINI_API_KEY=HINGIN NYO SAKIN
```

> 💡 **Tip:** Never commit your `.env` file to GitHub. It's automatically ignored via `.gitignore`.

---

### 3. Create and Activate Virtual Environment

Make sure you are using Python 3.10+.

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

---

### 4. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

---

### 5. Run the Development Server

```bash
python manage.py runserver localhost:8080
```

Then open your browser and visit: [http://localhost:8080](http://localhost:8080)

---

### 6. Apply Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧠 Features

- 📍 Emergency reporting with location mapping
- 🧾 Admin dashboard for reviewing reports
- 📸 File upload and GridFS storage for evidence
- 👤 Google social authentication via `django-allauth`
- 💬 Embedded comments system
- 📊 MongoDB + SQLite hybrid database support

---

## 🛠 Tech Stack

- Django, MongoEngine/Djongo, GridFS
- Bootstrap 5 (frontend)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Contributing

Feel free to fork the repo, submit pull requests, or file issues. Let's make cities safer together!
