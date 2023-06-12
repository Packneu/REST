from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from flask import jsonify, Blueprint, request
from sovaa.db import get_db

bp = Blueprint('pay', __name__, url_prefix='/api/paypal')

def createOrder(paypalid, customer, price, status):
    payment_db = get_db()
    payment_db.execute('INSERT INTO paypal (paypalid, customer, price, status) VALUES (?, ?, ?, ?)',
                       (paypalid, customer, price, status))
    payment_db.commit()

@bp.route('/', methods=['POST'])
def payment():
    data = request.get_json()
    customer = data.get('username')
    price = data.get('price')
    if not customer or not price:
        return jsonify({'error': 'buyer and amount are required'}), 400

    client_id = "AZrtKHauKdGTjaOXM3jyIVdf9c9Z6pl1Fchr743J0Mgb1m9az1jJ0iG7YBAOY6_6iQUkMcPBc1eR-uNe"
    client_secret = "ELKQSj377I-ObKMkakEf4hSXI_mWHRKCL6ObV_5SlhKzeRp35VufvP8j-XbZwYbhA9ENyamZmfewWNBN"

    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)

    from paypalcheckoutsdk.orders import OrdersCreateRequest
    from paypalhttp import HttpError

    req = OrdersCreateRequest()

    req.prefer('return=representation')

    req.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(price)
                    }
                }
            ]
        }
    )

    try:
        response = client.execute(req)

        status = response.result.status
        paypalid = response.result.id
        createOrder(paypalid, customer, price, status)
        return jsonify({'Status Code:': response.status_code, 'Status:': response.result.status, 'paypalid': response.result.id })
    except HttpError as e:
        return jsonify({'status': e.status_code}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500


