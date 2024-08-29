#!/usr/bin/python3
from os import getenv

# Conditional import based on the environment variable
if getenv('DD_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload storage after initializing it
storage.reload()
