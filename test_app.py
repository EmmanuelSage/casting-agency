import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor


class CastingAgencyTest(unittest.TestCase):
    """This is the test suite for the casting agency"""
    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  GET /movies Test
    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
