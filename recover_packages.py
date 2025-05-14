import os

site_packages = r'venv\Lib\site-packages'  # 相対パスでもOK
packages = []

for item in os.listdir(site_packages):
    if item.endswith(".dist-info"):
        pkg = item.split("-")[0]
        packages.append(pkg)

print("✅ 推定されるインストール済みパッケージ：")
for p in sorted(set(packages)):
    print(p)
