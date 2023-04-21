from fastapi.testclient import TestClient

from unittest import TestCase
from examples.non_integer_versions import app, versions


class TestNonIntegerVersions(TestCase):

    def test_non_integer_versions(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([('2023-1-1', 0), ('2023-2-1', 0), ('2023-10-1', 0)], versions)
        self.assertEqual(404, test_client.get('/').status_code)
        self.assertEqual(404, test_client.get('/docs').status_code)
        self.assertEqual(200, test_client.get('/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/versions').status_code)

        self.assertEqual(200, test_client.get('/2023-1-1/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-1-1/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-1-1/jan').status_code)
        self.assertEqual(404, test_client.get('/2023-1-1/feb').status_code)
        self.assertEqual(404, test_client.get('/2023-1-1/oct').status_code)

        self.assertEqual(200, test_client.get('/2023-2-1/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-2-1/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-2-1/jan').status_code)
        self.assertEqual(200, test_client.get('/2023-2-1/feb').status_code)
        self.assertEqual(404, test_client.get('/2023-2-1/oct').status_code)

        self.assertEqual(200, test_client.get('/2023-10-1/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-10-1/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-10-1/jan').status_code)
        self.assertEqual(200, test_client.get('/2023-10-1/feb').status_code)
        self.assertEqual(200, test_client.get('/2023-10-1/oct').status_code)

        self.assertDictEqual(
            {'versions': [{'version': '2023-1-1'}, {'version': '2023-2-1'}, {'version': '2023-10-1'}]},
            test_client.get('/versions').json()
        )

        self.assertEqual(
            '"jan"',
            test_client.get('/2023-1-1/jan').text
        )
        self.assertEqual(
            '"jan"',
            test_client.get('/2023-2-1/jan').text
        )
        self.assertEqual(
            '"feb"',
            test_client.get('/2023-2-1/feb').text
        )
        self.assertEqual(
            '"jan"',
            test_client.get('/2023-10-1/jan').text
        )
        self.assertEqual(
            '"feb"',
            test_client.get('/2023-10-1/feb').text
        )
        self.assertEqual(
            '"oct"',
            test_client.get('/2023-10-1/oct').text
        )
