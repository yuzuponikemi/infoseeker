# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
try:
    import config
except ImportError:
    print("Error: config.py not found. Please create it by copying config.py.example and filling in your details.")
    exit(1)

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
