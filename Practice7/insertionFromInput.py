import psycopg2
from config import load_config
def insert_manual_contact():
    """ Takes input from the console and saves it to PostgreSQL """
    
    print("\n--- Add New Contact ---")
    f_name = input("Enter First Name: ").strip()
    l_name = input("Enter Last Name (optional): ").strip()
    phone = input("Enter Phone Number: ").strip()

    # Basic validation: Name and Phone cannot be empty
    if not f_name or not phone:
        print("Error: First Name and Phone Number are required!")
        return

    sql = """INSERT INTO phonebook (first_name, last_name, phone_number)
             VALUES (%s, %s, %s) RETURNING contact_id;"""
    
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute with a tuple of the user's input
                cur.execute(sql, (f_name, l_name, phone))
                
                # Get the new ID to confirm it worked
                new_id = cur.fetchone()[0]
                conn.commit()
                
                print(f"Success! Contact added with ID: {new_id}")

    except psycopg2.errors.UniqueViolation:
        print(f"Error: The phone number '{phone}' already exists in the book.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database Error: {error}")
if __name__ == '__main__':
    while True:
        print("\n1. Add Contact")
        print("2. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            insert_manual_contact()
        elif choice == '2':
            break