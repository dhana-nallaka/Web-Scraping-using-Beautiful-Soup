##to scrape all the books name,price,availability,
import sqlite3
import requests#obtain info in form of HTML
from bs4 import BeautifulSoup#parse HTML to extract info
con=sqlite3.connect('booksprice.db')
curr=con.cursor()
###Creating Database Table Books
curr.execute("CREATE TABLE IF NOT EXISTS BOOKS(NAME TEXT,PRICE REAL,AVAILABILITY TEXT, RATING TEXT)")
con.commit()
###Inserting into Books
def insert_book(name,price,instock,rating):
    curr.execute("INSERT INTO BOOKS VALUES(?,?,?,?)",(name,price,instock,rating))
    con.commit()
#scraping throughout all the pages
raw_url="https://books.toscrape.com"
for i in range(1,51):
    website=f"{raw_url}/catalogue/page-{i}.html"
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    html_page=requests.get(website)
    soup=BeautifulSoup(html_page.content,'lxml')#lxml parser
    header=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    for i in header:
      name=i.find("h3").find('a').get('title')#name of the book
      price=i.find("p",class_='price_color').get_text()#price of the book
      instock=i.find("p",class_='instock availability').get_text()#availability of book
      insto=instock.strip()#removing spaces
      rating=i.find("p").get("class")[1]+" "+i.find("p").get("class")[0] #rating
      insert_book(name,price,insto,rating)
curr.close()
con.close()
