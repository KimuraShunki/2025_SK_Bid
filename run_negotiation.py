import subprocess
import os
import sys

SETTINGS_PATH = "settings.json"
OUTPUT_PATH = "result.json"

python_exec = sys.executable
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

try:
    result = subprocess.run(
        [python_exec, "-m", "geniusweb.simplerunner.NegoRunner", SETTINGS_PATH],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    # JSON 部分を「INFO:protocol ended normally: 」のあとから抽出
    for line in result.stdout.splitlines():
        if line.startswith("INFO:protocol ended normally: "):
            json_text = line.replace("INFO:protocol ended normally: ", "")
            break
    else:
        raise ValueError("❌ JSON block not found in output.")

    # 構文チェック付きで保存
    import json

    parsed = json.loads(json_text)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)

    print(f"✅ Valid JSON saved to {OUTPUT_PATH}")

except subprocess.CalledProcessError as e:
    print("❌ Negotiation failed.")
    print("STDOUT:\n", e.stdout)
    print("STDERR:\n", e.stderr)
except Exception as e:
    print(f"❌ Error extracting JSON: {e}")
