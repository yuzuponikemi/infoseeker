import pytest
from unittest.mock import patch, MagicMock
from core import fetch_and_notify
from database import Paper
from datetime import datetime

class MockArxivResult:
    def __init__(self, title, pdf_url):
        self.title = title
        self.pdf_url = pdf_url
        mock_author = MagicMock()
        mock_author.name = "Test Author"
        self.authors = [mock_author]
        self.summary = "A summary"
        self.published = datetime.now()

@patch('core.requests.post')
@patch('core.SessionLocal')
@patch('core.arxiv.Search')
def test_fetch_and_notify_new_paper(mock_arxiv_search, mock_session_local, mock_requests_post, monkeypatch):
    """Test that a new paper is added to the DB and a notification is sent."""
    # Arrange: Mock config to only have one keyword
    monkeypatch.setattr('core.config.SEARCH_KEYWORDS', ['test'])

    # Arrange: Mock arXiv search to return one new paper
    mock_result = MockArxivResult("New Test Paper", "http://example.com/new.pdf")
    mock_arxiv_search.return_value.results.return_value = [mock_result]

    # Arrange: Mock DB to find no existing paper
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_session_local.return_value = mock_session

    # Act: Call the function
    fetch_and_notify()

    # Assert: Check that the paper was added and committed
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    # Assert: Check that a Slack notification was sent
    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert "New Test Paper" in kwargs['json']['text']

@patch('core.requests.post')
@patch('core.SessionLocal')
@patch('core.arxiv.Search')
def test_fetch_and_notify_no_new_paper(mock_arxiv_search, mock_session_local, mock_requests_post):
    """Test that no notification is sent if the paper already exists."""
    # Arrange: Mock arXiv search to return one existing paper
    mock_result = MockArxivResult("Existing Test Paper", "http://example.com/existing.pdf")
    mock_arxiv_search.return_value.results.return_value = [mock_result]

    # Arrange: Mock DB to find an existing paper
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = Paper()
    mock_session_local.return_value = mock_session

    # Act: Call the function
    fetch_and_notify()

    # Assert: Check that no paper was added
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

    # Assert: Check that no Slack notification was sent
    mock_requests_post.assert_not_called()
