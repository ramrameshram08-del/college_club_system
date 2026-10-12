-- ====================================================================
-- College Club Event Management System
-- Sample Data Insertion Script for Oracle Database 21c XE
--
-- Data counts:
-- - 10 Students
-- - 5 Clubs
-- - 10 Events (Mix of upcoming and past events)
-- - 15 Memberships
-- - 20 Registrations
-- ====================================================================

-- 1. Insert 10 Students
INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (1, 'Aarav Sharma', 'aarav.sharma@college.edu', 'Computer Science', 2);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (2, 'Diya Patel', 'diya.patel@college.edu', 'Information Technology', 3);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (3, 'Rohan Verma', 'rohan.verma@college.edu', 'Electronics', 1);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (4, 'Ananya Iyer', 'ananya.iyer@college.edu', 'Computer Science', 4);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (5, 'Karthik Nair', 'karthik.nair@college.edu', 'Mechanical', 2);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (6, 'Sneha Gupta', 'sneha.gupta@college.edu', 'Information Technology', 2);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (7, 'Vikram Singh', 'vikram.singh@college.edu', 'Civil', 3);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (8, 'Pooja Joshi', 'pooja.joshi@college.edu', 'Computer Science', 1);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (9, 'Rahul Mehta', 'rahul.mehta@college.edu', 'Electronics', 4);

INSERT INTO STUDENT (student_id, student_name, email, department, year)
VALUES (10, 'Ishita Rao', 'ishita.rao@college.edu', 'Information Technology', 3);


-- 2. Insert 5 Clubs
INSERT INTO CLUB (club_id, club_name, category, faculty_coordinator)
VALUES (1, 'Coding & Algo Club', 'Technical', 'Dr. Ramesh Sundaram');

INSERT INTO CLUB (club_id, club_name, category, faculty_coordinator)
VALUES (2, 'Robotics Society', 'Technical', 'Prof. Sunita Deshmukh');

INSERT INTO CLUB (club_id, club_name, category, faculty_coordinator)
VALUES (3, 'Cultural & Drama Guild', 'Cultural', 'Prof. Meera Kulkarni');

INSERT INTO CLUB (club_id, club_name, category, faculty_coordinator)
VALUES (4, 'Literary & Debating Club', 'Literary', 'Dr. Alok Mukherjee');

INSERT INTO CLUB (club_id, club_name, category, faculty_coordinator)
VALUES (5, 'Sports & Fitness Club', 'Sports', 'Coach Vikram Rathore');


-- 3. Insert 10 Events (Events 1-3 are recent past; Events 4-10 are upcoming)
INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (1, 'Intro to Competitive Programming', TRUNC(SYSDATE) - 15, 'Lab 301, CS Block', 1);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (2, 'RoboWars Workshop', TRUNC(SYSDATE) - 7, 'Mechanical Workshop Hall', 2);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (3, 'Annual Street Play Auditions', TRUNC(SYSDATE) - 2, 'Open Air Theatre', 3);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (4, 'Hackathon 2026: CodeStorm', TRUNC(SYSDATE) + 5, 'Main Auditorium', 1);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (5, 'Drone Flying & Autonomous Navigation', TRUNC(SYSDATE) + 10, 'Football Ground', 2);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (6, 'Inter-College Debate Championship', TRUNC(SYSDATE) + 14, 'Seminar Hall B', 4);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (7, 'Spring Music Fest & Battle of Bands', TRUNC(SYSDATE) + 18, 'College Amphitheatre', 3);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (8, 'Table Tennis & Badminton Tournament', TRUNC(SYSDATE) + 22, 'Indoor Sports Complex', 5);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (9, 'Web Development Bootcamp with Flask', TRUNC(SYSDATE) + 28, 'Lab 204, IT Block', 1);

INSERT INTO EVENT (event_id, event_name, event_date, venue, club_id)
VALUES (10, 'Creative Writing & Poetry Slam', TRUNC(SYSDATE) + 35, 'Central Library Reading Room', 4);


-- 4. Insert 15 Memberships (Students joining clubs)
INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (1, 1, 1, TRUNC(SYSDATE) - 60);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (2, 1, 2, TRUNC(SYSDATE) - 45);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (3, 2, 1, TRUNC(SYSDATE) - 50);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (4, 2, 4, TRUNC(SYSDATE) - 30);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (5, 3, 2, TRUNC(SYSDATE) - 40);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (6, 3, 5, TRUNC(SYSDATE) - 20);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (7, 4, 1, TRUNC(SYSDATE) - 90);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (8, 4, 3, TRUNC(SYSDATE) - 80);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (9, 5, 2, TRUNC(SYSDATE) - 35);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (10, 6, 1, TRUNC(SYSDATE) - 25);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (11, 6, 4, TRUNC(SYSDATE) - 15);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (12, 7, 5, TRUNC(SYSDATE) - 55);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (13, 8, 1, TRUNC(SYSDATE) - 10);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (14, 9, 2, TRUNC(SYSDATE) - 70);

INSERT INTO MEMBERSHIP (membership_id, student_id, club_id, join_date)
VALUES (15, 10, 3, TRUNC(SYSDATE) - 12);


-- 5. Insert 20 Registrations
-- Past event registrations (Event 1, 2, 3)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (1, 1, 1, 'ATTENDED', TRUNC(SYSDATE) - 18);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (2, 2, 1, 'ATTENDED', TRUNC(SYSDATE) - 17);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (3, 4, 1, 'ATTENDED', TRUNC(SYSDATE) - 16);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (4, 3, 2, 'ATTENDED', TRUNC(SYSDATE) - 9);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (5, 5, 2, 'CANCELLED', TRUNC(SYSDATE) - 8);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (6, 9, 2, 'ATTENDED', TRUNC(SYSDATE) - 8);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (7, 4, 3, 'ATTENDED', TRUNC(SYSDATE) - 4);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (8, 10, 3, 'ATTENDED', TRUNC(SYSDATE) - 3);

-- Upcoming event registrations (Event 4: CodeStorm)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (9, 1, 4, 'REGISTERED', TRUNC(SYSDATE) - 2);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (10, 2, 4, 'REGISTERED', TRUNC(SYSDATE) - 2);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (11, 4, 4, 'REGISTERED', TRUNC(SYSDATE) - 1);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (12, 6, 4, 'REGISTERED', TRUNC(SYSDATE) - 1);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (13, 8, 4, 'REGISTERED', TRUNC(SYSDATE));

-- Upcoming event registrations (Event 5: Drone)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (14, 3, 5, 'REGISTERED', TRUNC(SYSDATE) - 1);

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (15, 5, 5, 'REGISTERED', TRUNC(SYSDATE));

-- Upcoming event registrations (Event 6: Debate)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (16, 2, 6, 'REGISTERED', TRUNC(SYSDATE));

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (17, 6, 6, 'REGISTERED', TRUNC(SYSDATE));

-- Upcoming event registrations (Event 7: Music Fest)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (18, 4, 7, 'REGISTERED', TRUNC(SYSDATE));

INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (19, 10, 7, 'REGISTERED', TRUNC(SYSDATE));

-- Upcoming event registrations (Event 8: Sports)
INSERT INTO REGISTRATION (registration_id, student_id, event_id, status, registration_date)
VALUES (20, 7, 8, 'REGISTERED', TRUNC(SYSDATE));

COMMIT;
