#!/usr/bin/env python3
""" this a Python function that lists all documents in a collection """


def list_all(mongo_collection):
    """list function"""
    documents = list(mongo_collection.find())
    if len(documents) > 0:
        return documents
    return []
