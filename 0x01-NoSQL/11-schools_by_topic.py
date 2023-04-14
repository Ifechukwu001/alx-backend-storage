#!/usr/bin/env python3
"""Find school having a topic

"""


def schools_by_topic(mongo_collection, topic):
    """Returns schools having that topic

    Args:
        mongo_collection: Pymongo collection.
        topic: Topic to be found.

    Returns:
        dict: school Documents
    """
    return mongo_collection.find({'topics': topic})
