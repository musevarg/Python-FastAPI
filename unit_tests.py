import unittest
import main
from main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)

class TestStringMethods(unittest.TestCase):

    def test_root(self):
        root_value = main.read_root()
        self.assertEqual(root_value['Hello'], 'World')

    def test_get_quote(self):
        first_quote = main.read_item(1)
        self.assertEqual(first_quote.id, 1)
        self.assertEqual(first_quote.author, 'Lemmy Kilmister')

    def test_insert_quote(self):
        response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": 100, "quote":"New quote", "author":"New author"},
        )
        assert response.status_code == 200
        assert response.json() == {"id": 100, "quote":"New quote", "author":"New author"}


if __name__ == '__main__':
    unittest.main()