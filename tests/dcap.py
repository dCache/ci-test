import unittest
import dcachetestcase
import localtools
import os


class DcapSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.uniqueFile = localtools.uniqueFileNameGenerator("DcapSuite").next()
        self.localFile = "/etc/profile"
        self.tempFile = "/tmp/%s" % (self.uniqueFile)


    def testGsiDccp(self):
        self.remoteURL = "gsidcap://%s:22128/%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['/usr/bin/dccp', self.localFile, self.remoteURL] )
        self.assertCommandPass( ['/usr/bin/dccp', self.remoteURL, self.tempFile] )

        self.assertSameSum(self.localFile, self.tempFile)

    def testPrestageOnDir(self):
        self.assertCommandFail( ['/usr/bin/dccp', '-P', self.basepath ] )

    def tearDown(self):

        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)


if __name__ == '__main__':
    unittest.main()
