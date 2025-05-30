# 🏙️ Safe City Hub

## 🚀 Live Website

Check out the deployed project here:  
👉 [Safe City Hub](https://safe-city-hub.onrender.com/safecityhub/home/)

---

## 🛠️ Installation Guide

## 📥 1. Clone the repository (branch: updatemike)
```
git clone --branch updatemike --single-branch https://github.com/Fusbydev/Safe_City_Hub.git
```
```
cd Safe_City_Hub
```

## 🧪 2. Create a virtual environment
note: make sure you have python 3.10 version of python to prevent version conflict
```
py -3.10 -m venv venv
```
## ⚙️ 3. Activate the virtual environment (for Windows)
```
venv\Scripts\activate
```
## If you're using macOS/Linux, use:
```
source venv/bin/activate
```

Note: Make sure to make .env file level of manage.py and include the MONGO_URI and GEMINI_API_KEY

## 📦 4. Install dependencies
```
pip install -r requirements.txt
```
## 🚀 5. Run the development server
```
python manage.py runserver localhost:8080
```
