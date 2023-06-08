from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from flask import jsonify, Blueprint, request
from sovaa.db import get_db
bp = Blueprint('paypal', __name__, url_prefix='/api/paypal')


def createPayment(self, paypalid, client, price, status):
    payment_db = get_db()
    payment_db.execute('INSERT INTO paypal (paypalid, client, price, status) VALUES (?, ?, ?, ?)',
                       (paypalid, client, price, status))
    payment_db.commit()

@bp.route('/', methods=['POST'])
def paypal():
    client = request.json.get('client')
    price = request.json.get('price')
    if not client or not price:
        return jsonify({'error': 'client and price are required'}), 400

    user_id = "AZrtKHauKdGTjaOXM3jyIVdf9c9Z6pl1Fchr743J0Mgb1m9az1jJ0iG7YBAOY6_6iQUkMcPBc1eR-uNe"
    user_secret = "ELKQSj377I-ObKMkakEf4hSXI_mWHRKCL6ObV_5SlhKzeRp35VufvP8j-XbZwYbhA9ENyamZmfewWNBN"

    environment = SandboxEnvironment(user_id=user_id, user_secret=user_secret)
    user = PayPalHttpClient(environment)

    from paypalcheckoutsdk.orders import OrdersCreateRequest
    from paypalhttp import HttpError
    req = OrdersCreateRequest()

    req.prefer('return=representation')

    req.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "price": {
                        "currency_code": "PLN",
                        "value": str(price)
                    }
                }
            ]
        }
    )

    try:
        # Call API with your client and get a response for your call
        response = user.execute(req)

        status = response.result.status
        paypalid = response.result.id
        createPayment(paypalid, client, price, status)
        return jsonify({'Status Code:': response.status_code, 'Status:': status, 'paypalid': paypalid})
    except HttpError as e:
        # Something went wrong server-side
        return jsonify({'status': e.status_code}), 501
    except Exception as e:  # Catch any other exceptions
        return jsonify({'error': str(e)}), 500