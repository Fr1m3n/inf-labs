from Parsers.XmlParser import XmlParser
from Tests.Fritest import Tester

tester = Tester()
parser = XmlParser()


@tester.test
def single_object_test():
    parsed = parser.parse("<q> 12 </q>")
    would_be = {'q' : 12}
    tester.equals_to(parsed, would_be)


@tester.test
def b():
    tester.equals_to(2, 2)


if __name__ == "__main__":
    tester.run_tests()