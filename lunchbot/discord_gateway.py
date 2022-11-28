from discord_webhook import DiscordWebhook, DiscordEmbed
from os import environ

try:
    DISCORD_WEBHOOK_URL = environ["DISCORD_WEBHOOK_URL"]
except KeyError as err:
    print('WARNING: Unable to find enviroment variable "DISCORD_WEBHOOK_URL".')
    DISCORD_WEBHOOK_URL = ""


print(f"Using discord webhook url: {DISCORD_WEBHOOK_URL}")


def debug(txt: str, args: list = [], kwargs: dict = {}):
    print(f"[Discord Gateway] {txt}", *args, **kwargs)


def to_discord_date(t: int) -> str:
    return f"<t:{t}:F> (<t:{t}:R>)"


def create_embed(event) -> DiscordEmbed:
    # create embed object for webhook
    embed = DiscordEmbed(title=event.title, description=event.desc, color="03b2f8")

    embed.set_author(
        name="elal",
        url="https://wych.dev",
        icon_url="https://avatars.githubusercontent.com/u/38406360",
    )

    # set thumbnail
    # embed.set_thumbnail(url="your thumbnail url")

    # set footer
    embed.set_footer(text="A very cool WebHook made by **elal** :)")

    # set timestamp (default is now)
    embed.set_timestamp()

    # add fields to embed
    embed.add_embed_field(name="Location", value=event.location, inline=False)
    embed.add_embed_field(name="Start", value=to_discord_date(event.dtstart), inline=False)
    embed.add_embed_field(name="End", value=to_discord_date(event.dtend))
    embed.add_embed_field(name="Created", value=to_discord_date(event.dtstamp))

    return embed


def alert_lunch(events: list):
    webhook_handle = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL, 
        username="Free Shit Scraper",
    )

    debug("EVENTS:")
    for ev in events:
        embed = create_embed(ev)
        print(f"\t{ev} {embed=}")
        webhook_handle.add_embed(embed)

    response = webhook_handle.execute()
    debug(f"Got response: {response.status_code}")
