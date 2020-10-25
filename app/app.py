from flask import Flask, render_template
import app.dataEuropa as dataEuropa
import app.dataPolska as dataPolska
from flask_charts import GoogleCharts, Chart

app = Flask(__name__)
charts = GoogleCharts(app)

@app.route('/')
def index():
    return render_template('index.html', the_title="Statystyki COVID-19: Strona Główna")

@app.route('/europa')
def tabelaEuropa():
    ranking_tablica= dataEuropa.getCountries()
    data = dataEuropa.getTime()
    return render_template('tabela.html', tab=ranking_tablica, time=data, the_title="Statystyki COVID-19 w Europie")


@app.route('/polska')
def tabelaPolska():
    ranking_polska, description = dataPolska.getWojewodztwa()
    return render_template('tabela-polska.html', tab=ranking_polska, the_title="Statystyki COVID-19 w Polsce", description=description)

@app.route('/wykresy')
def wykresy():
    return render_template('lista_wykresow.html', the_title="Lista wykresów")

@app.route('/o_nas')
def o_nas():
    return render_template('o_nas.html', the_title="O nas")

#My own number formater
@app.template_filter()
def numberFormat(value):
    if value == "Brak Danych":
        return "Brak Danych"
    return '{:,}'.format(value).replace(',', ' ')

#Modifed parsing string to int
def toInt(value):
    if isinstance(value, int):
        return value
    return 0

@app.route('/wykres')
def wykres():
    #Make declaration of chart
    my_chart = Chart("ColumnChart", "my_chart", options={ 'title': "Wykres nowych zakażeń COVID-19 w Europie", 'height': 400})
    my_chart.data.add_column("string", "Nazwa państwa")
    my_chart.data.add_column("number", "Ilość nowych zakażeń")
    #Get all countries except last 10 countries
    data = dataEuropa.getCountries()
    data = data[:-10]
    for country in data:
        data_for_country = []
        data_for_country.append(country.Name)
        if country.NewCases != "Brak Danych":
            data_for_country.append(country.NewCases)
        else:
            data_for_country.append(0)
        my_chart.data.add_row(data_for_country)
    return render_template("wykres.html", my_chart=my_chart, the_title="Wykres nowych zakażeń COVID-19 w Europie")

@app.route('/wykres2')
def wykres2():
    my_chart = Chart("ColumnChart", "my_chart", options={ 'title': "Wykres procentowy dziennego przyrostu zakażeń COVID-19 w Europie", 'height': 400})
    my_chart.data.add_column("string", "Nazwa państwa")
    my_chart.data.add_column("number", "Przyrost zakażeń (%)")
    data = dataEuropa.getCountries()
    for country in data:
        data_for_country = []
        data_for_country.append(country.Name)
        active_yesterday= toInt(country.TotalCases)-toInt(country.TotalDeaths)-toInt(country.TotalRecovered)
        change= toInt(country.NewCases)/active_yesterday
        change*=100
        data_for_country.append(change)
        my_chart.data.add_row(data_for_country)
    return render_template("wykres.html", my_chart=my_chart, the_title="Wykres procentowy dziennego przyrostu zakażeń COVID-19 w Europie")

@app.route('/wykres3')
def wykres3():
    my_chart = Chart("ColumnChart", "my_chart", options={ 'title': "Wykres procentowy zmiany aktywnych zakażeń COVID-19 w Europie", 'height': 400})
    my_chart.data.add_column("string", "Nazwa państwa")
    my_chart.data.add_column("number", "procentowy przyrost przypadków aktywnych")
    data = dataEuropa.getCountries()
    for country in data:
        data_for_country = []
        data_for_country.append(country.Name)
        active_yesterday=toInt(country.TotalCases)-toInt(country.TotalDeaths)-toInt(country.TotalRecovered)
        active_today=active_yesterday+toInt(country.NewCases)-toInt(country.NewDeaths)-toInt(country.NewRecovered)
        change=(active_today-active_yesterday)/active_yesterday
        change*=100
        data_for_country.append(change)
        my_chart.data.add_row(data_for_country)
    return render_template("wykres.html", my_chart=my_chart, the_title="Wykres procentowy zmiany aktywnych zakażeń COVID-19 w Europie")

@app.route('/wykres4')
def wykres4():
    #Make declaration of chart
    my_chart = Chart("ColumnChart", "my_chart", options={ 'title': "Wykres wszystkich zakażeń COVID-19 w Europie od początku epidemii", 'height': 400})
    my_chart.data.add_column("string", "Nazwa państwa")
    my_chart.data.add_column("number", "Ilość zakażeń")
    #Get all countries except last 10 countries
    data = dataEuropa.getCountries()
    data = data[:-10]
    for country in data:
        data_for_country = []
        data_for_country.append(country.Name)
        if country.TotalCases != "Brak Danych":
            data_for_country.append(country.TotalCases)
        else:
            data_for_country.append(0)
        my_chart.data.add_row(data_for_country)
    return render_template("wykres.html", my_chart=my_chart, the_title="Wykres wszystkich zakażeń COVID-19 w Europie od początku epidemii")
