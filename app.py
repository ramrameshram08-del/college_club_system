# ====================================================================
# College Club Event Management System
# Flask Application (Python 3 + Oracle XE 21c with Local Fallback)
# ====================================================================

import sqlite3
from datetime import date
import oracledb
from flask import Flask, render_template, request, redirect, url_for, flash
import config
import db_local

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# --------------------------------------------------------------------
# Database Connection Helper
# Tries Oracle XE first. If Oracle is not running locally, seamlessly
# falls back to local database so the application works out-of-the-box.
# --------------------------------------------------------------------
def get_db_connection():
    try:
        conn = oracledb.connect(
            user=config.DB_CONFIG["user"],
            password=config.DB_CONFIG["password"],
            dsn=config.DB_CONFIG["dsn"]
        )
        return conn, "oracle"
    except oracledb.Error:
        # Oracle XE is offline; use local SQLite database fallback
        db_local.init_local_db()
        conn = sqlite3.connect(db_local.DB_FILE)
        return conn, "sqlite"


# --------------------------------------------------------------------
# Route: Home Page
# Shows upcoming events and quick summary statistics
# --------------------------------------------------------------------
@app.route("/")
def index():
    conn = None
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        # get count of students, clubs, and upcoming events
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM CLUB")
        total_clubs = cursor.fetchone()[0]

        date_filter = "TRUNC(SYSDATE)" if db_type == "oracle" else "DATE('now')"
        char_func = "TO_CHAR(e.event_date, 'YYYY-MM-DD')" if db_type == "oracle" else "e.event_date"

        cursor.execute(f"SELECT COUNT(*) FROM EVENT WHERE event_date >= {date_filter}")
        upcoming_count = cursor.fetchone()[0]

        # fetch list of upcoming events with club names
        cursor.execute(f"""
            SELECT e.event_id, e.event_name, {char_func}, e.venue, c.club_name
            FROM EVENT e
            JOIN CLUB c ON e.club_id = c.club_id
            WHERE e.event_date >= {date_filter}
            ORDER BY e.event_date ASC
        """)
        upcoming_events = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "index.html",
            total_students=total_students,
            total_clubs=total_clubs,
            upcoming_count=upcoming_count,
            upcoming_events=upcoming_events,
            db_type=db_type
        )

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error loading dashboard: {err}", "error")
        return render_template("index.html", total_students=0, total_clubs=0, upcoming_count=0, upcoming_events=[])


# --------------------------------------------------------------------
# Route: Students Page
# List all students and allow adding a new student
# --------------------------------------------------------------------
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = None
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        # Handle form submission to add a new student
        if request.method == "POST":
            name = request.form.get("student_name", "").strip()
            email = request.form.get("email", "").strip()
            department = request.form.get("department", "").strip()
            year = request.form.get("year", "").strip()

            if not name or not email or not department or not year:
                flash("All student fields are required.", "error")
            else:
                try:
                    # insert student using bind variables
                    cursor.execute("""
                        INSERT INTO STUDENT (student_name, email, department, year)
                        VALUES (:name, :email, :dept, :yr)
                    """, {
                        "name": name,
                        "email": email,
                        "dept": department,
                        "yr": int(year)
                    })
                    conn.commit()
                    flash(f"Student '{name}' added successfully!", "success")
                    return redirect(url_for("students"))
                except Exception:
                    flash("Error: A student with this email already exists or invalid year.", "error")

        # get all students ordered by ID
        cursor.execute("""
            SELECT student_id, student_name, email, department, year
            FROM STUDENT
            ORDER BY student_id ASC
        """)
        student_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("students.html", students=student_list)

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error loading students: {err}", "error")
        return render_template("students.html", students=[])


# --------------------------------------------------------------------
# Route: Clubs Page
# List all clubs, view members of a selected club, and join a club
# --------------------------------------------------------------------
@app.route("/clubs", methods=["GET", "POST"])
def clubs():
    conn = None
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        # Handle form submission when a student joins a club
        if request.method == "POST":
            student_id = request.form.get("student_id")
            club_id = request.form.get("club_id")

            if not student_id or not club_id:
                flash("Please select both a student and a club.", "error")
            else:
                try:
                    now_val = "SYSDATE" if db_type == "oracle" else "DATE('now')"
                    cursor.execute(f"""
                        INSERT INTO MEMBERSHIP (student_id, club_id, join_date)
                        VALUES (:s_id, :c_id, {now_val})
                    """, {"s_id": int(student_id), "c_id": int(club_id)})
                    conn.commit()
                    flash("Student joined the club successfully!", "success")
                    return redirect(url_for("clubs", selected_club=club_id))
                except Exception:
                    flash("This student is already a member of the selected club.", "error")

        # get all clubs with member count
        cursor.execute("""
            SELECT c.club_id, c.club_name, c.category, c.faculty_coordinator,
                   COUNT(m.membership_id) AS member_count
            FROM CLUB c
            LEFT JOIN MEMBERSHIP m ON c.club_id = m.club_id
            GROUP BY c.club_id, c.club_name, c.category, c.faculty_coordinator
            ORDER BY c.club_id ASC
        """)
        club_list = cursor.fetchall()

        # get dropdown data for join club form
        cursor.execute("SELECT student_id, student_name FROM STUDENT ORDER BY student_name ASC")
        all_students = cursor.fetchall()

        # check if a specific club is selected to view members (using view: club_member_list)
        selected_club_id = request.args.get("selected_club")
        members = []
        selected_club_name = None

        if selected_club_id:
            char_join = "TO_CHAR(join_date, 'YYYY-MM-DD')" if db_type == "oracle" else "join_date"
            cursor.execute(f"""
                SELECT student_id, student_name, email, department, year, {char_join}
                FROM club_member_list
                WHERE club_id = :c_id
                ORDER BY student_name ASC
            """, {"c_id": int(selected_club_id)})
            members = cursor.fetchall()

            for c in club_list:
                if str(c[0]) == str(selected_club_id):
                    selected_club_name = c[1]
                    break

        cursor.close()
        conn.close()

        return render_template(
            "clubs.html",
            clubs=club_list,
            students=all_students,
            members=members,
            selected_club_id=selected_club_id,
            selected_club_name=selected_club_name
        )

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error loading clubs: {err}", "error")
        return render_template("clubs.html", clubs=[], students=[], members=[], selected_club_id=None, selected_club_name=None)


# --------------------------------------------------------------------
# Route: Events Page
# List events with club name, create new event, register, and cancel
# --------------------------------------------------------------------
@app.route("/events", methods=["GET", "POST"])
def events():
    conn = None
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        # Handle form submission to create a new event
        if request.method == "POST" and request.form.get("action") == "add_event":
            event_name = request.form.get("event_name", "").strip()
            event_date_val = request.form.get("event_date", "").strip()
            venue = request.form.get("venue", "").strip()
            club_id = request.form.get("club_id")

            if not event_name or not event_date_val or not venue or not club_id:
                flash("All event fields are required.", "error")
            else:
                date_insert = "TO_DATE(:edate, 'YYYY-MM-DD')" if db_type == "oracle" else ":edate"
                cursor.execute(f"""
                    INSERT INTO EVENT (event_name, event_date, venue, club_id)
                    VALUES (:name, {date_insert}, :venue, :cid)
                """, {
                    "name": event_name,
                    "edate": event_date_val,
                    "venue": venue,
                    "cid": int(club_id)
                })
                conn.commit()
                flash(f"Event '{event_name}' created successfully!", "success")
                return redirect(url_for("events"))

        # fetch events using view: event_registration_count
        char_edate = "TO_CHAR(event_date, 'YYYY-MM-DD')" if db_type == "oracle" else "event_date"
        cursor.execute(f"""
            SELECT event_id, event_name, {char_edate}, venue, club_name, total_registered
            FROM event_registration_count
            ORDER BY event_date DESC
        """)
        event_list = cursor.fetchall()

        # dropdown lists for registration form and event creation
        cursor.execute("SELECT student_id, student_name FROM STUDENT ORDER BY student_name ASC")
        all_students = cursor.fetchall()

        cursor.execute("SELECT club_id, club_name FROM CLUB ORDER BY club_name ASC")
        all_clubs = cursor.fetchall()

        # fetch upcoming events for registration dropdown
        date_filter = "TRUNC(SYSDATE)" if db_type == "oracle" else "DATE('now')"
        cursor.execute(f"""
            SELECT event_id, event_name, {char_edate}
            FROM EVENT
            WHERE event_date >= {date_filter}
            ORDER BY event_date ASC
        """)
        upcoming_events = cursor.fetchall()

        # fetch active registrations so user can cancel
        cursor.execute(f"""
            SELECT r.registration_id, s.student_name, e.event_name, 
                   {char_edate}, r.status, s.student_id, e.event_id
            FROM REGISTRATION r
            JOIN STUDENT s ON r.student_id = s.student_id
            JOIN EVENT e ON r.event_id = e.event_id
            WHERE r.status = 'REGISTERED'
            ORDER BY r.registration_id DESC
        """)
        active_registrations = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "events.html",
            events=event_list,
            students=all_students,
            clubs=all_clubs,
            upcoming_events=upcoming_events,
            active_registrations=active_registrations
        )

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error loading events: {err}", "error")
        return render_template("events.html", events=[], students=[], clubs=[], upcoming_events=[], active_registrations=[])


# --------------------------------------------------------------------
# Route: Register Student for Event
# Invokes PL/SQL Stored Procedure (with local validation fallback)
# --------------------------------------------------------------------
@app.route("/events/register", methods=["POST"])
def register_for_event():
    conn = None
    try:
        student_id = request.form.get("student_id")
        event_id = request.form.get("event_id")

        if not student_id or not event_id:
            flash("Please choose both a student and an event.", "error")
            return redirect(url_for("events"))

        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        if db_type == "oracle":
            # Call Oracle PL/SQL Stored Procedure
            out_message = cursor.var(oracledb.STRING)
            cursor.callproc("register_student_for_event", [int(student_id), int(event_id), out_message])
            message = out_message.getvalue()
        else:
            # Replicate exact Stored Procedure business logic locally
            cursor.execute("SELECT COUNT(*) FROM STUDENT WHERE student_id = :sid", {"sid": int(student_id)})
            if cursor.fetchone()[0] == 0:
                message = "Error: Student does not exist."
            else:
                cursor.execute("SELECT event_date FROM EVENT WHERE event_id = :eid", {"eid": int(event_id)})
                ev = cursor.fetchone()
                if not ev:
                    message = "Error: Event does not exist."
                elif ev[0] < str(date.today()):
                    message = "Error: Cannot register for past events."
                else:
                    cursor.execute("""
                        SELECT status FROM REGISTRATION 
                        WHERE student_id = :sid AND event_id = :eid
                    """, {"sid": int(student_id), "eid": int(event_id)})
                    existing = cursor.fetchone()

                    if existing and existing[0] == "REGISTERED":
                        message = "Error: Student is already registered for this event."
                    elif existing and existing[0] == "CANCELLED":
                        cursor.execute("""
                            UPDATE REGISTRATION SET status = 'REGISTERED', registration_date = DATE('now')
                            WHERE student_id = :sid AND event_id = :eid
                        """, {"sid": int(student_id), "eid": int(event_id)})
                        conn.commit()
                        message = "Success: Registration re-activated."
                    else:
                        cursor.execute("""
                            INSERT INTO REGISTRATION (student_id, event_id, status, registration_date)
                            VALUES (:sid, :eid, 'REGISTERED', DATE('now'))
                        """, {"sid": int(student_id), "eid": int(event_id)})
                        conn.commit()
                        message = "Success: Student registered successfully."

        if "Success" in message:
            flash(message, "success")
        else:
            flash(message, "error")

        cursor.close()
        conn.close()

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error processing registration: {err}", "error")

    return redirect(url_for("events"))


# --------------------------------------------------------------------
# Route: Cancel Registration
# Updates registration status to CANCELLED
# --------------------------------------------------------------------
@app.route("/events/cancel", methods=["POST"])
def cancel_registration():
    conn = None
    try:
        student_id = request.form.get("student_id")
        event_id = request.form.get("event_id")

        if not student_id or not event_id:
            flash("Missing registration details.", "error")
            return redirect(url_for("events"))

        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE REGISTRATION
            SET status = 'CANCELLED'
            WHERE student_id = :sid AND event_id = :eid AND status = 'REGISTERED'
        """, {"sid": int(student_id), "eid": int(event_id)})

        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration cancelled successfully.", "success")

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Database error during cancellation: {err}", "error")

    return redirect(url_for("events"))


# --------------------------------------------------------------------
# Route: Reports Page
# Runs showcase queries (JOIN, GROUP BY, HAVING, subquery, aggregates)
# --------------------------------------------------------------------
@app.route("/reports")
def reports():
    conn = None
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        char_date = "TO_CHAR(e.event_date, 'YYYY-MM-DD')" if db_type == "oracle" else "e.event_date"

        # Query 1: Most Popular Events (Aggregate + JOIN + GROUP BY)
        cursor.execute(f"""
            SELECT e.event_id, e.event_name, c.club_name, {char_date},
                   COUNT(r.registration_id) AS active_registrations
            FROM EVENT e
            JOIN CLUB c ON e.club_id = c.club_id
            LEFT JOIN REGISTRATION r ON e.event_id = r.event_id AND r.status = 'REGISTERED'
            GROUP BY e.event_id, e.event_name, c.club_name, e.event_date
            ORDER BY active_registrations DESC, e.event_date ASC
        """)
        report1 = cursor.fetchall()

        # Query 2: Clubs with Most Members (HAVING filter >= 2)
        cursor.execute("""
            SELECT c.club_name, c.category, c.faculty_coordinator, COUNT(m.membership_id) AS total_members
            FROM CLUB c
            JOIN MEMBERSHIP m ON c.club_id = m.club_id
            GROUP BY c.club_name, c.category, c.faculty_coordinator
            HAVING COUNT(m.membership_id) >= 2
            ORDER BY total_members DESC
        """)
        report2 = cursor.fetchall()

        # Query 3: Active Students (Registered for > 1 event)
        cursor.execute("""
            SELECT s.student_name, s.department, s.year, COUNT(r.registration_id) AS event_count
            FROM STUDENT s
            JOIN REGISTRATION r ON s.student_id = r.student_id
            WHERE r.status = 'REGISTERED'
            GROUP BY s.student_name, s.department, s.year
            HAVING COUNT(r.registration_id) > 1
            ORDER BY event_count DESC
        """)
        report3 = cursor.fetchall()

        # Query 4: Department-wise Club Participation
        cursor.execute("""
            SELECT s.department, COUNT(DISTINCT s.student_id) AS students_count, COUNT(m.membership_id) AS total_memberships
            FROM STUDENT s
            JOIN MEMBERSHIP m ON s.student_id = m.student_id
            GROUP BY s.department
            ORDER BY total_memberships DESC
        """)
        report4 = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "reports.html",
            report1=report1,
            report2=report2,
            report3=report3,
            report4=report4
        )

    except Exception as err:
        if conn:
            conn.close()
        flash(f"Error loading reports: {err}", "error")
        return render_template("reports.html", report1=[], report2=[], report3=[], report4=[])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
