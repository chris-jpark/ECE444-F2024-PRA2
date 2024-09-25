from flask import Flask, render_template, session, redirect, url_for, flash
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, ValidationError



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('Enter your utoronto email address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # Custom validator to ensure the email ends with '.edu'
    # def validate_email(self, email):
    #     if not email.data.contains('utoronto'):
    #         raise ValidationError('Email address must contain utoronto')

@app.route('/', methods=['GET', 'POST'])
def index():
    name_form = NameForm()
    if name_form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != name_form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = name_form.name.data
        # return redirect(url_for('index'))

        old_email = session.get('email')
        if old_email is not None and old_email != name_form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = name_form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', name_form=name_form, name=session.get('name'), email=session.get('email'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.now(timezone.utc))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500