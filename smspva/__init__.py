import requests
from urllib.parse import urlencode
from .smsrequest import SMSRequest
from .countries import Country
from .services import Service

class SMSpva:

    def __init__(self, api_key):
        self.api_key = api_key

    def _build_method_url(self, method, **kwargs):
        url = "http://smspva.com/priemnik.php?"
        params = {
            "metod": method,
            "apikey": self.api_key
        }
        if len(kwargs):
            params.update(kwargs)
        url += urlencode(params)
        return url

    def get_user_info(self):
        url = self._build_method_url("get_userinfo")
        data = requests.get(url).json()
        if data.get("response") == "1":
            del data["response"]
            data["balance"] = float(data["balance"])
            data["karma"] = int(data["karma"])
            return data
        else:
            raise RuntimeError("API response code indicates failure.")

    def get_name(self):
        info = self.get_user_info()
        return info.get("name")

    def get_karma(self):
        info = self.get_user_info()
        return info.get("karma")

    def get_balance(self):
        info = self.get_user_info()
        return info.get("balance")

    def get_price(self, service, country):
        params = {
            "service": service.value,
            "country": country.value
        }
        url = self._build_method_url("get_service_price", **params)
        data = requests.get(url).json()
        if data.get("response") == "1":
            return float(data["price"])
        else:
            raise RuntimeError("API response code indicates failure.")

    def get_count(self, service, country):
        params = {
            "service": service.value,
            "country": country.value
        }
        url = self._build_method_url("get_count_new", **params)
        data = requests.get(url).json()
        count = data.get("online")
        if count is not None:
            return count
        else:
            raise RuntimeError("API response missing expected value.")

    def get_cheapest_country(self, service, require_available = True):
        prices = dict()
        for country in Country:
            prices[country] = self.get_price(service, country)
        prices = sorted(prices.items(), key = lambda vk: vk[1])
        if require_available:
            for price in prices:
                count = self.get_count(service, price[0])
                if count:
                    return price[0]
            return None
        else:
            return prices[0][0] if len(prices) else None

    def request_sms(self, service, country):
        return SMSRequest(self, service, country)
