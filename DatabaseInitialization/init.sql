CREATE TABLE IF NOT EXISTS timetable_computed (
	person_name VARCHAR(20), 
	timetable_name VARCHAR(20), 
	actual_timetable TEXT 
);


CREATE TABLE IF NOT EXISTS timetable_pending (
	person_name VARCHAR(20), 
	timetable_name VARCHAR(20), 
	actual_restrictions TEXT 
);
