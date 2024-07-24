from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap
import smtplib
import datetime
import os
import email_validator

EM_PWD = os.environ.get('NOREPLY_PWD')
EMAIL = os.environ.get('NOREPLY_EMAIL')
DEST_EMAIL = os.environ.get('PAPA_EMAIL')


class ContactForm(FlaskForm):
    name = StringField(label='', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    email = StringField(label='', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    phone = StringField(label='', validators=[DataRequired()], render_kw={'placeholder': 'Phone Number'})
    message = StringField(label='', validators=[DataRequired()], widget=TextArea(), render_kw={'placeholder': "Please type a detailed message."})
    submit = SubmitField(label='Submit')


app = Flask(__name__)
app.secret_key = "key"
Bootstrap(app)


def send_msg(name, email, phone, message):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(EMAIL, EM_PWD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=DEST_EMAIL,
            msg=f"Subject:PFR Message from {name.title()}\n\n"
                f"Name: {name.title()}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Message: {message}"
        )


@app.route('/', methods=['POST', 'GET'])
def index():
    year = datetime.date.today().year
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        data = request.form
        send_msg(data['name'], data['email'], data['phone'], data['message'])
        return render_template('contact.html'), {f'Refresh': f'3; url= {url_for("index")}'}
    else:
        return render_template('index.html', form=contact_form)
    return render_template('index.html', form=contact_form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
