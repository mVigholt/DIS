from flask import render_template, request, Blueprint , flash , redirect
from flask_login import login_required, current_user

from src.forms import AddMatchInfoForm, ManagerLoginForm, UserSignupForm, SearchPlayerForm
from src.models import Produce as ProduceModel, ProduceOrder , Match , MatchInfo
from src.queries import insert_produce, get_produce_by_pk, Sell, insert_manager , insert_match , insert_match_info,\
    insert_sell, get_all_produce_by_manager, get_produce_by_filters, insert_produce_order, update_sell, \
    get_orders_by_customer_pk, get_player_by_name

Info = Blueprint('Produce', __name__)

class PrimaryKeyGenerator:
    def __init__(self):
        self.last_pk = 0
    
    def generate_unique_pk(self):
        self.last_pk += 1
        return self.last_pk
    
pkg = PrimaryKeyGenerator()

@Info.route("/players", methods=['GET', 'POST'])
def players():
    form = SearchPlayerForm()
    title = 'All players!'
    players = []
    if request.method == 'POST':
        players = get_player_by_name(player_name=request.form.get('player_name'))
        title = f'Searching for playes...!'
    return render_template('pages/players.html', players=players, form=form, title=title)


@Info.route("/add-match-info", methods=['GET', 'POST'])
@login_required
def add_match_info():

    form = AddMatchInfoForm(data=dict(manager_pk=current_user.pk))
    if request.method == 'POST':
        #make unique key munaly beacause other tgins dont work apparently
        
        unique_pk = pkg.generate_unique_pk()
        #if form.validate_on_submit():   #THIS IS ALWAYS FALSE IDK WHY
        if True:
            # Generate a unique primary key for the match

            # Create a Match object
            match_data = {
                'match_id' : unique_pk , 
                'home_team_name': form.home_team.data,
                'away_team_name': form.away_team.data ,
                'home_team_goals' : form.home_team_goals.data , 
                'away_team_goals' : form.away_team_goals.data
            }
            match = Match(match_data)

            match_pk = insert_match(match)
            

            # Process and save match info
            for goalscorer_form in form.goalscorers:
                match_info_data = {
                    'match_id': unique_pk,
                    'shirt_number': goalscorer_form.shirt_number.data,
                    'club_name': goalscorer_form.club.data,
                    'goals_scored': goalscorer_form.goals.data
                }
                match_info = MatchInfo(match_info_data)
                insert_match_info(match_info)

            
            flash('Morm submitted successfully!', 'success')
            
            #return redirect('pages/add-match-info.html')

    return render_template('pages/add-match-info.html', form=form)


@Info.route("/clubs", methods=['GET', 'POST'])
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/clubs.html', orders=orders)