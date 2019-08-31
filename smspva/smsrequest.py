import requests
import time

class SMSRequest:

    sent = False

    def __init__(self, client, service, country):
        self.client = client
        self.service = service
        self.country = country

    def send(self):
        params = {
            "service": self.service.value,
            "country": self.country.value
        }
        url = self.client._build_method_url("get_number", **params)
        data = requests.get(url).json()
        if data.get("response") == "1":
            self.sent = True
            self.created = time.time()
            self.id = int(data["id"])
            self.number = data["number"]
            self.country_code = data["CountryCode"]
            self.full_number = "{}{}".format(self.country_code, self.number)
        else:
            raise RuntimeError("API response code indicates failure.")

    def get_code(self):
        params = {
            "id": self.id,
            #"country": self.country.value,
            "service": self.service.value
        }
        url = self.client._build_method_url("get_sms", **params)
        data = requests.get(url).json()
        response = data.get("response")
        if response == "2":
            # still pending
            return False
        elif response == "1":
            # successful
            return data["sms"]
        else:
            # something's wrong
            raise RuntimeError("API Response code indicates failure.")

    def ban(self):
        url = self.client._build_method_url("ban", id = self.id, service = self.service.value)
        data = requests.get(url).json()
        if data.get("response") != "1":
            raise RuntimeError("API Response code indicates failure.")

    def run(self):
        autoban = (10 * 60) - 30
        while self.time_elapsed < autoban:
            code = self.get_code()
            if code:
                return code
            else:
                time.sleep(20)
        self.ban()

    @property
    def time_elapsed(self):
        return -1 if not self.sent else time.time() - self.created
