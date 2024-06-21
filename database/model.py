from sqlalchemy import Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True)
    login = mapped_column(String(30), nullable=False, unique=True)
    password_hash = mapped_column(String, nullable=False)
    role = mapped_column(String, nullable=True)

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return True if self.role == "Administrator" else False


DATABASE_URI = "sqlite:///dash_users_login.db"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


init_db()

