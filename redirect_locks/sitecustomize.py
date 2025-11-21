import os, hashlib
from pathlib import Path

import_suceeded = True
try:
    import filelock
except ModuleNotFoundError as e:
    import_suceeded = False
    
if import_suceeded:
    LOCK_ROOT = Path('/home/brank/.hf_locks/datasets')
    PREFIXES = ['/fast/brank/cache/huggingface/datasets', '/fast/brank/cache/huggingface/hub']
    LOCK_ROOT.mkdir(parents=True, exist_ok=True)

    def _map(path: str) -> str:
        path = os.path.abspath(os.path.expanduser(path))
        if PREFIXES and not any(path.startswith(p) for p in PREFIXES):
            return path
        digest = hashlib.sha1(path.encode("utf-8")).hexdigest()
        bucket = LOCK_ROOT / digest[:2]
        bucket.mkdir(parents=True, exist_ok=True)
        return str(bucket / f"{digest[2:]}.lock")

    class RedirectedFileLock(filelock.FileLock):
        def __init__(self, lock_file, *args, **kwargs):
            super().__init__(_map(lock_file), *args, **kwargs)

    filelock.FileLock = RedirectedFileLock
