from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField, StringField, PasswordField, FileField, DateField, DateTimeField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Required, EqualTo


class RegisterForm(Form):
   
   full_name = TextField("Full Name*",[validators.Required("Name Required.")])

   dob  = DateTimeField('DOB', format='%d/%m/%y')

   phone_number = StringField("Phone*", validators=[validators.Required("Phone Number Required."), validators.Regexp('^[789]\d{9}$', message="Invalid Phone Number(Ignore Country Codes)."),
])
   email = TextField("Email*",[validators.Required("Email Required."),validators.Email("Invalid Email.")])

   passport = StringField("Passport*", validators=[validators.Required("Passport Number Required."), validators.Regexp('^(?!^0+$)[a-zA-Z0-9]{3,20}$', message="Invalid Phone Number(Ignore Country Codes)."),
])
   username = TextField("User Name*",[validators.Required("User Name Required."), validators.Regexp('^\w+$', message="Only Alpha-Numeric Characters Allowed.")])

   password = PasswordField("Password*",[validators.Required("Please enter your password.")])

   image_file = FileField('Upload Image*' )
   
   submit = SubmitField("Register")