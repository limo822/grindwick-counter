
import os
import json
import urllib.request

APP_ID = "5353310"
PEAK_FILE = "peak.txt"


def get_players():
    url = (
        "https://api.steampowered.com/"
        "ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
        f"?appid={APP_ID}"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "GrindwickCounter/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode())

    return int(data["response"]["player_count"])


def get_and_save_peak(current):
    with open(PEAK_FILE, "r") as file:
        peak = int(file.read().strip())

    if current > peak:
        peak = current

        with open(PEAK_FILE, "w") as file:
            file.write(str(peak))

        print("NOWY REKORD!", peak)

    return peak


def update_discord(peak):
    token = os.environ["DISCORD_BOT_TOKEN"]
    channel_id = os.environ["PEAK_CHANNEL_ID"]

    url = f"https://discord.com/api/v10/channels/{channel_id}"

    payload = json.dumps({
        "name": f"🏆All-Time Peak: {peak}🏆"
    }).encode()

    request = urllib.request.Request(
        url,
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://discord.com, 1.0)",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        print("Discord:", response.status)
        print("Rekord Grindwick:", peak)


if __name__ == "__main__":
    current = get_players()
    print("Aktualnie gra:", current)

    peak = get_and_save_peak(current)
    print("Najwyższy rekord:", peak)

    update_discord(peak)

