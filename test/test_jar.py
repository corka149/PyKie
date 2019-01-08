from pykie import jar
from unittest import TestCase
from zipfile import ZipFile
import unittest

__author__ = "corka149"


def __test_jar__():
    import os
    if "test" in os.listdir("."):
        return "test/py-kie-tes-1.0.0.jar"
    else:
        return "./py-kie-tes-1.0.0.jar"


class TestJar(TestCase):

    def test_is_pom(self):
        self.assertTrue(jar.is_pom("pom.xml"))

    def test_is_not_pom(self):
        self.assertFalse(jar.is_pom("pom.properties"))

    def test_search_pom(self):
        with ZipFile(__test_jar__()) as test_jar:
            expected = "META-INF/maven/com.myspace/py-kie-tes/pom.xml"
            result = jar.search_pom(test_jar)
            self.assertEqual(expected, result)

    def test_extract_pom(self):
        content = jar.extract_pom(__test_jar__())
        self.assertIn(b"py-kie-tes", content)


if __name__ == '__main__':
    unittest.main()
