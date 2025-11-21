import os, hashlib
os.environ["SOFT_FILELOCK"]= "1"
from pathlib import Path

import_suceeded = True
try:
    import filelock
except ModuleNotFoundError as e:
    import_suceeded = False

if import_suceeded:
    from filelock import SoftFileLock
    filelock.FileLock = SoftFileLock
