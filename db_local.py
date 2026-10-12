# ====================================================================
# Local Fallback Database Helper
# Allows the web app to run immediately when Oracle XE is offline
# ====================================================================

import sqlite3
import os
from datetime import date, timedelta

DB_FILE = os.path.join(os.path.dirname(__file__), "college_club_local.db")

def init_local_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STUDENT (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 4)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CLUB (
            club_id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            faculty_coordinator TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EVENT (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            venue TEXT NOT NULL,
            club_id INTEGER NOT NULL,
            FOREIGN KEY (club_id) REFERENCES CLUB(club_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MEMBERSHIP (
            membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            club_id INTEGER NOT NULL,
            join_date TEXT NOT NULL,
            UNIQUE (student_id, club_id),
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
            FOREIGN KEY (club_id) REFERENCES CLUB(club_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS REGISTRATION (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('REGISTERED', 'CANCELLED', 'ATTENDED')),
            registration_date TEXT NOT NULL,
            UNIQUE (student_id, event_id),
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE
        )
    """)

    # Views
    cursor.execute("DROP VIEW IF EXISTS event_registration_count")
    cursor.execute("""
        CREATE VIEW event_registration_count AS
        SELECT 
            e.event_id,
            e.event_name,
            e.event_date,
            e.venue,
            c.club_name,
            COUNT(CASE WHEN r.status = 'REGISTERED' THEN 1 END) AS total_registered
        FROM EVENT e
        JOIN CLUB c ON e.club_id = c.club_id
        LEFT JOIN REGISTRATION r ON e.event_id = r.event_id
        GROUP BY e.event_id, e.event_name, e.event_date, e.venue, c.club_name
    """)

    cursor.execute("DROP VIEW IF EXISTS club_member_list")
    cursor.execute("""
        CREATE VIEW club_member_list AS
        SELECT 
            c.club_id,
            c.club_name,
            c.category,
            s.student_id,
            s.student_name,
            s.email,
            s.department,
            s.year,
            m.join_date
        FROM MEMBERSHIP m
        JOIN CLUB c ON m.club_id = c.club_id
        JOIN STUDENT s ON m.student_id = s.student_id
    """)

    # Populate sample data if empty
    cursor.execute("SELECT COUNT(*) FROM STUDENT")
    if cursor.fetchone()[0] == 0:
        today = date.today()
        students = [
            (1, 'Aarav Sharma', 'aarav.sharma@college.edu', 'Computer Science', 2),
            (2, 'Diya Patel', 'diya.patel@college.edu', 'Information Technology', 3),
            (3, 'Rohan Verma', 'rohan.verma@college.edu', 'Electronics', 1),
            (4, 'Ananya Iyer', 'ananya.iyer@college.edu', 'Computer Science', 4),
            (5, 'Karthik Nair', 'karthik.nair@college.edu', 'Mechanical', 2),
            (6, 'Sneha Gupta', 'sneha.gupta@college.edu', 'Information Technology', 2),
            (7, 'Vikram Singh', 'vikram.singh@college.edu', 'Civil', 3),
            (8, 'Pooja Joshi', 'pooja.joshi@college.edu', 'Computer Science', 1),
            (9, 'Rahul Mehta', 'rahul.mehta@college.edu', 'Electronics', 4),
            (10, 'Ishita Rao', 'ishita.rao@college.edu', 'Information Technology', 3)
        ]
        cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?, ?)", students)

        clubs = [
            (1, 'Coding & Algo Club', 'Technical', 'Dr. Ramesh Sundaram'),
            (2, 'Robotics Society', 'Technical', 'Prof. Sunita Deshmukh'),
            (3, 'Cultural & Drama Guild', 'Cultural', 'Prof. Meera Kulkarni'),
            (4, 'Literary & Debating Club', 'Literary', 'Dr. Alok Mukherjee'),
            (5, 'Sports & Fitness Club', 'Sports', 'Coach Vikram Rathore')
        ]
        cursor.executemany("INSERT INTO CLUB VALUES (?, ?, ?, ?)", clubs)

        events = [
            (1, 'Intro to Competitive Programming', str(today - timedelta(days=15)), 'Lab 301, CS Block', 1),
            (2, 'RoboWars Workshop', str(today - timedelta(days=7)), 'Mechanical Workshop Hall', 2),
            (3, 'Annual Street Play Auditions', str(today - timedelta(days=2)), 'Open Air Theatre', 3),
            (4, 'Hackathon 2026: CodeStorm', str(today + timedelta(days=5)), 'Main Auditorium', 1),
            (5, 'Drone Flying & Autonomous Navigation', str(today + timedelta(days=10)), 'Football Ground', 2),
            (6, 'Inter-College Debate Championship', str(today + timedelta(days=14)), 'Seminar Hall B', 4),
            (7, 'Spring Music Fest & Battle of Bands', str(today + timedelta(days=18)), 'College Amphitheatre', 3),
            (8, 'Table Tennis & Badminton Tournament', str(today + timedelta(days=22)), 'Indoor Sports Complex', 5),
            (9, 'Web Development Bootcamp with Flask', str(today + timedelta(days=28)), 'Lab 204, IT Block', 1),
            (10, 'Creative Writing & Poetry Slam', str(today + timedelta(days=35)), 'Central Library Reading Room', 4)
        ]
        cursor.executemany("INSERT INTO EVENT VALUES (?, ?, ?, ?, ?)", events)

        memberships = [
            (1, 1, 1, str(today - timedelta(days=60))),
            (2, 1, 2, str(today - timedelta(days=45))),
            (3, 2, 1, str(today - timedelta(days=50))),
            (4, 2, 4, str(today - timedelta(days=30))),
            (5, 3, 2, str(today - timedelta(days=40))),
            (6, 3, 5, str(today - timedelta(days=20))),
            (7, 4, 1, str(today - timedelta(days=90))),
            (8, 4, 3, str(today - timedelta(days=80))),
            (9, 5, 2, str(today - timedelta(days=35))),
            (10, 6, 1, str(today - timedelta(days=25))),
            (11, 6, 4, str(today - timedelta(days=15))),
            (12, 7, 5, str(today - timedelta(days=55))),
            (13, 8, 1, str(today - timedelta(days=10))),
            (14, 9, 2, str(today - timedelta(days=70))),
            (15, 10, 3, str(today - timedelta(days=12)))
        ]
        cursor.executemany("INSERT INTO MEMBERSHIP VALUES (?, ?, ?, ?)", memberships)

        registrations = [
            (1, 1, 1, 'ATTENDED', str(today - timedelta(days=18))),
            (2, 2, 1, 'ATTENDED', str(today - timedelta(days=17))),
            (3, 4, 1, 'ATTENDED', str(today - timedelta(days=16))),
            (4, 3, 2, 'ATTENDED', str(today - timedelta(days=9))),
            (5, 5, 2, 'CANCELLED', str(today - timedelta(days=8))),
            (6, 9, 2, 'ATTENDED', str(today - timedelta(days=8))),
            (7, 4, 3, 'ATTENDED', str(today - timedelta(days=4))),
            (8, 10, 3, 'ATTENDED', str(today - timedelta(days=3))),
            (9, 1, 4, 'REGISTERED', str(today - timedelta(days=2))),
            (10, 2, 4, 'REGISTERED', str(today - timedelta(days=2))),
            (11, 4, 4, 'REGISTERED', str(today - timedelta(days=1))),
            (12, 6, 4, 'REGISTERED', str(today - timedelta(days=1))),
            (13, 8, 4, 'REGISTERED', str(today)),
            (14, 3, 5, 'REGISTERED', str(today - timedelta(days=1))),
            (15, 5, 5, 'REGISTERED', str(today)),
            (16, 2, 6, 'REGISTERED', str(today)),
            (17, 6, 6, 'REGISTERED', str(today)),
            (18, 4, 7, 'REGISTERED', str(today)),
            (19, 10, 7, 'REGISTERED', str(today)),
            (20, 7, 8, 'REGISTERED', str(today))
        ]
        cursor.executemany("INSERT INTO REGISTRATION VALUES (?, ?, ?, ?, ?)", registrations)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_local_db()
    print("Local database initialized successfully!")
