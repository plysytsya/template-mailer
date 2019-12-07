from jinja2 import Environment, BaseLoader, StrictUndefined, Undefined


policies = {
    "forbid": StrictUndefined,
    "allow": Undefined
}


def render_template(template: str, data: dict, undefined="forbid") -> str:
    rtemplate = Environment(
        loader=BaseLoader(),
        undefined=policies[undefined]
    ).from_string(template)
    return rtemplate.render(data)
