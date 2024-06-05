from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from src.forms import FilterProduceForm, AddProduceForm, BuyProduceForm, RestockProduceForm, SearchPlayerForm
from src.models import Produce as ProduceModel, ProduceOrder
from src.queries import insert_produce, get_produce_by_pk, Sell, \
    insert_sell, get_all_produce_by_manager, get_produce_by_filters, insert_produce_order, update_sell, \
    get_orders_by_customer_pk, get_player_by_name

Info = Blueprint('Produce', __name__)

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
def add_produce():
    form = AddProduceForm(data=dict(manager_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            produce_data = dict(
                category=form.category.data,
                item=form.item.data,
                variety=form.variety.data,
                unit=form.unit.data,
                price=form.price.data
            )
            produce = ProduceModel(produce_data)
            new_produce_pk = insert_produce(produce)
            sell = Sell(dict(manager_pk=current_user.pk, produce_pk=new_produce_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-match-info.html', form=form)


@Info.route("/clubs", methods=['GET', 'POST'])
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/clubs.html', orders=orders)