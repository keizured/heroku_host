from flask import Flask
from flask import send_file
from flask import render_template
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time


app = Flask(__name__)


links = {"Download" : "/download",
         "Pairplot" : "/pairplot",
         "Fair vs Pclass"  : "fair_vs_pclass",
         "PClass vs Sex" : "pclass_vs_sex",
         "Numeral_plot": "/num_plot"}

def render_index (image = None):
    return render_template("index.html", links=links, image = (image, image), code=time.time())


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", links=links, image=None)


@app.route('/download', methods=['GET'])
def download_data():
    return send_file("data/titanic_train.csv", as_attachment=True)


@app.route('/pairplot', methods=['GET'])
def pairplot():
    import seaborn as sns
    import pandas as pd
    data = pd.read_csv ("data/titanic_train.csv")
    sns_plot = sns.pairplot(data, hue="Survived")
    sns_plot.savefig("static/tmp/pairplot.png")
    return render_template("index.html", links=links, image = ("pairplot.png", "pairplot"))


@app.route('/pclass_vs_sex', methods=['GET'])
def pclass_vs_sex():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    data = pd.read_csv ("data/titanic_train.csv")
    result = {}
    for (cl, sex), sub_df in data.groupby(['Pclass', 'Sex']):
        result[f"{cl} {sex}"] = sub_df['Age'].mean()

    plt.bar (result.keys(), result.values())
    plt.savefig('static/tmp/pclass_vs_sex.png')
    return render_index ("pclass_vs_sex.png")


@app.route('/fair_vs_pclass', methods=['GET'])
def fair_vs_pclass():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    data = pd.read_csv ("data/titanic_train.csv")
    filtered_data = data.query('Fare < 200')
    sns.boxplot(x='Pclass', y='Fare', data=filtered_data, ax=ax)
    plt.savefig('static/tmp/fair_vs_pclass.png')

    return render_index ("fair_vs_pclass.png")

@app.route('/num_plot', methods=['GET'])
def numplot():
    from random import randint
    x = range(5)
    y = []
    for g in x:
        y.append(randint(0, 100))
    fig, ax = plt.subplots()
    plt.plot(x, y, 'o')
    plt.title('Title')
    plt.xlabel('X label')
    plt.ylabel('Y label')
    plt.savefig('static/tmp/numplot.png')
    return render_index('numplot.png')
