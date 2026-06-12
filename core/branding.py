"""core/branding.py — Central branding configuration for MATT."""
import json
import sys
from pathlib import Path

_DEFAULT = {
    "assistant_name": "MATT",
    "assistant_name_spoken": "Matt",
    "wake_words": ["matt", "oye matt", "hey matt", "despierta"],
    "legacy_wake_words": ["jarvis", "oye jarvis"],
    "honorific_default": "señor",
    "log_prefix": "[MATT]",
    "executable_name": "MATT",
    "default_image_folder": "MATT_Generadas",
}


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


_BRANDING_PATH = _base_dir() / "config" / "branding.json"
_cached: dict | None = None


def load_branding() -> dict:
    global _cached
    if _cached is not None:
        return _cached
    if _BRANDING_PATH.exists():
        try:
            data = json.loads(_BRANDING_PATH.read_text(encoding="utf-8"))
            _cached = {**_DEFAULT, **data}
            return _cached
        except Exception:
            pass
    _cached = dict(_DEFAULT)
    return _cached


def get_wake_words(include_legacy: bool = True) -> list[str]:
    b = load_branding()
    words = list(b.get("wake_words", []))
    if include_legacy:
        words.extend(b.get("legacy_wake_words", []))
    return words


def log_prefix() -> str:
    return load_branding().get("log_prefix", "[MATT]")
