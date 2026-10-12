-- ====================================================================
-- College Club Event Management System
-- Views, Stored Procedure, and Trigger for Oracle Database 21c XE
-- ====================================================================

-- --------------------------------------------------------------------
-- VIEW 1: event_registration_count
-- Description: Aggregates total registrations for each event along with
--              club information. Useful for coordinators to monitor capacity.
-- --------------------------------------------------------------------
CREATE OR REPLACE VIEW event_registration_count AS
SELECT 
    e.event_id,
    e.event_name,
    e.event_date,
    e.venue,
    c.club_name,
    COUNT(CASE WHEN r.status = 'REGISTERED' THEN 1 END) AS total_registered,
    COUNT(CASE WHEN r.status = 'ATTENDED' THEN 1 END) AS total_attended,
    COUNT(r.registration_id) AS total_history
FROM EVENT e
JOIN CLUB c ON e.club_id = c.club_id
LEFT JOIN REGISTRATION r ON e.event_id = r.event_id
GROUP BY e.event_id, e.event_name, e.event_date, e.venue, c.club_name;
/

-- --------------------------------------------------------------------
-- VIEW 2: club_member_list
-- Description: Joins CLUB, MEMBERSHIP, and STUDENT to provide a clean
--              roster of members for each club.
-- --------------------------------------------------------------------
CREATE OR REPLACE VIEW club_member_list AS
SELECT 
    c.club_id,
    c.club_name,
    c.category,
    s.student_id,
    s.student_name,
    s.email,
    s.department,
    s.year,
    m.join_date
FROM MEMBERSHIP m
JOIN CLUB c ON m.club_id = c.club_id
JOIN STUDENT s ON m.student_id = s.student_id;
/

-- --------------------------------------------------------------------
-- TRIGGER: prevent_past_event_registration
-- Description: Database-level safety rule. Blocks inserting a registration
--              with status 'REGISTERED' for any event whose date has passed.
-- --------------------------------------------------------------------
CREATE OR REPLACE TRIGGER prevent_past_event_registration
BEFORE INSERT ON REGISTRATION
FOR EACH ROW
DECLARE
    v_event_date DATE;
BEGIN
    -- Only check active registrations
    IF :NEW.status = 'REGISTERED' THEN
        SELECT event_date INTO v_event_date 
        FROM EVENT 
        WHERE event_id = :NEW.event_id;

        IF v_event_date < TRUNC(SYSDATE) THEN
            RAISE_APPLICATION_ERROR(-20001, 'Registration Closed: Event date has already passed.');
        END IF;
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Invalid Event: Referenced event does not exist.');
END;
/

-- --------------------------------------------------------------------
-- STORED PROCEDURE: register_student_for_event
-- Description: Business logic to register a student for an event.
-- Checks:
-- 1. Student existence
-- 2. Event existence and date (blocks past events)
-- 3. Duplicate registration check
-- Returns: p_message with status description.
-- --------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE register_student_for_event (
    p_student_id IN NUMBER,
    p_event_id   IN NUMBER,
    p_message    OUT VARCHAR2
) AS
    v_student_count NUMBER;
    v_event_count   NUMBER;
    v_event_date    DATE;
    v_reg_count     NUMBER;
    v_curr_status   VARCHAR2(20);
BEGIN
    -- 1. Check if student exists
    SELECT COUNT(*) INTO v_student_count 
    FROM STUDENT 
    WHERE student_id = p_student_id;

    IF v_student_count = 0 THEN
        p_message := 'Error: Student does not exist.';
        RETURN;
    END IF;

    -- 2. Check if event exists and get event date
    BEGIN
        SELECT event_date INTO v_event_date 
        FROM EVENT 
        WHERE event_id = p_event_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_message := 'Error: Event does not exist.';
            RETURN;
    END;

    -- 3. Check if event is in the past
    IF v_event_date < TRUNC(SYSDATE) THEN
        p_message := 'Error: Cannot register for past events.';
        RETURN;
    END IF;

    -- 4. Check existing registration
    BEGIN
        SELECT status INTO v_curr_status
        FROM REGISTRATION
        WHERE student_id = p_student_id AND event_id = p_event_id;

        IF v_curr_status = 'REGISTERED' THEN
            p_message := 'Error: Student is already registered for this event.';
            RETURN;
        ELSIF v_curr_status = 'CANCELLED' THEN
            -- Reactivate cancelled registration
            UPDATE REGISTRATION
            SET status = 'REGISTERED', registration_date = SYSDATE
            WHERE student_id = p_student_id AND event_id = p_event_id;

            COMMIT;
            p_message := 'Success: Registration re-activated.';
            RETURN;
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- No previous record, proceed to insert
            NULL;
    END;

    -- 5. Insert new registration
    INSERT INTO REGISTRATION (student_id, event_id, status, registration_date)
    VALUES (p_student_id, p_event_id, 'REGISTERED', SYSDATE);

    COMMIT;
    p_message := 'Success: Student registered successfully.';

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_message := 'Error: ' || SQLERRM;
END;
/
