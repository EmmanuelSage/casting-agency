import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIyMjI4NWY4MjhmYzBlOTM5ZWEyMTEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTMwMzk3MSwiZXhwIjoxNTc5MzkwMzcxLCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.eYCMTtFtgt0FpJpEyDAbuxYUTC5FSB5aZ4BidirWnpzdjvqi-ybFVIlGdw2Q2NKNEROLme1MCdQGWt5th14d8DfVqhOHqMtclm-fSwVfcpPJfD_IE6PzWEmaVVunr43NauVtUVBvu3tINNzteIKUGqx4T1Prv7wBKDfPLKxN3-Xl-glfSida4DDf9sl3jlcucsT9AHEG943rRTwAABxx-3ShBSoew3oBNEOs2JK8674qQ6pKf7yPB_NWANtP9677yUOkLfW6-z7RwtGKlueVQeW2Gpnr9BXCX7zkLeW5Bfkoj8G0PgCJCcBnUpr0I5PJ4v7MBE5jyttDO5FlPEVIsA'

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIxZGExNWVmMzkzNDBkY2QxYzczOWQiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU3OTMwNDA0NSwiZXhwIjoxNTc5MzkwNDQ1LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.PtcNKOMSyIz9yI1vPZ20ouIBjNO0bwo5tPWiMtPsFAmpb-xleLKtk5BQVfkRud8pBvExHgjkXNcIEFsC281K1fc7z60oX1gTj1A8bqTNG3-Z3gjZfR5L_Wq0sM_jtaTdgiM8xgasZHUS_bah7fF4vcYrAr1c6l49GJYrOpXgDPbL4cS9vQBDii7VefN442YFe48Z5DO_EaSmTokS9xZEAa0C9NGfsm3BS3xLqYCDRDgh1LT71KLum9ztuHb07iATYK5LQF4uajmxmIkKZynz_txo8wuMxDpgL--0KtDIkD2QlQUEU2gteJddCbAQVcKC4s12Tp5W6rb3DZ3O567qyg'

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNME00TXpjNVJrTXlOelZCTTBORFJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL2VzYWdlLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMjc4NzYxODkzNDU0NDQ3NTgxNyIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vZXNhZ2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU3OTMwMzgxOCwiZXhwIjoxNTc5MzkwMjE4LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.RqRlh72nTwgW3JpfmMqRtHFXy9J6RXu_OMdrmX0ojaIMbx2GiRbEw5S9zIRd_Wt0WFh9EjwRYZkkaneGeRrg5vowQ8qeELSLxuPD9psK9XgeQEK4zBwoYhvMa80YzTFPKXOkgpegrfv6ALRgdx3EmSMEiHWpDWtj7Wtq4R2us7-f1HF31KOA4xpa2Cds_JjMRhhhWLOZU95_TNxc2WtpdoUO_eSirtF0wXZJ-_L1S6uE2JbvQr2GG168bKqTR3xptc9GR_RHCX9c8XyqMw5t83m9qR2M9lI3I2oBFM4eB1_8HFuzJEZGWZwHlFiyQkhVjoPiX2KW_hCsW9C4ww7-ng'

class CastingAgencyTest(unittest.TestCase):
    """This is the test suite for the casting agency"""
    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Kungfu Masters',
            'release_date': '2020-05-06',
        }
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  GET /movies Test
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test to get a specific movie
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Terminator Dark Fate')

    # tests for an invalid id to get a specific movie
    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Kungfu Masters')
        self.assertEqual(data['movie']['release_date'], 'Wed, 06 May 2020 00:00:00 GMT')

    # Test to create a movie if no data is sent
    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests for an invalid id to get a specific movie
    def test_401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'Revelations', 'release_date': "2019-11-12"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Revelations')
        self.assertEqual(data['movie']['release_date'], 'Tue, 12 Nov 2019 00:00:00 GMT')

    # Test to create a movie if no data is sent
    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests for an invalid id to get a specific movie
    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific movie
    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for an invalid id to get a specific movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests for an invalid id to get a specific movie
    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific movie
    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    #  GET /Actors Test
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test to get a specific actor
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Will Smith')

    # tests for an invalid id to get a specific movie
    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Karl', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Karl')
        self.assertEqual(data['actor']['age'], 20)
        self.assertEqual(data['actor']['gender'], 'male')

    # Test to create an actor if no data is sent
    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    #
    def test_401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Mary', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update a movie
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Mariam', 'age': 25, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Mariam')
        self.assertEqual(data['actor']['age'], 25)
        self.assertEqual(data['actor']['gender'], 'female')

    # Test to create a actor if no data is sent
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests for an invalid id to get a specific movie
    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific movie
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'Johnathan', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for an invalid id to get a specific movie
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests for an invalid id to get a specific movie
    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific movie
    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
