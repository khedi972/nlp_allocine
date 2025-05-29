from dataclasses import dataclass, field
from typing import Type, Dict, List

import requests
from bs4 import BeautifulSoup

import pandas as pd
import warnings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings('ignore')


@dataclass
class AllocineScraper:
    type_dict: Dict[str, str] 
    MAX_PAGES: int = 200
    list_href: List[str] = field(default_factory=list)
    list_score: List[int] = field(default_factory=list)
    list_critics: List[str] = field(default_factory=list)
    list_years: List[str] = field(default_factory=list)
    list_type: List[str] = field(default_factory=list)

    driver: webdriver.Chrome = field(init=False)
    
    def __post_init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)
    
    def collect_review_links(self): 
        for type_name, type_id in self.type_dict.items():
            for nb_page in range(1, self.MAX_PAGES + 1):
                url = f"https://www.allocine.fr/films/genre-{type_id}/pays-5002/?page={nb_page}"
                try:
                    self.driver.get(url)
                    self.driver.implicitly_wait(5)
                    rating_tags = self.driver.find_elements(By.CSS_SELECTOR, "a.xXx.rating-title")
                    for i in range(1, len(rating_tags), 2): 
                        text = rating_tags[i].text.strip().lower()
                        if "spectateurs" not in text:
                            continue
                        link = rating_tags[i].get_attribute("href")
                        self.list_href.append((link, type_name))
                except TimeoutException:
                    print(f"⚠️ Timeout on {url}, we pass to next page", flush=True)
                    continue
        self.driver.quit()
    
    def scrape_reviews(self, max_reviews: Type[int] = 4000):
        for i, (link, type_name) in enumerate(self.list_href):
            if i >= max_reviews:
                break
            href_url = link + "?page=1"
            print("🔗  Movie Treatment n°{} {}".format((i + 1), link))
            try:
                r = requests.get(href_url, timeout=10)
                if r.ok:
                    soup = BeautifulSoup(r.text, "html.parser")
                    score_tags = soup.find_all("span", attrs={"class":"stareval-note"})
                    critics_tags = soup.find_all("div", attrs={"class":"review-card-content"})
                    years_tags = soup.find_all("span", attrs={"class":"review-card-meta-date light"})
                    for score, critic, year in zip(score_tags, critics_tags, years_tags):
                        score_clean = int(score.text.strip().split(",")[0].strip())
                        critic_clean = critic.text.strip()
                        year_clean = ' '.join(year.text.strip().split(' ')[2:])
                        self.list_score.append(score_clean)
                        self.list_critics.append(critic_clean)
                        self.list_years.append(year_clean)
                        self.list_type.append(type_name)
            except Exception as e:
                print(f"❌ Error on {link}: {e}", flush=True)
                continue

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "critics": self.list_critics,
            "scores": self.list_score,
            "date" : self.list_years,
            "types_movie" : self.list_type
        })

    def export_to_parquet(self, filepath: str):
        df = self.to_dataframe()
        df.to_parquet(filepath, index=False)
        
    