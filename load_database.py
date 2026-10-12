# ====================================================================
# Database Initialization Script
# Runs schema.sql, sample_data.sql, and views_procedures_triggers.sql
# ====================================================================

import os
import oracledb
import config

def execute_sql_file(cursor, file_path):
    print(f"\n---> Executing: {os.path.basename(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split commands by '/' for PL/SQL blocks and by ';' for standard SQL
    # Handle PL/SQL blocks separated by slash on its own line
    chunks = content.split("\n/\n")

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        # If it's a PL/SQL block (CREATE OR REPLACE TRIGGER / PROCEDURE / BEGIN / DECLARE)
        if any(chunk.upper().startswith(keyword) for keyword in [
            "CREATE OR REPLACE TRIGGER", 
            "CREATE OR REPLACE PROCEDURE", 
            "CREATE OR REPLACE VIEW",
            "BEGIN", 
            "DECLARE"
        ]):
            try:
                cursor.execute(chunk)
                print("  [OK] Executed PL/SQL Block / View")
            except oracledb.Error as e:
                print(f"  [ERROR] PL/SQL Error: {e}")
        else:
            # Standard SQL statements separated by ';'
            statements = chunk.split(";")
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt or stmt.startswith("--"):
                    continue
                try:
                    cursor.execute(stmt)
                    cmd_name = stmt.split()[0].upper()
                    print(f"  [OK] {cmd_name} executed successfully.")
                except oracledb.Error as e:
                    print(f"  [ERROR] {e} on: {stmt[:60]}...")

def main():
    print("==========================================================")
    print("College Club System - Oracle XE Database Initializer")
    print("==========================================================")
    print(f"Connecting to: {config.DB_CONFIG['user']}@{config.DB_CONFIG['dsn']} ...")

    try:
        conn = oracledb.connect(
            user=config.DB_CONFIG["user"],
            password=config.DB_CONFIG["password"],
            dsn=config.DB_CONFIG["dsn"]
        )
        cursor = conn.cursor()
        print("Connected to Oracle Database successfully!")

        sql_dir = os.path.join(os.path.dirname(__file__), "sql")
        
        # 1. Execute schema.sql
        execute_sql_file(cursor, os.path.join(sql_dir, "schema.sql"))
        conn.commit()

        # 2. Execute sample_data.sql
        execute_sql_file(cursor, os.path.join(sql_dir, "sample_data.sql"))
        conn.commit()

        # 3. Execute views_procedures_triggers.sql
        execute_sql_file(cursor, os.path.join(sql_dir, "views_procedures_triggers.sql"))
        conn.commit()

        cursor.close()
        conn.close()

        print("\n==========================================================")
        print("Database initialized with sample data, views, procedure, and trigger!")
        print("==========================================================")

    except oracledb.Error as err:
        print("\n[FAILED TO CONNECT TO ORACLE XE]")
        print(f"Details: {err}")
        print("\nTroubleshooting:")
        print("1. Ensure Oracle XE service is running (e.g., net start OracleServiceXE).")
        print("2. Ensure Oracle Listener is running (e.g., lsnrctl status).")
        print("3. Ensure user 'clubadmin' was created as explained in the setup steps.")

if __name__ == "__main__":
    main()
