import unittest
import os
import select
import streamer
import localtools



class SETestCase(unittest.TestCase):

    def __init__(self, methodName):
        self.commandOutput = ''
        unittest.TestCase.__init__(self, methodName);
        self.sut = os.environ.get("DFTS_SUT")
        self.basepath = os.environ.get("DFTS_BASEPATH")
#        self.ws1path = os.environ.get("SRMV1WS")
#        self.ws2path = os.environ.get("SRMV2WS")

        self.ws1path = "srm/managerv1"
        self.ws2path = "srm/managerv2?SFN="

        self.user = os.environ.get("USER")

        #
        # locations of client tools
        #
        self.srmcp_home = os.environ.get('DFTS_SRMCP_HOME', '/opt/d-cache/srm')
        self.globus_home = os.environ.get('DFTS_GLOBUS_HOME', '/opt/globus')
        self.glite_home = os.environ.get('DFTS_GLITE_HOME', '/opt/lcg')
        self.edg_home = os.environ.get('DFTS_EDG_HOME', '/opt/edg')

        try:
            self.timeout = int(os.environ.get("DFTS_TIMEOUT"))
        except:
            self.timeout = 0
            self.commandOutput = ''



    def assertCommandPass(self, attributes, msg=None ):
        self.assertCommandPassWithENVs(attributes, None, msg)

    # similar to assertCommandPass(), but you additionally need to specify a dictionary of
    # key-value-pairs of environment variables, which you want to have applied before
    # the command gets executed. This only affects the child process.
    def assertCommandPassWithENVs(self, attributes, newENVs, msg=None ):

        (rc, output) = self.__executeCommand(attributes, newENVs)

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

        if msg is None:
            msg =  output

        self.failIf( rc == 0, msg)
        return self.commandOutput

    def execute(self, attributes):
        (rc, output) = self.__executeCommand(attributes)
        return output

    def __executeCommand(self, attributes, additionalENVs=None):

        executable = attributes[0]

        self.failIf( not os.path.exists(executable), "%s : doesn't exist or not an absolute path" % executable)

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



        rc = self.externalCommand.run()
        return (rc, self.commandOutput)

    def assertSameSum(self, original, compareto):
        self.assertEqual(localtools.md5sum(original),localtools.md5sum(compareto) , "Check sum do not match")


    def collectorStdErrOut(self,handle,output,EventFileDesc):

        if ( EventFileDesc and select.POLLIN):
            self.commandOutput += output.replace('<','&lt;').replace('>','&gt;')

    def collectorTimeout(self,obj):
        self.externalCommand.abort()
