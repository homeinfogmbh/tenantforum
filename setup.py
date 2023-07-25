#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name="tenantforum",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    install_requires=[
        "comcatlib",
        "configlib",
        "mdb",
        "peewee",
        "peeweeplus",
        "tenant2tenant",
        "wsgilib",
    ],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    packages=["tenantforum"],
    license="GPLv3",
    description="Tenant forum library.",
)
