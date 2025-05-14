# 2025_SK_Bid
1. `./venv/Scripts/activate` で仮想環境起動
2. `python run_negotiation.py` で交渉起動
   1. 設定は`settings.json`
   2. 結果は`result.json`
3. `python plot_result.py` でグラフ（途中）



以下、GPT作成

# GeniusWeb Python サンプル環境構築ガイド

このガイドでは、Delft大学が提供する GeniusWeb の Python サンプル環境をローカルで構築する方法を解説します。

## 📁 プロジェクト構成例

```
2025_SK_Bid/
├── GeniusWebPython/           # GeniusWeb のソースコード（Trac サーバーから取得）
│   ├── geniuswebcore/
│   ├── exampleparties/
├── libs/                      # ローカル依存ライブラリ (.tar.gz) 格納場所
├── requirements.txt
├── settings.json              # 交渉の設定ファイル
├── run_negotiation.py         # 実行スクリプト例
├── plot_result.py             # 結果可視化スクリプト
├── init_env.bat               # 仮想環境セットアップバッチ（オプション）
├── .gitignore                 # Git 除外設定
```

## 🔽 1. GeniusWeb ソースコードの取得

以下の Delft 大学の Trac サーバーからアクセス：

* GeniusWebPython リポジトリ:
  [https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/](https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/)

### ダウンロード手順：

1. 以下のディレクトリにアクセス：

   * [geniuswebcore](https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/export/93/geniuswebcore/)
   * [exampleparties](https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/export/93/exampleparties/)
2. 左下の "Zip Archive" をクリックしてダウンロード
3. 解凍し、`GeniusWebPython/` として保存

## 📦 2. ローカル依存ライブラリ (.tar.gz) の準備

以下のパッケージを `libs/` フォルダに保存してください：

| パッケージ     | バージョン | 取得元 URL                                                                                                                                                                                                                    |
| --------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| geniusweb | 1.2.1 | [https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/export/93/geniuswebcore/dist/geniusweb-1.2.1.tar.gz](https://tracinsy.ewi.tudelft.nl/pubtrac/GeniusWebPython/export/93/geniuswebcore/dist/geniusweb-1.2.1.tar.gz) |
| pyson     | 1.1.3 | [https://tracinsy.ewi.tudelft.nl/pubtrac/Utilities/export/312/pyson/dist/pyson-1.1.3.tar.gz](https://tracinsy.ewi.tudelft.nl/pubtrac/Utilities/export/312/pyson/dist/pyson-1.1.3.tar.gz)                                   |

> 💡 `pyson` は `geniusweb` が依存しているため、バージョンを合わせる必要があります。

## 📄 3. requirements.txt の例

```txt
matplotlib
numpy
PyQt5==5.15.6
PyQt5-sip
PyQt5-Qt5
python-dateutil
pillow
websocket-client==1.0.1
pyson @ file://./libs/pyson-1.1.3.tar.gz
geniusweb @ file://./libs/geniusweb-1.2.1.tar.gz
```

> ⚠ 依存関係の警告が出る場合は `PyQt5==5.15.6` や `websocket-client==1.0.1` にバージョンを合わせてください。
> pip の依存解決を回避するために以下のオプションを推奨：
>
> ```bash
> pip install -r requirements.txt --use-deprecated=legacy-resolver
> ```

## ⚙ 4. 仮想環境の作成とセットアップ

```bash
# Python 3.9.13 を推奨（pyenv などで用意）
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt --use-deprecated=legacy-resolver
```

もしくは `init_env.bat` を使って自動化：

### 📄 init\_env.bat

```bat
@echo off
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --use-deprecated=legacy-resolver
```

実行方法：

```bash
init_env.bat
```

## ▶ 5. サンプル実行

```bash
python run_negotiation.py
python plot_result.py
```

`settings.json` や `party1.json`, `party2.json` などのプロファイルファイルが適切に設定されていることを確認してください。

## 📝 補足

* `venv/` は Git に含めないようにしてください。
* `.gitignore` の例：

  ```gitignore
  venv/
  __pycache__/
  *.pyc
  *.pyo
  *.pyd
  .DS_Store
  ```
* `pyson` は Trac の `Utilities` プロジェクトで管理されています。
* この構成により、他マシン間でも再現可能な GeniusWeb 開発環境を構築できます。

---

必要に応じて、環境構築用の `init_env.bat` や `Makefile` を追加して自動化することも可能です。
