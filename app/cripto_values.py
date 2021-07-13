import requests

class Crypto_report:

    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start' : '1',
            'limit' : '200',
            'convert' : 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '6f172a84-71dc-4852-bb5c-2b38b21c8e0f',
        }

        self.id = Crypto_report.params = {'start':'1','limit':'200','convert':'USD','sort':'market_cap'}

    def cmc(self):
        c = requests.get(url=self.url, headers=self.headers, params=self.id).json()
        return c

c_r = Crypto_report()

def btcValue():
    criptovalute = c_r.cmc()
    BTC = criptovalute["data"][0]["quote"]["USD"]["price"]
    return round(BTC,4)


