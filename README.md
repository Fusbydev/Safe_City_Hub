# Safe City Hub 🚨

A Django-based emergency reporting system that allows users to report incidents, view reports, and interact with administrators. Integrated with MongoDB, SQLite, and supports file uploads and Google social authentication.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Safe_City_Hub.git](https://github.com/Fusbydev/Safe_City_Hub.git
cd Safe_City_Hub
```

---

### 2. Create & Configure `.env` File

Inside the `Safe_City_Hub/` directory, create a `.env` file:

```bash
touch .env
```

Then add your environment variables:

```
MONGO_URI=HINGIN NYO SAKIN
GEMINI_API_KEY=HINGIN NYO SAKIN
```

> 💡 **Tip:** Never commit your `.env` file to GitHub. It's automatically ignored via `.gitignore`.

---

### 3. Install Dependencies

Ensure you have Python 3.10+ and `pipenv` or `venv` installed. Then run:

```bash
pip install -r requirements.txt
```

---

### 4. Run the Development Server

```bash
python manage.py runserver localhost:8080
```

Visit: [http://localhost:8080](http://localhost:8080)

---

### 5. Apply Migrations & Create Superuser

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
