from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from config import Config
import Flask_2 as alchemy


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app


app = create_app()
with app.app_context():
    db = SQLAlchemy(app)
migrate = Migrate(app, db)

columns = ['id', 'date', 'channel', 'country', 'os', 'impressions', 'clicks',
           'installs', 'installs', 'spend', 'revenue']


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    channel = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    os = db.Column(db.Enum('ios', 'android', name='os'))
    impressions = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)
    installs = db.Column(db.Integer, nullable=False)
    spend = db.Column(db.Float, nullable=False)
    revenue = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"- {self.date} {self.channel} {self.country} {self.os}, {self.impressions}, {self.clicks}"


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/")
def register():
    text = []
    with open('README.md', 'r') as f:
        for line in f:
            text.append(line)
    return render_template("about.html", title="Readme", text=text)


@app.route("/query;<value>")
def parser(value):
    value = value.replace('&', ' ')
    values = value.split('  ')
    items = []
    for item in values:
        items.append(item.split(';'))
    values = dict(items)
    print(f'values = {values}')
    query_result = alchemy.main_constructor(values)
    result = [u._asdict() for u in query_result]
    try:
        head = result[0].keys()
    except:
        head = []
    res = []
    for item in result:
        res.append({v: k for k, v in item.items()})
    return render_template("index.html", title="Result", items=res, head=head)

@app.route("/sort/date=<date>")
def sort(date):
    # Show the number of impressions and clicks that occurred before
    # the date, broken down by channel and country, sorted by clicks in descending order
    head = ['channel', 'country', 'impressions', 'clicks']
    query = db.session.query(Dataset.channel, Dataset.country, func.sum(Dataset.impressions).label('impressions'),
                             func.sum(Dataset.clicks).label('clicks')).filter(Dataset.date < date) \
        .group_by(Dataset.channel, Dataset.country)
    try:
        request = query.all()
        result = sorted(request, key=lambda x: x[3], reverse=True)
    except:
        result = ["No data found"]

    return render_template("index.html", title="Result", items=result, head=head)


@app.route("/sort_1/os=<os>")
def sort_1(os):
    # Show the number of installs that occurred in May of 2017 on iOS, broken down by date,
    # sorted by date in ascending order
    head = ['os', 'date', 'installs']
    query = db.session.query(Dataset.os, Dataset.date, func.sum(Dataset.installs).label('installs')) \
        .filter(Dataset.os == os).filter(Dataset.date >= '2017-05-01') \
        .filter(Dataset.date <= '2017-05-31').group_by(Dataset.date, Dataset.os) \
        .order_by(Dataset.date)
    try:
        result = query.all()

    except:
        result = ["No data found"]
    return render_template("index.html", title="Result", items=result, head=head)


@app.route("/sort_2/country=<country>&date=<date>")
def sort_2(country, date):
    # Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by
    # revenue in descending order.
    # ..sort_2/country=Your_country&date=Your_date
    head = ['os', 'country', 'revenue']
    query = db.session.query(Dataset.os, Dataset.country, func.sum(Dataset.revenue).label('revenue')) \
        .filter(Dataset.date <= date) \
        .filter(Dataset.country == country) \
        .group_by(Dataset.os, Dataset.country)
    try:
        result = query.all()
    except:
        result = ["No data found"]
    return render_template("index.html", title="Result", items=result, head=head)


@app.route("/sort_3/country=<country>")
def sort_3(country):
    # Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.
    # Please think carefully which is an appropriate aggregate function for CPI.
    # ..sort_3/country=Your_country
    head = ['channel', 'country', 'CPI']
    query = db.session.query(Dataset.channel, Dataset.country,
                             func.sum(Dataset.revenue / Dataset.installs).label('CPI')) \
        .filter(Dataset.country == country) \
        .group_by(Dataset.channel, Dataset.country)
    try:
        request = query.all()
        result = sorted(request, key=lambda x: x[2], reverse=True)
    except:
        result = ["No data found"]
    print(result)
    return render_template("index.html", title="Result", items=result, head=head)

'''
@app.route("/filter/<value>")
def filter_by(value):
    # filter by time range (date_from+date_to is enough), channels, countries, operating systems
    if 'date' in value:
        value = value[4:]
        dates = value.split('+')
        date_from = dates[0]
        date_to = dates[1]
        result, head = sort_by(Dataset.date, date_from, date_to)
    elif 'channel' in value:
        channel = value[8:]
        result, head = sort_by(Dataset.channel, channel)
    elif 'country' in value:
        country = value[8:]
        result, head = sort_by(Dataset, country)
    elif 'os' in value:
        os = value[3:]
        result, head = sort_by(Dataset.os, os)

    return render_template("index.html", title="Result", items=result, head=head)


@app.route("/group/<value>")
def group_by(value):
    # group by one or more columns: date, channel, country, operating system
    if 'date' in value:
        result, head = group(Dataset.date)
    elif 'channel' in value:
        result, head = group(Dataset.channel)
    elif 'country' in value:
        result, head = group(Dataset.country)
    elif 'os' in value:
        result, head = group(Dataset.os)

    return render_template("index.html", title="Result", items=result, head=head)


@app.route("/order/<value>")
def order_by(value):
    # group by one or more columns: date, channel, country, operating system
    if 'date' in value:
        result, head = order(Dataset.date)
    elif 'channel' in value:
        result, head = order(Dataset.channel)
    elif 'country' in value:
        result, head = country_order(Dataset.country)
    elif 'os' in value:
        result, head = order(Dataset.os)
    elif 'impressions' in value:
        result, head = order(Dataset.impressions)
    elif 'clicks' in value:
        result, head = order(Dataset.clicks)
    elif 'installs' in value:
        result, head = order(Dataset.installs)
    elif 'spend' in value:
        result, head = order(Dataset.spend)
    elif 'revenue' in value:
        result, head = order(Dataset.revenue)



    return render_template("index.html", title="Result", items=result, head=head)


def order(col):
    query = db.session.query(Dataset).order_by(col)
    print(query)
    # try:
    result = query.all()
    # except:
    # result = ["No data found"]

    return get_res_head(result)


def group(col):
    query = db.session.query(Dataset).group_by(col, Dataset.id)
    try:
        result = query.all()
        # need to order_by date
    except:
        result = ["No data found"]

    return get_res_head(result)


def sort_by(col, arg_1, arg_2=None):
    if arg_2:
        query = db.session.query(Dataset).filter(col >= arg_1) \
            .filter(col <= arg_2)
    else:
        query = db.session.query(Dataset).filter(col == arg_1)
    try:
        result = query.all()
    except:
        result = ["No data found"]

    return get_res_head(result)


def get_res_head(result):
    # transform result to dictionary excluding 'id' and '_sa_instance_state'
    result_dic = [row.__dict__ for row in result]
    for i in result_dic:
        try:
            i.pop('_sa_instance_state')
        except ValueError as e:
            print(e)
        try:
            i.pop('id')
        except ValueError as e:
            print(e)
    head = result_dic[0].keys()
    result = []
    for item in result_dic:
        result.append({v: k for k, v in item.items()})
    return result, head


def main():
    app.run(debug=True)
'''

if __name__ == '__main__':
    app.run(debug=True)
