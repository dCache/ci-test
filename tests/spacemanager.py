#!/usr/bin/env python

import unittest
import dcachetestcase
import localtools


class SpaceManagerSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.surlBase = "srm://%s/" % (self.sut)
        self.uniqueFile = localtools.uniqueFileNameGenerator("SpaceManagerSuite").next()
        self.localFile = "/etc/profile"
        self.localURL = "file:////%s" % (self.localFile)

    def testGetSpaceTokens(self):
       self.assertCommandPass( ['srm-get-space-tokens', '-space_desc=release_test_space', self.surlBase] )

    def testPutRemoved(self):
        self.remoteURL = "srm://%s%s/%s" % (self.sut, self.basepath, self.uniqueFile)

        self.assertCommandPass( ['srmcp','-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( ['srmrm', self.remoteURL])
        self.assertCommandPass( ['srmcp','-2', '-retry_num=1', self.localURL, self.remoteURL] )


if __name__ == '__main__':
    unittest.main()
