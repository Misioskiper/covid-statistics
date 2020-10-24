import json, requests
from bs4 import BeautifulSoup as bs

class Wojewodztwo():
    def __init__(self, name, cases, deaths):
        self.Name = name
        self.Cases = int("".join(cases.split()))
        self.Deaths = int("".join(deaths.split()))


def getWojewodztwa():
    req = requests.get('https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2')
    soup = bs(req.content, 'lxml')
    pre = soup.select_one('pre').text
    data = json.loads(pre)
    dane = data['data'].split('\n')
    Wojewodztwa = []
    for line in dane[2:-1]:
        dane_wojewodztwo = line.split(';')
        Wojewodztwa.append(Wojewodztwo(dane_wojewodztwo[0], dane_wojewodztwo[1], dane_wojewodztwo[2]))
    return Wojewodztwa, data['description']
