from dataclasses import dataclass, field
from typing import List, Optional


# ==========================
# GUILD
# ==========================

@dataclass
class GuildData:
    id: int
    name: str
    icon: Optional[str]
    banner: Optional[str]


# ==========================
# CHANNEL
# ==========================

@dataclass
class ChannelData:
    id: int
    name: str
    topic: Optional[str]
    category: Optional[str]


# ==========================
# AUTHOR
# ==========================

@dataclass
class AuthorData:
    id: int
    username: str
    display_name: str
    avatar: str
    color: str
    bot: bool


# ==========================
# ATTACHMENTS
# ==========================

@dataclass
class AttachmentData:
    filename: str
    url: str
    content_type: Optional[str]
    size: int


# ==========================
# EMBED
# ==========================

@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool = False


@dataclass
class EmbedData:
    title: Optional[str]
    description: Optional[str]
    color: Optional[str]

    author_name: Optional[str]
    author_icon: Optional[str]

    thumbnail: Optional[str]
    image: Optional[str]

    footer: Optional[str]
    footer_icon: Optional[str]

    fields: List[EmbedField] = field(default_factory=list)


# ==========================
# BUTTONS
# ==========================

@dataclass
class ButtonData:
    label: str
    style: int
    emoji: Optional[str]
    url: Optional[str]
    disabled: bool


# ==========================
# REACTION
# ==========================

@dataclass
class ReactionData:
    emoji: str
    count: int


# ==========================
# MESSAGE
# ==========================

@dataclass
class MessageData:

    id: int

    author: AuthorData

    content: str

    created_at: str

    edited: bool

    attachments: List[AttachmentData] = field(default_factory=list)

    embeds: List[EmbedData] = field(default_factory=list)

    buttons: List[ButtonData] = field(default_factory=list)

    reactions: List[ReactionData] = field(default_factory=list)

    reference: Optional[int] = None


# ==========================
# TRANSCRIPT
# ==========================

@dataclass
class TranscriptData:

    guild: GuildData

    channel: ChannelData

    generated_at: str

    message_count: int

    messages: List[MessageData]
