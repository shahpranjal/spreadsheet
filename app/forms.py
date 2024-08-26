from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BankCsvForm(FlaskForm):
    bank_name = StringField('Bank Name', validators=[DataRequired()])
    description_column = IntegerField('Description Column', validators=[DataRequired(), NumberRange(min=0)])
    date_column = IntegerField('Date Column', validators=[DataRequired(), NumberRange(min=0)])
    debit_column = IntegerField('Debit Column', validators=[DataRequired(), NumberRange(min=0)])
    credit_column = IntegerField('Credit Column', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save')
