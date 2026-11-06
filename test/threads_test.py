import json, time, requests
from useful_resources import pull_config
TOKEN_FILE = "threads_token.json"
THREADS_CRED = pull_config('THREADS')

def load_threads_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)

def save_threads_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump(
            {
                "access_token": token,
                "refreshed_at": time.time()
            }, f
        )

def get_valid_threads_token():
    th_json_data = load_threads_token()
    age_days = (time.time() - data["refreshed_at"]) / 86400
    if age_days > 7:
        r = requests.get(
            "https://graph.threads.net/refresh_access_token",
            params={
                "grant_type": "th_refresh_token",
                "access_token": th_json_data["access_token"]
            }
        )
        r.raise_for_status()
        save_threads_token(r.json()["access_token"])
        return r.json()["access_token"]
    return th_json_data["access_token"]

def post_to_threads(text):
    threads_url = "https://graph.threads.net/v1.0"
    threads_id = "me"
    threads_token = load_threads_token()['access_token']
    params = {
        "access_token": load_threads_token()["access_token"],
        "media_type": "TEXT",
        "text": text
        }
    r = requests.post(
        "{}/{}/threads".format(threads_url,threads_id),params=params)
    print(r.status_code, r.text)
    r.raise_for_status()
    container_id = r.json()["id"]

    r = requests.post("{}/{}/threads_publish".format(threads_url,threads_id),
                        params= {
                            "creation_id": container_id,
                            "access_token": threads_token
                        }
                    )
    r.raise_for_status()
    return r.json()["id"]

post_to_threads("this is a test")