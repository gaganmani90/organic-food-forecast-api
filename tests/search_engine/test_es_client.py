import unittest
from elasticsearch import Elasticsearch
from search_engine.es_client import get_es_client

class TestElasticsearchClient(unittest.TestCase):

    def test_es_connection(self):
        es = get_es_client()
        self.assertIsInstance(es, Elasticsearch)
        self.assertTrue(es.ping())

if __name__ == '__main__':
    unittest.main()
