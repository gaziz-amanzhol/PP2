from connect import connect

def run_phonebook():
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()

    try:
        # Example 1: Calling a Procedure (Upsert)
        print("Adding/Updating 'Alice'...")
        cur.execute("CALL upsert_contact(%s, %s)", ("Alice Smith", "1234567890"))

        # Example 2: Bulk Insert with logic
        names = ["Bob", "Charlie", "InvalidUser"]
        phones = ["9876543210", "5551234567", "abc-wrong"]
        print("Running bulk insert...")
        cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (names, phones, []))
        errors = cur.fetchone()[0]
        if errors:
            print(f"Skipped records: {errors}")

        # Example 3: Calling a Function (Search)
        print("\nSearching for 'Alice':")
        cur.execute("SELECT * FROM search_contacts(%s)", ("Alice",))
        for row in cur.fetchall():
            print(row)

        # Example 4: Pagination
        print("\nPage 1 (Limit 2):")
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (2, 0))
        for row in cur.fetchall():
            print(row)

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_phonebook()
