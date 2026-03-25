import psycopg2
from config import load_config
def create_table():
    config = load_config()
    command ='''
        CREATE TABLE phonebook (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone_number VARCHAR(15) UNIQUE NOT NULL
            );
        '''
    try:
        with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
if __name__=='__main__':
    create_table()