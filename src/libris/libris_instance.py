"""Module for handling librisinstances"""
import urllib.parse as urlparse


class LibrisInstance:
    """Librisinstance that hold data and etag"""

    def __init__(self, etag, libris_instance):
        self.etag = etag
        self.data = libris_instance
        self.id = urlparse.urlparse(self.nav(['@graph', '@id'])).path

    def nav(self, path):
        """navigate the data to the specified point"""
        point = self.data
        for key in path:
            if isinstance(point, dict) and key in point:
                point = point[key]
            elif isinstance(point, list):
                for item in point:
                    if isinstance(item, dict) and key in item:
                        point = item[key]
            else:
                raise TypeError
        return point

    def add(self, path, data):
        """add data to the instance"""
        point = self.nav(path)
        if isinstance(point, list):
            point.append(data)
        if isinstance(point, dict):
            point = point | data

    @staticmethod
    def _check_conditions(point, conditions):
        print('checking conditions')
        condition_list = []
        for condition in conditions:
            if isinstance(point, dict):
                if condition['key'] is None:
                    condition_list.append(condition['value'] in point.values())
                elif condition['value'] is None:
                    condition_list.append(condition['key'] in point.keys())
                else:
                    condition_list.append(condition['value'] in point.values()
                                          and condition['key'] in point.keys())
            else:
                raise TypeError
        return all(condition_list)

    def delete_without_conditions(self, path):
        """delete the data from the instance"""
        deletion_target = path[-1:]
        deletion_point = self.nav(path[:-1])
        if isinstance(deletion_point, list):
            for item in deletion_point:
                if deletion_target in item:
                    if isinstance(item, dict):
                        del item[deletion_target]
                    if isinstance(item, list):
                        item.remove(deletion_target)
        elif isinstance(deletion_point, dict) and deletion_target in deletion_point:
            del deletion_point[deletion_target]
        else:
            raise TypeError

    def delete(self, path, conditions):
        """delete the data from the instance"""
        if conditions is None:
            self.delete_without_conditions(path)
        point = self.nav(path)
        if isinstance(point, list):
            for item in point:
                if self._check_conditions(item, conditions):
                    point.remove(item)
        elif isinstance(point, dict):
            for item in point:
                if self._check_conditions(item, conditions):
                    del point[item]
        else:
            raise TypeError
