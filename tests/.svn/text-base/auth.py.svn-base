#!/usr/bin/env python

import unittest
import dcachetestcase
import localtools


class AuthSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):
        self.surlBase = "srm://%s:8443/%s" % (self.sut, self.ws2path)

    # this test require special setup on SRM:
    #    two space tokens have to be generated one for production role, one without role:
    #
    #  reserve -vog=/desy -vor=production 10 "-1"
    #  reserve -vog=/desy  10 "-1"
    #
    # according to current implementation ( 12.06.2008 ) get-space-tokens returns a list of tokens
    # which can be used by requesters group and role 
    # test checks that after changing the role, returned list changed as well
    def testCredentialCaching(self):
        self.assertCommandPass( ['/opt/glite/bin/voms-proxy-init','--voms', 'desy:/desy/Role=production'] )
        tokens1 = self.assertCommandPass( ['/opt/d-cache/srm/bin/srm-get-space-tokens', self.surlBase] )

        self.assertCommandPass( ['/opt/glite/bin/voms-proxy-init'] )
        toekns2 = self.assertCommandPass( ['/opt/d-cache/srm/bin/srm-get-space-tokens', self.surlBase] )

        self.assertNotEquals(tokens1 , toekns2 , "differ roles got same list")

if __name__ == '__main__':
    unittest.main()


