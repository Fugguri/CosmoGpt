import requests


class LavaService:
    def __init__(self) -> None:
        self.access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6QUpUQ1g0WV9rcEd3VW1QeUFCOWN4clRWd09RNE5ITmNQUzlWMmRSSXUwIn0.eyJleHAiOjE3MTA0MTY5MDYsImlhdCI6MTcwNzgyNDkwNiwianRpIjoiMDY1ZThiMjMtMGU1NC00OTNkLWJlMTQtZTgwZGRmZDg1MmRlIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXByb2QubGF2YXRvcC1wcm9kLnN2Yy5jbHVzdGVyLmxvY2FsL3JlYWxtcy9jb20iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYTczMTMzY2YtMDAxOS00OGM1LThlYzctOGIwOWI2Y2IwZDcwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibGF2YS1hYSIsInNlc3Npb25fc3RhdGUiOiI2MTE3Njc0ZS1hMjRkLTQ0OWEtYTY1Mi00ZTRjOWFlMzI3OGEiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLWNvbSJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI2MTE3Njc0ZS1hMjRkLTQ0OWEtYTY1Mi00ZTRjOWFlMzI3OGEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkZhcmlkYSBTYWxpa2hvdmEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhbmFpcmE3QG1haWwucnUiLCJnaXZlbl9uYW1lIjoiRmFyaWRhIFNhbGlraG92YSIsImVtYWlsIjoiYW5haXJhN0BtYWlsLnJ1In0.JG0ZAKt4IQBxw8ISCTEqRzJYYBRqen2g0DJhg6gPaBTD6AI0AtGums78T8aSX78zqCtnHB7rHRCXgWp6z4QP2PBC054S1eH88ay3njCrv1nIsxM9NRtD1gnoyPR2Nxx3oG9tvuq8FPjtP2GMErmI_cMam5L1N5z2gojPK_1QtEZfz_fxloPiY1k8259DXmdti_vaqHIjrKY0Y9zM2V06jsDYFLEbv2oYzIwixtImG7572t0hKPXp7DmbiUUA17NoJC7hRd8JnHbHhn-F_A9fKQKRW8yyaHssi_tRe-oWicCtwLFDER8WVw2qIduhjPfKkHy_2VVGMZGQ0ogyy8tdtw"
        self.invoice_url = 'https://gate.lava.top/api/v1/invoice'
        self.webhook_url = 'https://gate.lava.top/api/v1/webhooks'
        self.api_key = "CUWOsF4EVV9eZmUvvEnEgliObGUALbuZVbxmTWjmpsJK1CWFNUUbUVPPPvDB8UQ7"
        # "QIUh9roZ6emubnzY97nmuij5DPzry1Fi0UrUwPhkC3FKW3hGDT314KCWPlMHweXR"

    def get_invoice(self, email="Fygguri@icloud.com"):

        headers = {'Content-Type': 'application/json',
                   "X-Api-Key": self.api_key}
        data = {
            "email": email,
            "offerId": "03764fb7-793e-4a3d-9ba6-5a60c3254b2d",
            "currency": "USD",
            "buyerLanguage": "RU"
        }

        response = requests.post(
            url=self.invoice_url,
            headers=headers,
            json=data
        )
        print(response.json())
        return response.json()

    def set_webhook(self, url="https://tops-actively-lion.ngrok-free.app/"):
        data = {
            "url": url,
            "eventType": "recurrent_payment",
            "authConfig": {
                "authType": "api_key",
                "authValue": "49f2d6ae-7253-402c-a2de-ece59bf9cbd7"
            }
        }

        headers = {'Content-Type': 'application/json',
                   'Authorization': "Bearer " + self.access_token}

        response = requests.post(
            url=self.webhook_url,
            headers=headers,
            json=data
        )
        print(response.text)
        # /return response.json()

    def get_webhook(self, url="https://tops-actively-lion.ngrok-free.app"):
        headers = {'Content-Type': 'application/json',
                   'Authorization': "Bearer " + self.access_token}

        response = requests.get(
            url=self.webhook_url,
            headers=headers,
        )
        return response.json()


if __name__ == "__main__":

    lava = LavaService()
    {"id": "dfb54c1e-94a2-404b-86a0-0e15add904bb",
     "url": "https://tops-actively-lion.ngrok-free.app/", "eventType": "payment_result", "isActive": "true", "authType": "api_key", "createdAt": "2024-02-08T15:28:25.730089+02:00", "updatedAt": "2024-02-08T15:28:25.730089+02:00"}
    print(lava.set_webhook())
