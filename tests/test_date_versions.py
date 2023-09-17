import datetime
from fastapi.testclient import TestClient
from unittest import TestCase

from examples.date_versions import app, versions


class TestNonIntegerVersions(TestCase):

    def test_non_integer_versions(self) -> None:
        self.maxDiff = None
        test_client = TestClient(app)

        self.assertListEqual([
            (datetime.date(2023, 1, 1), 0),
            (datetime.date(2023, 2, 1), 0),
            (datetime.date(2023, 10, 1), 0)
        ], versions)
        self.assertEqual(404, test_client.get('/').status_code)
        self.assertEqual(404, test_client.get('/docs').status_code)
        self.assertEqual(200, test_client.get('/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/versions').status_code)

        self.assertEqual(200, test_client.get('/2023-01-01/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-01-01/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-01-01/jan').status_code)
        self.assertEqual(404, test_client.get('/2023-01-01/feb').status_code)
        self.assertEqual(404, test_client.get('/2023-01-01/oct').status_code)

        self.assertEqual(200, test_client.get('/2023-02-01/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-02-01/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-02-01/jan').status_code)
        self.assertEqual(200, test_client.get('/2023-02-01/feb').status_code)
        self.assertEqual(404, test_client.get('/2023-02-01/oct').status_code)

        self.assertEqual(200, test_client.get('/2023-10-01/docs').status_code)
        self.assertEqual(200, test_client.get('/2023-10-01/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/2023-10-01/jan').status_code)
        self.assertEqual(200, test_client.get('/2023-10-01/feb').status_code)
        self.assertEqual(200, test_client.get('/2023-10-01/oct').status_code)

        self.assertDictEqual(
            {
                'versions': [
                    {'version': '2023-01-01'},
                    {'version': '2023-02-01'},
                    {'version': '2023-10-01'}
                ]
            },
            test_client.get('/versions').json()
        )

        self.assertEqual(
            '"jan"',
            test_client.get('/2023-01-01/jan').text
        )
        self.assertEqual(
            '"jan"',
            test_client.get('/2023-02-01/jan').text
        )
        self.assertEqual(
            '"feb"',
            test_client.get('/2023-02-01/feb').text
        )
        self.assertEqual(
            '"jan"',
            test_client.get('/2023-10-01/jan').text
        )
        self.assertEqual(
            '"feb"',
            test_client.get('/2023-10-01/feb').text
        )
        self.assertEqual(
            '"oct"',
            test_client.get('/2023-10-01/oct').text
        )
