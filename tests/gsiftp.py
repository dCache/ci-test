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
        self.remoteURL = "gsiftp://%s/%s/%s" % (self.sut, self.basepath, self.uniqueFile)

    def testNoDCAU(self):

        self.assertCommandPass( [self.globus_home + '/bin/globus-url-copy', '-nodcau', self.localURL, self.remoteURL] )

    def testGsiftpSingleStream(self):

        self.assertCommandPass( [self.globus_home + '/bin/globus-url-copy', '-p', '1', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.globus_home + '/bin/globus-url-copy', '-p', '1', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)


    def testGsiftpMultipleStreams(self):

        self.assertCommandPass( [self.globus_home + '/bin/globus-url-copy', '-p', '10', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.globus_home + '/bin/globus-url-copy', '-p', '10', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

    def testLsOfNonPnfsPath(self):
        self.assertCommandFail([self.edg_home + '/bin/edg-gridftp-ls', 'gsiftp://%s/root'%(self.sut)], "List of non pnfs directory should not be allowed")


    def testLsOfTestBase(self):
        self.assertCommandPass([self.edg_home + '/bin/edg-gridftp-ls', 'gsiftp://%s/%s'%(self.sut,self.basepath)])

    def testLsNonExistingPath(self):
        self.assertCommandFail([self.edg_home + '/bin/edg-gridftp-ls', self.remoteURL])

    def tearDown(self):

        self.execute([self.edg_home + '/bin/edg-gridftp-rm', self.remoteURL])
        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)




if __name__ == '__main__':
    unittest.main()
