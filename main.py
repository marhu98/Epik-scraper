from bs4 import BeautifulSoup as bs
import requests
import re


def convert(s):
    pattern = re.search("\$(?P<number>(\d,?)*.\d*)",s.replace(",",""))
    if pattern:
        return float(pattern.groupdict()["number"])
    else:
        return s

class PriceList(list):
    def __init__(self,l):
        for el in l:
            self.append(el)
    def __str__(self):
        res = ""
        end=", "
        for el in self:
            res+=str(el)+end
        return res[:-len(end)]
    
class Prices(list):
    def __init__(self,l=[]):
        for el in l:
            self.append(el)
    def __str__(self):
        res =""
        for el in self:
            res+=str(el)+"\n"
        return res[:-1]

def main():
    url1 = "https://registrar.epik.com/prices/registration/toplevel"
    url2 = "https://registrar.epik.com/prices/registration/gtld/#prices"
    urls = [url1,url2]
    for url in urls:

        res = requests.get(url).text
        soup = bs(res,"html.parser")
        trs = soup.find_all("tr",class_="tld-pricing-grey")
    
        prices = Prices()
    
        for tr in trs:
            tds = tr.find_all("td")
            tds=[convert(s.string) for s in tds]
            prices.append(PriceList([s for s in tds]))
    
    
    prices.sort(key=lambda x:x[2])    
    print(prices)


if __name__=="__main__":
    main()
