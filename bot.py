
import json
import os
import urllib.request
import urllib.error

STEAM_APP_ID = "5353310"

def get_players():
    url = (
        "https://api.steampowered.com/"
        "ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
        f"?appid={STEAM_APP_ID}"
    )

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    return data["response"]["player_count"]


def update_discord(players):
    token = os.environ["DISCORD_BOT_TOKEN"]
    channel_id = os.environ["DISCORD_CHANNEL_ID"]

    url = f"https://discord.com/api/v10/channels/{channel_id}"

    payload = json.dumps({
        "name": f"Grindwick: {players} graczy"
    }).encode()

    request = urllib.request.Request(
        url,
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(request) as response:
        print("Discord:", response.status)
        print("Nowa nazwa:", response.read().decode())


if __name__ == "__main__":
    players = get_players()
    print("Gracze Steam:", players)
    update_discord(players)
