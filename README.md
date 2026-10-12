# College Club Event Management System 🎓

A comprehensive DBMS course project built with **Oracle Database 21c XE**, **Python 3 + Flask**, and **python-oracledb (thin mode)** with a clean, responsive HTML5/CSS3 frontend.

---

## 📁 Repository Structure

```text
college_club_system/
├── sql/
│   ├── schema.sql                      # DDL: Tables, PK, FK, CHECK, and UNIQUE constraints
│   ├── sample_data.sql                 # Sample Data: 10 Students, 5 Clubs, 10 Events, 15 Memberships, 20 Registrations
│   ├── queries.sql                     # Showcase queries (JOIN, GROUP BY, HAVING, subqueries, aggregates)
│   └── views_procedures_triggers.sql  # 2 Views, 1 PL/SQL Stored Procedure, 1 Trigger
├── templates/
│   ├── base.html                       # Base layout, navbar, flash alerts
│   ├── index.html                      # Home dashboard & upcoming events
│   ├── students.html                   # Student roster & add student form
│   ├── clubs.html                      # Club directory, member roster, join club form
│   ├── events.html                     # Events list, new event form, procedure registration, cancel
│   └── reports.html                    # Analytical showcase reports
├── static/
│   ├── style.css                       # Clean, vanilla CSS stylesheet
│   └── er_diagram.jpg                  # High-resolution ER Diagram
├── docs/
│   ├── Review_1_Presentation.pptx      # Review 1 PPT (Problem, ER Model, Schema, 3NF Normalization)
│   ├── Review_2_Presentation.pptx      # Review 2 PPT (Final Working Prototype, Demo Script, PL/SQL)
│   ├── REVIEW_GUIDE.md                 # Step-by-step presentation & demo script
│   └── VIVA_QA.md                      # 15 likely viva questions and answers
├── app.py                              # Flask application with parameterized SQL queries
├── config.py                           # Database credentials & configuration
├── db_local.py                         # Automatic local database fallback
├── load_database.py                    # Database loader script for Oracle XE
├── view_db.py                          # Interactive command-line SQL console
├── test_app.py                         # Automated test suite (6 passing unit tests)
├── college_club_app.exe                # Standalone web app executable (Single-click launcher)
├── view_db.exe                         # Standalone SQL console executable
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Standard git ignore file
└── README.md                           # Project documentation
```

---

## 🚀 Quick Start Guide

### Option 1: Run via Standalone Executable (No Python Required)
You can launch the web application directly without installing Python dependencies:
- Double-click **`college_club_app.exe`** (or run `.\college_club_app.exe` in CMD).
- It will automatically launch the server and open your browser to **`http://127.0.0.1:5000`**.

To use the command-line SQL console without SQL*Plus:
- Run **`view_db.exe`** in CMD.

---

### Option 2: Run via Python

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Web Server:**
   ```bash
   python app.py
   ```
   Open your browser at: **`http://127.0.0.1:5000`**

3. **Run the Interactive SQL Console in CMD:**
   ```bash
   python view_db.py
   ```

4. **Run Automated Unit Tests:**
   ```bash
   python test_app.py
   ```

---

## 🗄️ Oracle Database 21c XE Setup (Optional for Lab / Evaluation)

When deploying to a machine with Oracle Database 21c XE installed:

1. Connect as SYSDBA:
   ```sql
   sqlplus sys as sysdba
   ALTER SESSION SET CONTAINER = XEPDB1;
   ```

2. Create the user:
   ```sql
   CREATE USER clubadmin IDENTIFIED BY clubpass;
   GRANT CONNECT, RESOURCE TO clubadmin;
   ALTER USER clubadmin QUOTA UNLIMITED ON USERS;
   GRANT CREATE VIEW, CREATE PROCEDURE, CREATE TRIGGER, CREATE SEQUENCE TO clubadmin;
   EXIT;
   ```

3. Populate the database:
   ```bash
   python load_database.py
   ```

*(Note: If Oracle XE is not running locally, `app.py` automatically utilizes the built-in fallback engine in `db_local.py` so the web app runs seamlessly anywhere).*

---

## 📊 Presentations & Evaluation Materials

All evaluation materials are organized inside the **`docs/`** folder:
- **`docs/Review_1_Presentation.pptx`**: 10-slide deck covering problem statement, ER diagram, entities, constraints, and 3NF normalization.
- **`docs/Review_2_Presentation.pptx`**: 11-slide deck covering system architecture, views, PL/SQL procedures, triggers, complex queries, live demo steps, and deliverables.
- **`docs/REVIEW_GUIDE.md`**: Complete presentation talking points and live demonstration walkthrough.
- **`docs/VIVA_QA.md`**: 15 standard viva questions with plain-English answers.

---

## 📐 Database Normalization (3NF)

- **1NF**: Every attribute contains atomic values. No repeating groups or comma-separated lists. Primary keys defined on all tables.
- **2NF**: In 1NF and contains no partial functional dependencies. In `MEMBERSHIP` and `REGISTRATION`, surrogate keys are used and non-key attributes depend on the entire primary key.
- **3NF**: In 2NF and contains no transitive dependencies ($X \rightarrow Y$). Club details exist exclusively in `CLUB` (referenced via `club_id` in `EVENT`). Student details exist exclusively in `STUDENT` (referenced via `student_id` in `REGISTRATION`).
