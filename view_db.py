# ====================================================================
# Command Line Database Viewer for College Club System
# Allows viewing tables and running SQL directly in Command Prompt
# ====================================================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "college_club_local.db")

def print_table(headers, rows):
    if not rows:
        print("  (0 rows found)")
        return

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Format header and divider
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    divider_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    print("\n" + header_line)
    print(divider_line)
    for row in rows:
        row_line = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        print(row_line)
    print(f"({len(rows)} row(s) returned)\n")

def run_query(cursor, query):
    try:
        cursor.execute(query)
        if cursor.description:
            headers = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            print_table(headers, rows)
        else:
            print("Command executed successfully.")
    except Exception as e:
        print(f"SQL Error: {e}\n")

def main():
    if not os.path.exists(DB_PATH):
        import db_local
        db_local.init_local_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("  College Club Event Management System - SQL Console")
    print("=" * 60)
    print("Quick Commands:")
    print("  1 - View STUDENTS")
    print("  2 - View CLUBS")
    print("  3 - View EVENTS")
    print("  4 - View MEMBERSHIPS")
    print("  5 - View REGISTRATIONS")
    print("  Or type any SQL query (e.g., SELECT * FROM STUDENT;)")
    print("  Type 'exit' or 'quit' to close.\n")

    while True:
        try:
            cmd = input("SQL> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit", "q"]:
                break
            elif cmd == "1":
                run_query(cursor, "SELECT student_id, student_name, email, department, year FROM STUDENT")
            elif cmd == "2":
                run_query(cursor, "SELECT club_id, club_name, category, faculty_coordinator FROM CLUB")
            elif cmd == "3":
                run_query(cursor, "SELECT event_id, event_name, event_date, venue, club_id FROM EVENT")
            elif cmd == "4":
                run_query(cursor, "SELECT m.membership_id, s.student_name, c.club_name, m.join_date FROM MEMBERSHIP m JOIN STUDENT s ON m.student_id = s.student_id JOIN CLUB c ON m.club_id = c.club_id")
            elif cmd == "5":
                run_query(cursor, "SELECT r.registration_id, s.student_name, e.event_name, r.status, r.registration_date FROM REGISTRATION r JOIN STUDENT s ON r.student_id = s.student_id JOIN EVENT e ON r.event_id = e.event_id")
            else:
                run_query(cursor, cmd.rstrip(";"))
        except (KeyboardInterrupt, EOFError):
            break

    conn.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
