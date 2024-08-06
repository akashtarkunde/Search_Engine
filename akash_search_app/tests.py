
from django.test import TestCase
from django.conf import settings
from pymongo import MongoClient


class MongoDBSearchTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Connect to MongoDB
        cls.client = MongoClient(settings.MONGO_URI)
        cls.db = cls.client[settings.MONGO_DBNAME]
        cls.collection = cls.db['products']  # Replace 'product' with your collection name

    @classmethod
    def tearDownClass(cls):
        # Close the connection
        cls.client.close()
        super().tearDownClass()

    def test_mongodb_search_existing_data(self):
        # Query to search within the existing data
        query = {'ProductName': {'$regex': 'DRW2 - Westernwear-Women', '$options': 'i'}}
        result = self.collection.find_one(query)

        # Print the search results for debugging
        print("MongoDB Search Result:")
        print(result)

        self.assertIsNotNone(result)  # Ensure the product is found
        self.assertEqual(result['ProductName'], 'DRW2 - Westernwear-Women')
