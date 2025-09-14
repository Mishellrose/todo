

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base     
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:youbitch@localhost/todolist'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='todolist',
#             user='postgres',
#             password='youbitch',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#      print("Error connecting to the database")
#      print("Error:", error)
#     time.sleep(2)
