import arxiv
import requests
from datetime import datetime
from database import SessionLocal, Paper

try:
    import config
except ImportError:
    print("Error: config.py not found. Please create it by copying config.py.example and filling in your details.")
    exit(1)

def fetch_and_notify():
    db = SessionLocal()
    new_papers = []
    
    for keyword in config.SEARCH_KEYWORDS:
        search = arxiv.Search(
            query=keyword,
            max_results=10,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in search.results():
            # Check if paper already exists
            exists = db.query(Paper).filter_by(pdf_url=result.pdf_url).first()
            if not exists:
                paper = Paper(
                    title=result.title,
                    authors=", ".join(author.name for author in result.authors),
                    abstract=result.summary,
                    pdf_url=result.pdf_url,
                    published_date=result.published.replace(tzinfo=None)
                )
                db.add(paper)
                new_papers.append(paper)

    if new_papers:
        db.commit()
        message = f"📚 新着論文が {len(new_papers)} 件見つかりました。\n\n"
        for paper in new_papers:
            message += f"*{paper.title}*\nURL: {paper.pdf_url}\n\n"
        
        requests.post(config.SLACK_WEBHOOK_URL, json={"text": message})
        print(f"{len(new_papers)}件の論文を通知しました。")
    else:
        print("新着論文はありませんでした。")
        
    db.close()

def job_function():
    print(f"--- Job started at {datetime.now()} ---")
    fetch_and_notify()
    print(f"--- Job finished at {datetime.now()} ---")
