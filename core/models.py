from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine

Base = declarative_base()
engine = create_engine('sqlite:///test.db', echo=False  )


class Issue(Base):
    __tablename__ = "issues"

    language = Column(String)
    id = Column(Integer, primary_key=True)
    title = Column(String)
    html_url = Column(String)
    category = Column(String)
    timestamp = Column(DateTime)
    score = Column(Float)

    def __repr__(self):
        return "<Issue(title='%s', url='%s', language='%s')>" % (self.title, self.html_url, self.language)
