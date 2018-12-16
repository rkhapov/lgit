import os
from os.path import join

CONFIG_DIR = '.lgit'
STORAGE_PATH = join('.lgit', 'storage')
OBJECTS_DIR = join('.lgit', 'objects')
COMMITS_DIR = os.path.join(CONFIG_DIR, 'objects', 'commits')
BRANCHES_DIR = os.path.join(CONFIG_DIR, 'objects', 'branches')
CURRENT_BRANCH_FILE = join(OBJECTS_DIR, "CURRENT_BRANCH")
