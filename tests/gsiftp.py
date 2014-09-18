import unittest
import dcachetestcase
import localtools
import os


class GsiFtpSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.uniqueFile = localtools.uniqueFileNameGenerator("GsiFtpSuite").next()
        self.localFile = "/etc/profile"
        self.localURL = "file:////%s" % (self.localFile)
        self.tempFile = "/tmp/%s" % (self.uniqueFile)
        self.tempURL =  "file:////%s" % (self.tempFile)
        self.remoteURL = "gsiftp://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)

    def testNoDCAU(self):
        self.assertCommandPass( ['globus-url-copy', '-nodcau', self.localURL, self.remoteURL] )
        self.execute(['edg-gridftp-rm', self.remoteURL])

    def testGsiftpSingleStream(self):
        self.assertCommandPass( ['globus-url-copy', '-p', '1', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['globus-url-copy', '-p', '1', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)
        self.execute(['edg-gridftp-rm', self.remoteURL])


    def testGsiftpMultipleStreams(self):
        self.assertCommandPass( ['globus-url-copy', '-p', '10', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['globus-url-copy', '-p', '10', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)
        self.execute(['edg-gridftp-rm', self.remoteURL])

    def testLsOfNonPnfsPath(self):
        self.assertCommandFail(['edg-gridftp-ls', 'gsiftp://%s/root' % (self.sut)], "List of non pnfs directory should not be allowed")

    def testLsOfTestBase(self):
        self.assertCommandPass(['edg-gridftp-ls', 'gsiftp://%s%s' % (self.sut, self.basepath)])

    def testLsNonExistingPath(self):
        self.assertCommandFail(['edg-gridftp-ls', self.remoteURL])

    def tearDown(self):
        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)




if __name__ == '__main__':
    unittest.main()
