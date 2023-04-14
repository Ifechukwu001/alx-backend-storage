#!/usr/bin/env python3
"""Change all topics of school document

"""


def update_topics(mongo_collection, name, topics):
    """Updates a topics

    Args:
        name (str): School name.
        topics (list[str]): List of topics approached.

    """
    mongo_collection.update({'name': "{}".format(name)},
                            {"$push": {"topics": {"$each": topics}}})
