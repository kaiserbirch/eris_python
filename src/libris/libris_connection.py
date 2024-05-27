"""Module for handling connecting to Libris"""
import requests


class LibrisConnection:
    """Class for handling Libris operations"""

    def __init__(self, libris_url):
        self.libris_url = libris_url

    def get(self, libris_id):
        """Get a post with its Libris id"""
        response = requests.get(
            f'{self.libris_url}/{libris_id}',
            headers={'accept': 'application/json+ld'},
            params={'embellished': 'false'},
            timeout=5
        )
        return response.json()

    def find(self, query):
        """Gets the items from the search query"""
        mtm = {'@reverse.itemOf.heldBy.@id': 'https://libris.kb.se/library/Mtm'}
        limit = {'_limit': 4000}
        offset = {'_offset': 0}
        query = query | limit | offset | mtm
        items = []
        response = requests.get(
            f'{self.libris_url}/find?',
            params=query,
            headers={'accept': 'application/json+ld'},
            timeout=30
        )
        items = response.json()['items']
        while 'next' in response.json():
            next_query = response.json()['next']['@id']
            response = requests.get(
                f'{self.libris_url}{next_query}',
                headers={'accept': 'application/json+ld'},
                timeout=30
            )
            items = items + response.json()['items']
        return items
