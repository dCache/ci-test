import unittest
import string
import os
import select
import streamer
import localtools
import datetime


class SETestCase(unittest.TestCase):

    def __init__(self, methodName):
        self.commandOutput = ''
        unittest.TestCase.__init__(self, methodName);
        self.sut = os.environ.get("DFTS_SUT")
        self.basepath = os.environ.get("DFTS_BASEPATH")
        self.dCacheVersion = os.environ.get("DCACHE_VERSION")
        if self.dCacheVersion and self.dCacheVersion != "":
            elements = self.dCacheVersion.split('.')
            self.dCacheVersionMajor = int(elements[0])
            self.dCacheVersionMinor = int(elements[1])
        else:
            print
            print "    FAILED TO DISCOVER DCACHE VERSION"
            print
            print "        assuming 2.10"
            print
            self.dCacheVersionMajor = 2
            self.dCacheVersionMinor = 10

        self.ws1path = "srm/managerv1"

        self.user = os.environ.get("USER")

        try:
            self.timeout = int(os.environ.get("DFTS_TIMEOUT"))
        except:
            self.timeout = 0
            self.commandOutput = ''


    def dCacheOlderThan(self, version):
        elements = version.split('.')
        major = int(elements[0])
        minor = int(elements[1])
        return self.dCacheVersionMajor < major or (self.dCacheVersionMajor == major and self.dCacheVersionMinor < minor)

    def dCacheOlderThanOrIs(self, version):
        elements = version.split('.')
        major = int(elements[0])
        minor = int(elements[1])
        return self.dCacheVersionMajor < major or (self.dCacheVersionMajor == major and self.dCacheVersionMinor <= minor)

    def dCacheIs(self, version):
        elements = version.split('.')
        major = int(elements[0])
        minor = int(elements[1])
        return self.dCacheVersionMajor == major and self.dCacheVersionMinor == minor

    def dCacheNewerThanOrIs(self, version):
        elements = version.split('.')
        major = int(elements[0])
        minor = int(elements[1])
        return self.dCacheVersionMajor > major or (self.dCacheVersionMajor == major and self.dCacheVersionMinor >= minor)

    def dCacheNewerThan(self, version):
        elements = version.split('.')
        major = int(elements[0])
        minor = int(elements[1])
        return self.dCacheVersionMajor > major or (self.dCacheVersionMajor == major and self.dCacheVersionMinor > minor)

    def assertCommandPass(self, attributes, msg=None ):
        self.assertCommandPassWithENVs(attributes, None, msg)

    # similar to assertCommandPass(), but you additionally need to specify a dictionary of
    # key-value-pairs of environment variables, which you want to have applied before
    # the command gets executed. This only affects the child process.
    def assertCommandPassWithENVs(self, attributes, newENVs, msg=None ):

        (rc, output) = self.__executeCommand(attributes, newENVs)

        if rc == 0:
            print "[%s] OK: %s" % (self.duration, " ".join(attributes))
        else:
            print "[%s] FAILED: %s" % (self.duration, " ".join(attributes))
            print "    " + output.replace('\n', '\n    ')
            print output

        if msg is None:
            msg = output

        self.failIf( rc != 0, msg)


    def assertCommandFail(self, attributes,  msg=None ):
        self.assertCommandFailWithENVs(attributes, None, msg )

    # similar to assertCommandFail(), but you additionally need to specify a dictionary of
    # key-value-pairs of environment variables, which you want to have applied before
    # the command gets executed. This only affects the child process.
    def assertCommandFailWithENVs(self, attributes, newEnvs, msg=None ):

        (rc, output) = self.__executeCommand(attributes, newEnvs)

        if rc == 0:
            print "[%s] FAILED (unexpected succeeded): %s" % (self.duration, " ".join(attributes))
            print "    " + output.replace('\n', '\n    ')
        else:
            print "[%s] OK (expected failure): %s" % (self.duration, " ".join(attributes))

        if msg is None:
            msg =  output

        self.failIf( rc == 0, msg)
        return self.commandOutput

    def execute(self, attributes):
        (rc, output) = self.__executeCommand(attributes)
        if rc == 0:
            print "[%s] Ran : %s" % (self.duration, " ".join(attributes))
        else:
            print "[%s] Ran (rc=%s): %s" % (self.duration, rc, " ".join(attributes))
            print output
            print "        " + output.replace('\n', '\n         ')
        return output


    def executeIgnoreFailure(self, attributes):
        (rc, output) = self.__executeCommand(attributes)
        if rc == 0:
            print "[%s] Ran: %s" % (self.duration, " ".join(attributes))
        else:
            print "[%s] Ran (rc=%s): %s" % (self.duration, rc, " ".join(attributes))


    def __executeCommand(self, attributes, additionalENVs=None):
        executable = attributes[0]

        self.externalCommand = streamer.childprocessstreeam()

        self.externalCommand.executableSet(executable)
        self.externalCommand.attributesSet(attributes)

        self.externalCommand.CallBackSet(1,self.collectorStdErrOut)
        self.externalCommand.CallBackSet(2,self.collectorStdErrOut)
        if self.timeout > 0:
            self.externalCommand.timeOutSecondsCallBackSet(self.timeout,self.collectorTimeout,None)

        # set environments variables if specified
        if additionalENVs is not None:

            # get a deep copy of the environment dictionary
            env = dict(self.externalCommand.environmentGet())

            for k, v in additionalENVs.iteritems():
                env[k] = v

            self.externalCommand.environmentSet(env)

        self.commandOutput = ''

        rc = self.externalCommand.run()

        self.duration = str(datetime.timedelta(seconds=self.externalCommand.duration))
        index = string.find(self.duration, '.')
        if index != -1:
            self.duration = self.duration[:index+2]

        return (rc, self.commandOutput)


    def assertSameSum(self, original, compareto):
        self.assertEqual(localtools.md5sum(original),localtools.md5sum(compareto) , "Checksum do not match")


    def collectorStdErrOut(self,handle,output,EventFileDesc):
        if ( EventFileDesc and select.POLLIN):
            self.commandOutput += output.replace('<','&lt;').replace('>','&gt;')

    def collectorTimeout(self,obj):
        self.externalCommand.abort()
