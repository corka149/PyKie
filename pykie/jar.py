"""
Util module for processing maven JARs.
"""
__author__ = "corka149"

from zipfile import ZipFile
from typing import AnyStr


def extract_pom(jar: str) -> AnyStr:
    """Extracts the pom.xml of a JAR"""
    content = ""
    with ZipFile(jar) as jar_file:
        pom_path = search_pom(jar_file)
        with jar_file.open(pom_path) as pom:
            content = pom.read()
    return content


def search_pom(zip_file: ZipFile):
    """Searches the pom.xml in a JAR"""
    pom = filter(is_pom, zip_file.namelist())
    pom = list(pom)
    assert len(pom) == 1, "Jar should container only one pom.xml."
    return pom[0]


def is_pom(item):
    """Checks if a item is a pom.xml"""
    return "pom.xml" in item
