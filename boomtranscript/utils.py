from datetime import datetime
import html


def escape(text: str | None) -> str:
    """
    Escapa HTML para evitar inyecciones.
    """

    if text is None:
        return ""

    return html.escape(text)


def format_datetime(dt: datetime) -> str:
    """
    Convierte una fecha a formato legible.
    """

    return dt.strftime("%d/%m/%Y %H:%M")


def format_filesize(size: int) -> str:

    units = ["B", "KB", "MB", "GB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} TB"
