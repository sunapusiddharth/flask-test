from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Sidhu@9693@localhost:5432/test?gssencmode=disable"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(Base):
    __tablename__ = 'users2'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)

print(User.__table__)