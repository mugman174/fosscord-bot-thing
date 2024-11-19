import config

import aiohttp
from patcher import discord
import disnake

discord.http.Route.BASE = config.API_BASE
discord.asset.Asset.BASE = "https://cdn.old.server.spacebar.chat"

bot = discord.Client()
intents = disnake.Intents(messages=True, message_content=True, guilds=True)
dbot = disnake.Client(intents=intents)


@bot.event
async def on_message(message: discord.Message):
    print("[F]", "M", message)
    if message.channel.id != config.fosscord_channel or message.author == bot.user:
        return
    print(
        await post_message(
            content=message.content,
            username=message.author.name,
            avatar_url=str(message.author.avatar_url),
            allowed_mentions={"parse":[]}
        )
    )


@dbot.event
async def on_message(message: disnake.Message):
    if message.channel.id != config.discord_channel or message.author.bot:
        return
    print("M", message.content, message.clean_content)
    await bot.get_channel(config.fosscord_channel).send(
        f"{message.author}: {message.clean_content}",
        allowed_mentions=disnake.AllowedMentions.none()
    )


@bot.event
async def on_ready():
    print("[F] Connected!")
    await dbot.start(config.DTOKEN)


@dbot.event
async def on_ready():
    print("[D] Connected")


async def post_message(**data):
    async with aiohttp.ClientSession() as session:
        async with session.post(config.webhook, json=data) as response:
            return await response.text()


bot.run(config.TOKEN)
