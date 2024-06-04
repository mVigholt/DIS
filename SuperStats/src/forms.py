from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from src.queries import get_user_by_user_name, get_manager_by_pk, get_customer_by_pk
from src.utils.choices import ProduceItemChoices, ProduceCategoryChoices, ClubChoices, \
    ProduceVarietyChoices, ProduceUnitChoices
#UserTypeChoices

class ManagerLoginForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))
    club_name = SelectField('Club name',
                            validators=[DataRequired()],
                            choices=ClubChoices.values())
    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')


class FilterProduceForm(FlaskForm):
    category = SelectField('Category',
                           choices=ProduceCategoryChoices.choices())
    item = SelectField('Item',
                       choices=ProduceItemChoices.choices())
    variety = SelectField('Variety',
                          choices=ProduceVarietyChoices.choices())
    sold_by = StringField('Sold by')
    price = FloatField('Price (lower than or equal to)',
                       validators=[NumberRange(min=0, max=100)])

    submit = SubmitField('Filter')

class SearchPlayerForm(FlaskForm):
    player_name = StringField('Player name')

    submit = SubmitField('Search')


class AddProduceForm(FlaskForm):
    category = SelectField('Category',
                           validators=[DataRequired()],
                           choices=ProduceCategoryChoices.choices())
    item = SelectField('Item (Subcategory)',
                       validators=[DataRequired()],
                       choices=ProduceItemChoices.choices())
    variety = SelectField('Variety',
                          validators=[DataRequired()],
                          choices=ProduceVarietyChoices.choices())
    unit = SelectField('Unit',
                       validators=[DataRequired()],
                       choices=ProduceUnitChoices.choices())
    price = IntegerField('Price',
                         validators=[DataRequired(), NumberRange(min=0, max=100)])
    manager_pk = IntegerField('Manager',
                             validators=[DataRequired()],
                             render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add produce')

    def validate_price(self, field):
        manager = get_manager_by_pk(self.manager_pk.data)
        if manager is None:
            raise ValidationError("You need to be a farmer to sell produce!")


class BuyProduceForm(FlaskForm):
    submit = SubmitField('Yes, buy it')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You must be a customer in order to create orders.")


class RestockProduceForm(FlaskForm):
    submit = SubmitField('Yes, restock it')
