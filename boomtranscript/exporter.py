from pathlib import Path

from .renderer import TranscriptRenderer


class TranscriptExporter:

    def __init__(self, channel):
        self.channel = channel

    async def export(self):

        guild = self.channel.guild

        messages = []

        async for msg in self.channel.history(limit=None, oldest_first=True):

            member = guild.get_member(msg.author.id)

            embeds = []
            for embed in msg.embeds:

                embeds.append({
                    "title": embed.title,
                    "description": embed.description,
                    "url": embed.url,
                    "color": embed.color.value if embed.color else None,
                    "thumbnail": embed.thumbnail.url if embed.thumbnail else None,
                    "image": embed.image.url if embed.image else None,
                    "footer": embed.footer.text if embed.footer else None,
                    "author": embed.author.name if embed.author else None,
                })

            attachments = []

            for attachment in msg.attachments:
                attachments.append({
                    "filename": attachment.filename,
                    "url": attachment.url,
                    "size": attachment.size,
                    "content_type": attachment.content_type,
                })

            reactions = []

            for reaction in msg.reactions:
                reactions.append({
                    "emoji": str(reaction.emoji),
                    "count": reaction.count,
                })

            messages.append({

                "id": msg.id,

                "author": {
                    "id": msg.author.id,
                    "username": msg.author.name,
                    "display_name": member.display_name if member else msg.author.display_name,
                    "avatar": msg.author.display_avatar.url,
                    "color": str(member.color) if member else "#ffffff",
                    "bot": msg.author.bot,
                },

                "content": msg.content,

                "created_at": msg.created_at,

                "edited_at": msg.edited_at,

                "embeds": embeds,

                "attachments": attachments,

                "stickers": [
                    {
                        "name": s.name,
                        "url": s.url if hasattr(s, "url") else None,
                    }
                    for s in msg.stickers
                ],

                "reactions": reactions,

                "reference": msg.reference.message_id if msg.reference else None,
            })

        renderer = TranscriptRenderer(
            guild=guild,
            channel=self.channel,
            messages=messages,
        )

        html = renderer.render()

        file = Path(f"transcript-{self.channel.name}.html")

        file.write_text(
            html,
            encoding="utf-8"
        )

        return file
