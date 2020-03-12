import json
import stripe
import os

from flask import Flask, render_template, request, jsonify 

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./staticfiles")))
app = Flask(__name__, static_folder=static_dir, template_folder=static_dir)

@app.route("/")
def hello():
    return "Working for you... On Development!"

@app.route("/api/echo", methods=['POST'])
def create_share_link():
    return request.args

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():


    name = request.args.get('name', '')
    brand = request.args.get('brand', '')
    original_price = request.args.get('original_price', '')
    username = request.args.get('username', '')
    discounted_price = request.args.get('discounted_price', '')
    specific_naming = request.args.get('specific_naming', '')

    domain_url = os.getenv('DOMAIN')

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "/success.html?session_id={CHECKOUT_SESSION_ID}", \
            cancel_url=domain_url + "/canceled.html", \
            metadata = {'name': name, 'brand': brand, 'original_price': original_price, 'username': username, 'specific_naming': specific_naming}, \
            payment_method_types=["card"], \
            line_items=[
                {
                    "name": name,
                    "images": ["https://picsum.photos/300/300?random=4"],
                    "quantity": 1,
                    "currency": "eur",
                    "amount": discounted_price
                }
            ]
        )
        return jsonify({'linkinfo': domain_url + '/checkout_session?sessionId=' + checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403

# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)