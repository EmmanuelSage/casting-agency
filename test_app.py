import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

# Tokens are formatted as such to limit lenght on a line
CASTING_ASSISTANT = (
                      'eyJhbGciOiJSUzI1NiIsInR5cCI6'
                      'IkpXVCIsImtpZCI6Ik5qQkNSa1'
                      'EzTmtSRlJVUXdNME00TXpjNVJr'
                      'TXlOelZCTTBORFJEUXlNVGsyU'
                      'XpKQ1JrTXlRdyJ9.eyJpc3MiOiJodHRwczovL'
                      '2VzYWdlLmF1dGgwLmNvbS8'
                      'iLCJzdWIiOiJhdXRoMHw1ZT'
                      'IyMjI4NWY4MjhmYzBlOTM5'
                      'ZWEyMTEiLCJhdWQiOiJjYX'
                      'N0aW5nLWFnZW5jeSIsImlhdCI6MT'
                      'U3OTUxMzk3OSwiZXhwIjoxNTc5NjAw'
                      'Mzc5LCJhenAiOiJ0S0lIT0NpVkVzTUQ'
                      'wYVZ1eUZ6WW1VU3BVUzFCV2hyeSIsInNj'
                      'b3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ'
                      '2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0'
                      '.dWp9RxbudYBH4dOVGEBZhGJOQFF4XwS7'
                      'DsBBFNmrF6dpCK4B-CEnJpV1JLVG8UMTb'
                      'NJP_VtsraMhshwWVwb8godKroue4pgCr'
                      'BsI8V5Q3cSHQ-8FhnpOTf0_te6ydoBy78u'
                      'O9dQCYtA7i2A32QW9OU7MTV9m9iCj70-kt'
                      'lhpYweP5SGMxyK8hfoNSXD9a1rKDAEvP4u'
                      'Y57eI-TQaHg-4odEZhACy78LBdeRADbu0O'
                      '6bfkxa27sJTBq3cVLbyscVJRr-TrJpcqh42v'
                      'v9SJRoDo1RRtnNeggmybg_UB_C2weK7HezvbsJA'
                      '-v6Dz49pMY7v29Oj_QRLo5-2bD2M5cM-jw'
                    )


CASTING_DIRECTOR = (
                    'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVC'
                    'IsImtpZCI6Ik5qQkNSa1EzTmtSRlJVUXdNM'
                    'E00TXpjNVJrTXlOelZCTTBORFJEUXlNVGs'
                    'yUXpKQ1JrTXlRdyJ9.eyJpc3MiO'
                    'iJodHRwczovL2VzYWdlLmF1dGgw'
                    'LmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIxZGExNWVmM'
                    'zkzNDBkY2QxYzczOWQiLCJhdWQiOiJjYXN0aW5nLWFnZW'
                    '5jeSIsImlhdCI6MTU3OTUxNDAxNCwiZXhwIjoxNTc5NjAwND'
                    'E0LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU3BVUzF'
                    'CV2hyeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVs'
                    'ZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzI'
                    'iwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdD'
                    'phY3RvcnMiXX0.N93SmGsmSyZlJe_XjKxtYi'
                    'xj9O3HDBfXQcnUisNCme8e6OK2v'
                    '_mz1Ws2xaSL_GXhuFIAfgciVXphOkIBxGDAN6Hr33CTzBFEjlG'
                    'lMLodhbGehGM2WsNIb3-kKLQx4pqb-vtdpzIt7ECjdEIGoQM1os'
                    'j_0bbu1aD6iXPHl3rqh9Tgzv3cHOi_uvWAcaX2uzYan5jtq'
                    '7k5-0YoDJ2Ygd3M5N5XS-K9UUt1s66M647nWohL-b20RG9RLq-v60Y2'
                    '2MjZJ2l3HLKR05SL1EhzpyH5qPz0idFxZaU-BkpriUvSSKYAMRep3gj'
                    'ZsMXYp3BVONZ-DF22U-KqEF-0aIMSNswrfw'
                    )

EXECUTIVE_PRODUCER = (
                    'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXV'
                    'CIsImtpZCI6Ik5qQkNSa1EzTmtSRl'
                    'JVUXdNME00TXpjNVJrTXlOelZCTTBOR'
                    'FJEUXlNVGsyUXpKQ1JrTXlRdyJ9.eyJpc'
                    '3MiOiJodHRwczovL2VzYWdlLmF'
                    '1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUt'
                    'b2F1dGgyfDEwMjc4NzYxODkzNDU0NDQ3NTgxNyIs'
                    'ImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBz'
                    'Oi8vZXNhZ2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sI'
                    'mlhdCI6MTU3OTUxMzkwOSwiZXhwIjoxNTc5NjAwMz'
                    'A5LCJhenAiOiJ0S0lIT0NpVkVzTUQwYVZ1eUZ6WW1VU'
                    '3BVUzFCV2hyeSIsInNjb3BlIjoib3BlbmlkIHByb2Zpb'
                    'GUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y'
                    'WN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3Rvcn'
                    'MiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0'
                    'Y2g6bW92aWVzIiwicG9zdDphY3Rvcn'
                    'MiLCJwb3N0Om1vdmllcyJdfQ.Ki2Dxc9aTHmlrAIOG0XOsUI'
                    'S0CypvD3CG7JoxF3i6w_3g'
                    't4LyDow0zbnrdyIqoozF5pjspVG6slfgsU1Urff-MOOjK5Pd'
                    'bczB-qAUIKRQvI5X6PrfAYizriiFHGIYfYqGVXbI_e_urrwcp'
                    'VQZhybRQaCUOXnmIAI3Smx7i7YgOsp1dMQXnzLJD6NMEZCNd'
                    'Aspl7aP4vW66ULObI8JWhLrnoe7kHc6uRrogJ0gV1gUfEiU0'
                    'eG6tvs_xTFFeXYKJyVtNczwIe5wCpLJOATV4Gu44eqZFHq'
                    'cRjPez_B-KAgswXBrCAjQq4-mY1U-Q89w2OKH-r'
                    'IAa7TXgI9tydaj9d0gQ'
                    )


class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""
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

    #  Tests that you can get all movies
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
        self.assertEqual(
                    data['movie']['release_date'],
                    'Wed, 06 May 2020 00:00:00 GMT'
                    )

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

    # tests RBAC for creating a movie
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
        self.assertEqual(
            data['movie']['release_date'],
            'Tue, 12 Nov 2019 00:00:00 GMT'
            )

    # Test that 400 is returned if no data is sent to update a movie
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

    # tests RBAC for updating a movie
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

    # tests that 404 is returned for an invalid id to get a specific movie
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

    # tests to delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting a movie
    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to delete a specific movie
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

    #  Tests that you can get all actors
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
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Will Smith')

    # tests for an invalid id to get a specific actor
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

    # tests RBAC for creating an actor
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

    # Test to Update an actor
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

    # Test that 400 is returned if no data is sent to update an actor
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

    # tests RBAC for updating an actor
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

    # tests that 404 is returned for an invalid id to get a specific actor
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

    # tests to delete an actor
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting an actor
    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific actor
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


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
