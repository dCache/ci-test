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

    def testDcapOn22125(self):
        try:
            self.socket.connect( (self.sut, 22125))
        except:
            self.fail("dcap door not available")

    def testGsiDcapOn22128(self):
        try:
            self.socket.connect( (self.sut, 22128))
        except:
            self.fail("GsiDcap door not available")

    def testHttpOn2288(self):
        try:
            self.socket.connect( (self.sut, 2288))
        except:
            self.fail("http door not available")

    def testFtpOn2811(self):
        try:
            self.socket.connect( (self.sut, 2811))
        except:
            self.fail("GsiFtp door not available")

    def testSrmOn8443(self):
        try:
            self.socket.connect( (self.sut, 8443))
        except:
            self.fail("SRM door not available")

    def testXrootOn1094(self):
        try:
            self.socket.connect( (self.sut, 1094))
        except:
            self.fail("xroot door not available")

if __name__ == '__main__':
    unittest.main()

