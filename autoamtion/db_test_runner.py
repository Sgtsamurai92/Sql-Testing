import sqlite3
import glob
import os

DB_PATH = "qa_test.db"
TEST_FOLDER = "test_queries"

def run_sql_file(conn, sql_file):
    with open(sql_file, "r") as f:
        sql = f.read()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        results = cursor.execute(sql).fetchall()
        if len(results) == 0:
            print(f"✅ PASS: {os.path.basename(sql_file)}")
        else:
            print(f"❌ FAIL: {os.path.basename(sql_file)} returned {len(results)} result(s)")
            for row in results:
                print(f"   - {row}")
        cursor.execute("ROLLBACK")
    except Exception as e:
        print(f"⚠️ ERROR running {sql_file}: {e}")

def main():
    conn = sqlite3.connect(DB_PATH)
    print("Running SQL QA tests...\n")

    sql_files = sorted(glob.glob(os.path.join(TEST_FOLDER, "*.sql")))
    for file in sql_files:
        run_sql_file(conn, file)

    conn.close()
    print("\nTest run complete.")

if __name__ == "__main__":
    main()