#!/usr/bin/env python

import unittest
import dcachetestcase
import os
import pydcap


class ROOTParallelOpenSuite(dcachetestcase.SETestCase):

    def __init__(self, methodName):
        dcachetestcase.SETestCase.__init__(self,methodName);

    def setUp(self):


        self.rootHome = os.environ.get("ROOTSYS")
        if (self.rootHome <= 0):
            self.fail("ROOTSYS not set")

        try:
            os.stat(self.rootHome + "/bin/root")
        except OSError:
            self.fail(self.rootHome + "/bin/root not found")

        self.prefix = os.environ.get("DATASET_PREFIX")
        if (self.prefix <= 0):
            self.fail("DATASET_PREFIX not set")

        self.filelistLocation = os.environ.get("DATASET_LIST")
        if (self.filelistLocation <= 0):
            self.fail("DATASET_LIST not set")


        #
        # read in the list of datafiles
        #
        file = open(self.filelistLocation, 'r')
        # each line in the file corresponds to a data file name,
        # remove trailing CRs and whitespaces from the end of each line
        self.filelist = [ line.rstrip(' \n') for line in file ]
        file.close()

        if len(self.filelist) < 1:
            self.fail("at least one datafile required")

    #
    # test if all files being part of the dataset are available from dCache (remote stat)
    # missing files get uploaded via dccp
    #
    def testBringDatasetOnline(self):

        print 'bringing dataset online'

        #make sure the url starts with dcap://, since we instrument dcap to stat and upload files
        url='dcap://' + self.prefix

        localdatasetdir = '/opt/d-cache/test/ROOT/H1Analysis/dataset/'

        for file in self.filelist:
            if (pydcap.dc_access(url + file, 0) != 0):

                print url + file + " not found, uploading from " + localdatasetdir + file

                self.assertCommandPass( ['/opt/d-cache/dcap/bin/dccp', '-A', localdatasetdir + file, url + file] )
                self.failIf( pydcap.dc_access(url + file, 0) != 0, url + file + " was uploaded but still not accessible")
            else:
                print url + file + " online"

        print "dataset upload complete"
        
    #
    # do the analysis against ROOT using xrootd
    #
    def testROOTAnalysisXrootd(self):

        workdir = "/opt/d-cache/test/ROOT/H1Analysis/"
        test = workdir+"h1_parallel_analysis.C"
        env = {"DATASET_PREFIX" : "root://" + self.prefix }

        print "starting analysis, io-protocol=xrootd"
        
        self.assertCommandPassWithENVs([self.rootHome+'/bin/root', '-b', '-q', 'dir', workdir, test], env)
        
        self.__cleanupOutput(workdir + "ROOT_output_file.xrootd")      
        


    #
    # do the analysis against ROOT using dcap
    #
    def testROOTAnalysisDcap(self):

        workdir = "/opt/d-cache/test/ROOT/H1Analysis/"
        test = workdir+"h1_parallel_analysis.C"
        env = {"DATASET_PREFIX" : "dcap://" + self.prefix }

        print "starting analysis, io-protocol=dcap" 

        self.assertCommandPassWithENVs([self.rootHome+'/bin/root', '-b', '-q', 'dir', workdir, test], env)
        
        self.__cleanupOutput(workdir + "ROOT_output_file.dcap")
                   
           
    #
    # helper method that reads the URL of the remote outputfile from the passed textfile
    # and then deletes both the remote file from dCache and the textfile
    #
    def __cleanupOutput(self, filename):
        
        file = open(filename, 'r')
        outputUrl = file.readline()
        file.close()
        
        if len(outputUrl) < 1:
            self.fail("incorrect URL of the outputfile")
        
        if (outputUrl.startswith("dcap://")):
            
            # does not work with unauthenticated dcap: permission denied
            # pydcap.dc_unlink(outputUrl)
            #
            # Unable to use gsiftp-rm, since owner of the file written with 
            # unauthenticated dcap is root:root 
            
            print "unable to perform cleanup of file " + outputUrl
        
        elif (outputUrl.startswith("root://")):
            
            # dirty workaround: use gsiftp-rm to delete the file and 
            # avoid "Permission denied"
             
            outputUrl = outputUrl.replace("root://", "gsiftp://")
            self.assertCommandPass(['/opt/edg/bin/edg-gridftp-rm', outputUrl])
            print "cleanup of file " + outputUrl +" successful."
            
        else:
        
            print "error: wrong protocol in url: " +  outputUrl

        os.remove(filename)        
             

if __name__ == '__main__':
    unittest.main()