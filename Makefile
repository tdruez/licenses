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

PYTHON_EXE=python3.6
MANAGE=bin/python manage.py
ACTIVATE=. bin/activate;

conf:
	@echo "-> Configure the Python venv and install dependencies"
	${PYTHON_EXE} -m venv .
	@${ACTIVATE} pip install "scancode-toolkit[full]"

clean:
	git rm -r docs

build:
	@echo "-> Generate the HTML content"
	bin/python licenses.py

.PHONY: conf build
