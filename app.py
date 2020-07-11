from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from rdbms_ingestor.src.helper import update_conf, generate_message
######################
##### CONFIG ########
####################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecret'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "mikeamjadi20@gmail.com"
app.config['MAIL_PASSWORD'] = None
app._static_folder = "C:\\Users\mikea\Desktop\Developer\Projects\Work\RDBMS_WebApp\\rdbms_ingestor\static"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)



########################
###### MODELS #########
######################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

############################
##### FORMS ###############
#########################
# Defining a form that will be called later
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterRDBMSForm(FlaskForm):
    env_choices = [('dev', 'Development'),('tst', 'Test'), ('prd', 'Production')]
    environment = SelectField('Environment', validators=[DataRequired()],
                              choices=env_choices)
    server = StringField('Server', validators=[DataRequired()])
    database = StringField('Database', validators=[DataRequired()])
    schema = StringField('Schema', validators=[DataRequired()])
    reason = StringField('Reason')

    submit = SubmitField('Submit')

#########################
##### HELPER FUNCTIONS ##
########################

def send_email(to, subject, template, **kwargs):
    msg = Message("RDBMS Ingestor -" + subject,
                  sender="mikeamjadi20@gmail.com", recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

###################################
###### VIEW FUNCTIONS / ROUTES ###
#################################
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@app.route('/confirmation', methods=['GET'])
def confirmation():
    return render_template("confirmation.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    database = None
    form = RegisterRDBMSForm()
    if form.validate_on_submit():
        database = form.database.data
        environment = form.environment.data
        confdict = dict()
        for field, value in form.data.items():
            if field in ['csrf_token','submit']:
                continue
            confdict.update({field: value})

        update_conf(environment + "_" + database, confdict)

        # send_email("mikeamjadi20@gmail.com", 'New Data Source', 'mail/new_user', user=confdict)

        return redirect(url_for("confirmation"))
    return render_template('register_source.html', form=form, name=database)



## Will present the 404.html if user runs into 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=True)