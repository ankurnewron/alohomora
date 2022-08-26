# Step 1.  Get user,device,verification code/id.

import os
import requests
import time
import webbrowser

class Auth0():
    auth0url = "https://dev-pg1h84k1.us.auth0.com"
    url = auth0url + '/oauth/device/code'
    clientId = os.environ("CLIENT_ID")
    audience = "https://grpc-api-gateway-d8q71ttn.uc.gateway.dev/"
    clientCredentials = {"client_id": clientId , "scope" : "openid email profile newron-server" , "audience" : audience}

    def __init__(self) -> None:
        pass
    
    def authenticate(self):
        x = requests.post(self.url, json = self.clientCredentials)
        if x.status_code != 200:
            print("Error in verification: " + str(x.status_code))
            print(x.text)
            exit()
        resp = x.json()
        print("\n\n************************************************************\n\n")
        print("Please verify the following code on the device: " + str(resp['user_code']))
        print("\n\n************************************************************\n\n")
        time.sleep(2)
        # Step 2: Open Webbrowser
        webbrowser.open(resp["verification_uri_complete"])
        # Step 3: Poll for token
        pollUrl = self.auth0url + "/oauth/token"
        pollObj = { 
            "client_id": self.clientId,
            "device_code": resp["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        maxPolls = 60
        op = requests.post(pollUrl, json = pollObj)
        opJson = op.json()
        # print(op.text)
        # print(op.status_code)
        while op.status_code != 200 and maxPolls > 0:
            op = requests.post(pollUrl, json = pollObj)
            opJson = op.json()
            maxPolls -= 1
            if op.status_code == 200:
                print("Authorization Successful")
                print(op.text)
                break;
            if op.status_code == 400 or op.status_code == 401:
                print("Authorization Failed")
                print(op.text)
                exit();
            if opJson["error"] == "invalid_grant":
                print("Authorization Failed")
                break;
            if opJson["error"] == "authorization_pending":
                print("Authorization Pending")
                time.sleep(2)
            elif opJson["error"] == "slow_down":
                print("Slow Down")
                time.sleep(8)
            else:
                time.sleep(10)
                break
        if(op.status_code != 200 or maxPolls == 0):
            # print("Error: " + op.text)
            exit()
        return op.text

# Step 4: Get access token
#  use access token to make api call to https://grpc-api-gateway-d8q71ttn.uc.gateway.dev/
# It should be passed as a header in the request. Authorization: Bearer <access_token>