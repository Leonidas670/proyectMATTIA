"""One-shot migration: JARVIS branding → MATT for local user data."""
import json
import shutil
import sys
from pathlib import Path


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def _rename_profile_keys(obj):
    if isinstance(obj, dict):
        if "jarvis_ui_control" in obj and "matt_ui_control" not in obj:
            obj["matt_ui_control"] = obj.pop("jarvis_ui_control")
        for v in obj.values():
            _rename_profile_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            _rename_profile_keys(item)


def migrate() -> None:
    base = _base_dir()
    config_dir = base / "config"
    api_path = config_dir / "api_keys.json"
    profile_path = config_dir / "user_profile.json"
    old_log = base / "jarvis.log"
    new_log = base / "matt.log"

    if api_path.exists():
        try:
            cfg = json.loads(api_path.read_text(encoding="utf-8"))
            if "matt_voice" not in cfg and "jarvis_voice" in cfg:
                cfg["matt_voice"] = cfg["jarvis_voice"]
            if "matt_theme" not in cfg and "jarvis_theme" in cfg:
                cfg["matt_theme"] = cfg["jarvis_theme"]
            cfg["migrated_to_matt"] = True
            api_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            print("[migrate] api_keys.json updated")
        except Exception as e:
            print(f"[migrate] api_keys.json error: {e}")

    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            _rename_profile_keys(profile)
            profile_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
            print("[migrate] user_profile.json updated")
        except Exception as e:
            print(f"[migrate] user_profile.json error: {e}")

    if old_log.exists() and not new_log.exists():
        try:
            shutil.move(str(old_log), str(new_log))
            print("[migrate] jarvis.log -> matt.log")
        except Exception as e:
            print(f"[migrate] log rename error: {e}")

    print("[migrate] Done.")


if __name__ == "__main__":
    migrate()
