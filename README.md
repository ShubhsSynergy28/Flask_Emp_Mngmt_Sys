# 🧑‍💼 Flask Employee Management System

This is a Flask-based **Employee Management System** (EMP Mngmt), similar in structure and functionality to the PHP version. It allows you to add, view, update, and delete employee records using a MySQL database.

---

## 🚀 Features

- Add new employees
- Edit employee details
- Delete employees
- View employee list
- MySQL DB integration
- File upload support (e.g., profile photos or documents)

---

## 🛠️ Project Setup

### 1. 📦 Clone the repository

```bash
git clone https://github.com/yourusername/flask-emp-mngmt.git
cd flask-emp-mngmt
```

### 2. ⚙️ Configure `.env`

Create a `.env` file in the root of your project directory:

```env
PORT=5000
IP=127.0.0.1

MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database_name

UPLOAD_PATH=static/uploads
```

### 3. 🐬 Create Database Tables

Ensure your MySQL server is running.

Check that the database (from `.env`'s `MYSQL_DB`) exists. If not, create it manually or via a script.

Then run:

```bash
python createdb.py
```

This script will create necessary tables inside your specified database.

### 4. 🧰 Verify Tables

After running `createdb.py`, verify the tables by logging into MySQL:

```bash
mysql -u your_mysql_username -p
USE your_database_name;
SHOW TABLES;
```

You should see your employee-related tables listed.

---

## 🏁 Run the App

```bash
flask run
```

Or (if using `app.py`):

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 📁 Folder Structure

```
flask-emp-mngmt/
├── static/
│   └── uploads/
├── templates/
│   └── ...
├── createdb.py
├── app.py
├── .env
└── README.md
```

---

## ✅ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
Flask
python-dotenv
mysql-connector-python
```

---

## 🙌 Credits

- Original PHP version inspiration
- Flask Documentation
- Your contributions!

