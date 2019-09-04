# imports
import requests
from bs4 import BeautifulSoup
import sqlalchemy as sa


# scrap craigslist NY for apartments

result = requests.get("https://newyork.craigslist.org/search/aap")
print(result.status_code)
src = result.content
soup = BeautifulSoup(src, 'html.parser')

all_listings = soup.find(class_='rows')
listing = all_listings.find_all(class_='result-info')


title = [apt.find('a').get_text() for apt in listing]
price = [apt.find(class_='result-price').get_text() for apt in listing]
listing_date = [apt.find(class_='result-date').get_text() for apt in listing]
nieghborhood = []
url = []


for link in listing:
    for a_tag in link.find_all('a'):
            if a_tag.attrs['href'] is not '#':
                url.append(a_tag.attrs['href'])

for apt in listing:
        hood = apt.find(class_='result-hood')
        if hood is not None:
                nieghborhood.append(hood.get_text())
        else:
                nieghborhood.append(None)


apt_dict = []

placeholder_dict = {}
for i in range(len(title)):
        placeholder_dict = {
                'title': title[i],
                'price': price[i],
                'listing_date': listing_date[i],
                'nieghborhood': nieghborhood[i],
                'url': url[i]
        }
        apt_dict.append(placeholder_dict)







#database connection

engine = sa.create_engine('mysql+pymysql://root:password@localhost/aptlisting')
connection = engine.connect()
metadata = sa.MetaData()


# create table
NYC_apts = sa.Table('NYC_apts', metadata,
sa.Column('title', sa.String(255)),
sa.Column('nieghborhood', sa.String(255)),
sa.Column('price', sa.String(10)),
sa.Column('listing_date', sa.String(10)),
sa.Column('url', sa.String(255))
)

metadata.create_all(engine)



# update data

query = sa.insert(NYC_apts)
result_proxy = connection.execute(query, apt_dict)



