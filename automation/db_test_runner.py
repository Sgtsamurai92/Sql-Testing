import sqlite3
import glob
import os
import re

DB_PATH = "qa_test.db"
SCHEMA_FOLDER = os.path.join("schema")
TEST_FOLDER = os.path.join("test_queries")


def read_sql_clean(path: str) -> str:
    """Read a .sql file and strip common markdown artifacts and fenced code blocks."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Remove triple backtick blocks and leading markdown header/separator lines
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("`"):
            # skip any Markdown code fence lines (``` or ````)
            continue
        if s.startswith("#"):
            # skip markdown headings
            continue
        if s == "---":
            continue
        lines.append(line)

    return "\n".join(lines).strip()


def split_sql_statements(sql_text: str):
    """Split SQL text into individual statements by semicolon, ignoring comments and blanks."""
    # A simple split on semicolons that are not inside quotes
    statements = []
    statement = []
    in_single = False
    in_double = False

    for ch in sql_text:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        if ch == ";" and not in_single and not in_double:
            statements.append("".join(statement).strip())
            statement = []
        else:
            statement.append(ch)
    # tail
    tail = "".join(statement).strip()
    if tail:
        statements.append(tail)

    # Remove comments and empty
    cleaned = []
    for stmt in statements:
        # Drop full-line comments and trim
        lines = []
        for ln in stmt.splitlines():
            s = ln.strip()
            if s.startswith("--") or not s:
                continue
            lines.append(ln)
        stmt2 = "\n".join(lines).strip()
        if stmt2:
            cleaned.append(stmt2)
    return cleaned


def init_db(conn: sqlite3.Connection):
    # Create schema
    schema_file = os.path.join(SCHEMA_FOLDER, "create_tables.sql")
    if not os.path.exists(schema_file):
        raise FileNotFoundError(f"Missing schema file: {schema_file}")
    schema_sql = read_sql_clean(schema_file)
    conn.executescript(schema_sql)

    # Load seed data
    data_file = os.path.join(SCHEMA_FOLDER, "insert_test_data.sql")
    if os.path.exists(data_file):
        data_sql = read_sql_clean(data_file)
        conn.executescript(data_sql)


def run_test_file(conn: sqlite3.Connection, sql_file: str) -> int:
    """Run each statement in a test file; return the number of failures encountered."""
    raw = read_sql_clean(sql_file)
    statements = split_sql_statements(raw)

    failures = 0
    for idx, stmt in enumerate(statements, start=1):
        # Only evaluate SELECT statements; skip others
        if not stmt.strip().lower().startswith("select"):
            continue
        try:
            rows = conn.execute(stmt).fetchall()
            if len(rows) == 0:
                print(f"✅ PASS: {os.path.basename(sql_file)} [#{idx}]")
            else:
                failures += 1
                print(
                    f"❌ FAIL: {os.path.basename(sql_file)} [#{idx}] returned {len(rows)} row(s)"
                )
                for row in rows[:5]:
                    print(f"   - {row}")
                if len(rows) > 5:
                    print(f"   ... (+{len(rows)-5} more)")
        except Exception as e:
            failures += 1
            print(f"⚠️ ERROR in {os.path.basename(sql_file)} [#{idx}]: {e}")
    return failures


def main():
    print("Initializing SQLite database and running SQL QA tests...\n")
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        conn.close()
        return

    total_failures = 0
    sql_files = sorted(glob.glob(os.path.join(TEST_FOLDER, "*.sql")))
    if not sql_files:
        print(f"No test files found in '{TEST_FOLDER}'.")
    for file in sql_files:
        total_failures += run_test_file(conn, file)

    conn.close()
    print("\nTest run complete.")
    if total_failures == 0:
        print("All tests passed ✅")
    else:
        print(f"Total failures: {total_failures} ❌")


if __name__ == "__main__":
    main()
