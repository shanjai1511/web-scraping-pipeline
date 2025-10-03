import os
import mysql.connector # type: ignore
import csv
import sys

def create_table_if_not_exists(cursor, table_name, columns):
    # Ensure uniq_id is unique in the table
    create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    create_query += ", ".join([f"`{col}` TEXT" for col in columns])
    if 'uniq_id' in columns:
        create_query += ", UNIQUE(`uniq_id`)"  # Ensure uniq_id is unique
    create_query += ");"
    cursor.execute(create_query)

def upsert_data(cursor, table_name, columns, data):
    # Constructing the insert query with ON DUPLICATE KEY UPDATE for upsert
    update_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    update_query += " ON DUPLICATE KEY UPDATE "
    update_query += ", ".join([f"`{col}`=VALUES(`{col}`)" for col in columns if col != 'uniq_id'])  # Exclude 'uniq_id' from update part
    cursor.executemany(update_query, data)

def upload_csv_to_mysql(base_dir, csv_filename, site_name, project_name, db_user="root", db_pass="root", db_name="sdf_main"):
    # Construct table name
    table_name = f"{site_name}_{project_name}".lower()

    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_pass,
        database=db_name
    )
    cursor = connection.cursor()

    # Define the path to the CSV file
    csv_path = os.path.join(base_dir, csv_filename)

    # Check if file exists
    if not os.path.isfile(csv_path):
        print(f"File not found: {csv_path}")
        return

    # Read CSV file
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        columns = next(csv_data)  # Get the header row (column names)
        data = list(csv_data)     # Get all rows

    # Create table if it doesn't exist
    create_table_if_not_exists(cursor, table_name, columns)

    # Upsert data into table
    upsert_data(cursor, table_name, columns, data)

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

    print(f"Data successfully uploaded to table '{table_name}'.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python upload_csv.py <site_name> <project_name> <csv_filename>")
        sys.exit(1)

    site_name = sys.argv[2]
    project_name = sys.argv[1]
    csv_filename = sys.argv[3]
    base_dir = f"C:/Users/shanj/OneDrive/Desktop/web-scrapping-pipeline/scrape_output/extractor_output/{project_name}"

    # Upload CSV to MySQL
    upload_csv_to_mysql(base_dir, csv_filename, site_name, project_name)