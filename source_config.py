"""Local source checkout configuration; no third-party dependencies."""
from pathlib import Path
import json


def guangzhou_root():
    config = Path(__file__).resolve().parent / 'config' / 'local.json'
    if not config.is_file():
        raise SystemExit('Copy config/local.example.json to config/local.json and set guangzhou_source_root.')
    value = json.loads(config.read_text(encoding='utf-8-sig')).get('guangzhou_source_root')
    if not isinstance(value, str) or not value.strip():
        raise SystemExit('guangzhou_source_root must be a non-empty absolute path.')
    root = Path(value)
    if not root.is_absolute() or not (root / 'Learun.Application.Web').is_dir():
        raise SystemExit('Configured checkout must be an absolute path containing Learun.Application.Web.')
    return root
