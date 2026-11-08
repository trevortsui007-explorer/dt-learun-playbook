"""Compare local checkout with the saved workflow evidence, without changing either."""
from pathlib import Path
import hashlib
import json
import sys

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from source_config import guangzhou_root


def check(root, refs):
    errors = []
    for key, entry in refs.items():
        path = (root / entry['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f'{key}: unsafe relative path')
        elif not path.is_file():
            errors.append(f'{key}: missing {entry["path"]}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            errors.append(f'{key}: changed {entry["path"]}')
    return errors


if __name__ == '__main__':
    evidence = REPO / '力软开发模式工作流-2026-11-08' / 'workflow-evidence.json'
    refs = json.loads(evidence.read_text(encoding='utf-8-sig'))['refs']
    errors = check(guangzhou_root(), refs)
    print('\n'.join(errors) if errors else f'PASS: {len(refs)} source hashes match the workflow snapshot.')
    raise SystemExit(bool(errors))
