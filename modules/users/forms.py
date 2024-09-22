from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional
from modules.models import User

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=40)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=40)])
    firm = StringField('Firm', validators=[DataRequired(), Length(min=1, max=40)])
    role = StringField('Role', validators=[DataRequired(), Length(min=1, max=40)])


    submit = SubmitField('Register')

    def populate(self, user: User):
        self.email.data = user.email
        self.fname.data = user.first_name
        self.lname.data = user.last_name
        self.firm.data = user.firm.firm_name
        self.role.data = user.role

