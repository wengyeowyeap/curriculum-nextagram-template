import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from models.image import Image
from models.donation import Donation
from flask_login import login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3
import braintree
from instagram_web.util.braintree_helpers import generate_client_token, transact
from money.money import Money
from money.currency import Currency
import requests


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@donations_blueprint.route('/<id>/new', methods=['GET'])
@login_required
def new(id):
  image = Image.get_or_none(Image.id == id)
  client_token = generate_client_token()
  return render_template('donations/new.html', image = image, client_token = client_token)

@donations_blueprint.route('/', methods=['POST'])
@login_required
def create():
  amount = request.form["amount"]
  nonce_from_the_client = request.form["payment_method_nonce"]
  result = transact({
    "amount": amount,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
  })

  if result.is_success or result.transaction:
    flash('Donation Successful!')
    donated_image_id = request.form["donated_image"]
    m = Money(amount, Currency.USD)
    db_m = m.sub_units
    new_donation = Donation(user_id = current_user.id, image_id= donated_image_id, amount = db_m)

    if new_donation.save():
        send_donation_message()
        return redirect(url_for('donations.show', transaction_id=result.transaction.id))
    else:
        for error in new_donation.errors:
            flash(error, "danger")
        return redirect(url_for('donations.new'))
  else:
    for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
    return redirect(url_for('donations.new'))

@donations_blueprint.route('/show', methods=['GET'])
@login_required
def show():
  return render_template('donations/show.html')

def send_donation_message():
  return requests.post(
    "https://api.mailgun.net/v3/sandbox43f9a81e2806462b86a4ed1def365719.mailgun.org/messages",
    auth=("api", "84b58e87bd3a560b50a4ec9e14f0afbc-07e45e2a-be4abb61"),
    data={"from": "Nextagram <mailgun@sandbox43f9a81e2806462b86a4ed1def365719.mailgun.org>",
          "to": ["wengyeowyeap@gmail.com"],
          "subject": "You have received a donation!",
          "text": "Test"})