from mailjet_rest import Client

from dotenv import load_dotenv
import os
# importing env variables
load_dotenv()

def sendOTPEmail(emailTo,name,otp):
    api_key = os.getenv("MJ_APIKEY_PUBLIC")
    api_secret = os.getenv("MJ_APIKEY_PRIVATE")
    
    
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "gautampraveen351@gmail.com",
            "Name": "Praveen"
          },
          "To": [
            {
              "Email": emailTo,
              "Name": name
            }
          ],
          "Subject": "OTP for BUDDY Music",
        
          "HTMLPart": "<h2>Hi {} ,</h2><br> <h3>The OTP for your account is {}.</h3>".format(name,otp),
          
        }
      ]
    }
    
    # send the email
    result = mailjet.send.create(data=data)
    # print(result.json())