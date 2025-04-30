import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
    url = f"https://ca.indeed.com/jobs?q=computer+science&l=Alberta&radius=50&start={page}"
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
c = extract(0)