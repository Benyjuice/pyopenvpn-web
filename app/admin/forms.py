from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,48)])
    password = StringField('Password' ,validators=[DataRequired(), Length(4)])
    #role_id = IntegerField('Role ID', validators=[DataRequired()])
    submit = SubmitField('Add')
