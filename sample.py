import bs4
import requests
from bs4 import BeautifulSoup

r = requests.get('https://au.finance.yahoo.com/quote/BHP.AX?p=BHP.AX')
soup = bs4.BeautifulSoup(r.text, "xml")

specific = soup.findAll('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})
print(specific)