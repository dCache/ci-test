#!/usr/bin/env python

import unittest
import dcachetestcase
import localtools
import os


class SrmCpSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.uniqueFile = localtools.uniqueFileNameGenerator("SrmCpSuite").next()
        self.uniqueFile1 = localtools.uniqueFileNameGenerator("SrmCpSuite1").next()
        self.localFile = "/etc/profile"
        self.localURL = "file:////%s" % (self.localFile)
        self.tempFile = "/tmp/%s" % (self.uniqueFile)
        self.tempURL =  "file:////%s" % (self.tempFile)

    def testV2Copy(self):

        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL])

    def testV2CopyMD5(self):

        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', '-cksm_type=MD5', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL])

    def testV1Copy(self):

        self.remoteURL = "srm://%s:8443/%s/%s" % (self.sut, self.basepath, self.uniqueFile)
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-1', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-1', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL])

    def testv2CopyBadChecksum(self):
        #
        # while srmcp calculates checksum prior transfer
        # modified file will produce differ checksum
        #
        self.localURL = "file://///proc/uptime"
        self.remoteURL = "srm://%s:8443/%s/%s" % (self.sut, self.basepath, self.uniqueFile)
        self.assertCommandFail( [self.srmcp_home + '/bin/srmcp','-1','-retry_num=', '1', self.localURL, self.remoteURL] )

        self.executeIgnoreFailure([self.srmcp_home + '/bin/srmrm', self.remoteURL])

    def testv2CopyBadChecksumMD5(self):
        #
        # while srmcp calculates checksum prior transfer
        # modified file will produce differ checksum
        #
        self.localURL = "file://///proc/uptime"
        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)
        self.assertCommandFail( [self.srmcp_home + '/bin/srmcp','-1','-retry_num=', '1', '-cksm_type=MD5', self.localURL, self.remoteURL] )

        self.executeIgnoreFailure([self.srmcp_home + '/bin/srmrm', self.remoteURL])

    def testV2CopyDirNotExist(self):

        uniqDir = localtools.uniqueFileNameGenerator("GenDir").next();

        self.remoteURL = "srm://%s:8443/%s/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, uniqDir, self.uniqueFile)

        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL])
        dirURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, uniqDir)
        self.execute([self.srmcp_home + '/bin/srmrmdir', dirURL])

    def testSrmLsValidPAth(self):
        self.remoteURL = "srm://%s:8443/%s/%s" % (self.sut, self.ws2path, self.basepath)
        self.assertCommandPass( [self.srmcp_home + '/bin/srmls', '-2', self.remoteURL] )

    def testSrmLsInValidPAth(self):

        self.remoteURL = "srm://%s:8443/%s/var/log" % (self.sut, self.ws2path)
        self.assertCommandFail( [self.srmcp_home + '/bin/srmls', '-2', self.remoteURL] )

    def testSrmChangePerm(self):
        uniqDir = localtools.uniqueFileNameGenerator("GenDir").next();
        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, uniqDir)
        self.assertCommandPass( [self.srmcp_home + '/bin/srmmkdir', self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srm-set-permissions','-2','-type=CHANGE','-other=NONE', self.remoteURL] )
        dirURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, uniqDir)
        self.execute([self.srmcp_home + '/bin/srmrmdir', dirURL])

    def testSrmmvIntoSame(self):
        self.remoteSourceURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)
        self.remoteDestURL = "srm://%s:8443/%s/%s/./%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)
        self.assertCommandPass([self.srmcp_home + '/bin/srmcp', '-2', self.localURL, self.remoteSourceURL])
        self.assertCommandPass([self.srmcp_home + '/bin/srmmv', self.remoteSourceURL, self.remoteDestURL])
        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteSourceURL])

    def testV2CopyHTTP(self):

        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)
        self.remoteURL1 = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile1)
        self.remoteHTTP = "http://%s:2880/%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.remoteHTTP, self.remoteURL1] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.remoteURL1, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL])
        self.execute([self.srmcp_home + '/bin/srmrm', self.remoteURL1])

def tearDown(self):

        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)




if __name__ == '__main__':
    unittest.main()
