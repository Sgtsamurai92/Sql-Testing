# QA SQL Testing Suite

This project demonstrates how **SQL is used in Quality Assurance** to verify database integrity, validate business rules, and support automated testing workflows.

## Objectives
- Verify **data accuracy and integrity** across multiple tables  
- Test **referential and business logic** consistency  
- Automate SQL-based checks via Python for continuous validation  

## Schema Overview
Tables:
- **users** — customer info  
- **orders** — each user’s purchases  
- **payments** — linked payment records  

## Example Test Cases
### Data Validation
```sql
-- Check for missing customer_id values
SELECT order_id FROM orders WHERE customer_id IS NULL;

## How to run (Windows PowerShell)

This repo uses SQLite for a zero-config demo. The automation script will:
- Create a fresh SQLite database `qa_test.db`
- Apply schema from `schema/create_tables.sql`
- Insert seed data from `schema/insert_test_data.sql`
- Execute each query in `test_queries/*.sql` and report PASS/FAIL

Steps:

1) Ensure you have Python 3.8+ installed.
2) From the repo root, run the test runner:

```powershell
python .\automation\db_test_runner.py
```

You should see per-query results like PASS/FAIL. Queries that return rows are considered failures (they identify data violations). Errors are printed as warnings.

Notes:
- If you previously used the older path `autoamtion/db_test_runner.py`, switch to `automation/db_test_runner.py`.
- To reset, simply delete `qa_test.db` and re-run the script.