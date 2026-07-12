import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

class JobScraper:
    def scrape_job(self, url: str) -> Dict[str, Any]:
        """
        Attempts to scrape job title, company, and description from a URL.
        Falls back to dummy mock details if blocked or connection fails.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                
                # Try standard generic tags
                title = ""
                title_tag = soup.find("h1") or soup.find("h2")
                if title_tag:
                    title = title_tag.text.strip()
                    
                # Clean up description
                body_text = ""
                paragraphs = soup.find_all(["p", "li"])
                if paragraphs:
                    body_text = "\n".join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 20])
                    
                if title and body_text:
                    return {
                        "title": title,
                        "company": "Scraped Company",
                        "location": "Remote",
                        "description": body_text[:2000]
                    }
        except Exception as e:
            print(f"Scraper encountered error: {e}. Running fallback.")

        # Fallback Mock Job Description
        return {
            "title": "Python Backend Developer (FastAPI/AWS)",
            "company": "CloudVentures LLC",
            "location": "Austin, TX (Hybrid)",
            "description": (
                "We are looking for a Python Backend Developer. "
                "Requirements:\n"
                "- 3+ years experience with Python & FastAPI\n"
                "- Strong familiarity with SQL and AWS services (EC2, S3)\n"
                "- Experience with Docker and CI/CD pipelines.\n"
                "Nice to have: Kubernetes and PyTorch."
            )
        }

job_scraper = JobScraper()
