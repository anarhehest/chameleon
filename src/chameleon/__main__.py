import json
import sys
from pathlib import Path
from pprint import pprint

from chameleon import Chameleon

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "examples" / "config.json"


def load_config(path: Path) -> Chameleon:
    if not path.is_file():
        raise SystemExit(f"config file found at {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise SystemExit("config is empty")
    try:
        data = json.loads(text)
    except json.decoder.JSONDecodeError as e:
        raise SystemExit("config is not valid json") from e
    if not isinstance(data, dict):
        raise SystemExit(f"config root must be a JSON object, got {type(data).__name__}")
    return Chameleon(data, strict=True)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONFIG
    cfg = load_config(path)
    pprint(cfg['service'].name)


if __name__ == "__main__":
    main()