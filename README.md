# 📊 Automated Reporting System  

## **🔹 Project Overview**  
The Automated Reporting System is designed to fetch student data from MySQL and generate reports in **PDF, Excel, and Dashboards**.

---

## **🚀 Features**  
✔ Fetches student records from MySQL  
✔ Generates **PDF reports** for each student  
✔ Creates **Excel reports** for batch processing  
✔ Provides an **interactive dashboard** for analytics  

---

## **🛠 Prerequisites**  
1️⃣ **Install Python** (if not already installed)  
   - Download from [python.org](https://www.python.org/downloads/)  
   - Verify installation:
     ```sh
     python --version
     ```

2️⃣ **Install MySQL Server**  
   - Download from [mysql.com](https://dev.mysql.com/downloads/mysql/)  
   - Create a database **manually** or let the script create it.  

---

## **📂 Project Setup**  
### **1️⃣ Clone the Repository**# 📊 Automated Reporting System  

## **🛠 Project Overview**  
The Automated Reporting System is designed to fetch student data from MySQL and generate reports in **PDF, Excel, and Dashboards**.

---

## **🚀 Features**  
✔ Fetches student records from MySQL  
✔ Generates **PDF reports** for each student  
✔ Creates **Excel reports** for batch processing  
✔ Provides an **interactive dashboard** for analytics  

---

## **🛠 Prerequisites**  
### **1. Install Python (if not already installed)**  
- Download from [python.org](https://www.python.org/downloads/)  
- Verify installation:
  ```sh
  python --version
  ```

### **2. Install MySQL Server**  
- Download from [mysql.com](https://dev.mysql.com/downloads/mysql/)  
- Create a database **manually** or let the script create it.  

---

## **📂 Project Setup**  
### **1. Clone the Repository**  
```sh
git clone https://github.com/your-username/Automated_Reporting_System.git
cd Automated_Reporting_System
```

### **2. Create a Virtual Environment (Recommended)**  
```sh
python -m venv venv
```

### **3. Activate Virtual Environment**  
- **Windows:**  
  ```sh
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux:**  
  ```sh
  source venv/bin/activate
  ```

### **4. Install Required Dependencies**  
```sh
pip install -r requirements.txt
```

### **5. Configure Database**  
- Open **`database/db_config.py`** and update the MySQL credentials:  
  ```python
  DB_CONFIG = {
      "host": "localhost",
      "user": "root",
      "password": "yourpassword",
      "database": "StudentReportingDB"
  }
  ```

- Create the database and tables (only needed for first-time setup):  
  ```sh
  python -m database.setup_db
  ```

- Insert sample data for testing (optional):  
  ```sh
  python -m utils.insert_sample_data
  ```

---

## **🎯 Running the Project**  
To **generate reports** and **start the dashboard**, run:  
```sh
python main.py
```

---

## **📊 Running Individual Components**  
| Task | Command |
|------|---------|
| Generate PDF Reports | `python -m reports.generate_pdf` |
| Generate Excel Reports | `python -m reports.generate_excel` |
| Start Dashboard | `python -m reports.generate_dashboard` |

The dashboard will be available at: **[http://127.0.0.1:8050](http://127.0.0.1:8050)**  

---

## **🛠 Troubleshooting**  
**1. `ModuleNotFoundError` for `database` or `utils`?**  
➡ Run the script using `-m`, e.g.:  
```sh
python -m utils.insert_sample_data
```

**2. MySQL connection error?**  
➡ Make sure MySQL is **running** and **credentials** in `db_config.py` are correct.

---

## **🔧 Contributors**  
👨‍💻 **KRISHNA BHAGAVAN** – Developer  
👨‍💻 **NAREEN** – Contributor   

---
