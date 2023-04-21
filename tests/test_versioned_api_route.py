from fastapi.testclient import TestClient

from unittest import TestCase
from examples.versioned_api_route import app, versions


class TestVersionedAPIRoute(TestCase):

    def test_simple(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (1, 1)], versions)
        self.assertEqual(404, test_client.get('/').status_code)
        self.assertEqual(404, test_client.get('/docs').status_code)
        self.assertEqual(200, test_client.get('/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/versions').status_code)

        self.assertEqual(200, test_client.get('/v1_0/docs').status_code)
        self.assertEqual(200, test_client.get('/v1_0/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/v1_0/hey/dude').status_code)

        self.assertEqual(200, test_client.get('/v1_1/docs').status_code)
        self.assertEqual(200, test_client.get('/v1_1/openapi.json').status_code)
        self.assertEqual(404, test_client.get('/v1_1/hey/dude').status_code)
        self.assertEqual(200, test_client.get('/v1_1/sup/dawg').status_code)

        self.assertDictEqual(
            {'versions': [{'version': '1.0'}, {'version': '1.1'}]},
            test_client.get('/versions').json()
        )

        self.assertEqual(
            '"dude"',
            test_client.get('/v1_0/hey/dude').text
        )
        self.assertEqual(
            '"dawg"',
            test_client.get('/v1_1/sup/dawg').text
        )