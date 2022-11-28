from discord_webhook import DiscordWebhook, DiscordEmbed
from os import environ

try:
    DISCORD_WEBHOOK_URL = environ["DISCORD_WEBHOOK_URL"]
except KeyError as err:
    print('WARNING: Unable to find enviroment variable "DISCORD_WEBHOOK_URL".')
    DISCORD_WEBHOOK_URL = ""


def debug(txt: str, args: list = [], kwargs: dict = {}):
    print(f"[Discord Gateway] {txt}", *args, **kwargs)


def to_discord_date(t: int) -> str:
    return f"<t:{t}:f> (<t:{t}:R>)"


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
    embed.add_embed_field(name="Ends", value=f"<t:{event.dtend}:t>", inline=False)

    return embed


def alert_lunch(events: list):
    sliced_events = [events[i::10] for i in range(10)]

    for evs in sliced_events:
        webhook_handle = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
        )

        debug("EVENTS:")
        for ev in evs:
            print(f"\t{ev}")
            embed = create_embed(ev)
            webhook_handle.add_embed(embed)

        response = webhook_handle.execute()
        debug(f"Got response: {response.status_code}")
