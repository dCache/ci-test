import unittest
import dcachetestcase
import localtools
import os
from socket import  *


class SericePortpSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(1)
    def tearDown(self):
        self.socket.close();

    def testSrmOn8443(self):
        try:
            self.socket.connect( (self.sut, 8443))
        except:
            self.fail("SRM door not available")


if __name__ == '__main__':
    unittest.main()

