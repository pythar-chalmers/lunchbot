from os import environ
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import logging

try:
    DISCORD_WEBHOOK_URL = environ["DISCORD_WEBHOOK_URL"]
except KeyError as err:
    logging.warning('Unable to find enviroment variable "DISCORD_WEBHOOK_URL".')
    DISCORD_WEBHOOK_URL = ""


def debug(txt: str, args: list = [], kwargs: dict = {}):
    logging.debug(f"[Discord Gateway] {txt}", *args, **kwargs)


def to_discord_date(date: datetime, method: str = "f") -> str:
    t = int(date.timestamp())
    return f"<t:{t}:{method}>"


def create_embed(event) -> DiscordEmbed:
    # create embed object for webhook
    embed = DiscordEmbed(title=event.title, description=event.desc, color="ffffff")

    # Author
    embed.set_author(
        name="wych.dev",
        url="https://wych.dev",
        icon_url="https://avatars.githubusercontent.com/u/38406360",
    )

    # Thumbnail
    embed.set_thumbnail(url=event.icon_url)

    # Fields
    embed.add_embed_field(name="Location", value=f"@ {event.location}", inline=False)
    embed.add_embed_field(
        name="When?", value=to_discord_date(event.dtstart), inline=False
    )
    embed.add_embed_field(
        name="Ends", value=to_discord_date(event.dtend, "t"), inline=False
    )

    return embed


def alert_lunch(events: list):
    debug("EVENTS:")
    webhook_handle = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL,
    )

    for event in events:
        logging.debug(f"\t{event}")
        embed = create_embed(event)
        webhook_handle.add_embed(embed)

    response = webhook_handle.execute()
    debug(f"Got response: {response.status_code}")
