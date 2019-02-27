# Copyright 2019 Geoffrey A. Reed. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# ----------------------------------------------------------------------
"""Setup script for The Cancer Imaging Archive (TCIA) REST client."""
import os

import setuptools

import tcia


__all__ = []


def _read_long_description(*, path_or_buffer="README.md"):
    """Read the package long description from a file path or buffer."""
    with open(path_or_buffer, "rt") as file_handle:
        long_description = file_handle.read()
        
    return long_description

        
if __name__ == "__main__":
    setuptools.setup(
        name="tcia",
        version=tcia.__version__,
        description="A REST client for The Cancer Imaging Archive (TCIA)",
        long_description=_read_long_description(),
        license="Apache 2.0",
        author="Geoffrey A. Reed",
        author_email="geoffrey.a.reed@gmail.com",
        url="https://github.com/geoffrey-a-reed/TCIA",
        zip_safe=False,
        packages=setuptools.find_packages(exclude=["tests"], ),
        python_requires=">=3.6",
        install_requires=[
            "requests>=2.21"
        ],
        tests_require=[
            "pytest>=4.3"
        ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Communications :: File Sharing",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Scientific/Engineering :: Medical Science Apps."
        ]
    )
