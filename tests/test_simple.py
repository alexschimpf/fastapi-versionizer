from fastapi.testclient import TestClient

from unittest import TestCase
from examples.simple import app, versions


class TestSimpleExample(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_simple_example(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0)], versions)

        # Make sure some pages don't exist
        self.assertEqual(404, test_client.get('/redoc').status_code)
        self.assertEqual(404, test_client.get('/v1/redoc').status_code)
        self.assertEqual(404, test_client.get('/v2/redoc').status_code)
        self.assertEqual(404, test_client.get('/latest/redoc').status_code)
        self.assertEqual(404, test_client.post('/users').status_code)
        self.assertEqual(404, test_client.post('/items').status_code)
        self.assertEqual(404, test_client.get('/users').status_code)
        self.assertEqual(404, test_client.get('/items').status_code)
        self.assertEqual(404, test_client.get('/users/1').status_code)
        self.assertEqual(404, test_client.get('/items/1').status_code)
        self.assertEqual(404, test_client.get('/v2/items/1').status_code)

        # v1
        self.assertDictEqual(
            {'id': 1, 'name': 'alex'},
            test_client.post('/v1/users', json={'id': 1, 'name': 'alex'}).json()
        )
        self.assertDictEqual(
            {'id': 1, 'name': 'laptop'},
            test_client.post('/v1/items', json={'id': 1, 'name': 'laptop'}).json()
        )
        self.assertListEqual(
            [{'id': 1, 'name': 'alex'}],
            test_client.get('/v1/users').json()
        )
        self.assertListEqual(
            [{'id': 1, 'name': 'laptop'}],
            test_client.get('/v1/items').json()
        )
        self.assertDictEqual(
            {'id': 1, 'name': 'alex'},
            test_client.get('/v1/users/1').json()
        )
        self.assertDictEqual(
            {'id': 1, 'name': 'laptop'},
            test_client.get('/v1/items/1').json()
        )

        # v2
        self.assertDictEqual(
            {'id': 2, 'name': 'zach', 'age': 30},
            test_client.post('/v2/users', json={'id': 2, 'name': 'zach', 'age': 30}).json()
        )
        self.assertDictEqual(
            {'id': 2, 'name': 'phone', 'cost': 10},
            test_client.post('/v2/items', json={'id': 2, 'name': 'phone', 'cost': 10}).json()
        )
        self.assertListEqual(
            [
                {'id': 1, 'name': 'alex', 'age': None},
                {'id': 2, 'name': 'zach', 'age': 30}
            ],
            test_client.get('/v2/users').json()
        )
        self.assertListEqual(
            [
                {'id': 1, 'name': 'laptop', 'cost': None},
                {'id': 2, 'name': 'phone', 'cost': 10}
            ],
            test_client.get('/v2/items').json()
        )
        self.assertDictEqual(
            {'id': 2, 'name': 'zach', 'age': 30},
            test_client.get('/v2/users/2').json()
        )

        # latest
        self.assertDictEqual(
            {'id': 3, 'name': 'dan', 'age': 65},
            test_client.post('/latest/users', json={'id': 3, 'name': 'dan', 'age': 65}).json()
        )
        self.assertDictEqual(
            {'id': 3, 'name': 'tv', 'cost': 1000},
            test_client.post('/latest/items', json={'id': 3, 'name': 'tv', 'cost': 1000}).json()
        )
        self.assertListEqual(
            [
                {'id': 1, 'name': 'alex', 'age': None},
                {'id': 2, 'name': 'zach', 'age': 30},
                {'id': 3, 'name': 'dan', 'age': 65}
            ],
            test_client.get('/latest/users').json()
        )
        self.assertListEqual(
            [
                {'id': 1, 'name': 'laptop', 'cost': None},
                {'id': 2, 'name': 'phone', 'cost': 10},
                {'id': 3, 'name': 'tv', 'cost': 1000}
            ],
            test_client.get('/latest/items').json()
        )
        self.assertDictEqual(
            {'id': 3, 'name': 'dan', 'age': 65},
            test_client.get('/latest/users/3').json()
        )

        # docs
        self.assertEqual(200, test_client.get('/docs').status_code)
        self.assertEqual(200, test_client.get('/v1/docs').status_code)
        self.assertEqual(200, test_client.get('/v2/docs').status_code)
        self.assertEqual(200, test_client.get('/latest/docs').status_code)

        # openapi
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test',
                    'version': '0.1.0'
                },
                'paths': {
                    '/v1/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items',
                            'operationId': 'get_items_v1_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/Item'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V1 Items Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item',
                            'operationId': 'create_item_v1_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Item'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/Item'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    },
                    '/v1/items/{item_id}': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Item',
                            'operationId': 'get_item_v1_items__item_id__get',
                            'deprecated': True,
                            'parameters': [
                                {
                                    'name': 'item_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'Item Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/Item'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v1_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users',
                            'operationId': 'get_users_v1_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/User'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V1 Users Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User',
                            'operationId': 'create_user_v1_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/User'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/User'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    },
                    '/v1/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User',
                            'operationId': 'get_user_v1_users__user_id__get',
                            'deprecated': True,
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/User'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items V2',
                            'operationId': 'get_items_v2_v2_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/ItemV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V2 V2 Items Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item V2',
                            'operationId': 'create_item_v2_v2_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ItemV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/ItemV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v2_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users V2',
                            'operationId': 'get_users_v2_v2_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/UserV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V2 V2 Users Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User V2',
                            'operationId': 'create_user_v2_v2_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/UserV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User V2',
                            'operationId': 'get_user_v2_v2_users__user_id__get',
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items V2',
                            'operationId': 'get_items_v2_latest_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/ItemV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V2 Latest Items Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item V2',
                            'operationId': 'create_item_v2_latest_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ItemV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/ItemV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
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
                            'summary': 'Get Status',
                            'operationId': 'get_status_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status Latest Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users V2',
                            'operationId': 'get_users_v2_latest_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/UserV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V2 Latest Users Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User V2',
                            'operationId': 'create_user_v2_latest_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/UserV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User V2',
                            'operationId': 'get_user_v2_latest_users__user_id__get',
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'components': {
                    'schemas': {
                        'HTTPValidationError': {
                            'properties': {
                                'detail': {
                                    'items': {
                                        '$ref': '#/components/schemas/ValidationError'
                                    },
                                    'type': 'array',
                                    'title': 'Detail'
                                }
                            },
                            'type': 'object',
                            'title': 'HTTPValidationError'
                        },
                        'Item': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'Item'
                        },
                        'ItemV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'ItemV2'
                        },
                        'ItemV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'cost'
                            ],
                            'title': 'ItemV2'
                        },
                        'User': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'User'
                        },
                        'UserV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'UserV2'
                        },
                        'UserV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'age'
                            ],
                            'title': 'UserV2'
                        },
                        'ValidationError': {
                            'properties': {
                                'loc': {
                                    'items': {
                                        'anyOf': [
                                            {
                                                'type': 'string'
                                            },
                                            {
                                                'type': 'integer'
                                            }
                                        ]
                                    },
                                    'type': 'array',
                                    'title': 'Location'
                                },
                                'msg': {
                                    'type': 'string',
                                    'title': 'Message'
                                },
                                'type': {
                                    'type': 'string',
                                    'title': 'Error Type'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'loc',
                                'msg',
                                'type'
                            ],
                            'title': 'ValidationError'
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
                    'title': 'test - v1',
                    'version': 'v1'
                },
                'paths': {
                    '/v1/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items',
                            'operationId': 'get_items_v1_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/Item'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V1 Items Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item',
                            'operationId': 'create_item_v1_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Item'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/Item'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    },
                    '/v1/items/{item_id}': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Item',
                            'operationId': 'get_item_v1_items__item_id__get',
                            'deprecated': True,
                            'parameters': [
                                {
                                    'name': 'item_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'Item Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/Item'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v1_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v1/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users',
                            'operationId': 'get_users_v1_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/User'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V1 Users Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User',
                            'operationId': 'create_user_v1_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/User'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/User'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    },
                    '/v1/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User',
                            'operationId': 'get_user_v1_users__user_id__get',
                            'deprecated': True,
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/User'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'components': {
                    'schemas': {
                        'HTTPValidationError': {
                            'properties': {
                                'detail': {
                                    'items': {
                                        '$ref': '#/components/schemas/ValidationError'
                                    },
                                    'type': 'array',
                                    'title': 'Detail'
                                }
                            },
                            'type': 'object',
                            'title': 'HTTPValidationError'
                        },
                        'Item': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'Item'
                        },
                        'User': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'User'
                        },
                        'ValidationError': {
                            'properties': {
                                'loc': {
                                    'items': {
                                        'anyOf': [
                                            {
                                                'type': 'string'
                                            },
                                            {
                                                'type': 'integer'
                                            }
                                        ]
                                    },
                                    'type': 'array',
                                    'title': 'Location'
                                },
                                'msg': {
                                    'type': 'string',
                                    'title': 'Message'
                                },
                                'type': {
                                    'type': 'string',
                                    'title': 'Error Type'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'loc',
                                'msg',
                                'type'
                            ],
                            'title': 'ValidationError'
                        }
                    }
                }
            },
            test_client.get('/v1/openapi.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - v2',
                    'version': 'v2'
                },
                'paths': {
                    '/v2/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items V2',
                            'operationId': 'get_items_v2_v2_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/ItemV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V2 V2 Items Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item V2',
                            'operationId': 'create_item_v2_v2_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ItemV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/ItemV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status',
                            'operationId': 'get_status_v2_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users V2',
                            'operationId': 'get_users_v2_v2_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/UserV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V2 V2 Users Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User V2',
                            'operationId': 'create_user_v2_v2_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/UserV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User V2',
                            'operationId': 'get_user_v2_v2_users__user_id__get',
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'components': {
                    'schemas': {
                        'HTTPValidationError': {
                            'properties': {
                                'detail': {
                                    'items': {
                                        '$ref': '#/components/schemas/ValidationError'
                                    },
                                    'type': 'array',
                                    'title': 'Detail'
                                }
                            },
                            'type': 'object',
                            'title': 'HTTPValidationError'
                        },
                        'ItemV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'ItemV2'
                        },
                        'ItemV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'cost'
                            ],
                            'title': 'ItemV2'
                        },
                        'UserV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'UserV2'
                        },
                        'UserV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'age'
                            ],
                            'title': 'UserV2'
                        },
                        'ValidationError': {
                            'properties': {
                                'loc': {
                                    'items': {
                                        'anyOf': [
                                            {
                                                'type': 'string'
                                            },
                                            {
                                                'type': 'integer'
                                            }
                                        ]
                                    },
                                    'type': 'array',
                                    'title': 'Location'
                                },
                                'msg': {
                                    'type': 'string',
                                    'title': 'Message'
                                },
                                'type': {
                                    'type': 'string',
                                    'title': 'Error Type'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'loc',
                                'msg',
                                'type'
                            ],
                            'title': 'ValidationError'
                        }
                    }
                }
            },
            test_client.get('/v2/openapi.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - v2',
                    'version': 'v2'
                },
                'paths': {
                    '/latest/items': {
                        'get': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Get Items V2',
                            'operationId': 'get_items_v2_latest_items_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/ItemV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Items V2 Latest Items Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Items'
                            ],
                            'summary': 'Create Item V2',
                            'operationId': 'create_item_v2_latest_items_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ItemV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/ItemV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
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
                            'summary': 'Get Status',
                            'operationId': 'get_status_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status Latest Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/users': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get Users V2',
                            'operationId': 'get_users_v2_latest_users_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'items': {
                                                    '$ref': '#/components/schemas/UserV2-Output'
                                                },
                                                'type': 'array',
                                                'title': 'Response Get Users V2 Latest Users Get'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        'post': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Create User V2',
                            'operationId': 'create_user_v2_latest_users_post',
                            'requestBody': {
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/UserV2-Input'
                                        }
                                    }
                                },
                                'required': True
                            },
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/users/{user_id}': {
                        'get': {
                            'tags': [
                                'Users'
                            ],
                            'summary': 'Get User V2',
                            'operationId': 'get_user_v2_latest_users__user_id__get',
                            'parameters': [
                                {
                                    'name': 'user_id',
                                    'in': 'path',
                                    'required': True,
                                    'schema': {
                                        'type': 'integer',
                                        'title': 'User Id'
                                    }
                                }
                            ],
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/UserV2-Output'
                                            }
                                        }
                                    }
                                },
                                '422': {
                                    'description': 'Validation Error',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                '$ref': '#/components/schemas/HTTPValidationError'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'components': {
                    'schemas': {
                        'HTTPValidationError': {
                            'properties': {
                                'detail': {
                                    'items': {
                                        '$ref': '#/components/schemas/ValidationError'
                                    },
                                    'type': 'array',
                                    'title': 'Detail'
                                }
                            },
                            'type': 'object',
                            'title': 'HTTPValidationError'
                        },
                        'ItemV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'ItemV2'
                        },
                        'ItemV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'cost': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Cost'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'cost'
                            ],
                            'title': 'ItemV2'
                        },
                        'UserV2-Input': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name'
                            ],
                            'title': 'UserV2'
                        },
                        'UserV2-Output': {
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'title': 'Id'
                                },
                                'name': {
                                    'type': 'string',
                                    'title': 'Name'
                                },
                                'age': {
                                    'anyOf': [
                                        {
                                            'type': 'integer'
                                        },
                                        {
                                            'type': 'null'
                                        }
                                    ],
                                    'title': 'Age'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'id',
                                'name',
                                'age'
                            ],
                            'title': 'UserV2'
                        },
                        'ValidationError': {
                            'properties': {
                                'loc': {
                                    'items': {
                                        'anyOf': [
                                            {
                                                'type': 'string'
                                            },
                                            {
                                                'type': 'integer'
                                            }
                                        ]
                                    },
                                    'type': 'array',
                                    'title': 'Location'
                                },
                                'msg': {
                                    'type': 'string',
                                    'title': 'Message'
                                },
                                'type': {
                                    'type': 'string',
                                    'title': 'Error Type'
                                }
                            },
                            'type': 'object',
                            'required': [
                                'loc',
                                'msg',
                                'type'
                            ],
                            'title': 'ValidationError'
                        }
                    }
                }
            },
            test_client.get('/latest/openapi.json').json()
        )
