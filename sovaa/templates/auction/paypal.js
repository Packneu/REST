import { currentUserInit } from "./modules/currentUserInit";
window.addEventListener("DOMContentLoaded", () => {
    "use strict";

    currentUserInit("pay");
    const payButton = document.getElementById("pay");
    const amount = JSON.parse(localStorage.getItem("amount"));
    const name = localStorage.getItem("user_name");

    paypal.Buttons({
        // Order is created on the server and the order id is returned
        // cretaeOrder - это просто создание чека в payPal, Paypal ждет именно onApprove() - чтобы снять деньги
        // Это создание чека, payPal создает чек, где onApprove() - это когда пользователь нажимает на кнопку Complete Purchase - это этот метод срабатывает и дальше Егор запрашивает у payPal на снятии платежа
        createOrder() {
        console.info()
          return fetch(window.env.host + "/api/paypal/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            // use the "body" param to optionally pass additional order information
            // like product skus and quantities
            body: JSON.stringify({
                buyer: name,
                amount,
                sku: "YOUR_PRODUCT_STOCK_KEEPING_UNIT",
                quantity: "YOUR_PRODUCT_QUANTITY",
            }),
          })
          .then((response) => response.json())
          .then((order) => {
            localStorage.removeItem('payment_id');
            localStorage.setItem('payment_id', order.id);
            return order.token
          });
        },
        // Finalize the transaction on the server after payer approval
        // Логика работы платежки
        // Пользователь нажимает на желтую кнопку --> срабатывает createOrder() --> Далее отправляется Егору данные --> Егор создает запрос pay() и отправляет данные на payPal, срабатывает payment.create() у Егора --> Егор отправляет мне это {'id': token, 'link': redirect_url, 'state': payment.state} --> в then ждет {'id': token, 'link': redirect_url, 'state': payment.state} и возвращает только order.token, чтобы скрипт payPal понял, что нужно открыть окошко для введении данных (все, платежка на payPal создана и payPal ждет сигнал от Егора, что можно вытаскивать деньги, но у payPal нет данных у кого брать деньги, для этого Егор и ждет метод onApprove() - это и означает, что пользователь нажал на кнопку Complete purchase - это сигнал Егору, и Егор получает данные карточки и отправляет payPal и payPal вытаскивает деньги с карточки) --> Далее у Егора срабатывается @bp.route('/success', methods=['GET','POST']) и метод succes (по сути открывается портал success и он принимает метод GET и POST), и он ждет от пользователя, чтобы пользователь нажал на кнопку Complete purchase, после того как пользователь нажал на эту кнопку срабатывает onApprove(data) и отправляется данные (можешь увидеть data в Network --> слева снизу в табличке будет ссылка success --> Payload, там есть объект Data, по этому объекту и ориентируется Егор для отправки данных на payPal, чтобы сказать payPal, что можно вытащить такую сумму из этой карточки), чтобы Егор мог отправить запрос на payPal что деньги можно снять по данным который я отправил Егору.  
        // Далее у Егора срабатывается     
        // if payment.execute({'payer_id': data['payerID']}):
        // paypal.createPayment(buyer, amount, status='success')
        // return jsonify({'message': 'Success'}) 
        // и мне возвращается {'message': 'Success'}
        onApprove(data) {
          return fetch(window.env.host + "/api/paypal/success", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              data: data
            })
          })
          .then((response) => response.json())
          .then((orderData) => {
            // Successful capture! For dev/demo purposes:
//            console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
//            const transaction = orderData.purchase_units[0].payments.captures[0];
//            alert(`Transaction ${transaction.status}: ${transaction.id}\n\nSee console for all available details`);
            // When ready to go live, remove the alert and show a success message within this page. For example:
             const element = document.getElementById('paypal-pay-button-alert');
             element.innerHTML = '<h3>Thank you for your payment!</h3>';
            // Or go to another URL:  window.location.href = 'thank_you.html';
          });
        },
        onCancel: function (data) {
            // Show a cancel page or return to cart
            data.payment_id = localStorage.getItem('payment_id')

            fetch(window.env.host + "/api/paypal/cancel", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
              })
              .then((response) => response.json())
              .then((orderData) => {alert('payment cancel')})
        },
        onError: function (err) {
            console.info(err)
        }
      }).render('#paypal-pay-button');
})