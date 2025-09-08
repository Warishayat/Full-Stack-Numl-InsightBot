from firecrawl import Firecrawl
from dotenv import load_dotenv
import os, time

load_dotenv()
client = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

def scrape_all_text_to_markdown(urls, filename="all_text.md", delay=3):
    all_text = ""
    for url in urls:
        try:
            doc = client.scrape(url, formats=["markdown"])
            text = getattr(doc, "markdown", "")
            if text:
                all_text += text.strip() + "\n\n"
                print(f"Scraped: {url}")
            else:
                print(f"No text extracted: {url}")
        except Exception as e:
            print(f"Failed: {url} ({e})")
        time.sleep(delay)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(all_text)

urls = [
    "https://numl.edu.pk/",
    "https://numl.edu.pk/admission",
    "https://numl.edu.pk/programs/undergraduate",
    "https://numl.edu.pk/faculties/Faculty%20of%20Engineering%20and%20Computing",
    "https://numl.edu.pk/department/273/faculty",
    "https://numl.edu.pk/programs/phd",
    "https://numl.edu.pk/programs/diploma",
    "https://numl.edu.pk/facilities",
    "https://numl.edu.pk/jobs/all",
    "https://numl.edu.pk/department/195/faculty",
    "https://numl.edu.pk/department/179/faculty",
    "https://numl.edu.pk/admission/faqs",
    "https://transport.numl.edu.pk/frontend/listing/transport/routes",
    "https://numl.edu.pk/department/269/faculty",
    "https://numl.edu.pk/department/199/faculty",
    "https://numl.edu.pk/department/175/faculty",
    "https://numl.edu.pk/programs/program/258",
    "https://numl.edu.pk/programs/program/57",
    "https://numl.edu.pk/programs/program/520",
    "https://numl.edu.pk/programs/program/349",
    "https://numl.edu.pk/programs/program/535",
    "https://numl.edu.pk/programs/program/536",
    "https://numl.edu.pk/programs/program/351",
    "https://numl.edu.pk/programs/program/240",
    "https://numl.edu.pk/programs/program/238",
    "https://numl.edu.pk/programs/program/264",
    "https://numl.edu.pk/programs/program/252",
    "https://numl.edu.pk/pcc",
    "https://numl.edu.pk/offices/ITCON",
    "https://numl.edu.pk/offices/Rector%20Office",
    "https://numl.edu.pk/offices/Registrar%20Office"
]

if __name__ == "__main__":
    scrape_all_text_to_markdown(urls)
