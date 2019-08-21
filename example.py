from smspva import SMSpva
from smspva.countries import Country
from smspva.services import Service

# TODO: implement logging module

key = open("key").read()
client = SMSpva(key)
