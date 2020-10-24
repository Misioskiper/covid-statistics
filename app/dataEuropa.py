import json, requests
import dateutil.parser

translation={'Albania' : 'Albania','Algeria' : 'Algieria','Andorra' : 'Andora','Austria' : 'Austria','Belarus' : 'Białoruś','Belgium' : 'Belgia','Bosnia and Herzegovina' : 'Bośnia i Hercegowina','Bulgaria' : 'Bułgaria','Croatia' : 'Chorwacja','Czech Republic' : 'Czechy','Denmark' : 'Dania','Estonia' : 'Estonia','Finland' : 'Finlandia','France' : 'Francja','Germany' : 'Niemcy','Greece' : 'Grecja','Holy See (Vatican City State)' : 'Stolica Apostolska (Watykan)','Hungary' : 'Węgry','Iceland' : 'Islandia','Ireland' : 'Irlandia','Italy' : 'Włochy','Kazakhstan' : 'Kazachstan','Latvia' : 'Łotwa','Liechtenstein' : 'Liechtenstein','Lithuania' : 'Litwa','Luxembourg' : 'Luksemburg','Macedonia, Republic of' : 'Macedonia Północna','Malta' : 'Malta','Moldova' : 'Mołdawia','Monaco' : 'Monako','Montenegro' : 'Czarnogóra','Netherlands' : 'Holandia','Norway' : 'Norwegia','Poland' : 'Polska','Portugal' : 'Portugalia','Romania' : 'Rumunia','Russian Federation' : 'Rosja','San Marino' : 'San Marino','Serbia' : 'Serbia','Slovakia' : 'Słowacja','Slovenia' : 'Słowenia','Spain' : 'Hiszpania','Switzerland' : 'Szwajcaria','Turkey' : 'Turcja','Ukraine' : 'Ukraina','United Kingdom' : 'Wielka Brytania'}

class Country():
    def __init__(self, name, newCases, newDeaths, totalDeaths, totalCases, newRecovered, totalRecovered):
        self.Name = translation[name]
        if newCases == 0:
            self.NewCases = 'Brak Danych'
        else:
            self.NewCases = newCases
        if newDeaths == 0:
            self.NewDeaths = 'Brak Danych'
        else:
            self.NewDeaths = newDeaths
        if totalDeaths == 0:
            self.TotalDeaths = 'Brak Danych'
        else:
            self.TotalDeaths = totalDeaths
        if totalCases == 0:
            self.TotalCases = 'Brak Danych'
        else:
            self.TotalCases = totalCases
        if newRecovered == 0:
            self.NewRecovered = 'Brak Danych'
        else:
            self.NewRecovered = newRecovered
        if totalRecovered == 0:
            self.TotalRecovered = 'Brak Danych'
        else:
            self.TotalRecovered = totalRecovered

time = 0

def getCountries():
    #Create request
    req = requests.get('https://api.covid19api.com/summary')
    data = req.content
    converted = json.loads(data)
    Countries = []
    global time 
    time = converted['Date']
    #Make list of Countries object
    for countryData in converted['Countries']:
        if countryData['Country'] in translation.keys():
            Countries.append(Country(countryData['Country'], countryData['NewConfirmed'], countryData['NewDeaths'], countryData['TotalDeaths'], countryData['TotalConfirmed'], countryData['NewRecovered'], countryData['TotalRecovered']))
    #Sort list by total cases
    sortedCountries = sorted(Countries, key=lambda x: x.TotalCases, reverse=True)
    return sortedCountries

def getTime():
    #Return date of downloaded data
    date = dateutil.parser.parse(time)
    return date.strftime('%d/%m/%Y %H:%M:%S')