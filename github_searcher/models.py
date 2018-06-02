from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship
import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL, echo=False)


class Repo(Base):
    __tablename__ = "repos"
    repo_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)
    language = Column(String)
    created_at = Column(DateTime)
    total_stars = Column(Integer)

    issues = relationship("Issue", back_populates="repo")

    def __repr__(self):
        return "<Repo(title = '%s', url = '%s')>" % (self.name, self.url)


class Issue(Base):
    __tablename__ = "issues"

    issue_id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey('repos.repo_id'))
    title = Column(String)
    description = Column(String)
    url = Column(String)
    category = Column(String)
    created_at = Column(DateTime)
    total_comments = Column(Integer)

    repo = relationship("Repo", back_populates="issues")

    def __repr__(self):
        return "<Issue(title='%s', url='%s')>" % (self.title, self.url)

