from smspva import SMSpva
from smspva.countries import Country
from smspva.services import Service

# TODO: implement logging module

key = open("key").read()
client = SMSpva(key)

# relatively complete example
service = Service.MS_BING_HOTMAIL
country = client.get_cheapest_country(service)
if country is not None:
    request = client.request_sms(service, country)
    request.send()
    print(request.full_number)
    print(request.run())
else:
    print("service not available.")
