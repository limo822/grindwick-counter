
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
        "name": f"🎮Players In Game:{players}🎮"
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

    try:
        with urllib.request.urlopen(request) as response:
            print("Sukces:", response.status)

    except urllib.error.HTTPError as error:
        print("Discord HTTP:", error.code)
        print("Szczegóły:", error.read().decode())
        raise


if __name__ == "__main__":
    players = get_players()
    print("Gracze Steam:", players)
    update_discord(players)
