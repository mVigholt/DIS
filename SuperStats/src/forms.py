from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from src.queries import get_user_by_user_name, get_manager_by_pk, get_customer_by_pk
from src.utils.choices import ClubChoices, PlayerChoices 
    
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


#class FilterProduceForm(FlaskForm):
#    category = SelectField('Category',
#                           choices=ProduceCategoryChoices.choices())
#    item = SelectField('Item',
#                       choices=ProduceItemChoices.choices())
#    variety = SelectField('Variety',
#                          choices=ProduceVarietyChoices.choices())
#    sold_by = StringField('Sold by')
#    price = FloatField('Price (lower than or equal to)',
#                       validators=[NumberRange(min=0, max=100)])
#
#    submit = SubmitField('Filter')

class SearchPlayerForm(FlaskForm):
    player_name = StringField('Player name')

    submit = SubmitField('Search')

class SearchClubForm(FlaskForm):
    club_name = StringField('Club name')

    submit = SubmitField('Search')

class GoalscorerForm(FlaskForm):
    club = SelectField('Club', choices=ClubChoices.choices())
    shirt_number = IntegerField('Shirt Number', validators=[DataRequired(), NumberRange(min=1, max=99)])
    player = SelectField('Player', choices=PlayerChoices.values())
    goals = IntegerField('Goals', validators=[DataRequired(), NumberRange(min=0, max=20)])

    
class AddMatchInfoForm(FlaskForm):
    home_team = SelectField('Home Team', choices=ClubChoices.values())
    away_team = SelectField('Away Team', choices=ClubChoices.values())
    home_team_goals = IntegerField('Home Goals', validators=[NumberRange(min=0, max=20)])
    away_team_goals = IntegerField('Away Goals', validators=[NumberRange(min=0, max=20)])
    goalscorers = FieldList(FormField(GoalscorerForm), min_entries=1)
    manager_pk = IntegerField('Manager', validators=[DataRequired()], render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add MatchInfo')

    def validate_manager_pk(self, field):
        manager = get_manager_by_pk(self.manager_pk.data)
        if manager is None:
            raise ValidationError("You need to be a manager to submit matchinfo!")

class DeleteMatchForm(FlaskForm):
    match_id = IntegerField('Match ID', validators=[DataRequired()])
    submit = SubmitField('Delete Match')

class BuyProduceForm(FlaskForm):
    submit = SubmitField('Yes, buy it')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You must be a customer in order to create orders.")


class RestockProduceForm(FlaskForm):
    submit = SubmitField('Yes, restock it')
