#!/usr/bin/env python3
from distutils.core import setup

classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
]

setup(name="FreeMageDB",
        version="1.2",
        description="FreeMage - A Free File Database Back-End",
        author="Chloride Cull",
        author_email="chloride@devurandom.net",
        url="https://github.com/ChlorideCull/FreeMageDB",
        classifiers=classifiers,
        packages=['FreeMage']
        scripts=['scripts/fmdbc.py']
        )
