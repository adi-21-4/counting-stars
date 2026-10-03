import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLASH_API_TOKEN = os.getenv("CLASH_API_TOKEN")
CLASH_PROXY_URL = os.getenv("CLASH_PROXY_URL")

BASE_URL = "https://api.clashofclans.com/v1"


def get_headers():
    return {
        "Authorization": f"Bearer {CLASH_API_TOKEN}",
        "Accept": "application/json"
    }


def get_proxies():
    if not CLASH_PROXY_URL:
        return None

    return {
        "http": CLASH_PROXY_URL,
        "https": CLASH_PROXY_URL
    }


def get_clan(clan_tag):
    if not CLASH_API_TOKEN:
        return 500, {"error": "CLASH_API_TOKEN is not configured"}

    encoded_tag = clan_tag.replace("#", "%23")
    url = f"{BASE_URL}/clans/{encoded_tag}"

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            proxies=get_proxies(),
            timeout=30
        )
        return response.status_code, response.json()

    except requests.RequestException as error:
        return 502, {
            "error": "Failed to connect to Clash of Clans API",
            "details": str(error)
        }

    except ValueError:
        return 502, {
            "error": "Invalid response from Clash of Clans API"
        }


def get_current_war(clan_tag):
    if not CLASH_API_TOKEN:
        return 500, {"error": "CLASH_API_TOKEN is not configured"}

    encoded_tag = clan_tag.replace("#", "%23")
    url = f"{BASE_URL}/clans/{encoded_tag}/currentwar"

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            proxies=get_proxies(),
            timeout=10
        )
        return response.status_code, response.json()

    except requests.RequestException as error:
        return 502, {
            "error": "Failed to connect to Clash of Clans API",
            "details": str(error)
        }

    except ValueError:
        return 502, {
            "error": "Invalid response from Clash of Clans API"
        }


def get_war_log(clan_tag):
    if not CLASH_API_TOKEN:
        return 500, {"error": "CLASH_API_TOKEN is not configured"}

    encoded_tag = clan_tag.replace("#", "%23")
    url = f"{BASE_URL}/clans/{encoded_tag}/warlog"

    try:
        response = requests.get(
            url,
            headers=get_headers(),
            proxies=get_proxies(),
            timeout=10
        )
        return response.status_code, response.json()

    except requests.RequestException as error:
        return 502, {
            "error": "Failed to connect to Clash of Clans API",
            "details": str(error)
        }

    except ValueError:
        return 502, {
            "error": "Invalid response from Clash of Clans API"
        }