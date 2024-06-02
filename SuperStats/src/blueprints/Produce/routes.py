from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from src.forms import FilterProduceForm, AddProduceForm, BuyProduceForm, RestockProduceForm
from src.models import Produce as ProduceModel, ProduceOrder
from src.queries import insert_produce, get_produce_by_pk, Sell, \
    insert_sell, get_all_produce_by_farmer, get_produce_by_filters, insert_produce_order, update_sell, \
    get_orders_by_customer_pk

Produce = Blueprint('Produce', __name__)


@Produce.route("/produce", methods=['GET', 'POST'])
def produce():
    form = FilterProduceForm()
    title = 'Our produce!'
    produce = []
    if request.method == 'POST':
        produce = get_produce_by_filters(category=request.form.get('category'),
                                         item=request.form.get('item'),
                                         variety=request.form.get('variety'),
                                         farmer_name=request.form.get('sold_by'),
                                         price=request.form.get('price'))
        title = f'Our {request.form.get("category")}!'
    return render_template('pages/produce.html', produce=produce, form=form, title=title)


@Produce.route("/add-produce", methods=['GET', 'POST'])
@login_required
def add_produce():
    form = AddProduceForm(data=dict(farmer_pk=current_user.pk))
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
            sell = Sell(dict(farmer_pk=current_user.pk, produce_pk=new_produce_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-produce.html', form=form)


@Produce.route("/your-produce", methods=['GET', 'POST'])
@login_required
def your_produce():
    form = FilterProduceForm()
    produce = []
    if request.method == 'GET':
        produce = get_all_produce_by_farmer(current_user.pk)
    if request.method == 'POST':
        produce = get_produce_by_filters(category=request.form.get('category'),
                                         item=request.form.get('item'),
                                         variety=request.form.get('variety'),
                                         farmer_pk=current_user.pk)
    return render_template('pages/your-produce.html', form=form, produce=produce)


@Produce.route('/produce/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_produce(pk):
    form = BuyProduceForm()
    produce = get_produce_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = ProduceOrder(dict(produce_pk=produce.pk,
                                      farmer_pk=produce.farmer_pk,
                                      customer_pk=current_user.pk))
            insert_produce_order(order)
            update_sell(available=False,
                        produce_pk=produce.pk,
                        farmer_pk=produce.farmer_pk)
    return render_template('pages/buy-produce.html', form=form, produce=produce)


@Produce.route('/produce/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_produce(pk):
    form = RestockProduceForm()
    produce = get_produce_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        produce_pk=produce.pk,
                        farmer_pk=produce.farmer_pk)
    return render_template('pages/restock-produce.html', form=form, produce=produce)


@Produce.route('/produce/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)