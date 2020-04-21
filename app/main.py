import json
import stripe
import os
from urllib.parse import urlencode

from flask import Flask, render_template, request, jsonify 

def create_line_items(request):
    # Precios
    preciofinal1 = request.args.get('preciofinal1', 0)
    preciofinal2 = request.args.get('preciofinal2', 0)
    preciofinal3 = request.args.get('preciofinal3', 0)
    preciofinal4 = request.args.get('preciofinal4', 0)
    preciofinal5 = request.args.get('preciofinal5', 0)
    nombreproducto1 = request.args.get('nombreproducto1', '')
    nombreproducto2 = request.args.get('nombreproducto2', '')
    nombreproducto3 = request.args.get('nombreproducto3', '')
    nombreproducto4 = request.args.get('nombreproducto4', '')
    nombreproducto5 = request.args.get('nombreproducto5', '')
    marcaproducto1 = request.args.get('marcaproducto1', '')
    marcaproducto2 = request.args.get('marcaproducto2', '')
    marcaproducto3 = request.args.get('marcaproducto3', '')
    marcaproducto4 = request.args.get('marcaproducto4', '')
    marcaproducto5 = request.args.get('marcaproducto5', '')
    multiplicador1 = request.args.get('multiplicador1', '')
    multiplicador2 = request.args.get('multiplicador2', '')
    multiplicador3 = request.args.get('multiplicador3', '')
    multiplicador4 = request.args.get('multiplicador4', '')
    multiplicador5 = request.args.get('multiplicador5', '')
    gastos_envios = request.args.get('gastos_envios', 0)

    name = request.args.get('nombre_consulta', '')
    protocolo = request.args.get('nombre_protocolo', '')

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
    if preciofinal1:
        line_items.append({'description': marcaproducto1,
                            'name': nombreproducto1,
                            'amount': preciofinal1,
                            'currency': 'eur',
                            'quantity': multiplicador1
                            })
    if preciofinal2:
        line_items.append({'description': marcaproducto2,
                            'name': nombreproducto2,
                            'amount': preciofinal2,
                            'currency': 'eur',
                            'quantity': multiplicador2
                            })

    if preciofinal3:
        line_items.append({'description': marcaproducto3,
                            'name': nombreproducto3,
                            'amount': preciofinal3,
                            'currency': 'eur',
                            'quantity': multiplicador3
                            })   

    if preciofinal4:
        line_items.append({'description': marcaproducto4,
                            'name': nombreproducto4,
                            'amount': preciofinal4,
                            'currency': 'eur',
                            'quantity': multiplicador4
                            }) 

    if preciofinal5:
        line_items.append({'description': marcaproducto5,
                            'name': nombreproducto5,
                            'amount': preciofinal5,
                            'currency': 'eur',
                            'quantity': multiplicador5
                            })

    if gastos_envios:
         line_items.append({'description': "Gastos de Envios",
                            'name': 'Envio',
                            'amount': gastos_envios,
                            'currency': 'eur',
                            'quantity': 1
                            })      
    total = 0
    total = sum([float(item['amount'])*float(item['quantity']) for item in line_items])
        
    return {'name': name, 'protocolo': protocolo, 'line_items': line_items, 'total': total, 'query_string': urlencode(line_items)}

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


@app.route("/create-link", methods=['POST'])
def create_link():
    domain_url = os.getenv('DOMAIN')
    data = create_line_items(request)
    return jsonify({'link_url': domain_url + '?' + data['id']})


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    if request.data:
        data = json.loads(request.data)
    else:
        data = create_line_items(request)

    line_items = data.pop('line_items', None)
    for item in line_items:
        item['amount'] = int(item['amount']*10)

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