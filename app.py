import uuid
from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import UrlForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '803e5fabcb7a33a4ce79fa20466b3cae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), nullable=False)
    slug = db.Column(db.String(16), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    count = db.Column(db.Integer, default=0)
    last_clicked_on = db.Column(db.DateTime, nullable=True)



@app.route('/')
def home():
    links = Link.query.all()
    return render_template('home.html', links=links)


@app.route('/<slug>')
def handle_redirect(slug):
    link = Link.query.filter_by(slug=slug).first()
    if link:
        link.count = link.count + 1
        link.last_clicked_on = datetime.utcnow()
        db.session.commit()
        return redirect(link.url)
    else:
        flash('The short url doesn\'t exist', 'danger')
        return redirect(url_for('home'))


@app.route("/add_url", methods=['GET', 'POST'])
def add_url():
    form = UrlForm()
    if form.validate_on_submit():
        # create a unique slug
        while True:
            slug = uuid.uuid4().hex[:6]
            link = Link.query.filter_by(slug=slug).first()
            if not link:
                break

        # enter the data into database with count = 0
        link = Link(url=form.url.data, slug=slug, count=0)
        db.session.add(link)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('add_url.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)