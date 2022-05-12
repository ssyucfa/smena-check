import json

from jinja2 import Environment, PackageLoader, select_autoescape

from checks.models import Check, CheckType


def get_rendered_template(check: Check) -> str:
    env = Environment(
        loader=PackageLoader("order"),
        autoescape=select_autoescape()
    )
    template = env.get_template("kitchen_check.html" if check.type == CheckType.KITCHEN else "client_check.html")
    return template.render(order=json.loads(check.order))
