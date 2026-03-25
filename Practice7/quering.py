import psycopg2
from config import load_config
def search_contacts():
    """ Search for contacts based on name or phone prefix """
    
    print("\n--- Search Contacts ---")
    print("1. Search by Name")
    print("2. Search by Phone Prefix (e.g. 7707)")
    choice = input("Choose filter: ")

    search_term = ""
    sql = ""

    if choice == '1':
        name = input("Enter name to search: ").strip()
        search_term = f"%{name}%"
        sql = "SELECT * FROM phonebook WHERE first_name ILIKE %s OR last_name ILIKE %s"
        params = (search_term, search_term)
    elif choice == '2':
        prefix = input("Enter phone prefix: ").strip()
        search_term = f"{prefix}%"
        sql = "SELECT * FROM phonebook WHERE phone_number LIKE %s"
        params = (search_term,)
    else:
        print("Invalid choice.")
        return

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()

                if rows:
                    print(f"\nFound {len(rows)} contact(s):")
                    print("-" * 50)
                    for row in rows:
                        print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Phone: {row[3]}")
                    print("-" * 50)
                else:
                    print("No contacts found matching that criteria.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
if __name__=='__main__':
    search_contacts()