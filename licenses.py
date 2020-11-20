# SPDX-License-Identifier: Apache-2.0
#
# http://nexb.com and https://github.com/nexB/licensedb
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
# Visit https://github.com/nexB/licensedb for support and download.

import json
import pathlib

import saneyaml
from jinja2 import Environment, PackageLoader
from licensedcode.models import load_licenses

licenses = load_licenses(with_deprecated=True)

# GitHub Pages support only /(root) or docs/ for the source
BUILD_LOCATION = "docs"

env = Environment(
    loader=PackageLoader("licenses", "templates"),
    autoescape=True,
)


def write_file(path, filename, content):
    (path / filename).open("w").write(content)


def generate():
    output_path = pathlib.Path(BUILD_LOCATION)
    output_path.mkdir(parents=False, exist_ok=True)

    licenses_path = output_path / "licenses"
    licenses_path.mkdir(parents=False, exist_ok=True)

    license_list_template = env.get_template("license_list.html")
    html = license_list_template.render(title="License list", licenses=licenses)
    (output_path / "index.html").open("w").write(html)

    license_details_template = env.get_template("license_details.html")
    for license in licenses.values():
        license_data = license.to_dict()
        yml = saneyaml.dump(license_data)
        html = license_details_template.render(license=license, license_data=yml)
        write_file(licenses_path, f"{license.key}.html", html)
        write_file(licenses_path, f"{license.key}.yml", yml)
        write_file(licenses_path, f"{license.key}.json", json.dumps(license_data))
        write_file(licenses_path, f"{license.key}.LICENSE", license.text)


if __name__ == "__main__":
    generate()
