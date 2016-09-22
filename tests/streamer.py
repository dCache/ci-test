
import commands
import popen2
import fcntl
import os
import select
from time import sleep
import sys
import time

LAUNCHER_PIPE_READ = 0
LAUNCHER_PIPE_WRITE = 1
LAUNCHER_PIPE_IGNORE = 2

def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd,fcntl.F_GETFL)
    try:
        fcntl.fcntl(fd,fcntl.F_SETFL,fl | os.O_NDELAY)
    except AttributeError:
        fcntl.fcntl(fd,fcntl.F_SETFL,fl | os.FNDELAY)

class launcherpipe:
    def __init__(self,childFd,Mode):
        self.childFd = childFd
        self.mode = Mode
    def initiate(self):

        if self.mode == LAUNCHER_PIPE_READ:
            self.FdPairent,self.FdChild = os.pipe()
        if self.mode == LAUNCHER_PIPE_WRITE:
            self.FdChild,self.FdPairent = os.pipe()
        if self.mode == LAUNCHER_PIPE_IGNORE:
            self.FdPairent = -1
            self.FdChild = os.open("/dev/null", os.O_RDWR)
        #print "self.childFd=%s" % (self.childFd)
        #print "self.FdChild=%s" % (self.FdChild)
        #print "self.FdPairent=%s" % (self.FdPairent)
    def connectChild(self):
        if self.FdPairent > 0:
            os.close(self.FdPairent)
            self.FdPairent = -1
        if self.FdChild > 0 and self.childFd > 0 :
            #print "self.childFd=%s" % (self.childFd)
            #print "self.FdChild=%s" % (self.FdChild)
            #print "self.FdPairent=%s" % (self.FdPairent)
            os.close(self.childFd)

            os.dup2(self.FdChild,self.childFd)
            os.close(self.FdChild)
            self.FdChild = -1


    def connectPairent(self):
        if self.FdChild > 0:
            os.close(self.FdChild)
            self.FdChild = -1


class launcher:
    def __init__(self):
        self.pipeList = []
        self.Attributes = []
    def pipeCreate(self,child_fd, PipeType):
        for pipe in self.pipeList:
            if pipe.childFd == child_fd:
                self.pipeList.remove(pipe)
        newpipe = launcherpipe(child_fd, PipeType)
        self.pipeList.append(newpipe)

    def pipeFree(self,child_fd):
        for pipe in self.pipeList:
            if pipe.childFd == child_fd:
                pipe.close()
                self.pipeList.remove(pipe)
    def pipeGet(self,child_fd):
        for pipe in self.pipeList:
            if pipe.childFd == child_fd:
                return pipe.FdPairent
        return -1
    def pidGet(self):
        if hasattr(self,"pid"):
            return self.pid
        return -1
    def executableSet(self,executable):
        self.executable = executable

    def attributesSet(self,Attributes):
        self.attributes = Attributes

    def environmentGet(self):
        if not hasattr (self,"environment"):
            self.environment = os.environ
        return self.environment
    def environmentSet(self,environment):
        self.environment = environment
        return self.environment

    def launch(self):
        for pipe in self.pipeList:
            pipe.initiate()

        processid = os.fork()
        if processid < 0:
            print "error forking"
            return -1
        if processid == 0:
            # this is child
            for pipe in self.pipeList:
                pipe.connectChild()

            os.execvpe(self.executable, self.attributes,self.environmentGet())

            sys.exit(127)
        if processid > 0:
            self.pid = processid
            for pipe in self.pipeList:
                pipe.connectPairent()

    def kill(self,singal):
        return os.kill(self.pidGet(), singal)

    def running(self):
        Result = False

        if 0 > self.pidGet():
            try:
                (var1,var2) = os.waitpid(self.pidGet(), os.WNOHANG)
            except:
                pass
            print var1,var2

        return Result


class childprocessstreeampipe:
    def __init__(self):
        self.fileDes = 0
        self.fileDesPairent = None
        self.Callbacks = []
    def setFileDesPairent(self,FileId):
        self.fileDesPairent  = FileId
    def fileno(self):
        return self.fileDesPairent

    def register(self,function,callerId):
        self.Callbacks.append([function,callerId])
        return
    def callback(self,text,selectBitmask):
        for callback in self.Callbacks:
            callback[0](callback[1],text,selectBitmask)

class childprocessstreeam:
    def __init__(self):
        self.Command = "sleep 10"
        self.ConnectorList = []
        self.timeOutSecondsCallBackSeconds = 1000000000
        self.timeOutSecondsCallBackContext = None
    def executableSet(self,Command):
        self.Command = Command

    def environmentGet(self):
        if not hasattr (self,"environment"):
            self.environment = os.environ
        return self.environment
    def environmentSet(self,environment):
        self.environment = environment
        return self.environment

    def CallBackSet(self,fileID, function, callerId = None):
        # Sets the CallBacks to give for
        # fileID = Os file descriptor
        # function = Function to call back
        # callerId attribute of the function you call
        #
        # The Callback must have 3 parameters
        # callerId, output, EventFileDesc
        Found = False
        for connector in self.ConnectorList:
            if connector.fileDes == fileID:
                connector.register(function, callerId)
                Found = True

        if not Found:
            newChildFdCallBack = childprocessstreeampipe()
            newChildFdCallBack.fileDes = fileID
            newChildFdCallBack.register(function, callerId)
            self.ConnectorList.append(newChildFdCallBack)
        #print self.ConnectorList



    def attributesSet(self,attributes):
        self.Attributes = attributes
        return self.Attributes

    def attributesGet(self):
        return self.Attributes

    def timeOutSecondsCallBackSet(self,seconds,function, callerId = None):
        self.timeOutSecondsCallBackSeconds = seconds
        self.timeOutSecondsCallBack = function
        self.timeOutSecondsCallBackContext = callerId


    def timestamp(self):
        self.TimeStamp = time.time()

    def timeout(self):
        TimeCurrnet = time.time()
        if TimeCurrnet > self.TimeStamp + (self.timeOutSecondsCallBackSeconds / 1000):
            self.timestamp()
            return True
        if TimeCurrnet < self.TimeStamp:
            self.timestamp()
            return True
        return False


    def run(self):
        # New improved version
        pobj = select.poll()
        lobj = launcher()
        lobj.executableSet(self.Command)
        lobj.attributesSet(self.Attributes)
        lobj.environmentSet(self.environmentGet())
        starttime = time.time()
        outfdlist = []
        for connection in self.ConnectorList:

            # Create a pipe to read
            lobj.pipeCreate(connection.fileDes,LAUNCHER_PIPE_READ)

            #holder = childprocessstreeampipe()
            #holder.fileDes = key
            #outfdlist.append(holder)
            #print key
            #print
            # value = self.CallBacks[key]
            #self.CallBacks[key] + lobj.pipeGet(key)
            #holder.fileno
            #outfdlist.append(key)
            #self.CallBacks[key].append(os.fdopen(self.CallBacks[key][3]))

            #ready[0]

        lobj.launch()
        self.timestamp()
        #child = popen2.Popen3(self.Command,1)
        #child.tochild.close()
        #outfile = child.fromchild
        #outfdlist = outfile.fileno()
        #print outfdlist

        for outfile in self.ConnectorList:

            outfile.setFileDesPairent(lobj.pipeGet(outfile.fileDes))



            pobj.register(outfile.fileDesPairent, select.POLLIN)

            outfile.childFileObjStdOut = os.fdopen(outfile.fileDesPairent)
            makeNonBlocking(outfile.fileDesPairent)
        #slect1 = outfdlist[0]
        #print int(selectlistIwtd)
        childFdStdOutEof = False
        var1 = 0
        self.somethingtoread = True
        self.wanttoread = True
        while (self.wanttoread and self.somethingtoread):
            tocheck = [outfdlist]*(not childFdStdOutEof)
            #print tocheck
            #print outfdlist
            tocheck = []
            #ready = select.select(tocheck,[],[],float(1))
            ready = pobj.poll(1)
            #print "ready=%s" % (ready)
            for filedescevent in ready:
                #print filedescevent

                for outfile in self.ConnectorList:
                    #print int(outfile.fileDesPairent),filedescevent[0]
                    if outfile.fileDesPairent == filedescevent[0]:
                        #print "match found"
                        outchunk = ""
                        if (filedescevent[1] and select.POLLIN):
                            outchunk = outfile.childFileObjStdOut.read()

                        outfile.callback(outchunk,filedescevent[1])


            #print "childpid=%s" % (child.pid)
            #print ready
            if 0 == len( ready):
                #outchunk = outfile.read()
                (var1,var2) = os.waitpid(lobj.pidGet(), os.WNOHANG)
                if lobj.pidGet() == var1:
                    #print "exiting"
                    ready = pobj.poll(float(1))
                    if 0 == len( ready):
                        self.somethingtoread = False
                else:
                    if self.timeout():
                        if hasattr(self,"timeOutSecondsCallBack"):
                            self.timeOutSecondsCallBack(self.timeOutSecondsCallBackContext)
            else:
                if var1 == lobj.pidGet():
                    self.somethingtoread = False

            if (var1 != lobj.pidGet()):
                (var1,var2) = os.waitpid(lobj.pidGet(), os.WNOHANG)
            else:
                self.retCode = var2
        if ( not self.wanttoread ) and not hasattr(self,"retCode"):
            lobj.kill(9)
            #print "Killing child process"
            (var1,var2) = os.waitpid(lobj.pidGet(), os.WNOHANG)
            self.retCode = var2

        self.duration = time.time() - starttime

        return (self.retCode)



    def abort(self):
        self.wanttoread = False

def test0():
    pipe = launcherpipe(4,LAUNCHER_PIPE_READ)
    pipe.initiate()
    os.write(pipe.FdChild,"hello")
    print os.read(pipe.FdPairent,100)

def testLauncher():
    lobj = launcher()
    lobj.executableSet("sleep")
    #lobj.pipeCreate(1,LAUNCHER_PIPE_READ)
    lobj.pipeCreate(1,LAUNCHER_PIPE_READ)
    lobj.pipeCreate(0,LAUNCHER_PIPE_IGNORE)
    lobj.pipeCreate(2,LAUNCHER_PIPE_IGNORE)
    lobj.executableSet("/bin/sleep")
    lobj.attributesSet(['sleep','--help'])
    lobj.launch()
    print "fildes=%s" % lobj.pipeGet(2)
    print lobj.pipeList[0].FdPairent
    fd = os.read(lobj.pipeGet(1),100)
    print "Application output is"
    print fd
    print "Application output is now finished"

def test2Callbacktest1(param1,param2,param3):
    pass

    if ( param3 and select.POLLIN):
        print "test2Callbacktest1 call back '%s','%s'" % (param1,param2)
    if (param3 and select.POLLHUP):
        print "We have a hang up '%s'"  % (param1)
    if (param3 and select.POLLOUT):
        print "Ready for output: writing will not block '%s'"  % (param1)
    if (param3 and select.POLLERR):
        print "Error condition of some sort '%s'"  % (param1)
    if (param3 and select.POLLNVAL):
        print "Invalid request: descriptor not open '%s'"  % (param1)

def test2Callbacktest2(param1,param2,param3):
    if ( param3 and select.POLLIN):
        print "test2Callbacktest2 call back '%s','%s'" % (param1,param2)
    if (param3 and select.POLLHUP):
        print "We have a hang up '%s'"  % (param1)
    if (param3 and select.POLLOUT):
        print "Ready for output: writing will not block '%s'"  % (param1)
    if (param3 and select.POLLERR):
        print "Error condition of some sort '%s'"  % (param1)
    if (param3 and select.POLLNVAL):
        print "Invalid request: descriptor not open '%s'"  % (param1)


def test2CallbacktimeOut(param1):
    print "timeout %s" % (param1.value)

    param1.value += 1
    if param1.value > 3:
        param1.lobj.abort()


def testChildProcessStreeam():
    lobj = childprocessstreeam()

    lobj.executableSet("/bin/ls")
    #lobj.pipeCreate(1,LAUNCHER_PIPE_READ)
    #lobj.CallBackSet(1,test2Callbacktest)
    lobj.CallBackSet(1,test2Callbacktest1,"Stdout")
    lobj.CallBackSet(2,test2Callbacktest2,"EtdErr")

    lobj.attributesSet(['ls with incorrect cmd','help'])
    print "Application output is"
    rc = lobj.run()
    print "Application output is now finished with code %i"  %(rc)
    lobj.attributesSet(['ls with correct help','--help'])
    print "Application output is"
    rc = lobj.run()
    print "Application output is now finished with code %i"  %(rc)

class bill:
    def __init__(self):
        self.value = 1



def testChildProcessStreeamCallbackTimeOut():
    lobj = childprocessstreeam()
    TimeOutStateObj = bill()
    TimeOutStateObj.lobj = lobj
    lobj.executableSet("/bin/sleep")
    lobj.attributesSet(['sleep','5'])
    lobj.timeOutSecondsCallBackSet(1000,test2CallbacktimeOut,TimeOutStateObj)
    rc = lobj.run()

    print "Application output is now finished with code %i"  %(rc)
if __name__ == "__main__":
    #testLauncher()
    testChildProcessStreeamCallbackTimeOut()
