from flask import Flask, render_template, request
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
    # show readme in browser
    text = []
    host = request.host_url
    with open('README.md', 'r') as f:
        for line in f:
            line = line.replace('http://127.0.0.1:5000/', host)
            text.append(line)
    return render_template("about.html", title="Readme", text=text)


@app.route("/query;<value>")
def parser(value):
    '''
    get query from browser and calling constructor
    convert result to dictionary
    make a header of a table from dictionary keys
    '''
    value = value.replace('&', ' ')
    values = value.split('  ')
    items = []
    for item in values:
        items.append(item.split(';'))
    values = dict(items)
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


@app.errorhandler(404)
def not_found_error(error):
    home = request.host_url
    return render_template('404.html', home=home), 404


@app.errorhandler(500)
def internal_error(error):
    home = request.host_url
    db.session.rollback()
    return render_template('500.html', home=home), 500


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
