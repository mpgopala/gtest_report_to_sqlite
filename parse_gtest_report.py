
import sqlite3
from xml.dom.minidom import *

class TestSuite:
    def __init__(self, name, tests, failures, disabled, errors, time, timeStamp):
        self.name = name
        self.tests = tests
        self.failures = failures
        self.disabled = disabled
        self.errors = errors
        self.time = time
        self.timeStamp = timeStamp

    def default(self, o):
        return o.__dict__

class TestCase:
    def __init__(self, name, status, result, time, timeStamp, testSuite):
        self.name = name
        self.status = status
        self.result = result
        self.time = time
        self.timeStamp = timeStamp
        self.testSuite = testSuite

    def default(self, o):
        return o.__dict__

testSuits = []
testCases = []
def process(fileName):

    xmlFile = parse(fileName)

    for node in xmlFile.getElementsByTagName("testcase"):
        tcName = node.attributes["name"].value
        tcStatus = node.attributes["status"].value
        tcResult = node.attributes["result"].value
        tcTime = node.attributes["time"].value
        tcTimeStamp = node.attributes["timestamp"].value
        tcTestSuite = node.attributes["classname"].value
        testCases.append(TestCase(tcName, tcStatus, tcResult, tcTime, tcTimeStamp, tcTestSuite))


    for node in xmlFile.getElementsByTagName("testsuite"):
        tsName = node.attributes["name"].value
        tsTests = node.attributes["tests"].value
        tsFailures = node.attributes["failures"].value
        tsDisabled = node.attributes["disabled"].value
        tsErrors = node.attributes["errors"].value
        tsTime = node.attributes["time"].value
        tsTimeStamp = node.attributes["timestamp"].value
        testSuits.append(TestSuite(tsName, tsTests, tsFailures, tsDisabled, tsErrors, tsTime, tsTimeStamp))

def writeToDB(fileName):
    print('Writing to the database...')
    conn = sqlite3.connect(fileName)
    c = conn.cursor()

    c.execute("DROP TABLE TestCase")
    c.execute("CREATE TABLE IF NOT EXISTS  `TestCase` ( `name` TEXT PRIMARY_KEY, `status` TEXT, `result` TEXT, `time` DECIMAL, `timeStamp` DATETIME, `testSuite` TEXT )")
    c.execute("DELETE FROM TestCase")

    for tc in testCases:
        c.execute("insert into TestCase values(?, ?, ?, ?, ?, ?)", [tc.name, tc.status, tc.result, tc.time, tc.timeStamp, tc.testSuite])
    conn.commit()

    c.execute("DROP TABLE TestSuite")
    c.execute(
        "CREATE TABLE IF NOT EXISTS  `TestSuite` ( `name` TEXT PRIMARY_KEY, `tests` INTEGER, `failures` INTEGER, `disaled` INTEGER, `errors` INTEGER, `time` DECIMAL, 'timeStamp' DATETIME, 'timePerTest' DECIMAL )")
    c.execute("DELETE FROM TestSuite")
    for ts in testSuits:
        c.execute("insert into TestSuite values(?, ?, ?, ?, ?, ?, ?, ?)",
                    [ts.name, ts.tests, ts.failures, ts.disabled, ts.errors, ts.time, ts.timeStamp, round(float(ts.time)/int(ts.tests), 2)])
    conn.commit()

    conn.close()
    print("Done...")

    
if __name__ == '__main__':
    process("in/report.xml")
    writeToDB("out/db.db")