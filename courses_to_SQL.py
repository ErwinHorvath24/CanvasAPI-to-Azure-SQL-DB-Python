#### CANVAS LMS LIST OF COURSES TO AZURE SQL ####

# Erwin Horvath
# 11/21/2022

# This code submits a GET request to Canvas LMS API to obtain a list of courses.
# It then transforms the JSON response into a CSV format.
# Then connects to an Azure SQL database 
# Writes the CSV file to the table name courses (This only inserts data to an existing table, see courses_table.sql file in repository)

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
import logging
import textwrap


#### API INFORMATION ####

# Courses URL
api_url ='https://YOUR_INSTANCE_NAME.instructure.com/api/v1/courses?per_page=1000'

# Authorization
api_key = 'YOUR AUTHORIZATION KEY HERE'

# Headers
headers = {'Authorization' : api_key} 

# Request to obtain API output
api_output=requests.get(api_url, headers=headers).json() 

#### DATA PREPROCESSING ####

# Parse the JSON response string to a python dictionary list
data = json.loads(json.dumps(api_output))

# Create dataframe from list
df1 = pd.DataFrame(data) 

# Convert dataframe to csv format and remove intial column 
courses_csv = df1.to_csv('courses.csv',index=False)

# Read CSV
df2 = pd.read_csv('courses.csv')

# Replace NaN or blanks with 0
df3 = df2.fillna(value=0)

# Rename the 'name' column to 'course_name' (names column caused issues info to show up as ints in SQL database)
df = df3.rename(columns={'id':'course_id','name':'course_name'})

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
    crsr.execute("INSERT INTO YOUR TABLE NAME HERE (course_id,course_name,account_id,uuid,start_at,grading_standard_id,is_public,created_at,course_code,default_view,root_account_id,enrollment_term_id,license,grade_passback_setting,end_at,public_syllabus,public_syllabus_to_auth,storage_quota_mb,is_public_to_auth_users,homeroom_course,course_color,friendly_name,apply_assignment_group_weights,calendar,time_zone,blueprint,template,sis_course_id,sis_import_id,integration_id,enrollments,hide_final_grades,workflow_state,restrict_enrollments_to_course_dates,overridden_course_visibility,blueprint_restrictions_by_object_type) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                row.course_id,
                row.course_name,
                row.account_id,
                row.uuid,
                row.start_at,
                row.grading_standard_id,
                row.is_public,
                row.created_at,
                row.course_code,
                row.default_view,
                row.root_account_id,
                row.enrollment_term_id,
                row.license,
                row.grade_passback_setting,
                row.end_at,
                row.public_syllabus,
                row.public_syllabus_to_auth,
                row.storage_quota_mb,
                row.is_public_to_auth_users,
                row.homeroom_course,
                row.course_color,
                row.friendly_name,
                row.apply_assignment_group_weights,
                row.calendar,
                row.time_zone,
                row.blueprint,
                row.template,
                row.sis_course_id,
                row.sis_import_id,
                row.integration_id,
                row.enrollments,
                row.hide_final_grades,
                row.workflow_state,
                row.restrict_enrollments_to_course_dates,
                row.overridden_course_visibility,
                row.blueprint_restrictions_by_object_type
                )
                
# Commit the inserts
cnxn.commit()

# Close the cursor
crsr.close()

# Close the connection
cnxn.close()
