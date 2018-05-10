from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine

Base = declarative_base()
engine = create_engine('sqlite:///test.db', echo=False  )


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    html_url = Column(String(512))
    language = Column(String(64))
    category = Column(String(64))
    timestamp = Column(DateTime)
    score = Column(Integer)

    def __repr__(self):
        return "<Issue(url='%s', language='%s')>" % (self.html_url, self.language)
