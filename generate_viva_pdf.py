# ====================================================================
# Comprehensive Project Explanation & Viva Guide PDF Generator
# Designed for 2nd Year DBMS Course Project Evaluation
# ====================================================================

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = os.path.join(r"d:\db project\college_club_system\docs", "College_Club_Project_Viva_Guide.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Don't draw header/footer on cover/first page
        if self._pageNumber > 1:
            # Header
            self.drawString(54, letter[1] - 36, "College Club Event Management System — Complete Viva & Project Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 30, page_text)
            self.drawString(54, 30, "Confidential — Prepared for DBMS Project Viva & Faculty Evaluation")
            self.line(54, 42, letter[0] - 54, 42)
            
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Slate Blue
    c_dark = colors.HexColor("#2D3748")      # Charcoal
    c_accent = colors.HexColor("#2C5282")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    speech_box_style = ParagraphStyle(
        'SpeechBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1A202C")
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # COVER / HEADER SECTION
    # =========================================================================
    story.append(Paragraph("College Club Event Management System", title_style))
    story.append(Paragraph("<b>DBMS Individual Evaluation & Viva Survival Guide</b> | Academic Year 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=12))

    # Info Banner Table
    banner_data = [
        [
            Paragraph("<b>Subject:</b> Database Management Systems (DBMS)", body_style),
            Paragraph("<b>Target Stack:</b> Oracle XE 21c / Python Flask", body_style)
        ],
        [
            Paragraph("<b>Student Role:</b> Second Year Engineering Student", body_style),
            Paragraph("<b>Prepared For:</b> One-on-One Faculty Review & Viva", body_style)
        ]
    ]
    t_banner = Table(banner_data, colWidths=[250, 254])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 1: THE 1-MINUTE PITCH
    # =========================================================================
    story.append(Paragraph("Part 1: The 1-Minute Pitch (What to Say When You Sit Down)", h1_style))
    story.append(Paragraph("When your faculty asks: <i>'Tell me about your project'</i>, do not panic or ramble. Speak this exact, confident answer:", body_style))

    speech_box = [
        [
            Paragraph(
                "\"Good morning / afternoon Ma'am. My project is the <b>College Club Event Management System</b>.<br/><br/>"
                "In our college, various technical, cultural, and sports clubs organize events throughout the semester. "
                "Usually, registrations and member lists are handled using scattered Google Forms or paper sheets. "
                "This causes major issues like duplicate signups, no membership verification, and students accidentally registering for past events.<br/><br/>"
                "To solve this, I designed a <b>normalized relational database in 3NF</b> with 5 core tables. "
                "I implemented strict database integrity constraints, <b>two database views</b> for reporting, a <b>PL/SQL stored procedure</b> "
                "that blocks duplicate or expired registrations, and a <b>database trigger</b>.<br/><br/>"
                "On top of this, I built a clean web interface using <b>Python Flask</b> and parameterized SQL queries to prevent SQL injection. "
                "May I demonstrate how the system works?\"",
                speech_box_style
            )
        ]
    ]
    t_speech = Table(speech_box, colWidths=[504])
    t_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCBF")), # Light amber callout
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D69E2E")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_speech)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 2: HOW THE SYSTEM WORKS UNDER THE HOOD
    # =========================================================================
    story.append(Paragraph("Part 2: How the System Works (Architecture in Plain English)", h1_style))
    story.append(Paragraph("Your system follows a clean 3-Tier Architecture that you can explain on the whiteboard:", body_style))

    arch_data = [
        [Paragraph("<b>Tier</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>What It Does in Simple Words</b>", body_style)],
        [
            Paragraph("<b>Frontend (Presentation)</b>", body_style),
            Paragraph("HTML5, Vanilla CSS3, Jinja2", body_style),
            Paragraph("Displays web pages (Home, Students, Clubs, Events, Reports). Takes user inputs via forms. No heavy JS frameworks.", body_style)
        ],
        [
            Paragraph("<b>Backend (Application)</b>", body_style),
            Paragraph("Python 3 + Flask (app.py)", body_style),
            Paragraph("Receives HTTP requests, runs parameterized SQL queries using bind variables (:param), commits transactions, and renders templates.", body_style)
        ],
        [
            Paragraph("<b>Database (Storage & Logic)</b>", body_style),
            Paragraph("Oracle Database 21c XE<br/>(with SQLite local fallback)", body_style),
            Paragraph("Stores tables in 3NF, executes views for fast analytical lookups, runs stored procedures for registration logic, and fires triggers.", body_style)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[110, 140, 254])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 3: STEP-BY-STEP LIVE DEMO GUIDE
    # =========================================================================
    story.append(Paragraph("Part 3: Step-by-Step Live Demo Guide (What to Click & What to Say)", h1_style))
    story.append(Paragraph("Follow this exact 5-step sequence when demonstrating on your laptop:", body_style))

    demo_steps = [
        ("Step 1: The Home Page (http://127.0.0.1:5000)", [
            "<b>Action:</b> Show the 3 top metric cards (Students, Clubs, Upcoming Events) and the upcoming events table.",
            "<b>What to Say:</b> <i>'Ma'am, this dashboard automatically fetches live metrics. The Upcoming Events table filters events dynamically using <code>WHERE event_date &gt;= SYSDATE</code> so expired events are never shown to students.'</i>"
        ]),
        ("Step 2: Students Page (/students) — Adding a Student", [
            "<b>Action:</b> Enter a name (e.g. 'Varun Kumar'), email ('varun@college.edu'), department ('Computer Science'), year ('2'). Click <b>Add Student</b>.",
            "<b>What to Say:</b> <i>'Here we have our Student table. The input year is strictly restricted between 1 and 4 using a domain CHECK constraint, and emails must be unique.'</i>"
        ]),
        ("Step 3: Clubs Page (/clubs) — Database View & Joining", [
            "<b>Action:</b> Point out the member count. Click <b>'View Members'</b> on Coding Club. Then enroll Varun into Robotics Society using the join form.",
            "<b>What to Say:</b> <i>'This member list is powered by our database view <b>club_member_list</b> which pre-joins CLUB, MEMBERSHIP, and STUDENT. When joining, the composite constraint <code>UNIQUE(student_id, club_id)</code> ensures a student cannot join the same club twice.'</i>"
        ]),
        ("Step 4: Events Page (/events) — Stored Procedure & Duplicate Block", [
            "<b>Action:</b> Try registering Aarav Sharma for 'CodeStorm' (already registered) -> Show red error message. Then register Varun Kumar -> Show green success message. Finally, click <b>Cancel</b> on any registration.",
            "<b>What to Say:</b> <i>'Registration is handled by our PL/SQL stored procedure <b>register_student_for_event</b>. Notice how it blocked Aarav because he was already registered, but allowed Varun. It returns a clean status message directly from the database.'</i>"
        ]),
        ("Step 5: Reports Page (/reports) — Showcase Advanced SQL", [
            "<b>Action:</b> Scroll through the 4 analytical report tables.",
            "<b>What to Say:</b> <i>'This page demonstrates complex SQL queries required in the DBMS curriculum: multi-table INNER and LEFT JOINs, GROUP BY, aggregate functions like COUNT(), and the <b>HAVING &gt;= 2</b> clause to filter grouped records.'</i>"
        ]),
        ("Step 6: Show the Command-Line Interface (view_db.exe)", [
            "<b>Action:</b> Open CMD, run <code>view_db.exe</code>, press <b>4</b> to show memberships.",
            "<b>What to Say:</b> <i>'Ma'am, our database is fully persistent and synchronized. Any member I just added in the web browser is immediately visible here in the SQL console.'</i>"
        ])
    ]

    for title, points in demo_steps:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # PART 4: DATABASE SCHEMA & ER DIAGRAM
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("Part 4: Database Schema & Entity-Relationship (ER) Design", h1_style),
        Paragraph("The database consists of <b>5 tables</b> designed strictly from your ER Diagram:", body_style)
    ]))

    # ER diagram image if available
    img_path = r"d:\db project\college_club_system\static\er_diagram.jpg"
    if os.path.exists(img_path):
        story.append(Spacer(1, 4))
        story.append(Image(img_path, width=6.8*inch, height=3.6*inch))
        story.append(Spacer(1, 6))

    schema_table_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Primary Key (PK)</b>", body_style), Paragraph("<b>Foreign Keys (FK)</b>", body_style), Paragraph("<b>Key Constraints</b>", body_style)],
        [
            Paragraph("<b>STUDENT</b>", body_style),
            Paragraph("student_id", body_style),
            Paragraph("None", body_style),
            Paragraph("<code>UNIQUE(email)</code><br/><code>CHECK(year BETWEEN 1 AND 4)</code>", body_style)
        ],
        [
            Paragraph("<b>CLUB</b>", body_style),
            Paragraph("club_id", body_style),
            Paragraph("None", body_style),
            Paragraph("<code>UNIQUE(club_name)</code>", body_style)
        ],
        [
            Paragraph("<b>EVENT</b>", body_style),
            Paragraph("event_id", body_style),
            Paragraph("club_id &rarr; CLUB(club_id)", body_style),
            Paragraph("<code>ON DELETE CASCADE</code>", body_style)
        ],
        [
            Paragraph("<b>MEMBERSHIP</b>", body_style),
            Paragraph("membership_id", body_style),
            Paragraph("student_id &rarr; STUDENT<br/>club_id &rarr; CLUB", body_style),
            Paragraph("<code>UNIQUE(student_id, club_id)</code><br/><code>ON DELETE CASCADE</code>", body_style)
        ],
        [
            Paragraph("<b>REGISTRATION</b>", body_style),
            Paragraph("registration_id", body_style),
            Paragraph("student_id &rarr; STUDENT<br/>event_id &rarr; EVENT", body_style),
            Paragraph("<code>UNIQUE(student_id, event_id)</code><br/><code>CHECK(status IN ('REGISTERED', 'CANCELLED', 'ATTENDED'))</code>", body_style)
        ]
    ]
    t_schema = Table(schema_table_data, colWidths=[90, 100, 140, 174])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 5: NORMALIZATION (3NF) MADE SUPER EASY
    # =========================================================================
    story.append(Paragraph("Part 5: Normalization Justification (How to Prove 3NF)", h1_style))
    story.append(Paragraph("If the faculty asks: <i>'Prove your database is normalized up to 3NF'</i>, explain these 3 clear points:", body_style))

    norm_points = [
        ("1. First Normal Form (1NF) — Atomic Values", [
            "Every column in every table contains single, indivisible (atomic) values.",
            "There are no repeating groups (e.g. we do not store multiple events in one column as 'Event1, Event2').",
            "Every table has a designated Primary Key."
        ]),
        ("2. Second Normal Form (2NF) — No Partial Dependency", [
            "The database is already in 1NF.",
            "No non-key attribute depends on a part of a composite primary key. Every non-key column depends on the full primary key.",
            "In associative tables (<code>MEMBERSHIP</code> and <code>REGISTRATION</code>), surrogate primary keys (<code>membership_id</code>, <code>registration_id</code>) are used, so all attributes depend on the full primary key."
        ]),
        ("3. Third Normal Form (3NF) — No Transitive Dependency", [
            "The database is already in 2NF.",
            "No non-key column determines another non-key column (no X &rarr; Y where X is non-prime).",
            "<b>Concrete Example:</b> In the <code>EVENT</code> table, we only store <code>club_id</code>. We do NOT duplicate <code>club_name</code> or <code>faculty_coordinator</code> in EVENT. Those details belong exclusively in <code>CLUB</code>.",
            "<b>Concrete Example 2:</b> In <code>REGISTRATION</code>, we only store <code>student_id</code> and <code>event_id</code>. We do not store <code>student_name</code> or <code>email</code> in REGISTRATION."
        ])
    ]
    for title, points in norm_points:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 6: ADVANCED DBMS FEATURES
    # =========================================================================
    story.append(Paragraph("Part 6: Advanced DBMS Features Implemented", h1_style))

    db_features = [
        ("1. View 1: event_registration_count", "Combines EVENT, CLUB, and REGISTRATION using a <code>LEFT JOIN</code> and <code>GROUP BY</code>. Counts how many students are currently registered for each event. Simplifies coordinator queries without calculating aggregates repeatedly."),
        ("2. View 2: club_member_list", "Combines CLUB, MEMBERSHIP, and STUDENT using <code>INNER JOIN</code>. Provides a complete student roster for each club, abstracting away the complex join logic from web pages."),
        ("3. Stored Procedure: register_student_for_event", "Accepts <code>p_student_id</code>, <code>p_event_id</code>, and returns <code>p_message (OUT)</code>.<br/>"
         "• Checks if student and event exist.<br/>"
         "• Validates event date: If <code>event_date &lt; SYSDATE</code>, rejects registration.<br/>"
         "• Checks duplicate registration: If already registered, rejects signup.<br/>"
         "• If previously cancelled, re-activates status to 'REGISTERED'. Otherwise inserts fresh row."),
        ("4. Trigger: prevent_past_event_registration", "A <code>BEFORE INSERT ON REGISTRATION FOR EACH ROW</code> trigger. If any application or user tries to insert a registration for an event whose date has already passed, the trigger executes <code>RAISE_APPLICATION_ERROR(-20001, 'Registration Closed')</code>. This guarantees database-level integrity even outside the web UI.")
    ]
    for feat_title, feat_desc in db_features:
        story.append(Paragraph(feat_title, h2_style))
        story.append(Paragraph(feat_desc, body_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 7: 15 MUST-KNOW VIVA QUESTIONS & INSTANT ANSWERS
    # =========================================================================
    story.append(Paragraph("Part 7: 15 Must-Know Viva Questions & Instant Answers", h1_style))
    story.append(Paragraph("Read these questions and short answers before walking into the room:", body_style))

    viva_qa = [
        ("Q1: What are the main entities in your ER diagram and what do they represent?",
         "We have 5 entities: STUDENT (student profile), CLUB (student organizations), EVENT (activities hosted by clubs), MEMBERSHIP (students joining clubs), and REGISTRATION (students signing up for events)."),
        
        ("Q2: What is an associative entity and why did you use it?",
         "An associative entity resolves a Many-to-Many (M:N) relationship. A Student can join many Clubs, and a Club has many Students. We cannot store this directly in one table without repeating data, so we created the associative entity MEMBERSHIP."),

        ("Q3: What is the difference between a Primary Key and a Unique Key?",
         "A table can have only one Primary Key, but multiple Unique keys. Primary Key cannot contain NULL, while Unique keys allow NULL (unless marked NOT NULL)."),

        ("Q4: What is Referential Integrity?",
         "Referential integrity ensures relationships between tables remain consistent. Foreign keys cannot reference a non-existent parent primary key. In our schema, an event cannot reference a club_id that does not exist."),

        ("Q5: What does ON DELETE CASCADE do in your schema?",
         "When a parent record is deleted, all matching child records are automatically removed. For example, deleting a club automatically deletes all events hosted by that club and its memberships, preventing orphan rows."),

        ("Q6: What is a Database View and what is its advantage?",
         "A View is a virtual table based on a saved SQL query. It does not duplicate physical data. It provides query simplicity, security (restricting direct table access), and abstraction of complex JOINs."),

        ("Q7: What is the difference between a Stored Procedure and a Function?",
         "A Stored Procedure does not have to return a value and can have IN, OUT, and IN OUT parameters. A Function must return a single value and can be called directly inside a SQL SELECT statement."),

        ("Q8: What is the difference between a Stored Procedure and a Trigger?",
         "A Stored Procedure must be explicitly invoked by an application or user (e.g. cursor.callproc). A Trigger executes automatically (fires) when a DML event like INSERT, UPDATE, or DELETE occurs on a table."),

        ("Q9: What is the difference between WHERE and HAVING clauses?",
         "WHERE filters individual rows BEFORE grouping. HAVING filters groups AFTER aggregate functions (like COUNT, SUM) have been calculated in a GROUP BY clause."),

        ("Q10: What is the difference between INNER JOIN and LEFT JOIN?",
         "INNER JOIN returns only rows that have matching keys in both tables. LEFT JOIN returns all rows from the left table, and matching rows from the right table (filling NULL if there is no match)."),

        ("Q11: Why did you use SQL bind variables (:param) instead of string formatting?",
         "Two reasons: 1. Security: Completely blocks SQL Injection attacks because input is treated purely as data, not executable code. 2. Performance: Allows Oracle to reuse compiled execution plans in the shared pool."),

        ("Q12: What CHECK constraints did you implement in your project?",
         "We implemented: 1. `CHECK (year BETWEEN 1 AND 4)` on STUDENT to prevent invalid academic years. 2. `CHECK (status IN ('REGISTERED', 'CANCELLED', 'ATTENDED'))` on REGISTRATION to enforce valid status values."),

        ("Q13: What is a composite UNIQUE constraint and where is it used?",
         "A composite UNIQUE constraint enforces uniqueness across a combination of multiple columns. In MEMBERSHIP, `UNIQUE(student_id, club_id)` prevents a student from joining the same club twice."),

        ("Q14: What are ACID properties in database transactions?",
         "Atomicity (all or nothing), Consistency (preserves constraints), Isolation (concurrent transactions do not interfere), and Durability (committed data survives server crashes). Every transaction in our app uses commit() or rollback()."),

        ("Q15: How does your application connect to Oracle Database?",
         "We use python-oracledb in pure Thin Mode. It connects directly over TCP/IP to localhost:1521/XEPDB1 without requiring Oracle Instant Client or external C libraries.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, ans_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # PART 8: FACULTY TRAP QUESTIONS & HOW TO ANSWER
    # =========================================================================
    story.append(Paragraph("Part 8: Faculty 'Trap' Questions & Confident Answers", h1_style))
    story.append(Paragraph("Evaluators love testing your conceptual depth with these tricky questions:", body_style))

    traps = [
        ("Trap 1: 'Why didn't you just add club_name into the EVENT table to make queries faster?'",
         "Answer: \"Ma'am, storing club_name in EVENT would introduce a <b>transitive dependency</b> (event_id &rarr; club_id &rarr; club_name), which violates Third Normal Form (3NF). If a club's name is ever updated, we would have to update multiple event records, creating an <b>update anomaly</b>. In 3NF, club_name stays strictly in the CLUB table.\""),

        ("Trap 2: 'If you already have a stored procedure checking the event date, why do you need a trigger?'",
         "Answer: \"Ma'am, the stored procedure protects registrations coming from our web app. But if a database administrator or another application directly executes an <code>INSERT</code> in SQL*Plus or DBeaver, the procedure is bypassed. The <b>trigger acts as a database-level safety net</b> that enforces the rule regardless of which client connects.\""),

        ("Trap 3: 'What happens if two students try to register at the exact same millisecond?'",
         "Answer: \"Our database uses <b>Isolation and unique constraints</b>. The constraint <code>UNIQUE(student_id, event_id)</code> ensures that even under concurrent requests, only one insert can succeed while the second will be rejected by the database engine without data corruption.\"")
    ]

    for q, a in traps:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, ans_style))

    # Build the PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
