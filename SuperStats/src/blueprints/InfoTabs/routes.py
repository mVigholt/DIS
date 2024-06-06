from flask import render_template, request, Blueprint , flash , redirect
from flask_login import login_required, current_user

from src.forms import AddMatchInfoForm, ManagerLoginForm, UserSignupForm, SearchPlayerForm, SearchClubForm , DeleteMatchForm
from src.models import Match , MatchInfo , DeleteMatchInfo
from src.queries import insert_manager , insert_match , insert_match_info,\
     get_player_by_name, get_club_by_name , delete_match_by_id , update_club_stats , update_player_stats, get_all_clubs_sorted_by_points

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
    title = 'Player info'
    players = []
    if request.method == 'POST':
        players = get_player_by_name(player_name=request.form.get('player_name'))
        title = f'Searching for playes...!'
    return render_template('pages/players.html', players=players, form=form, title=title)


@Info.route("/league-table", methods=['GET', 'POST'])
def league_table():
    clubs = get_all_clubs_sorted_by_points()
    return render_template('pages/league-table.html', clubs=clubs)


@Info.route("/clubs", methods=['GET', 'POST'])
def clubs():
    form = SearchClubForm()
    title = 'Club info'
    clubs = []
    if request.method == 'POST':
        clubs = get_club_by_name(club_name=request.form.get('club_name'))
        title = f'Searching for clubs...!'
    return render_template('pages/clubs.html', clubs=clubs, form=form, title=title)


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

            update_club_stats()
            update_player_stats()
            
            flash('Morm submitted successfully!', 'success')
            
            #return redirect('pages/add-match-info.html')

    return render_template('pages/add-match-info.html', form=form)


@Info.route("/delete-match", methods=['GET', 'POST'])
@login_required
def delete_match():

    form = DeleteMatchForm()
    if request.method == 'POST':
        if form.validate_on_submit():  # Check if form validation passes
            match_id = form.match_id.data
            match_delete = DeleteMatchInfo(match_id)

            # Assuming you have a function to delete the match by match_id
            delete_match_by_id(match_delete)
            
            update_club_stats()
            update_player_stats()
            flash('Match deleted successfully!', 'success')


    return render_template('pages/delete-match.html', form=form)


