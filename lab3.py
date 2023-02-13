# install postgreSQL
sudo apt install postgresql postgresql-contrib
sudo -i -u postgres

# open postgre command line
psql

# create database
CREATE DATABASE lab3;
\c lab3

# create table
CREATE TABLE faculty 
(
	id SERIAL, 
	course_name varchar(100) UNIQUE NOT NULL, 
	deans_office varchar(100) NOT NULL, 
	PRIMARY KEY (id)
);

# fill table
INSERT INTO faculty (course_name, deans_office) 
VALUES ('09.03.01', 'Gorodnichev M.G.');
INSERT INTO faculty (course_name, deans_office) 
VALUES ('15.03.04', 'Ievlev O.P.');

# check table is correct
SELECT * FROM faculty;

# create reference table 2
CREATE TABLE student_group 
(
	id SERIAL, 
	group_number varchar(100) UNIQUE NOT NULL, 
	faculty varchar(100) NOT NULL REFERENCES faculty(course_name), 
	PRIMARY KEY (id)
);

# fill table 2
INSERT INTO student_group (group_number, faculty) 
VALUES ('BVT2201', '09.03.01');
INSERT INTO student_group (group_number, faculty) 
VALUES ('BVT2204', '09.03.01');
INSERT INTO student_group (group_number, faculty) 
VALUES ('VVT2201', '15.03.04');
INSERT INTO student_group (group_number, faculty) 
VALUES ('VVT2204', '15.03.04');

# check table is correct
SELECT * FROM student_group;

# create a reference table 3
CREATE TABLE students 
(
	id SERIAL, 
	name varchar(100) NOT NULL, 
	passport varchar(100) NOT NULL, 
	group_number varchar(100) NOT NULL REFERENCES student_group(group_number), 
	PRIMARY KEY (id)
);

# fill table 3 
INSERT INTO students (name, passport, group_number) 
VALUES ('Bob', '13 13 101101', 'BVT2201');

# check table is correct
SELECT * FROM students;
