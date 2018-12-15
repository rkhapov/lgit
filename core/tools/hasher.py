#!/usr/bin/env python3
import hashlib


def get_bytes_hash(bytes_):
    return hashlib.sha256(bytes_).hexdigest()


def get_file_hash(path, read_part=1024):
    with open(path, 'rb') as file:
        h = hashlib.sha256()
        while True:
            part = file.read(read_part)

            if len(part) == 0:
                break

            h.update(part)

        return h.hexdigest()
