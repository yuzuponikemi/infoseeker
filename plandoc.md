承知いたしました。ローカル環境での開発に焦点を当て、より具体的で実践的なステップ2の実装計画書を以下に示します。

-----

### \#\# 【ローカル実行版】実装計画書：自動論文収集＆通知エージェント

この計画書は、お手元のPC（Windows, macOS, Linux）またはRaspberry Pi上で、指定したキーワードのarXiv論文を毎日自動収集し、Slackへ通知するエージェントを構築することを目的とします。

#### 1\. 開発のゴール 🥅

  * Pythonスクリプトを一つ用意する。
  * そのスクリプトを実行すると、毎日決まった時間に自動で論文収集が始まる。
  * 新しい論文が見つかった場合のみ、指定したSlackチャンネルに通知が飛ぶ。
  * 収集した論文の情報は、PC上のデータベースファイルに蓄積されていく。

-----

#### 2\. 技術スタックと環境設定 🛠️

| カテゴリ | 選択技術 | 理由 |
| :--- | :--- | :--- |
| **言語** | **Python 3.9+** | 豊富なライブラリとエコシステム。 |
| **データベース** | **SQLite** | サーバー不要のファイルベースDB。ローカル開発に最適で、Pythonに標準で組み込まれています。 |
| **DB操作** | **SQLAlchemy** | Pythonコードで直感的にDBを操作できるライブラリ（ORM）。将来DBを変更する際もコード修正が容易です。 |
| **論文取得** | **arxiv** | arXiv APIを簡単に利用するためのライブラリ。 |
| **スケジュール実行** | **APScheduler** | Pythonプログラム内でスケジュール管理を完結できるため、OSの機能に依存せずクロスプラットフォームで動作します。 |
| **通知** | **requests** | Slackへの通知（HTTP POST）を行うための標準的なライブラリ。 |

##### **▶️ 環境設定の手順**

1.  プロジェクト用のディレクトリを作成します。
2.  ターミナル（コマンドプロンプト）でそのディレクトリに移動し、仮想環境を作成します。<br>`python -m venv venv`
3.  仮想環境を有効化します。<br> (Windows) `venv\Scripts\activate`<br> (macOS/Linux) `source venv/bin/activate`
4.  必要なライブラリを一括でインストールします。<br>`pip install arxiv SQLAlchemy APScheduler requests pandas`

-----

#### 3\. 実装ステップとコードの骨子 📝

開発を以下の5つのステップに分けて進めます。

##### **ステップ 3.1: 設定ファイルの作成**

まず、キーワードやSlackのURLなどを一箇所で管理できるように、設定ファイル（`config.py`）を作成します。

```python
# config.py
SEARCH_KEYWORDS = [
    "consciousness", "self-awareness", "digital ghost",
    "embodied intelligence", "brain-computer interface"
]
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX" # ここにSlackのWebhook URLを貼る
DB_FILE = "papers.db"
```

> **補足:** SlackのWebhook URLは、[こちらのガイド](https://slack.com/intl/ja-jp/help/articles/115005265063-Slack-%E3%81%A7%E3%81%AE-Incoming-Webhook-%E3%81%AE%E5%88%A9%E7%94%A8)に従って取得してください。

##### **ステップ 3.2: データベースの定義**

`SQLAlchemy`を使い、論文情報を保存するためのテーブル構造を定義します。

```python
# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import config

# DBエンジンを作成
engine = create_engine(f'sqlite:///{config.DB_FILE}')
Base = declarative_base()

# 論文テーブルのモデル
class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = Column(String)
    abstract = Column(Text)
    pdf_url = Column(String, unique=True)
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

# テーブルを初期化する関数
def init_db():
    Base.metadata.create_all(engine)

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

##### **ステップ 3.3: 論文収集と通知のコアロジック作成**

論文を取得し、DBに保存し、Slackに通知するメインの処理を関数としてまとめます。

```python
# main.py
import arxiv
import requests
from datetime import datetime, timedelta
from database import SessionLocal, Paper, init_db
import config

# ... (中略) ...

def fetch_and_notify():
    # ... (Step1のコードをベースに、DBへの保存と重複チェック処理を追加) ...
    # 新規論文があれば、Slack通知用のメッセージを整形
    
    new_papers = [] # ここに新規保存した論文オブジェクトを入れる
    
    # ... DB保存ロジック ...

    if new_papers:
        message = f"📚 新着論文が {len(new_papers)} 件見つかりました。\n\n"
        for paper in new_papers:
            message += f"*{paper.title}*\nURL: {paper.pdf_url}\n\n"
        
        # Slackに通知
        requests.post(config.SLACK_WEBHOOK_URL, json={"text": message})
        print(f"{len(new_papers)}件の論文を通知しました。")
    else:
        print("新着論文はありませんでした。")

```

##### **ステップ 3.4: スケジューラーの実装**

`APScheduler`を使い、ステップ3.3で作成した関数を毎日決まった時間に実行するように設定します。

```python
# main.py (追記)
from apscheduler.schedulers.blocking import BlockingScheduler
import time

def job_function():
    print(f"--- Job started at {datetime.now()} ---")
    fetch_and_notify()
    print(f"--- Job finished at {datetime.now()} ---")

if __name__ == "__main__":
    # 起動時に一度DBを初期化
    init_db()

    # スケジューラーを設定
    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    # 毎日朝8時にjob_functionを実行
    scheduler.add_job(job_function, 'cron', hour=8, minute=0)

    print("スケジューラーを開始します。Ctrl+Cで終了します。")
    try:
        # スケジュールを開始
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
```

##### **ステップ 3.5: 実行**

全てのコードが完成したら、ターミナルでスクリプトを実行します。

`python main.py`

これを実行すると、ターミナルは待機状態になり、指定した時間（この例では毎朝8時）になると自動で処理が走り、結果がSlackに通知されます。実行を止めたい場合は `Ctrl + C` を押します。

-----

### ◆ 次のステップ

この計画書に沿って実装を進めてみてください。まずは各ステップのコードを個別に作成・テストし、最後に `main.py` で統合するのが良いでしょう。

実装中につまづいた点や、さらに具体的なコードの例が必要な場合は、いつでもお声がけください。