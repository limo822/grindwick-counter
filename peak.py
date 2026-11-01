
import os
import re
import json
import urllib.request
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def get_text(self):
        return " ".join(self.parts)


def get_all_time_peak():
    url = "https://steamdb.info/app/5353310/charts/"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; GrindwickCounter/1.0)",
            "Accept": "text/html"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = TextExtractor()
    parser.feed(html)

    text = re.sub(r"\s+", " ", parser.get_text())

    match = re.search(
        r"(\d[\d,]*)\s+all-time peak",
        text,
        re.IGNORECASE
    )

    if not match:
        raise ValueError("Nie znaleziono rekordu all-time peak na SteamDB")

    return int(match.group(1).replace(",", ""))


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
        print("Nowy rekord:", peak)


if __name__ == "__main__":
    peak = get_all_time_peak()
    print("Historyczny rekord Grindwick:", peak)
    update_discord(peak)
