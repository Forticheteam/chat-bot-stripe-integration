import json
import stripe
import os

from flask import Flask, render_template, request, jsonify 

def create_line_items(request):
    # Precios
    preciofinal_1 = request.args.get('preciofinal_1', 0)
    preciofinal_2 = request.args.get('preciofinal_2', 0)
    preciofinal_3 = request.args.get('preciofinal_3', 0)
    preciofinal_4 = request.args.get('preciofinal_4', 0)
    preciofinal_5 = request.args.get('preciofinal_5', 0)
    nombreproducto_1 = request.args.get('nombreproducto_1', '')
    nombreproducto_2 = request.args.get('nombreproducto_2', '')
    nombreproducto_3 = request.args.get('nombreproducto_3', '')
    nombreproducto_4 = request.args.get('nombreproducto_4', '')
    nombreproducto_5 = request.args.get('nombreproducto_5', '')
    marcaproducto_1 = request.args.get('marcaproducto_1', '')
    marcaproducto_2 = request.args.get('marcaproducto_2', '')
    marcaproducto_3 = request.args.get('marcaproducto_3', '')
    marcaproducto_4 = request.args.get('marcaproducto_4', '')
    marcaproducto_5 = request.args.get('marcaproducto_5', '')
    multiplicador_1 = request.args.get('multiplicador_1', '')
    multiplicador_2 = request.args.get('multiplicador_2', '')
    multiplicador_3 = request.args.get('multiplicador_3', '')
    multiplicador_4 = request.args.get('multiplicador_4', '')
    multiplicador_5 = request.args.get('multiplicador_5', '')
    gastos_envios = request.args.get('gastos_envios', 0)

    name = request.args.get('name', '')
    protocolo = request.args.get('protocolo', '')

    line_items = []
    # line_items = [{'description': "Centrum",
    #                         'name': "Vitamina C",
    #                         'amount': 35,
    #                         'currency': 'eur',
    #                         'quantity': 2
    #                         },
    #                         {'description': "Centrum",
    #                         'name': "Vitamina C",
    #                         'amount': 35,
    #                         'currency': 'eur',
    #                         'quantity': 2
    #                         }]
    if preciofinal_1:
        line_items.append({'description': marcaproducto_1,
                            'name': nombreproducto_1,
                            'amount': preciofinal_1,
                            'currency': 'eur',
                            'quantity': multiplicador_1
                            })
    if preciofinal_2:
        line_items.append({'description': marcaproducto_2,
                            'name': nombreproducto_2,
                            'amount': preciofinal_2,
                            'currency': 'eur',
                            'quantity': multiplicador_2
                            })

    if preciofinal_3:
        line_items.append({'description': marcaproducto_3,
                            'name': nombreproducto_3,
                            'amount': preciofinal_3,
                            'currency': 'eur',
                            'quantity': multiplicador_3
                            })   

    if preciofinal_4:
        line_items.append({'description': marcaproducto_4,
                            'name': nombreproducto_4,
                            'amount': preciofinal_4,
                            'currency': 'eur',
                            'quantity': multiplicador_4
                            }) 

    if preciofinal_5:
        line_items.append({'description': marcaproducto_5,
                            'name': nombreproducto_5,
                            'amount': preciofinal_5,
                            'currency': 'eur',
                            'quantity': multiplicador_5
                            })

    if gastos_envios:
         line_items.append({'description': "Gastos de Envios",
                            'name': 'Envio',
                            'amount': gastos_envios,
                            'currency': 'eur',
                            'quantity': 1
                            })      
    total = 0
    total = sum([item['amount']*item['quantity'] for item in line_items])
        
    return {'name': name, 'protocolo': protocolo, 'line_items': line_items, 'total': total}

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./staticfiles/templates")))
app = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def hello():

    data = create_line_items(request)
    domain_url = os.getenv('DOMAIN')
    total_lines = len(data['line_items'])

    return render_template('index.html', **locals())

@app.route('/config', methods=['GET'])
def get_publishable_key():
    return jsonify({
      'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
      'basePrice': os.getenv('BASE_PRICE'),
      'currency': "eur"
    })


@app.route("/api/echo", methods=['POST'])
def create_share_link():
    return request.args


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    if request.data:
        data = json.loads(request.data)
    else:
        data = create_line_items(request)

    line_items = data.pop('line_items', None)
    for item in line_items:
        item['amount'] = int(item['amount'])*10

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
            line_items=line_items, \
            metadata=data, \
            payment_method_types=["card"], \
        )
        if request.data:
            return jsonify({'sessionId': checkout_session['id']})
        else:
            return jsonify({'linkinfo': domain_url + '/checkout-session?sessionId=' + checkout_session['id']})

    except Exception as e:
        return jsonify(error=str(e)), 403

# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    # return jsonify(checkout_session)
    return render_template("checkout.html", id=id)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)