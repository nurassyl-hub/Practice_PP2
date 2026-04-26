import psycopg2
from config import load_config
def delete_contact():
    """ Deletes a contact based on a name or a specific phone number """
    
    print("\n--- Delete a Contact ---")
    print("1. Delete by First Name")
    print("2. Delete by Exact Phone Number")
    choice = input("Choose option: ")

    sql = ""
    param = ""

    if choice == '1':
        name = input("Enter the First Name to delete: ").strip()
        # We use an exact match here to avoid accidentally deleting multiple people
        sql = "DELETE FROM phonebook WHERE first_name = %s"
        param = (name,)
    elif choice == '2':
        phone = input("Enter the exact Phone Number to delete: ").strip()
        sql = "DELETE FROM phonebook WHERE phone_number = %s"
        param = (phone,)
    else:
        print("Invalid choice.")
        return

    # Confirmation step (Safety First!)
    confirm = input(f"Are you sure you want to delete this? (yes/no): ").lower()
    if confirm != 'yes':
        print("Deletion cancelled.")
        return

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, param)
                
                # Check how many rows were removed
                deleted_count = cur.rowcount
                
                conn.commit()
                
                if deleted_count > 0:
                    print(f"Success! {deleted_count} contact(s) removed.")
                else:
                    print("No matching contact found. Nothing was deleted.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
if __name__=='__main__':
    delete_contact()       