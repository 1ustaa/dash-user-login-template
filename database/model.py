from sqlalchemy import Integer, String, create_engine, ForeignKey, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

user_role_association = Table("user_role_association_table", Base.metadata,
                              Column("user_account_id", ForeignKey("user_account.id"), primary_key=True),
                              Column("user_role_id", ForeignKey("user_role.id"), primary_key=True),
                              )


class User(Base, UserMixin):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True)
    login = mapped_column(String(30), nullable=False, unique=True)
    password_hash = mapped_column(String, nullable=False)
    user_role = relationship("UserRole", secondary=user_role_association, back_populates="user")

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        admin = session.query(UserRole).filter_by(role="Administrator").first()
        return admin in self.user_role

    def is_unique(self, login):
        duplicate = session.query(User).filter_by(login=login).first()
        return duplicate is None

    def get_roles(self):
        role_ids = session.query(user_role_association.c.user_role_id).filter_by(user_account_id=self.id).all()
        role_ids_list = [role_id[0] for role_id in role_ids]
        roles = []
        for role_id in role_ids_list:
            roles.append(session.query(UserRole).filter_by(id=role_id).first().role)
        return roles

    def get_roles_str(self):
        roles = self.get_roles()
        return ", ".join(roles)

    def add_role(self, role):
        self.user_role.append(role)


def get_all_roles():
    roles = session.query(UserRole.role).all()
    return [role[0] for role in roles]


class UserRole(Base):
    __tablename__ = "user_role"
    id = mapped_column(Integer, primary_key=True)
    role = mapped_column(String(30), nullable=False, unique=True)
    user = relationship("User", secondary=user_role_association, back_populates="user_role")


DATABASE_URI = "sqlite:///dash_users_login.db"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


init_db()
