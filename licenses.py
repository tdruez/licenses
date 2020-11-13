import pathlib

import saneyaml
from licensedcode.models import load_licenses
from dominate.tags import *

licenses = load_licenses()


def generate_html():
    output_path = pathlib.Path(".")
    output_path.mkdir(parents=False, exist_ok=True)
    licenses_path = output_path / "licenses"
    licenses_path.mkdir(parents=False, exist_ok=True)

    index = html(body(ul(li(a(key, href=f"licenses/{key}.html")) for key in licenses.keys())))
    (output_path / "index.html").open('w').write(index.render())

    for license in licenses.values():
        data = saneyaml.dump(license.to_dict())
        content = html(body(pre(data), hr(), pre(license.text)))
        (licenses_path / f"{license.key}.html").open('w').write(content.render())


if __name__ == "__main__":
    generate_html()
