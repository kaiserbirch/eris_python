"""Module for handling librisinstances"""


class LibrisInstance:
    """Librisinstance that hold data and etag"""

    def __init__(self, etag, libris_instance):
        self.etag = etag
        self.data = libris_instance

    def nav(self, path):
        """navigate the data to the right point"""
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

    def add(self,path,data):
        """add data to the instance"""
        point = self.nav(path)
        if isinstance(point, list):
            point.append(data)
        if isinstance(point, dict):
            point = point | data
