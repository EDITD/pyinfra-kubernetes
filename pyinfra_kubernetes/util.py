from os import path


def get_template_path(template):
    return path.join(
        path.dirname(__file__),
        'templates',
        template,
    )
