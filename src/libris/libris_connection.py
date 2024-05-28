"""Module for handling connecting to Libris"""
import requests
from .libris_instance import LibrisInstance


class LibrisConnection:
    """Class for handling Libris operations"""

    def __init__(self, libris_url):
        self.libris_url = libris_url

    def get(self, libris_id):
        """Get a post with its Libris id"""
        response = requests.get(
            f'{self.libris_url}{libris_id}',
            headers={'accept': 'application/json+ld'},
            params={'embellished': 'false'},
            timeout=5
        )
        response.raise_for_status()
        return LibrisInstance(libris_instance=response.json(), etag=response.headers['etag'])

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
        response.raise_for_status()
        items += response.json()['items']
        while 'next' in response.json():
            next_query = response.json()['next']['@id']
            response = requests.get(
                f'{self.libris_url}{next_query}',
                headers={'accept': 'application/json+ld'},
                timeout=30
            )
            response.raise_for_status()
            items += response.json()['items']
        return items

    def update(self, instance):
        """Updates a Libris instance"""
        response = requests.put(
            f'{self.libris_url}{instance.id}',
            timeout=30,
            headers={
                'If-Match': instance.etag,
                'Authorization': 'Bearer ',
                'Content-Type': 'application/json+ld',
                "XL-active-sigel": 'Mtm'},
            data=instance.data
        )
        response.raise_for_status()
