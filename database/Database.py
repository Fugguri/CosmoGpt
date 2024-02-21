from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import datetime
import dotenv
# Создаем соединение с базой данных SQLite
env = dotenv.dotenv_values(".env")

DATABASE_URL = env.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session_ = sessionmaker(bind=engine)

# Создаем базовый класс для объявления моделей
Base = declarative_base()


def get_db():
    db = Session_()
    try:
        yield db
    finally:
        db.close()
# Определяем модель пользователя


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    firstname = Column(String(100))
    lastname = Column(String(100))
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)
    contract_id = Column(String(155), nullable=True)
    subscription_end = Column(DateTime, default=datetime.datetime.utcnow)
    free = Column(Boolean, default=False)
    use_promo = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}', fullname='{self.firstname} {self.lastname}'),contract_id={self.contract_id}, subscription_end='{self.subscription_end}')>"


# Создаем таблицу в базе данных
Base.metadata.create_all(engine)


class UserManager:
    def __init__(self):
        self.session = Session_()
        self.session.autoflush = True

    def add_user(self, telegram_id: int, username: str = None, firstname: str = None, lastname: str = None):
        with Session(engine) as session:
            session.begin()
            try:
                new_user = User(telegram_id=telegram_id, username=username,
                                firstname=firstname, lastname=lastname)
                session.add(new_user)
                session.commit()
            except:
                session.rollback()
                raise
            else:
                session.commit()

    def get_all_users(self):
        with Session(engine) as session:
            session.begin()
            try:
                all_users = session.ex(User).all()

            except:
                session.rollback()
                raise
            else:
                session.commit()
        return all_users

    def get_user_by_telegram_id(self, telegram_id: int):
        user = self.session.query(User).filter_by(
            telegram_id=telegram_id).first()
        return user

    def get_user_by_contract_id(self, contract_id: str):
        with Session(engine) as session:
            session.begin()
            try:
                user = self.session.query(User).filter_by(
                    contract_id=contract_id).first()
            except:
                session.rollback()
                raise
            else:
                session.commit()

        return user

    def delete_user(self, telegram_id: int):

        user = self.session.query(User).filter_by(
            telegram_id=telegram_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def update_user(self, telegram_id: int,
                    new_username: str = None,
                    new_firstname: str = None,
                    new_lastname: str = None,
                    contract_id: str = None,
                    subscription_end=None,
                    free: Boolean = False,
                    use_promo: Boolean = False
                    ):
        with Session(engine) as session:
            session.begin()
        try:
            user = self.session.query(User).filter_by(
                telegram_id=telegram_id).first()
            if user:
                if new_username:
                    user.username = new_username
                if new_firstname:
                    user.firstname = new_firstname
                if new_lastname:
                    user.lastname = new_lastname
                if contract_id:
                    user.contract_id = contract_id
                if subscription_end:
                    user.subscription_end = subscription_end
                if subscription_end:
                    user.use_promo = use_promo
                user.free = free
            self.session.commit()
        except:
            session.rollback()
            raise
        else:
            session.commit()
