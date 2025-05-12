import json
import matplotlib.pyplot as plt

# --- 設定 ---
RESULT_FILE = "result.json"

# --- JSON 読み込み ---
with open(RESULT_FILE, encoding="utf-8") as f:
    data = json.load(f)

actions = data["SAOPState"]["actions"]
utilities = {}
timeline = {}

# --- 効用スコア（擬似）の計算 ---
for i, action in enumerate(actions):
    for act_type, act_data in action.items():
        actor = act_data.get("actor")
        bid = act_data.get("bid", {}).get("issuevalues", {})

        # 擬似効用スコア（文字列のハッシュを整数化して加算）
        score = sum(hash(str(v)) % 100 for v in bid.values())

        utilities.setdefault(actor, []).append(score)
        timeline.setdefault(actor, []).append(i)

# --- グラフ描画 ---
for actor in utilities:
    plt.plot(timeline[actor], utilities[actor], label=actor)

plt.xlabel("提案回数")
plt.ylabel("擬似効用スコア")
plt.title("交渉中の効用推移（擬似）")
plt.legend()
plt.tight_layout()
plt.show()
