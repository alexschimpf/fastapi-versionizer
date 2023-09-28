from fastapi.testclient import TestClient

from unittest import TestCase
from examples.simple_no_versions_route import app, versions


class TestSimpleNoVersionsRoute(TestCase):

    def test_simple(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0), (3, 0), (4, 0)], versions)
        self.assertEqual(404, test_client.get('/').status_code)
        self.assertEqual(404, test_client.get('/docs').status_code)
        self.assertEqual(404, test_client.get('/redoc').status_code)
        self.assertEqual(200, test_client.get('/openapi.json').status_code)
        self.assertEqual(404, test_client.get('/versions').status_code)

        self.assertEqual(200, test_client.get('/v1/docs').status_code)
        self.assertEqual(200, test_client.get('/v1/redoc').status_code)
        self.assertEqual(200, test_client.get('/v1/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v1/do_something', json={'something': 'something'}).status_code)
        self.assertEqual(200, test_client.post('/v1/do_something_else').status_code)
        self.assertEqual(404, test_client.post('/v1/do_something_new').status_code)

        self.assertEqual(200, test_client.get('/v2/docs').status_code)
        self.assertEqual(200, test_client.get('/v2/redoc').status_code)
        self.assertEqual(200, test_client.get('/v2/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something_else').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something_new').status_code)

        self.assertEqual(200, test_client.get('/v3/docs').status_code)
        self.assertEqual(200, test_client.get('/v3/redoc').status_code)
        self.assertEqual(200, test_client.get('/v3/openapi.json').status_code)
        self.assertEqual(404, test_client.post('/v3/do_something').status_code)
        self.assertEqual(200, test_client.post('/v3/do_something_else').status_code)
        self.assertEqual(404, test_client.post('/v3/do_something_new').status_code)

        self.assertEqual(200, test_client.get('/v4/docs').status_code)
        self.assertEqual(200, test_client.get('/v4/redoc').status_code)
        self.assertEqual(200, test_client.get('/v4/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v4/do_something').status_code)
        self.assertEqual(200, test_client.post('/v4/do_something_else').status_code)
        self.assertEqual(404, test_client.post('/v4/do_something_new').status_code)

        self.assertEqual(404, test_client.get('/latest/docs').status_code)
        self.assertEqual(404, test_client.get('/latest/redoc').status_code)
        self.assertEqual(404, test_client.get('/latest/openapi.json').status_code)
        self.assertEqual(404, test_client.get('/latest/do_something').status_code)
        self.assertEqual(404, test_client.get('/latest/do_something_else').status_code)
        self.assertEqual(404, test_client.get('/latest/do_something_new').status_code)

        self.assertDictEqual(
            {'something': 'something'},
            test_client.post('/v1/do_something', json={'something': 'something'}).json()
        )
        self.assertDictEqual(
            {'message': 'something else'},
            test_client.post('/v1/do_something_else').json()
        )

        self.assertDictEqual(
            {'message': 'something'},
            test_client.post('/v2/do_something').json()
        )
        self.assertDictEqual(
            {'message': 'something else'},
            test_client.post('/v2/do_something_else').json()
        )
        self.assertDictEqual(
            {'message': 'something new'},
            test_client.post('/v2/do_something_new').json()
        )

        self.assertDictEqual(
            {'message': 'something re-added'},
            test_client.post('/v4/do_something').json()
        )
