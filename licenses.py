import pathlib

import saneyaml
from licensedcode.models import load_licenses
from jinja2 import Environment, PackageLoader
import json

licenses = load_licenses(with_deprecated=True)


env = Environment(
    loader=PackageLoader('licenses', 'templates'),
    autoescape=True,
)

def write_file(path, filename, content):
    (path / filename).open('w').write(content)


def generate_html():
    output_path = pathlib.Path(".")
    output_path.mkdir(parents=False, exist_ok=True)
    licenses_path = output_path / "licenses"
    licenses_path.mkdir(parents=False, exist_ok=True)

    license_list_template = env.get_template('license_list.html')
    html = license_list_template.render(title="License list", licenses=licenses)
    (output_path / "index.html").open('w').write(html)

    license_details_template = env.get_template('license_details.html')
    for license in licenses.values():
        license_data = license.to_dict()
        yml = saneyaml.dump(license_data)
        html = license_details_template.render(license=license, license_data=yml)
        write_file(licenses_path, f"{license.key}.html", html)
        write_file(licenses_path, f"{license.key}.yml", yml)
        write_file(licenses_path, f"{license.key}.json", json.dumps(license_data))
        write_file(licenses_path, f"{license.key}.LICENSE", license.text)


if __name__ == "__main__":
    generate_html()
