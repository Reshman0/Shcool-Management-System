import psycopg2
import threading

# PostgreSQL connection
DB_CONFIG = {
    "host": "localhost",
    "database": "school_db",
    "user": "postgres",
    # Write your password here
}

def transaction_one():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        cur = conn.cursor()
        
        print("Transaction 1: Adding a new student...")
        cur.execute(
            "INSERT INTO student (name, roll_no, section, class_id, photo) VALUES (%s, %s, %s, %s, %s)",
            ("Test Student 1", "ROLL_999", "A", 1, "test1.jpg")
        )
        conn.commit()
        print("Transaction 1: Committed successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Transaction 1: Error - {e}")
        if conn:
            conn.rollback()

def transaction_two():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        cur = conn.cursor()
        
        print("Transaction 2: Adding another student...")
        cur.execute(
            "INSERT INTO student (name, roll_no, section, class_id, photo) VALUES (%s, %s, %s, %s, %s)",
            ("Test Student 2", "ROLL_999", "B", 2, "test2.jpg")
        )
        conn.commit()
        print("Transaction 2: Committed successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Transaction 2: Error - {e}")
        if conn:
            conn.rollback()

if __name__ == "__main__":
    # Create threads to run two transactions concurrently
    thread1 = threading.Thread(target=transaction_one)
    thread2 = threading.Thread(target=transaction_two)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for the threads to complete
    thread1.join()
    thread2.join()

    print("Both transactions attempted.")
