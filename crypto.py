from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://crypto.com/price'
headers = {'User-Agent': 'Chrome/41.0.2228.0'}

req = Request(url,headers=headers)
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage,'html.parser')

data=soup.findAll("tr")

print("------------ Top 5 Cryptocurrencies ------------")

for row in data[1:6]:
    td=row.findAll("td")
    name_symbol = td[2].text.strip() 
    price=td[3].text[1:].split('$')[0].replace(",","")
    fprice=float(price)
    pct_change=float(td[4].text.strip().replace("%", "")) 
    last_price=float((pct_change/100*fprice)+fprice)

    for i in range(1, len(name_symbol)):
        if name_symbol[i-1].islower() and name_symbol[i].isupper():
            name = name_symbol[1:i].strip()
            symbol = name_symbol[i:].strip()

    print(f"Name: {name}")
    print(f"Symbol: {symbol}")
    print(f"Current Price: ${fprice:,}")
    print(f"DOD Change: {pct_change:.2f}% from ${last_price:.2f}")
    print()
    print()

