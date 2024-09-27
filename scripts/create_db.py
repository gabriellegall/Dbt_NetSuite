import pyodbc
import time
import yaml

# Load configuration from YAML file
with open("profiles.yml", "r") as f:
    config = yaml.safe_load(f)

# Sleep - to leave some time for the database to initialize
time.sleep(15)

# Create the DB if it does not exist
netsuite_project = config["netsuite_project"]

target_environment = netsuite_project["target"]
driver = netsuite_project["outputs"][target_environment]["driver"]
server = netsuite_project["outputs"][target_environment]["host"]
username = netsuite_project["outputs"][target_environment]["user"]
password = netsuite_project["outputs"][target_environment]["password"]

conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server},1433;'
    f'UID={username};'
    f'PWD={password};'
    'TrustServerCertificate=yes;'
)

conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

create_db_query = '''
    IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'netsuite')
    BEGIN
        CREATE DATABASE netsuite;
    END
'''

alter_login_query = f'''
    ALTER LOGIN {username} WITH DEFAULT_LANGUAGE = British;
'''

try:
    cursor.execute(create_db_query)
    conn.commit()
    print("Database created successfully.")
    
    cursor.execute(alter_login_query)
    conn.commit()
    print("Login language set to British successfully.")
    
finally:
    conn.close()