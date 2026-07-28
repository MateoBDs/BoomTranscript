import discord
from discord.ext import commands

from boomtranscript import TranscriptExporter


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.command()
async def transcript(ctx):

    exporter = TranscriptExporter(ctx.channel)

    file = await exporter.export()

    await ctx.send(
        "Transcript generado:",
        file=discord.File(file)
    )


bot.run("TOKEN")
