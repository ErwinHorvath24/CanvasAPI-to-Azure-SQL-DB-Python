#### CANVAS LMS STUDENT ROSTER FOR EACH COURSE TO AZURE SQL ####

# Erwin Horvath
# 11/21/2022

# This code submits a GET request through Canvas LMS API to obtain the roster with role student for each course.
# It then transforms the JSON response into a CSV format.
# Then connects to an Azure SQL database 
# Writes the CSV file to the table named roster (This only inserts data to an existing table, see roster_table.sql file in repository)

# Required: 
# - Azure Subscription
# - SQL Server
# - SQL Database
# - SQL table code (found in this repository)
# - FOR AUTOMATION recommended: Azure Functions App

# Import libraries
import requests
import json
import pyodbc
import pandas as pd
import textwrap

# Course IDs
course_ids = ['1','2','3','4','5','6','7','8','9','10']

# list of empty dataframes
dfs=[]

# Loop to obtain roster for each course ID, parse JSON response to convert to CSV format and append data to one file
for course_id in course_ids:

    # Roster URL
    api_url ='https://YOUR_INSTANCE_NAME.instructure.com/api/v1/courses/' +course_id+ '/students?per_page=1000'

    # Authorization
    api_key = 'YOUR AUTHORIZATION KEY HERE'

    # Headers
    headers = {'Authorization' : api_key}

    # Request to obtain API output
    api_output=requests.get(api_url, headers=headers).json()

    # Parse the json string to a dictionary list
    data = json.loads(json.dumps(api_output))

    # Create dataframe from json list
    df1 = pd.DataFrame(data)
    
    # Add a new column with course id to dataframe
    df2 = df1.assign(course_id=course_id)

    # Append the dataframes
    dfs.append(pd.DataFrame(df2))

# Concatenate the dfs array
final_df = pd.concat(dfs)

# Create a csv file and continue to append data to it 
roster_csv = final_df.to_csv('roster.csv', index=False)

# Read CSV
df3 = pd.read_csv('roster.csv')

# Replace NaN or blanks with 0
df4 = df3.fillna(value=0)

# Rename the 'name' column to 'student_name' (names column caused issues info to show up as ints in SQL database)
df = df4.rename(columns={'id':'student_id','name':'student_name'})

##### Connection to Azure SQL Server ##### 

# Driver for SQL Server
driver = '{ODBC Driver 17 for SQL Server}'

# Server Name and Database 
server_name = 'YOUR SERVER NAME HERE'
database_name = 'YOUR DATABASE NAME HERE'

# Server URL
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)

# Username and Password
username = "YOUR DATABASE USERNAME"
password = "YOUR DATABASE PASSWORD"

# Connection String
connection_string = textwrap.dedent('''
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))

# PYODBC Connection Object
cnxn: pyodbc.Connection = pyodbc.connect(connection_string)

# Cursor object for connection
crsr: pyodbc.Cursor = cnxn.cursor()

##### Writing the CSV file to the Courses Table ##### 

# SQL Insert
for index, row in df.iterrows():
    crsr.execute("INSERT INTO roster (student_id,student_name,created_at,sortable_name,short_name,sis_user_id,integration_id,sis_import_id,login_id,course_id) VALUES(?,?,?,?,?,?,?,?,?,?)",
                row.student_id,
                row.student_name,
                row.created_at,
                row.sortable_name,
                row.short_name,
                row.sis_user_id,
                row.integration_id,
                row.sis_import_id,
                row.login_id,
                row.course_id
                )
                
# Commit the inserts
cnxn.commit()

# Close the cursor
crsr.close()

# Close the connection
cnxn.close()
