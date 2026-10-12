# ====================================================================
# Unit Tests for Flask Application Routes and Templates
# ====================================================================

import unittest
from unittest.mock import MagicMock, patch
import app

class CollegeClubSystemTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()

    @patch("app.get_db_connection")
    def test_home_page(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        # Mock responses for counts and events
        cursor.fetchone.side_effect = [(10,), (5,), (7,)]
        cursor.fetchall.return_value = [
            (4, "Hackathon 2026: CodeStorm", "2026-10-17", "Main Auditorium", "Coding & Algo Club")
        ]

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to College Club Event Management System", response.data)
        self.assertIn(b"Hackathon 2026", response.data)

    @patch("app.get_db_connection")
    def test_students_page(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        cursor.fetchall.return_value = [
            (1, "Aarav Sharma", "aarav@college.edu", "Computer Science", 2)
        ]

        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Management", response.data)
        self.assertIn(b"Aarav Sharma", response.data)

    @patch("app.get_db_connection")
    def test_clubs_page(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        cursor.fetchall.side_effect = [
            [(1, "Coding Club", "Technical", "Dr. Ramesh", 5)],  # clubs
            [(1, "Aarav Sharma")],                                # students dropdown
            [(1, "Aarav Sharma", "aarav@college.edu", "CS", 2, "2026-09-01")] # members view
        ]

        response = self.client.get("/clubs?selected_club=1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"College Clubs", response.data)
        self.assertIn(b"Coding Club", response.data)

    @patch("app.get_db_connection")
    def test_events_page(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        cursor.fetchall.side_effect = [
            [(1, "Intro to CP", "2026-10-01", "Lab 301", "Coding Club", 3)], # event_registration_count
            [(1, "Aarav Sharma")],                                           # students dropdown
            [(1, "Coding Club")],                                            # clubs dropdown
            [(4, "Hackathon", "2026-10-20")],                                # upcoming dropdown
            [(1, "Aarav Sharma", "Intro to CP", "2026-10-01", "REGISTERED", 1, 1)] # active registrations
        ]

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Event Management", response.data)
        self.assertIn(b"Intro to CP", response.data)

    @patch("app.get_db_connection")
    def test_reports_page(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        cursor.fetchall.side_effect = [
            [(4, "Hackathon", "Coding Club", "2026-10-20", 5)],  # report1
            [("Coding Club", "Technical", "Dr. Ramesh", 8)],      # report2
            [("Aarav Sharma", "Computer Science", 2, 3)],         # report3
            [("Computer Science", 4, 6)]                          # report4
        ]

        response = self.client.get("/reports")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DBMS Showcase Reports", response.data)
        self.assertIn(b"Most Popular Events", response.data)

    @patch("app.get_db_connection")
    def test_procedure_registration(self, mock_get_conn):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_get_conn.return_value = (conn, "oracle")

        out_mock = MagicMock()
        out_mock.getvalue.return_value = "Success: Student registered successfully."
        cursor.var.return_value = out_mock

        response = self.client.post("/events/register", data={"student_id": "1", "event_id": "4"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        cursor.callproc.assert_called_once()
        self.assertIn(b"Success: Student registered successfully.", response.data)

if __name__ == "__main__":
    unittest.main()
