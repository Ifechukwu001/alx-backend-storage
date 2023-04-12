#!/usr/bin/env python3
"""Lists all documents
"""
import pymongo


def list_all(mongo_collection):
    """Lists all the documents

    Args:
        mongo_collection (Collection): Mongo collection.
    Returns:
        List: Of documents.
    """
    documents = mongo_collection.find()
    return documents
