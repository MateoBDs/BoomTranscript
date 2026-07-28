from html import escape


class TranscriptRenderer:

    def __init__(self, guild, channel, messages):
        self.guild = guild
        self.channel = channel
        self.messages = messages

    def render(self):

        body = ""

        for msg in self.messages:

            body += f"""
            <div class="message">

                <img class="avatar"
                     src="{msg['author']['avatar']}">

                <div class="content">

                    <div class="meta">

                        <span class="username"
                        style="color:{msg['author']['color']}">
                        {escape(msg['author']['display_name'])}
                        </span>

                        <span class="time">
                        {msg['created_at'].strftime("%d/%m/%Y %H:%M")}
                        </span>

                    </div>

                    <div class="text">
                        {escape(msg["content"]).replace(chr(10), "<br>")}
                    </div>

                </div>

            </div>
            """

        icon = self.guild.icon.url if self.guild.icon else ""

        return f"""
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<title>{escape(self.guild.name)}</title>

<style>

body{{
margin:0;
background:#313338;
font-family:Arial,sans-serif;
color:#dbdee1;
}}

.header{{
display:flex;
align-items:center;
gap:20px;
padding:24px;
background:#1e1f22;
border-bottom:1px solid #2b2d31;
}}

.header img{{
width:72px;
height:72px;
border-radius:50%;
}}

.server-name{{
font-size:30px;
font-weight:bold;
}}

.channel{{
color:#b5bac1;
margin-top:4px;
}}

.message{{
display:flex;
gap:16px;
padding:14px 22px;
}}

.message:hover{{
background:#2b2d31;
}}

.avatar{{
width:40px;
height:40px;
border-radius:50%;
}}

.username{{
font-weight:bold;
}}

.time{{
margin-left:8px;
font-size:12px;
color:#949ba4;
}}

.text{{
margin-top:3px;
white-space:pre-wrap;
}}

</style>

</head>

<body>

<div class="header">

<img src="{icon}">

<div>

<div class="server-name">
{escape(self.guild.name)}
</div>

<div class="channel">
#{escape(self.channel.name)}
</div>

</div>

</div>

{body}

</body>

</html>
"""
