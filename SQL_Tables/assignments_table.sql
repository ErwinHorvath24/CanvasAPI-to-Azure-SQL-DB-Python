CREATE TABLE [assignments](
[assignment_id] int NOT NULL, 
[due_at] varchar(200)NOT NULL,
[unlock_at] varchar(200) NOT NULL, 
[lock_at] varchar(200) NOT NULL, 
[points_possible] int NOT NULL, 
[grading_type] varchar(10) NOT NULL, 
[assignment_group_id] int NOT NULL, 
[grading_standard_id] varchar(50) NOT NULL, 
[created_at] varchar(100) NOT NULL, 
[updated_at] varchar(100) NOT NULL, 
[peer_reviews] varchar(100) NOT NULL, 
[automatic_peer_reviews] varchar(100) NOT NULL, 
[position] int NOT NULL,
[grade_group_students_individually] varchar(100) NOT NULL,
[anonymous_peer_reviews] varchar(100) NOT NULL, 
[group_category_id] varchar(100) NOT NULL, 
[post_to_sis] varchar(100) NOT NULL, 
[moderated_grading] varchar(100) NOT NULL, 
[omit_from_final_grade] varchar(100) NOT NULL, 
[intra_group_peer_reviews] varchar(100) NOT NULL, 
[anonymous_instructor_annotations] varchar(100) NOT NULL, 
[anonymous_grading] varchar(100) NOT NULL, 
[graders_anonymous_to_graders] varchar(100) NOT NULL, 
[grader_count] varchar(100) NOT NULL,
[grader_comments_visible_to_graders] varchar(100) NOT NULL, 
[final_grader_id] varchar(100) NOT NULL, 
[grader_names_visible_to_final_grader] varchar(100) NOT NULL, 
[allowed_attempts] varchar(100) NOT NULL, 
[annotatable_attachment_id] varchar(100) NOT NULL, 
[lti_context_id] varchar(500) NOT NULL, 
[course_id] varchar(100) NOT NULL, 
[assignment_name] varchar(500) NOT NULL, 
[submission_types] varchar(100) NOT NULL, 
[has_submitted_submissions] varchar(100) NOT NULL, 
[due_date_required] varchar(100) NOT NULL, 
[max_name_length] varchar(100) NOT NULL,
[in_closed_grading_period] varchar(100) NOT NULL,
[graded_submissions_exist] varchar(100) NOT NULL,
[is_quiz_assignment] varchar(100) NOT NULL,
[can_duplicate] varchar(100) NOT NULL,
[original_course_id] varchar(100) NOT NULL,
[original_assignment_id] varchar(100) NOT NULL,
[original_lti_resource_link_id] varchar(200) NOT NULL,
[original_assignment_name] varchar(500) NOT NULL,
[original_quiz_id] varchar(100) NOT NULL,
[workflow_state] varchar(500) NOT NULL,
[important_dates] varchar(500) NOT NULL,
[is_quiz_lti_assignment] varchar(500) NOT NULL,
[frozen_attributes] varchar(500) NOT NULL,
[external_tool_tag_attributes] varchar(500) NOT NULL,
[muted] varchar(500) NOT NULL,
[html_url] varchar(500) NOT NULL,
[has_overrides] varchar(500) NOT NULL,
[url] varchar(500) NOT NULL,
[needs_grading_count] int NOT NULL,
[sis_assignment_id] int NOT NULL,
[integration_id] varchar(500) NOT NULL,
[integration_data] varchar(500) NOT NULL,
[published] varchar(10) NOT NULL,
[unpublishable] varchar(10) NOT NULL,
[only_visible_to_overrides] varchar(10) NOT NULL,
[locked_for_user] varchar(10) NOT NULL,
[submissions_download_url] varchar(500) NOT NULL,
[post_manually] varchar(10) NOT NULL,
[anonymize_students] varchar(10) NOT NULL,
[require_lockdown_browser] varchar(10) NOT NULL,
[quiz_id] int NOT NULL,
[anonymous_submissions] int NOT NULL
)
GO