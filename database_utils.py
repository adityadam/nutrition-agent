import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file="nutrition_data.db"):
        self.db_file = db_file
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            age TEXT,
            country TEXT,
            state TEXT,
            health_goal TEXT,
            disease TEXT,
            preferences TEXT,
            allergies TEXT,
            fitness_routine TEXT
        )
        ''')

        # Create reports table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input_id INTEGER,
            report_content TEXT,
            timestamp DATETIME,
            FOREIGN KEY (user_input_id) REFERENCES user_inputs (id)
        )
        ''')

        # Create feedback table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            rating INTEGER,
            comments TEXT,
            timestamp DATETIME,
            FOREIGN KEY (report_id) REFERENCES nutrition_reports (id)
        )
        ''')

        conn.commit()
        conn.close()

    def save_user_input(self, user_data):
        """Save user input to database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO user_inputs (
            timestamp, age, country, state, health_goal, 
            disease, preferences, allergies, fitness_routine
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            user_data['age'],
            user_data['country'],
            user_data['state'],
            user_data['health_goal'],
            user_data['disease'],
            user_data['preferences'],
            user_data['allergies'],
            user_data['fitness_routine']
        ))

        user_input_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_input_id

    def save_report(self, user_input_id, report_content):
        """Save generated report to database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO nutrition_reports (user_input_id, report_content, timestamp)
        VALUES (?, ?, ?)
        ''', (user_input_id, report_content, datetime.now()))

        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return report_id

    def save_feedback(self, report_id, rating, comments):
        """Save user feedback to database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO user_feedback (report_id, rating, comments, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (report_id, rating, comments, datetime.now()))

        conn.commit()
        conn.close()

    def get_user_history(self, user_input_id):
        """Retrieve user's nutrition plan history."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT r.report_content, r.timestamp, f.rating, f.comments
        FROM nutrition_reports r
        LEFT JOIN user_feedback f ON r.id = f.report_id
        WHERE r.user_input_id = ?
        ORDER BY r.timestamp DESC
        ''', (user_input_id,))

        results = cursor.fetchall()
        conn.close()
        return results
