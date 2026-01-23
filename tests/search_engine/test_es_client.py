import unittest
import os
import subprocess
import time
import requests
from elasticsearch import Elasticsearch
from search_engine.es_client import get_es_client

class TestElasticsearchClientIntegration(unittest.TestCase):
    """Integration tests that start/stop Docker Elasticsearch container"""
    
    CONTAINER_NAME = "es-test-integration"
    ES_HOST = "http://localhost:9200"
    ES_IMAGE = "docker.elastic.co/elasticsearch/elasticsearch:7.17.13"
    TEST_INDEX = "test_organic_stores"
    
    @classmethod
    def setUpClass(cls):
        """Start Docker Elasticsearch container before all tests"""
        print("\n🐳 Starting Elasticsearch Docker container...")
        
        # Check if Docker is available
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise unittest.SkipTest("Docker is not available or not running")
        
        # Stop and remove existing container if it exists
        subprocess.run(
            ["docker", "stop", cls.CONTAINER_NAME],
            capture_output=True,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["docker", "rm", cls.CONTAINER_NAME],
            capture_output=True,
            stderr=subprocess.DEVNULL
        )
        
        # Start new container
        result = subprocess.run(
            [
                "docker", "run", "-d",
                "--name", cls.CONTAINER_NAME,
                "-p", "9200:9200",
                "-e", "discovery.type=single-node",
                "-e", "xpack.security.enabled=false",  # Disable security for easier testing
                cls.ES_IMAGE
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise unittest.SkipTest(f"Failed to start Docker container: {result.stderr}")
        
        # Wait for Elasticsearch to be ready (max 60 seconds)
        print("⏳ Waiting for Elasticsearch to be ready...")
        for i in range(60):
            try:
                response = requests.get(f"{cls.ES_HOST}/_cluster/health", timeout=2)
                if response.status_code == 200:
                    health = response.json()
                    if health.get("status") in ["yellow", "green"]:
                        print("✅ Elasticsearch is ready!")
                        break
            except (requests.RequestException, ConnectionError):
                pass
            time.sleep(1)
        else:
            raise unittest.SkipTest("Elasticsearch did not become ready in time")
        
        # Set environment to use local ES
        os.environ["USE_LOCAL_ES"] = "true"
        os.environ["ES_HOST_LOCAL"] = cls.ES_HOST
        
        # Reload module to pick up env vars
        import importlib
        import search_engine.es_client
        importlib.reload(search_engine.es_client)
    
    @classmethod
    def tearDownClass(cls):
        """Stop and remove Docker container after all tests"""
        print("\n🧹 Cleaning up Docker container...")
        
        # Delete test index
        try:
            es = get_es_client()
            if es.indices.exists(index=cls.TEST_INDEX):
                es.indices.delete(index=cls.TEST_INDEX)
                print(f"✅ Deleted test index: {cls.TEST_INDEX}")
        except Exception as e:
            print(f"⚠️ Error cleaning up index: {e}")
        
        # Stop and remove container
        subprocess.run(
            ["docker", "stop", cls.CONTAINER_NAME],
            capture_output=True,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["docker", "rm", cls.CONTAINER_NAME],
            capture_output=True,
            stderr=subprocess.DEVNULL
        )
        print("✅ Container stopped and removed")
    
    def setUp(self):
        """Set up before each test"""
        # Reload module to ensure fresh state
        import importlib
        import search_engine.es_client
        importlib.reload(search_engine.es_client)
    
    def tearDown(self):
        """Clean up after each test"""
        # Delete test index if it exists
        try:
            es = get_es_client()
            if es.indices.exists(index=self.TEST_INDEX):
                es.indices.delete(index=self.TEST_INDEX)
        except Exception:
            pass
    
    def test_es_connection(self):
        """Test that get_es_client returns a working Elasticsearch client"""
        es = get_es_client()
        self.assertIsInstance(es, Elasticsearch)
        self.assertTrue(es.ping())
    
    def test_create_and_delete_index(self):
        """Test creating and deleting an index"""
        es = get_es_client()
        
        # Create test index
        index_body = {
            "mappings": {
                "properties": {
                    "store_name": {"type": "text"},
                    "certification_id": {"type": "keyword"}
                }
            }
        }
        es.indices.create(index=self.TEST_INDEX, body=index_body)
        
        # Verify index exists
        self.assertTrue(es.indices.exists(index=self.TEST_INDEX))
        
        # Delete index
        es.indices.delete(index=self.TEST_INDEX)
        
        # Verify index is deleted
        self.assertFalse(es.indices.exists(index=self.TEST_INDEX))
    
    def test_index_and_search_document(self):
        """Test indexing a document and searching for it"""
        es = get_es_client()
        
        # Create test index
        from search_engine.index_setup import create_index
        es.indices.create(
            index=self.TEST_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "store_name": {"type": "text"},
                        "certification_id": {"type": "keyword"},
                        "state": {"type": "keyword"}
                    }
                }
            }
        )
        
        # Index a test document
        test_doc = {
            "store_name": "Test Organic Store",
            "certification_id": "TEST-001",
            "state": "TestState"
        }
        es.index(index=self.TEST_INDEX, id=test_doc["certification_id"], body=test_doc)
        
        # Refresh index to make document searchable
        es.indices.refresh(index=self.TEST_INDEX)
        
        # Search for the document
        response = es.search(
            index=self.TEST_INDEX,
            body={
                "query": {
                    "match": {"store_name": "Test Organic Store"}
                }
            }
        )
        
        self.assertEqual(response["hits"]["total"]["value"], 1)
        self.assertEqual(response["hits"]["hits"][0]["_source"]["certification_id"], "TEST-001")
        
        # Clean up
        es.delete(index=self.TEST_INDEX, id="TEST-001")
    
    def test_bulk_indexing(self):
        """Test bulk indexing multiple documents"""
        es = get_es_client()
        
        # Create test index
        es.indices.create(
            index=self.TEST_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "store_name": {"type": "text"},
                        "certification_id": {"type": "keyword"}
                    }
                }
            }
        )
        
        # Bulk index documents
        from elasticsearch.helpers import bulk
        test_docs = [
            {"store_name": "Store 1", "certification_id": "TEST-001"},
            {"store_name": "Store 2", "certification_id": "TEST-002"},
            {"store_name": "Store 3", "certification_id": "TEST-003"}
        ]
        
        actions = [
            {
                "_index": self.TEST_INDEX,
                "_id": doc["certification_id"],
                "_source": doc
            }
            for doc in test_docs
        ]
        
        success, failed = bulk(es, actions)
        self.assertEqual(success, 3)
        self.assertEqual(len(failed), 0)
        
        # Refresh and verify
        es.indices.refresh(index=self.TEST_INDEX)
        response = es.search(index=self.TEST_INDEX, body={"query": {"match_all": {}}})
        self.assertEqual(response["hits"]["total"]["value"], 3)

if __name__ == '__main__':
    unittest.main()
