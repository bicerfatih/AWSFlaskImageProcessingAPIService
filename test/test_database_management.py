import unittest
import database_management
import sqlite3
import os

class TestDatabaseManagement(unittest.TestCase):

    def test_database_creation_and_insertion(self):
        db_name = 'test_images.db'
        test_csv = 'test_data.csv'  # You should create a test CSV file
        database_management.create_and_populate_db(test_csv, db_name)

        # Check if database file is created
        self.assertTrue(os.path.exists(db_name))

        # Check if data is inserted
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM image_data")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0)

        # Clean up (delete test database file)
        os.remove(db_name)

if __name__ == '__main__':
    unittest.main()
