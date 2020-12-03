# SPDX-License-Identifier: Apache-2.0
#
# http://nexb.com and https://github.com/nexB/scancode-licensedb
# The LicenseDB software is licensed under the Apache License version 2.0.
# Data generated with LicenseDB is provided as-is without warranties.
# LicenseDB is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Data Generated with LicenseDB is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. No content created from
# LicenseDB should be considered or used as legal advice. Consult an Attorney
# for any legal advice.
#
# LicenseDB is a free software code scanning tool from nexB Inc. and others.
# Visit https://github.com/nexB/scancode-licensedb for support and download.

import json
import pathlib
from datetime import datetime

import saneyaml
from jinja2 import Environment, PackageLoader
from licensedcode.models import load_licenses
from scancode_config import __version__ as scancode_version

licenses = load_licenses(with_deprecated=True)

# GitHub Pages support only /(root) or docs/ for the source
BUILD_LOCATION = "docs"

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=True,
)


def write_file(path, filename, content):
    (path / filename).open("w").write(content)


def now():
    return datetime.now().strftime("%b %d, %Y")


def generate_indexes(output_path):
    license_list_template = env.get_template("license_list.html")
    index_html = license_list_template.render(
        licenses=licenses,
        scancode_version=scancode_version,
        is_root=True,
        now=now(),
    )
    (output_path / "index.html").open("w").write(index_html)

    index = [
        {
            "license_key": key,
            "json": f"licenses/{key}.json",
            "yml": f"licenses/{key}.yml",
            "html": f"licenses/{key}.html",
            "text": f"licenses/{key}.LICENSE",
        }
        for key in licenses.keys()
    ]
    (output_path / "index.json").open("w").write(json.dumps(index))
    (output_path / "index.yml").open("w").write(saneyaml.dump(index))


def generate_details(output_path):
    license_details_template = env.get_template("license_details.html")
    for license in licenses.values():
        license_data = license.to_dict()
        yml = saneyaml.dump(license_data)
        html = license_details_template.render(
            license=license,
            license_data=yml,
            scancode_version=scancode_version,
            now=now(),
        )
        write_file(output_path, f"{license.key}.html", html)
        write_file(output_path, f"{license.key}.yml", yml)
        write_file(output_path, f"{license.key}.json", json.dumps(license_data))
        write_file(output_path, f"{license.key}.LICENSE", license.text)


def generate_help(output_path):
    template = env.get_template("help.html")
    html = template.render(
        is_root=True,
        now=now(),
    )
    (output_path / "help.html").open("w").write(html)


def generate():
    root_path = pathlib.Path(BUILD_LOCATION)
    root_path.mkdir(parents=False, exist_ok=True)

    licenses_path = root_path / "licenses"
    licenses_path.mkdir(parents=False, exist_ok=True)

    generate_indexes(root_path)
    generate_details(licenses_path)
    generate_help(root_path)


if __name__ == "__main__":
    generate()
