from flask import request
from jinja2 import Markup
from datetime import datetime


class momentjs:
    def __init__(self, timestamp: datetime):
        self.timestamp = timestamp

    def render(self, format_time: datetime) -> Markup:
        return Markup("<script>\nmoment.locale('es');\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format_time))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def formatNow(self):
        return self.render("fromNow()")


def isActive(path: str = '') -> str:
    if (request.path == path):
        return "active"
    return ""
