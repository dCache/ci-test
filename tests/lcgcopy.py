import unittest
import dcachetestcase
import localtools
import os


class LcgCpSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.uniqueFile = localtools.uniqueFileNameGenerator("LcgCpSuite").next()
        self.localFile = "/etc/profile"
        self.localURL = "file:////%s" % (self.localFile)
        self.tempFile = "/tmp/%s" % (self.uniqueFile)
        self.tempURL =  "file:////%s" % (self.tempFile)

    def testLcgCp(self):

        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', self.remoteURL])

    def testLcgCpIntoNonExistDir(self):

        uniqDir = localtools.uniqueFileNameGenerator("GenDir").next();

        self.remoteURL = "srm://%s:8443/%s/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, uniqDir, self.uniqueFile)

        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', self.remoteURL])

    def testLcgGtGsiFtp(self):

        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['lcg-gt', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.remoteURL, 'gsiftp'] )

        self.execute(['srmrm', self.remoteURL])


    def testLcgLsFile(self):
        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['lcg-cp', '-b' , '-D', 'srmv2', '-T', 'srmv2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['lcg-ls', '-b' , '-T', 'srmv2', '-l', self.remoteURL] )

        self.execute(['srmrm', self.remoteURL])

    def testLcgLsDir(self):
        self.remoteURL = "srm://%s:8443/%s/%s" % (self.sut, self.ws2path, self.basepath)

        self.assertCommandPass( ['lcg-ls', '-b' , '-T', 'srmv2', '-l', self.remoteURL] )


    def tearDown(self):

        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)




if __name__ == '__main__':
    unittest.main()
