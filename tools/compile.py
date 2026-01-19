# python
import subprocess
import shutil
import sys
import os
from pathlib import Path

OUTPUT_FILENAME = "discord_message_deleter"


def ensure_pyinstaller():
    """Ensure PyInstaller is importable/runable from the current Python."""
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "--version"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("PyInstaller is not available in this Python environment") from exc


def main():
    ensure_pyinstaller()

    # Resolve project root and entry script reliably
    project_root = Path(__file__).resolve().parent.parent
    entry_script = project_root / "main.py"
    if not entry_script.exists():
        raise FileNotFoundError(f"Entry script not found: `{entry_script}`")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--optimize=2",
        "--noupx",
        "--noconfirm",
        "--name", OUTPUT_FILENAME,
        str(entry_script),
    ]

    subprocess.check_call(cmd)

    exe_suffix = ".exe" if os.name == "nt" else ""
    # Expect single-file exe in dist/, but also check the folder case
    candidate1 = Path("dist") / f"{OUTPUT_FILENAME}{exe_suffix}"
    candidate2 = Path("dist") / OUTPUT_FILENAME / f"{OUTPUT_FILENAME}{exe_suffix}"

    if candidate1.exists():
        src = candidate1
    elif candidate2.exists():
        src = candidate2
    else:
        raise FileNotFoundError(f"Built executable not found. Checked `{candidate1}` and `{candidate2}`")

    dst = Path.cwd() / f"{OUTPUT_FILENAME}{exe_suffix}"
    shutil.copy2(src, dst)
    print(f"Copied `{src}` to `{dst}`")


if __name__ == "__main__":
    main()
