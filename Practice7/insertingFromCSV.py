import csv
import psycopg2
from config import load_config

def import_contacts_from_csv(file_path):
    """ Reads a CSV file and inserts rows into the phonebook table """
    
    sql = """INSERT INTO phonebook (first_name, last_name, phone_number) 
             VALUES (%s, %s, %s) 
             ON CONFLICT (phone_number) DO NOTHING;"""
    
    config = load_config()
    count = 0

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    # DictReader uses the first row of the CSV as keys
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        # We extract the data using the column headers from the CSV
                        data = (
                            row['first_name'], 
                            row['last_name'], 
                            row['phone_number']
                        )
                        
                        cur.execute(sql, data)
                        count += cur.rowcount # Track how many were actually added
                
                conn.commit()
                print(f"Successfully imported {count} new contacts.")

    except (Exception, psycopg2.DatabaseError, FileNotFoundError) as error:
        print(f"Error: {error}")

if __name__ == '__main__':
    import_contacts_from_csv('contacts.csv')