import unittest
import dcachetestcase
from socket import  *


class SericePortpSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(1)
    def tearDown(self):
        self.socket.close();

    def testXrootOn1094(self):
        try:
            self.socket.connect( (self.sut, 1094))
        except:
            self.fail("xroot door not available")

if __name__ == '__main__':
    unittest.main()

