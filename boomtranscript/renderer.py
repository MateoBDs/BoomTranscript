from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


class TranscriptRenderer:

    def __init__(self):

        template_folder = (
            Path(__file__).parent
            / "templates"
        )

        self.environment = Environment(
            loader=FileSystemLoader(template_folder),
            autoescape=select_autoescape(["html"])
        )

    def render(self, transcript):

        template = self.environment.get_template(
            "transcript.html"
        )

        return template.render(
            transcript=transcript
        )
