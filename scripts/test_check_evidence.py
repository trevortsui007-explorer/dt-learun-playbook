"""Run with: python scripts/test_check_evidence.py."""
import hashlib
import tempfile
from pathlib import Path
from check_evidence import check

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / 'sample.cs').write_bytes(b'ok')
    refs = {'R': {'path': 'sample.cs', 'sha256': hashlib.sha256(b'ok').hexdigest()}}
    assert check(root, refs) == []
    (root / 'sample.cs').write_bytes(b'changed')
    assert 'changed' in check(root, refs)[0]
    refs['R']['path'] = 'missing.cs'
    assert 'missing' in check(root, refs)[0]
    refs['R']['path'] = '../outside.cs'
    assert 'unsafe' in check(root, refs)[0]
print('PASS: matching, changed, missing and outside-root evidence checks')
