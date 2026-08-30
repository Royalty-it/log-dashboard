import requests

def get_country(ip):
    if not ip:
        return None
    try:
        # Free, rate‑limited API – no API key needed
        resp = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
        data = resp.json()
        return data.get('countryCode') if data.get('status') == 'success' else None
    except:
        return None

def get_flag(ip):
    country = get_country(ip)
    if not country:
        return '🏴'
    # Convert country code to flag emoji
    flag = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country.upper())
    return flag
