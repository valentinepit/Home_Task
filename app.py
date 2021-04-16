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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
