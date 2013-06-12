#!/usr/bin/env python

import unittest
import dcachetestcase

class SimepleTest(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def  setUp(self):
        # nothing yet
        self.number = 5
        self.user = "tigran"

    def testTest(self):
        self.assertEqual(self.number, 5)


    def testUser(self):
        self.assertEqual(self.user, "tigran")

    def testLs(self):
        self.assertCommandPass(['/bin/ls','/etc'])

    def testLsFail(self):
        self.assertCommandFail(['/bin/ls','/etc/aa'])


if __name__ == '__main__':
    unittest.main()

