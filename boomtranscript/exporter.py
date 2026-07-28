from pathlib import Path
from datetime import datetime

from .renderer import TranscriptRenderer
from .models import *


class TranscriptExporter:

    def __init__(self, channel):
        self.channel = channel
        self.renderer = TranscriptRenderer()

    async def export(self, filename: str | None = None):

        guild = self.channel.guild

        transcript = TranscriptData(

            guild=GuildData(
                id=guild.id,
                name=guild.name,
                icon=guild.icon.url if guild.icon else None,
                banner=guild.banner.url if guild.banner else None
            ),

            channel=ChannelData(
                id=self.channel.id,
                name=self.channel.name,
                topic=self.channel.topic,
                category=self.channel.category.name if self.channel.category else None
            ),

            generated_at=datetime.utcnow().strftime("%d/%m/%Y %H:%M"),

            message_count=0,

            messages=[]
        )

        async for message in self.channel.history(
            oldest_first=True,
            limit=None
        ):

            transcript.messages.append(
                MessageData(

                    id=message.id,

                    author=AuthorData(
                        id=message.author.id,
                        username=message.author.name,
                        display_name=message.author.display_name,
                        avatar=message.author.display_avatar.url,
                        color=str(message.author.color),
                        bot=message.author.bot
                    ),

                    content=message.content,

                    created_at=message.created_at.strftime(
                        "%d/%m/%Y %H:%M"
                    ),

                    edited=message.edited_at is not None
                )
            )

        transcript.message_count = len(transcript.messages)

        html = self.renderer.render(transcript)

        if filename is None:
            filename = f"transcript-{self.channel.name}.html"

        path = Path(filename)

        path.write_text(
            html,
            encoding="utf-8"
        )

        return path
