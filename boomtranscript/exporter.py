from pathlib import Path
from datetime import datetime


class TranscriptExporter:

    def __init__(self, channel):
        self.channel = channel


    async def export(self):

        messages = []

        async for msg in self.channel.history(limit=None, oldest_first=True):
            messages.append({
                "author": msg.author.display_name,
                "avatar": msg.author.display_avatar.url,
                "content": msg.content,
                "time": msg.created_at.strftime("%d/%m/%Y %H:%M")
            })


        html = self.generate(messages)

        file = Path(
            f"transcript-{self.channel.name}.html"
        )

        file.write_text(
            html,
            encoding="utf-8"
        )

        return file


    def generate(self, messages):

        content = ""

        for msg in messages:
            content += f"""
            <div class="message">
                <img src="{msg['avatar']}">
                <div>
                    <b>{msg['author']}</b>
                    <span>{msg['time']}</span>
                    <p>{msg['content']}</p>
                </div>
            </div>
            """


        return f"""
<!DOCTYPE html>
<html>
<head>

<title>BoomNetwork Transcript</title>

<style>

body {{
    background:#111214;
    color:white;
    font-family:Arial;
}}

.header {{
    padding:25px;
    background:#5865f2;
    display:flex;
    align-items:center;
}}

.header h1 {{
    margin-left:20px;
}}

.message {{
    display:flex;
    gap:15px;
    padding:15px;
}}

.message img {{
    width:45px;
    height:45px;
    border-radius:50%;
}}

span {{
    color:#999;
    font-size:12px;
}}

</style>

</head>

<body>


<div class="header">

<h1>
BoomNetwork
</h1>

</div>


{content}


</body>
</html>
"""
