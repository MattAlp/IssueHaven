from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()
engine = create_engine('sqlite:///test.db', echo=True)


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=true)
    html_url = Column(String(256))
    language = Column(String(40))

    def __repr__(self):
        return "<Issue(id='%d', url='%s', language='%s')>" % (self.id, self.html_url, self.language)


# class Label(Base):
#     __tablename__ = "labels"

#
#
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)
