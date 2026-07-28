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
            
                # =========================
                # EMBEDS
                # =========================
            
                embeds = []
            
                for embed in message.embeds:
            
                    fields = []
            
                    for field in embed.fields:
                        fields.append(
                            EmbedField(
                                name=field.name,
                                value=field.value,
                                inline=field.inline
                            )
                        )
            
                    embeds.append(
                        EmbedData(
            
                            title=embed.title,
            
                            description=embed.description,
            
                            color=f"#{embed.color.value:06x}" if embed.color else "#5865F2",
            
                            author_name=embed.author.name if embed.author else None,
            
                            author_icon=str(embed.author.icon_url)
                            if embed.author and embed.author.icon_url
                            else None,
            
                            thumbnail=str(embed.thumbnail.url)
                            if embed.thumbnail
                            else None,
            
                            image=str(embed.image.url)
                            if embed.image
                            else None,
            
                            footer=embed.footer.text
                            if embed.footer
                            else None,
            
                            footer_icon=str(embed.footer.icon_url)
                            if embed.footer and embed.footer.icon_url
                            else None,
            
                            fields=fields
            
                        )
                    )
            
                # =========================
                # ATTACHMENTS
                # =========================
            
                attachments = []
            
                for attachment in message.attachments:
            
                    attachments.append(
                        AttachmentData(
            
                            filename=attachment.filename,
            
                            url=attachment.url,
            
                            content_type=attachment.content_type,
            
                            size=attachment.size
            
                        )
                    )
            
                # =========================
                # REACTIONS
                # =========================
            
                reactions = []
            
                for reaction in message.reactions:
            
                    reactions.append(
                        ReactionData(
            
                            emoji=str(reaction.emoji),
            
                            count=reaction.count
            
                        )
                    )
            
                # =========================
                # MESSAGE
                # =========================
            
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
            
                        edited=message.edited_at is not None,
            
                        embeds=embeds,
            
                        attachments=attachments,
            
                        reactions=reactions,
            
                        reference=message.reference.message_id
                        if message.reference
                        else None
            
                    )
            
                )

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
