from Parsers.XmlParser import XmlParser
from Tests.Fritest import Tester
from Parsers.JsonPrinter import JsonPrinter
import xmltodict
from xml.dom.minidom import parse

json_printer = JsonPrinter()
tester = Tester()
parser = XmlParser()
input_file = open("../p3112shedule.xml", "r")
s = input_file.read()


@tester.test
def my_parser_test():
    parser.parse(s)

@tester.test
def xmltodict_test():
    xmltodict.parse(s)

@tester.test
def minidom_test():
    parse("../p3112shedule.xml")


if __name__ == "__main__":
    tester.run_tests(10)