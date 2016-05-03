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

        self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', '-retry_num=0', self.remoteURL])

    def testV2CopyMD5(self):

        self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', '-cksm_type=MD5', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', '-retry_num=0', self.remoteURL])

    def testV1Copy(self):
        if self.dCacheVersionIsBefore("2.16"):
            self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)
            self.assertCommandPass( ['srmcp', '-retry_num=0', '-1', self.localURL, self.remoteURL] )
            self.assertCommandPass( ['srmcp', '-retry_num=0', '-1', self.remoteURL, self.tempURL] )
            self.assertSameSum(self.localFile, self.tempFile)

            self.execute(['srmrm', '-retry_num=0', self.remoteURL])

        else:
            print "Skipped test as dCache is v{}".format(self.dCacheVersion)

    def testv2CopyBadChecksum(self):
        if self.dCacheVersionIsBefore("2.16"):
            #
            # while srmcp calculates checksum prior transfer
            # modified file will produce differ checksum
            #
            self.localURL = "file://///proc/uptime"
            self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)
            self.assertCommandFail( ['srmcp', '-retry_num=0', '-1','-retry_num=', '1', self.localURL, self.remoteURL] )

            self.executeIgnoreFailure(['srmrm', '-retry_num=0', self.remoteURL])

        else:
            print "Skipped test as dCache is v{}".format(self.dCacheVersion)

    def testv2CopyBadChecksumMD5(self):
        if self.dCacheVersionIsBefore("2.16"):
            #
            # while srmcp calculates checksum prior transfer
            # modified file will produce differ checksum
            #
            self.localURL = "file://///proc/uptime"
            self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)
            self.assertCommandFail( ['srmcp', '-retry_num=0', '-1', '-cksm_type=MD5', self.localURL, self.remoteURL] )

            self.executeIgnoreFailure(['srmrm', '-retry_num=0', self.remoteURL])

        else:
            print "Skipped test as dCache is v{}".format(self.dCacheVersion)

    def testV2CopyDirNotExist(self):

        uniqDir = localtools.uniqueFileNameGenerator("GenDir").next();

        self.remoteURL = "srm://%s%s/%s/%s" % (self.sut, self.basepath, uniqDir, self.uniqueFile)

        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.remoteURL, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', '-retry_num=0', self.remoteURL])
        dirURL = "srm://%s%s/%s" % (self.sut, self.basepath, uniqDir)
        self.execute(['srmrmdir', '-retry_num=0', dirURL])

    def testSrmLsValidPAth(self):
        self.remoteURL = "srm://%s%s/" % (self.sut, self.basepath)
        self.assertCommandPass( ['srmls', '-retry_num=0', '-2', self.remoteURL] )

    def testSrmLsInValidPAth(self):

        self.remoteURL = "srm://%s/var/log" % (self.sut)
        self.assertCommandFail( ['srmls', '-retry_num=0', '-2', self.remoteURL] )

    def testSrmChangePerm(self):
        uniqDir = localtools.uniqueFileNameGenerator("GenDir").next();
        self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, uniqDir)
        self.assertCommandPass( ['srmmkdir', '-retry_num=0', self.remoteURL] )
        self.assertCommandPass( ['srm-set-permissions','-2','-type=CHANGE','-other=NONE', self.remoteURL] )
        dirURL = "srm://%s%s/%s" % (self.sut, self.basepath, uniqDir)
        self.execute(['srmrmdir', '-retry_num=0', dirURL])

    def testSrmmvIntoSame(self):
        self.remoteSourceURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)
        self.remoteDestURL = "srm://%s%s/./%s" % (self.sut, self.basepath, self.uniqueFile)
        self.assertCommandPass(['srmcp', '-retry_num=0', '-2', self.localURL, self.remoteSourceURL])
        self.assertCommandPass(['srmmv', '-retry_num=0', self.remoteSourceURL, self.remoteDestURL])
        self.execute(['srmrm', '-retry_num=0', self.remoteSourceURL])

    def testV2CopyHTTP(self):

        self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)
        self.remoteURL1 = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile1)
        self.remoteHTTP = "http://%s:2880/%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.remoteHTTP, self.remoteURL1] )
        self.assertCommandPass( ['srmcp', '-retry_num=0', '-2', self.remoteURL1, self.tempURL] )
        self.assertSameSum(self.localFile, self.tempFile)

        self.execute(['srmrm', '-retry_num=0', self.remoteURL])
        self.execute(['srmrm', '-retry_num=0', self.remoteURL1])

def tearDown(self):

        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)




if __name__ == '__main__':
    unittest.main()
