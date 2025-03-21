import requests
import base64

CLIENT_ID = "f6a341872e3f41de83b89ec49ad8462d"
CLIENT_SECRET = "075e3e4c953e41a88fc46ff6036a6dbd"
REDIRECT_URI = "http://localhost:8888/callback"
AUTHORIZATION_CODE = "AQDb1YTOFgCyNH0zTrsMIEVQA33z7kwjlAkIRtJ4dgb-pYC4zZBWdF8Dq_vWZQzT8HSVpYrR6lVCXCfNXGSJHSpmko0Yq0tntPOicORhMCHoc0QJOVDwOXofiJmA-JSZs-JmnXKycFaRzJT-2G-CBg7viEOaGzWbvzsElSmhiz0EQYbB01_2znMMXfZfyr2rpw"

def get_user_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": AUTHORIZATION_CODE,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data)
    print("🔍 User Token Response:", response.json())

get_user_access_token()



