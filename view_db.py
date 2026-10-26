# ====================================================================
# Command Line Database Console for College Club System
# Allows viewing tables and running SQL directly in Command Prompt
# Connects to the EXACT same database (Oracle XE or persistent Local SQLite)
# as the Flask Web UI.
# ====================================================================

import os
import sys
import sqlite3
import config
import db_local

def get_db_connection():
    """
    Connects to Oracle XE if available; otherwise falls back to the
    shared persistent local SQLite database file on disk.
    """
    try:
        import oracledb
        conn = oracledb.connect(
            user=config.DB_CONFIG["user"],
            password=config.DB_CONFIG["password"],
            dsn=config.DB_CONFIG["dsn"],
            tcp_connect_timeout=0.5
        )
        return conn, "oracle", f"Oracle XE 21c ({config.DB_CONFIG['user']}@{config.DB_CONFIG['dsn']})"
    except Exception:
        pass

    conn = db_local.connect_local_db()
    return conn, "sqlite", f"Local SQLite Database ({db_local.get_db_file()})"

def print_table(headers, rows):
    if not rows:
        print("  (0 rows found)\n")
        return

    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val if val is not None else "NULL")))

    # Format header and divider
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    divider_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    print("\n" + header_line)
    print(divider_line)
    for row in rows:
        row_line = " | ".join(str(val if val is not None else "NULL").ljust(col_widths[i]) for i, val in enumerate(row))
        print(row_line)
    print(f"({len(rows)} row(s) returned)\n")

def run_query(conn, cursor, db_type, query):
    try:
        cursor.execute(query)
        if cursor.description:
            headers = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            print_table(headers, rows)
        else:
            if hasattr(conn, "commit"):
                conn.commit()
            print("Command executed successfully and changes committed to database.\n")
    except Exception as e:
        print(f"SQL Error: {e}\n")

def main():
    conn, db_type, db_desc = get_db_connection()
    cursor = conn.cursor()

    print("=" * 70)
    print("  College Club Event Management System - SQL Console")
    print("=" * 70)
    print(f"  Connected to: {db_desc}")
    print("  Status: Synchronized with Web UI (Instant Real-Time Updates)")
    print("=" * 70)
    print("Quick Commands:")
    print("  1 - View STUDENTS")
    print("  2 - View CLUBS")
    print("  3 - View EVENTS")
    print("  4 - View MEMBERSHIPS (Club Members)")
    print("  5 - View REGISTRATIONS (Event Signups)")
    print("  Or type any SQL query (e.g., SELECT * FROM MEMBERSHIP;)")
    print("  Type 'exit' or 'quit' to close.\n")

    while True:
        try:
            cmd = input("SQL> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit", "q"]:
                break
            elif cmd == "1":
                run_query(conn, cursor, db_type, "SELECT student_id, student_name, email, department, year FROM STUDENT ORDER BY student_id ASC")
            elif cmd == "2":
                run_query(conn, cursor, db_type, "SELECT club_id, club_name, category, faculty_coordinator FROM CLUB ORDER BY club_id ASC")
            elif cmd == "3":
                run_query(conn, cursor, db_type, "SELECT event_id, event_name, event_date, venue, club_id FROM EVENT ORDER BY event_id ASC")
            elif cmd == "4":
                run_query(conn, cursor, db_type, "SELECT m.membership_id, s.student_name, c.club_name, m.join_date FROM MEMBERSHIP m JOIN STUDENT s ON m.student_id = s.student_id JOIN CLUB c ON m.club_id = c.club_id ORDER BY m.membership_id ASC")
            elif cmd == "5":
                run_query(conn, cursor, db_type, "SELECT r.registration_id, s.student_name, e.event_name, r.status, r.registration_date FROM REGISTRATION r JOIN STUDENT s ON r.student_id = s.student_id JOIN EVENT e ON r.event_id = e.event_id ORDER BY r.registration_id ASC")
            else:
                run_query(conn, cursor, db_type, cmd.rstrip(";"))
        except (KeyboardInterrupt, EOFError):
            break

    try:
        cursor.close()
        conn.close()
    except Exception:
        pass
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
