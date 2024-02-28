from fastapi.testclient import TestClient

from unittest import TestCase
from examples.with_static_file_mount import app

from pathlib import Path


class TestWithStaticFileMount(TestCase):
    def test_with_static_file_mount_example(self) -> None:
        test_client = TestClient(app)

        # Read example file from file system
        expected = Path('examples/with_static_file_mount.py').read_text()

        # Compare local file contents with the same retrieved via the static file mount
        self.assertEqual(expected, test_client.get('/examples/with_static_file_mount.py').text)

        # Check that a static mount before instantiating Versionizer will not work
        self.assertEquals('{"detail":"Not Found"}',
                          test_client.get('/examples-not-working/with_static_file_mount.py').text)
