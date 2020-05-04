import json
import stripe
import os
from urllib.parse import urlencode, parse_qsl

from flask import Flask, render_template, request, jsonify 
from airtable import Airtable

def empty_to_zero(value):
    return 0 if value == '' else value 

def create_line_items(request):
    # Precios

    if request.get('args', None):

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
        multiplicador1 = int(empty_to_zero(request.args.get('multiplicador1', 0)))
        multiplicador2 = int(empty_to_zero(request.args.get('multiplicador2', 0)))
        multiplicador3 = int(empty_to_zero(request.args.get('multiplicador3', 0)))
        multiplicador4 = int(empty_to_zero(request.args.get('multiplicador4', 0)))
        multiplicador5 = int(empty_to_zero(request.args.get('multiplicador5', 0)))
        gastos_envios = float(empty_to_zero(request.args.get('gastos_envios', 0)))
        precio_final = float(empty_to_zero(request.args.get('preciofinal', 0)))
        preciofinal1 = round(float(empty_to_zero(request.args.get('preciofinal1', 0)))/multiplicador1, 2) if multiplicador1 else 0
        preciofinal2 = round(float(empty_to_zero(request.args.get('preciofinal2', 0)))/multiplicador2, 2) if multiplicador2 else 0
        preciofinal3 = round(float(empty_to_zero(request.args.get('preciofinal3', 0)))/multiplicador3, 2) if multiplicador3 else 0
        preciofinal4 = round(float(empty_to_zero(request.args.get('preciofinal4', 0)))/multiplicador4, 2) if multiplicador4 else 0
        preciofinal5 = round(float(empty_to_zero(request.args.get('preciofinal5', 0)))/multiplicador5, 2) if multiplicador5 else 0

        name = request.args.get('nombre_consulta', '')
        protocolo = request.args.get('nombre_protocolo', '')

    else:

        nombreproducto1 = request.get('nombreproducto1', '')
        nombreproducto2 = request.get('nombreproducto2', '')
        nombreproducto3 = request.get('nombreproducto3', '')
        nombreproducto4 = request.get('nombreproducto4', '')
        nombreproducto5 = request.get('nombreproducto5', '')
        marcaproducto1 = request.get('marcaproducto1', '')
        marcaproducto2 = request.get('marcaproducto2', '')
        marcaproducto3 = request.get('marcaproducto3', '')
        marcaproducto4 = request.get('marcaproducto4', '')
        marcaproducto5 = request.get('marcaproducto5', '')
        multiplicador1 = int(empty_to_zero(request.get('multiplicador1', 0)))
        multiplicador2 = int(empty_to_zero(request.get('multiplicador2', 0)))
        multiplicador3 = int(empty_to_zero(request.get('multiplicador3', 0)))
        multiplicador4 = int(empty_to_zero(request.get('multiplicador4', 0)))
        multiplicador5 = int(empty_to_zero(request.get('multiplicador5', 0)))
        gastos_envios = float(empty_to_zero(request.get('gastos_envios', 0)))
        precio_final = float(empty_to_zero(request.get('preciofinal', 0)))
        preciofinal1 = round(float(empty_to_zero(request.get('preciofinal1', 0)))/multiplicador1, 2) if multiplicador1 else 0
        preciofinal2 = round(float(empty_to_zero(request.get('preciofinal2', 0)))/multiplicador2, 2) if multiplicador2 else 0
        preciofinal3 = round(float(empty_to_zero(request.get('preciofinal3', 0)))/multiplicador3, 2) if multiplicador3 else 0
        preciofinal4 = round(float(empty_to_zero(request.get('preciofinal4', 0)))/multiplicador4, 2) if multiplicador4 else 0
        preciofinal5 = round(float(empty_to_zero(request.get('preciofinal5', 0)))/multiplicador5, 2) if multiplicador5 else 0

        name = request.get('nombre_consulta', '')
        protocolo = request.get('nombre_protocolo', '')

    line_items = []
    total = 0

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
    if precio_final:
        total = round(precio_final+gastos_envios, 2) if gastos_envios else round(precio_final, 2)

    #total = round(sum([float(item['amount'])*float(item['quantity']) for item in line_items]), 2)
    return {'name': name, 'protocolo': protocolo, 'line_items': line_items, 'total': total}

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./staticfiles/templates")))
app = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
@app.route('/<string:short_url>')
@app.route('/<string:short_url>/')
def hello(short_url=None):
    
    domain_url = os.getenv('DOMAIN')

    if not short_url:
        # data = create_line_items(request)
        # total_lines = len(data['line_items'])
        return render_template('success.html', **locals())
    else: 
        try:
            air_base = os.getenv('AIR_TABLE_BASE')
            air_api_key = os.getenv('AIR_TABLE_API')
            air_table_name = os.getenv('AIR_PROTOCOLO_TABLE_NAME')
            at = Airtable(air_base, air_table_name, api_key=air_api_key)
            lookup_record = at.search('short_url', short_url)
            text_qs = lookup_record[0]['fields']['query_string']
            visits = int(lookup_record[0]['fields']['visits']) + 1 if lookup_record[0]['fields']['visits'] >= 0 else 0
            dict_qs = dict(parse_qsl(text_qs))
            data = create_line_items(dict_qs)
            total_lines = len(data['line_items'])
            view_counter = {'visits': visits}
            at.update(lookup_record[0]['id'], view_counter)


        except Exception as e:
            return jsonify(error=str(e)), 403

    return render_template('index.html', **locals())

@app.route('/success')
def success():
    return render_template('success.html', **locals())


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
    air_base = os.getenv('AIR_TABLE_BASE')
    air_api_key = os.getenv('AIR_TABLE_API')
    air_table_name = os.getenv('AIR_PROTOCOLO_TABLE_NAME')

    try:
        at = Airtable(air_base, air_table_name, api_key=air_api_key)
        new_record_content = dict(request.args)
        new_record_content['query_string'] = urlencode(request.args)
        new_record = at.insert(new_record_content)
        short_url = {'short_url': new_record['id'].split('rec')[1],
             'airtableID': new_record['id']}
        at.update(new_record['id'], short_url)

        return jsonify({'link_url': domain_url + '/' + short_url['short_url']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    if request.data:
        data = json.loads(request.data)
    else:
        data = create_line_items(request)

    line_items = data.pop('line_items', None)
    for item in line_items:
        item['amount'] = int(item['amount']*100)

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
            success_url=domain_url + "/success?session_id={CHECKOUT_SESSION_ID}", \
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