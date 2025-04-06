import requests
import os
import re
import time

AUTH_TOKEN = os.getenv("HTB_TOKEN") or "Bearer CHANGE THIS"

headers = {
    "Host": "labs.hackthebox.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Authorization": AUTH_TOKEN,
    "Origin": "https://app.hackthebox.com",
    "Referer": "https://app.hackthebox.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

output_dir = "writeups/"
os.makedirs(output_dir, exist_ok=True)

def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename="?([^"]+)"?', cd)
    return fname[0] if fname else None

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_machine_difficulty(namefile):
    name = namefile.replace(".pdf", "")
    url = f"https://labs.hackthebox.com/api/v4/machine/profile/{name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            return data["info"]["difficultyText"]
        except Exception as e:
            print(f"[!] Gagal parsing difficulty dari {name}: {e}")
    else:
        print(f"[!] Gagal ambil profil untuk {name} (status: {response.status_code})")
    return "Unknown"

start_id = 1            # Starting machine ID
end_id = 1000           # Ending machine ID
base_delay = 10         # Delay between requests (in seconds)
max_delay = 300         # Max delay after being rate-limited

for machine_id in range(start_id, end_id + 1):
    url = f"https://labs.hackthebox.com/api/v4/machine/writeup/{machine_id}"
    delay = base_delay
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                cd = response.headers.get('Content-Disposition')
                filename = get_filename_from_cd(cd)
                difficulty = get_machine_difficulty(filename)

                if not filename:
                    try:
                        json_data = response.json()
                        machine_name = sanitize_filename(json_data.get("info", {}).get("name", f"machine_{machine_id}"))
                        filename = f"{machine_id} - {machine_name}.pdf"
                    except:
                        filename = f"{machine_id}.pdf"

                diff_dir = os.path.join(output_dir, difficulty)
                os.makedirs(diff_dir, exist_ok=True)
                file_path = os.path.join(diff_dir, filename)
                
                if os.path.exists(file_path):
                    print(f"[→] Skip (exists): {filename}")
                    break

                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"[✓] Saved: {filename}")
                break

            elif response.status_code == 429:
                print(f"[!] Rate limit hit (429) for ID {machine_id}, retrying in {delay} seconds...")
                time.sleep(delay)
                delay = min(delay * 2, max_delay)  # (exponential backoff)
            else:
                print(f"[x] ID {machine_id} - Status: {response.status_code}")
                break  

        except Exception as e:
            if "Temporary failure in name resolution" in str(e) or "Name or service not known" in str(e):
                print(f"[!] DNS Error on ID {machine_id}, retrying in {delay} seconds...")
                time.sleep(1)
                continue
            print(f"[!] Error on ID {machine_id}: {e}")
            break


    time.sleep(base_delay)
