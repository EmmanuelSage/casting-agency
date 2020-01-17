import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIyMjI4NWY4MjhmYzBlOTM5ZWEyMTEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTI5NjUxMiwiZXhwIjoxNTc5MzAzNzEyLCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.RABDGAvVAoIcA2CqIWDNMojmTVEjdBcEsXon6V3tIZJcP0EnKnDwdB0jx4IFOiiAHiruhqGsGcP2grEWzc_fv5ErGNDh03YqNs9KU3pQIX3rhLALSAAB1DywGkWz0ENDM9zNEXv1R9yIQLB9zYq1thVo6TJF9NCjgTkjhGVo7DoeGA8WsCOaH5POyFtFyE8FFdGURfX0r7vdMYvCdhaCnVpdvZFo7t0cLoq0-tyljQDWIEpUgIpLDNdf0ksBvPP4FyEyRrYjUGPVcvRa5UKhVm4spcYjfsRryMxRaR3YxvKguQ9YwNZI4VvLIUf7-b8BO8iVJWNuBsoSW3Bnnwffcw'

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIxZGExNWVmMzkzNDBkY2QxYzczOWQiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTI5NTc2NywiZXhwIjoxNTc5MzAyOTY3LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.HTNFzsa0DEXv1UCDAyq7XAGAffiKpPElUeNOxqHpNaIrxg63sR3FfN2np5_6m7t77EV0u4wOxleNIdTnedXmxcQ1TWuB5vAM-CNIZdOuNvppCW_8peH9IfkEeH4A1XLZgjfm6lhU7Y6xALmqWXIic04nyNDDuHMP9DaBXL7lgIJGn8QUjcGhqbxnEnFoR8hrcsEKLYm1vu7wvG3gv0h-7lKDtcJnXVrEOJR-_62yAeRd7GSSQ_Rw5LwbYa8rOPh5SfBv1g5jsWIwmdUYNA4rUnXb6XKdS6VkgXEQAvIFHQYQ56WW4CV3a7MS_sLIYNJzGr8LEFIJ-OnGDCI2eB0S4Q'

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMjc4NzYxODkzNDU0NDQ3NTgxNyIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vZXNhZ2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3OTI5NDY0OSwiZXhwIjoxNTc5MzAxODQ5LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.R6ngftoQMNw39cOM7gfEG8p0uuzC1ngLzzxYHjmdXjmPk-O1xG-cBBkOWdabHo7dCJII6mAIg1ku3ygzfFlCsA6n6JQxmJiNGHL3cR5iDeiEDNTAWkwPbic071wopNepvPuzpnFoaivsYPE-fryKOhrrPMMZ7qRVoVYiG5ce5TiinuQsRIQ8_r3z-X72hyx0ui7U6Eb_f3Az3mVabde9zxm-anktzp_4I3aZR06WaUz4bLbtTi0flkd28-OY33DeZqNx8KCHjgjn2s6bFyagbPNYVBeIEbGZD4IR7jWTPu9er-38M2prMmGaiTCPi9WUzWjkTxnOmVRNkh_ZwHwbig'

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
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
