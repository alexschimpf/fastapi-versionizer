from fastapi.testclient import TestClient

from unittest import TestCase
from examples.docs_customization import app, versions


class TestDocsCustomizationExample(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_docs_customization_example(self) -> None:
        test_client = TestClient(app)

        correct_headers = {'Authorization': 'Basic dGVzdDpzZWNyZXQh'}
        incorrect_headers = {'Authorization': 'Basic incorrect'}

        self.assertListEqual([(1, 0), (2, 0)], versions)

        # Make sure some pages don't exist
        self.assertEqual(404, test_client.get('/deps').status_code)
        self.assertEqual(404, test_client.get('/status').status_code)
        self.assertEqual(404, test_client.get('/v2_0/deps').status_code)
        self.assertEqual(404, test_client.get('/latest/deps').status_code)

        # v1.0
        self.assertEqual(
            '"Ok - 1.0"',
            test_client.get('/v1_0/status').text
        )
        self.assertEqual(
            '"Ok"',
            test_client.get('/v1_0/deps').text
        )

        # v2.0
        self.assertEqual(
            '"Ok - 2.0"',
            test_client.get('/v2_0/status').text
        )

        # latest
        self.assertEqual(
            '"Ok - 2.0"',
            test_client.get('/latest/status').text
        )

        # docs
        self.assertEqual(401, test_client.get('/docs', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/redoc', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/v1_0/docs', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/v1_0/redoc', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/v2_0/docs', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/v2_0/redoc', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/latest/docs', headers=incorrect_headers).status_code)
        self.assertEqual(401, test_client.get('/latest/redoc', headers=incorrect_headers).status_code)
        self.assertEqual(200, test_client.get('/docs', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/redoc', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/v1_0/docs', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/v1_0/redoc', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/v2_0/docs', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/v2_0/redoc', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/latest/docs', headers=correct_headers).status_code)
        self.assertEqual(200, test_client.get('/latest/redoc', headers=correct_headers).status_code)

        # openapi
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test',
                    'version': ''
                },
                'paths': {
                    '/v1_0/deps': {
                        'get': {
                            'tags': [
                                'Deps'
                            ],
                            'summary': 'Get Deps',
                            'operationId': 'get_deps_v1_0_deps_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Deps V1 0 Deps Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1_0/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v1_0_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 0 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2_0/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_v2_0_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 V2 0 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Latest Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/openapi.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - 1.0',
                    'version': 'v1_0'
                },
                'paths': {
                    '/v1_0/deps': {
                        'get': {
                            'tags': [
                                'Deps'
                            ],
                            'summary': 'Get Deps',
                            'operationId': 'get_deps_v1_0_deps_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Deps V1 0 Deps Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1_0/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v1_0_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 0 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/v1_0/openapi.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - 2.0',
                    'version': 'v2_0'
                },
                'paths': {
                    '/v2_0/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_v2_0_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 V2 0 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/v2_0/openapi.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - 2.0',
                    'version': 'latest'
                },
                'paths': {
                    '/latest/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Success!',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Latest Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/latest/openapi.json').json()
        )
