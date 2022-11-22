import json
import requests
import pickle

COOKIE_FILE = 'cookie.txt'


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


session = requests.Session()
# response = session.get('http://google.com')


headers = {
    "Content-Type": "application/json",
}

# payload = {
#     "jsonrpc": "2.0",
#     "method": "call",
#     "id": 0,
#     "params": {
#         "db": "**********",
#         "login": "********",
#         "password": "**************"
#     },
# }
# response = session.get("*****************/web/session/authenticate", data=json.dumps(payload),
#                        headers={"Content-Type": "application/json"})
#
# save_cookies(session.cookies, COOKIE_FILE)

# print(session.cookies.get_dict())

applicant_payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params":
        {
            "model": "ir.attachment",
            "fields": [],
            "domain": [["mimetype", "=", "application/pdf"]],
            "limit": 1
        }
}

# headers.update({"cookie": json.dumps({'session_id': 'ecc8ef53ec90f619b865edd7eff30219b268b352'})})


applicant = requests.get("*************/web/dataset/search_read", data=json.dumps(applicant_payload),
                         headers=headers, cookies=load_cookies(COOKIE_FILE))

# print(applicant.json())
