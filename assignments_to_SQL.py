#### CANVAS LMS ASSIGNMENTS FOR EACH COURSE TO AZURE SQL ####

# Erwin Horvath
# 11/21/2022

# This code submits a GET request through Canvas LMS API to obtain a list of assignments for each 4.0 course.
# It then transforms the JSON response into a CSV format.
# Then connects to an Azure SQL database 
# Writes the CSV file to the table named assignments (This only inserts data to an existing table, see assignments_table.sql file in repository)

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
import azure.functions as func
import textwrap

# Course IDs
course_ids = ['1','2','3','4','5','6','7','8','9','10']

# list of empty dataframes
dfs=[]

# Loop to obtain assignments for each course ID, parse JSON response to convert to CSV format and append data to one file
for course_id in course_ids:

    # Assignment URL
    api_url ='https://YOUR_INSTANCE_HERE.instructure.com/api/v1/courses/' +course_id+ '/assignments?per_page=1000'

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
assignments_csv = final_df.to_csv('assignments.csv', index=False)

# Read CSV
df3 = pd.read_csv('assignments.csv')

# Replace NaN or blanks with 0
df4 = df3.fillna(value=0)

# Rename the 'name' column to 'student_name' (names column caused issues info to show up as ints in SQL database)
df5 = df4.rename(columns={'id':'assignment_id','name':'assignment_name'})

# Delete columns
df = df5.drop(['description','secure_params','discussion_topic'], axis=1)

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
    crsr.execute("INSERT INTO assignments (assignment_id,due_at,unlock_at,lock_at,points_possible,grading_type,assignment_group_id,grading_standard_id,created_at,updated_at,peer_reviews,automatic_peer_reviews,position,grade_group_students_individually,anonymous_peer_reviews,group_category_id,post_to_sis,moderated_grading,omit_from_final_grade,intra_group_peer_reviews,anonymous_instructor_annotations,anonymous_grading,graders_anonymous_to_graders,grader_count,grader_comments_visible_to_graders,final_grader_id,grader_names_visible_to_final_grader,allowed_attempts,annotatable_attachment_id,lti_context_id,course_id,assignment_name,submission_types,has_submitted_submissions,due_date_required,max_name_length,in_closed_grading_period,graded_submissions_exist,is_quiz_assignment,can_duplicate,original_course_id,original_assignment_id,original_lti_resource_link_id,original_assignment_name,original_quiz_id,workflow_state,important_dates,is_quiz_lti_assignment,frozen_attributes,external_tool_tag_attributes,muted,html_url,has_overrides,url,needs_grading_count,sis_assignment_id,integration_id,integration_data,published,unpublishable,only_visible_to_overrides,locked_for_user,submissions_download_url,post_manually,anonymize_students,require_lockdown_browser,quiz_id,anonymous_submissions) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                row.assignment_id,
                row.due_at,
                row.unlock_at,
                row.lock_at,
                row.points_possible,
                row.grading_type,
                row.assignment_group_id,
                row.grading_standard_id,
                row.created_at,
                row.updated_at,
                row.peer_reviews,
                row.automatic_peer_reviews,
                row.position,
                row.grade_group_students_individually,
                row.anonymous_peer_reviews,
                row.group_category_id,
                row.post_to_sis,
                row.moderated_grading,
                row.omit_from_final_grade,
                row.intra_group_peer_reviews,
                row.anonymous_instructor_annotations,
                row.anonymous_grading,
                row.graders_anonymous_to_graders,
                row.grader_count,
                row.grader_comments_visible_to_graders,
                row.final_grader_id,
                row.grader_names_visible_to_final_grader,
                row.allowed_attempts,
                row.annotatable_attachment_id,
                row.lti_context_id,
                row.course_id,
                row.assignment_name, 
                row.submission_types,
                row.has_submitted_submissions,
                row.due_date_required,
                row.max_name_length, 
                row.in_closed_grading_period,
                row.graded_submissions_exist,
                row.is_quiz_assignment, 
                row.can_duplicate,
                row.original_course_id,
                row.original_assignment_id,
                row.original_lti_resource_link_id,
                row.original_assignment_name,
                row.original_quiz_id,
                row.workflow_state,
                row.important_dates,
                row.is_quiz_lti_assignment,
                row.frozen_attributes,
                row.external_tool_tag_attributes,
                row.muted,
                row.html_url,
                row.has_overrides,
                row.url,
                row.needs_grading_count,
                row.sis_assignment_id,
                row.integration_id,
                row.integration_data,
                row.published,
                row.unpublishable,
                row.only_visible_to_overrides,
                row.locked_for_user,
                row.submissions_download_url,
                row.post_manually,
                row.anonymize_students,
                row.require_lockdown_browser,
                row.quiz_id,
                row.anonymous_submissions
                )
                
# Commit the inserts
cnxn.commit()

# Close the cursor
crsr.close()

# Close the connection
cnxn.close()
