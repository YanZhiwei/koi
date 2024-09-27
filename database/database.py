from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./koi_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB_Engine = create_engine(SQLALCHEMY_DATABASE_URL,
                          echo=False,
                          pool_size=5,  # 池最大连接数
                          max_overflow=10,  # 池最多溢出连接数
                          pool_recycle=600,  # 池回收connection的间隔，默认不回收（-1）。当前为10分钟。
                          pool_timeout=15,  # 从池获取connection的最长等待时间，默认30s,当前 15s
                          )
Base = declarative_base()
Session = sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
