#### CANVAS LMS SUBMISSIONS FOR EACH COURSE TO AZURE SQL ####

# Erwin Horvath
# 11/22/2022

# This code submits a GET request through Canvas LMS API to obtain a list of submissions for each 4.0 course.
# It then transforms the JSON response into a CSV format.
# Then connects to an Azure SQL database 
# Writes the CSV file to the table named submissions (This only inserts data to an existing table, see submissions_table.sql file in repository)

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

# Loop to obtain submissions for each course ID, parse JSON response to convert to CSV format and append data to one file
for course_id in course_ids:

    # Assignment URL
    api_url ='https://YOUR_INSTANCE_NAME_HERE.instructure.com/api/v1/courses/' +course_id+ '/students/submissions?student_ids[]=all&per_page=1000'

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
submissions_csv = final_df.to_csv('submissions.csv', index=False)

# Read CSV
df3 = pd.read_csv('submissions.csv')

# Replace NaN or blanks with 0
df4 = df3.fillna(value=0)

# Rename the 'id' column to 'submission_id' and 'user_id' to 'student_id'
df5 = df4.rename(columns={'id':'submission_id','user_id':'student_id'})

# Delete columns
df = df5.drop(['discussion_entries','attachments'], axis=1)

##### Connection to Azure SQL Server ##### 

# Driver for SQL Server
driver = '{ODBC Driver 17 for SQL Server}'

# Server Name and Database  
server_name = 'YOUR SERVER NAME'
database_name = 'YOUR DATABASE NAME'

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
    crsr.execute("INSERT INTO submissions (submission_id,body,url,grade,score,submitted_at,assignment_id,student_id,submission_type,workflow_state,grade_matches_current_submission,graded_at,grader_id,attempt,cached_due_date,excused,late_policy_status,points_deducted,grading_period_id,extra_attempts,posted_at,redo_request,late,missing,seconds_late,entered_grade,entered_score,preview_url,anonymous_id,external_tool_url) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                row.submission_id,
                row.body,
                row.url,
                row.grade,
                row.score,
                row.submitted_at,
                row.assignment_id,
                row.student_id,
                row.submission_type,
                row.workflow_state,
                row.grade_matches_current_submission,
                row.graded_at,
                row.grader_id,
                row.attempt,
                row.cached_due_date,
                row.excused,
                row.late_policy_status,
                row.points_deducted,
                row.grading_period_id,
                row.extra_attempts,
                row.posted_at,
                row.redo_request,
                row.late,
                row.missing,
                row.seconds_late,
                row.entered_grade,
                row.entered_score,
                row.preview_url,
                row.anonymous_id,
                row.external_tool_url
                )
                
# Commit the inserts
cnxn.commit()

# Close the cursor
crsr.close()

# Close the connection
cnxn.close()
