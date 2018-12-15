#!/usr/bin/env python3
import pickle
import json


def deserialize_from_bytes(bytes_):
    return pickle.loads(bytes_)


def deserialize_from_json(json_):
    return json.loads(json_)


def serialize_to_bytes(object_):
    return pickle.dumps(object_)


def serialize_to_json(object_):
    return json.dumps(object_)
