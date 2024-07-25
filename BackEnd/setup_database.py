import mysql.connector
from mysql.connector import errorcode
import configparser

# Load configuration from the config file
config = configparser.ConfigParser()
config.read('db_config.ini')

db_config = {
    'user': config['mysql']['user'],
    'password': config['mysql']['password'],
    'host': config['mysql']['host'],
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    with open('create_database.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script to setup the database and tables
    for result in cursor.execute(sql_script, multi=True):
        pass  # Skip any output

    print("Database setup complete!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if 'conn' in locals():
        cursor.close()
        conn.close()