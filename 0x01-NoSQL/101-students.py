#!/usr/bin/env/python3
"""Python function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """Top student function"""
    pipeline = [
        {"$unwind": "$scores"},  # Unwind scores array
        {"$group": {"_id": "$_id", "averageScore": {"$avg": "$scores.score"}, "name": {"$first": "$name"}}},
        {"$sort": {"averageScore": -1}}  # Sort by average score in descending order
    ]
    result = mongo_collection.aggregate(pipeline)
    return list(result)
