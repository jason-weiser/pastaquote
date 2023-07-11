import requests

def connection_validator(url_to_check):
    try:
        response = requests.head(url_to_check)
    except requests.ConnectionError:
        return("Failed to Connect")
    else:
        return response.status_code

        ##TODO: Add logging to this file