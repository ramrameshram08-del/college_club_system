-- ====================================================================
-- College Club Event Management System
-- Showcase Queries for DBMS Evaluation / Viva
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Most Popular Events
-- Concepts: INNER JOIN, LEFT JOIN, GROUP BY, Aggregate function (COUNT), ORDER BY
-- Description: Finds all events ranked by the number of active registrations.
-- --------------------------------------------------------------------
SELECT 
    e.event_id,
    e.event_name,
    c.club_name,
    e.event_date,
    e.venue,
    COUNT(r.registration_id) AS active_registrations
FROM EVENT e
JOIN CLUB c ON e.club_id = c.club_id
LEFT JOIN REGISTRATION r ON e.event_id = r.event_id AND r.status = 'REGISTERED'
GROUP BY e.event_id, e.event_name, c.club_name, e.event_date, e.venue
ORDER BY active_registrations DESC, e.event_date ASC;


-- --------------------------------------------------------------------
-- QUERY 2: Clubs with Most Members (HAVING filter)
-- Concepts: JOIN, GROUP BY, Aggregate function (COUNT), HAVING clause
-- Description: Lists clubs that have at least 2 registered members.
-- --------------------------------------------------------------------
SELECT 
    c.club_id,
    c.club_name,
    c.category,
    c.faculty_coordinator,
    COUNT(m.membership_id) AS total_members
FROM CLUB c
JOIN MEMBERSHIP m ON c.club_id = m.club_id
GROUP BY c.club_id, c.club_name, c.category, c.faculty_coordinator
HAVING COUNT(m.membership_id) >= 2
ORDER BY total_members DESC;


-- --------------------------------------------------------------------
-- QUERY 3: Highly Active Students (Registered for more than 1 event)
-- Concepts: JOIN, GROUP BY, HAVING, Aggregate function (COUNT)
-- Description: Identifies students who have registered for multiple events.
-- --------------------------------------------------------------------
SELECT 
    s.student_id,
    s.student_name,
    s.department,
    s.year,
    COUNT(r.registration_id) AS total_events_registered
FROM STUDENT s
JOIN REGISTRATION r ON s.student_id = r.student_id
WHERE r.status = 'REGISTERED'
GROUP BY s.student_id, s.student_name, s.department, s.year
HAVING COUNT(r.registration_id) > 1
ORDER BY total_events_registered DESC;


-- --------------------------------------------------------------------
-- QUERY 4: Events With No Registrations Yet (Subquery / NOT IN)
-- Concepts: Subquery, NOT IN / NOT EXISTS
-- Description: Identifies events that currently have 0 registrations.
-- --------------------------------------------------------------------
SELECT 
    e.event_id,
    e.event_name,
    c.club_name,
    e.event_date,
    e.venue
FROM EVENT e
JOIN CLUB c ON e.club_id = c.club_id
WHERE e.event_id NOT IN (
    SELECT DISTINCT event_id 
    FROM REGISTRATION
);


-- --------------------------------------------------------------------
-- QUERY 5: Department-wise Club Participation
-- Concepts: Multiple JOINs, GROUP BY, Aggregate function (COUNT)
-- Description: Shows which academic departments are most active in clubs.
-- --------------------------------------------------------------------
SELECT 
    s.department,
    COUNT(DISTINCT s.student_id) AS unique_participating_students,
    COUNT(m.membership_id) AS total_club_memberships
FROM STUDENT s
JOIN MEMBERSHIP m ON s.student_id = m.student_id
GROUP BY s.department
ORDER BY total_club_memberships DESC;
