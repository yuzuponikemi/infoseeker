import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Paper
from datetime import datetime

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_add_paper(db_session):
    # Create a new paper
    paper = Paper(
        title="Test Paper",
        authors="Test Author",
        abstract="This is a test paper.",
        pdf_url="http://example.com/test.pdf",
        published_date=datetime.utcnow()
    )

    # Add the paper to the session and commit
    db_session.add(paper)
    db_session.commit()

    # Query the paper back
    queried_paper = db_session.query(Paper).filter_by(pdf_url="http://example.com/test.pdf").first()

    # Assert that the paper was saved correctly
    assert queried_paper is not None
    assert queried_paper.title == "Test Paper"
