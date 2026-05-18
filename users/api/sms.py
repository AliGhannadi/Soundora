from kavenegar import *


def sms_message(receptor, code):
    message = f"Soundora Verifiction Code: {code}"

    api = KavenegarAPI("YOUR_API_KEY")
    params = {"sender": "2000660110", "receptor": receptor, "message": message}
    response = api.sms_send(params)
    print(response)