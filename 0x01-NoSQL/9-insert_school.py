#!/usr/bin/env python3
"""This a Python function that inserts a new document
in a collection based on kwargs
"""

def insert_school(mongo_collection, **kwargs):
    """ inserts_school function"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
