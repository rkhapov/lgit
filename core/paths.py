import os
from os.path import join

CONFIG_DIR = '.lgit'
STORAGE_PATH = join(CONFIG_DIR, 'storage')
OBJECTS_DIR = join(CONFIG_DIR, 'objects')
COMMITS_DIR = os.path.join(OBJECTS_DIR, 'commits')
BRANCHES_DIR = os.path.join(OBJECTS_DIR, 'branches')
CURRENT_BRANCH_FILE = join(OBJECTS_DIR, "CURRENT_BRANCH")
STAGE_FILE = join(CONFIG_DIR, 'STAGE')
