#!/usr/bin/env python

import unittest
import dcachetestcase
import localtools


class SpaceManagerSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.surlBase = "srm://%s:8443/%s" % (self.sut, self.ws2path)
        self.uniqueFile = localtools.uniqueFileNameGenerator("SpaceManagerSuite").next()
        self.localFile = "/etc/profile"
        self.localURL = "file:////%s" % (self.localFile)

    def testGetSpaceTokens(self):
       self.assertCommandPass( [self.srmcp_home + '/bin/srm-get-space-tokens', '-space_desc=release_test_space', self.surlBase] )

    def testPutRemoved(self):
        self.remoteURL = "srm://%s:8443/%s/%s/%s" % (self.sut, self.ws2path, self.basepath, self.uniqueFile)

        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', self.localURL, self.remoteURL] )
        self.assertCommandPass( [self.srmcp_home + '/bin/srmrm', self.remoteURL])
        self.assertCommandPass( [self.srmcp_home + '/bin/srmcp','-2', '-retry_num=1', self.localURL, self.remoteURL] )


if __name__ == '__main__':
    unittest.main()
