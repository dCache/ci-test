from __future__ import generators
import time
import shutil
import os
import md5

def sumfile(fobj):
    '''Returns an md5 hash for an object with read() method.'''
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def uniqueFileNameGenerator(prefix):
    iterator = 0
    while 1:
        output = "%s.%s.%s.%s.%s.%s" % (prefix,os.uname()[1],os.getuid(),os.getpid(),time.strftime("%Y%m%d%H%M%S",time.gmtime()),iterator)    
        yield output
        iterator += 1

def md5sum(filePath):
    f = file(filePath, 'rb')
    ret = sumfile(f)
    f.close()
    return ret



class LocalTestDir:
    def __init__(self):
        self.path = os.environ["HOME"] + time.strftime("/dcacheTestSuite.%Y%m%d%H%M%S/",time.gmtime())
        while os.path.exists(self.path):
            os.sleep(1)
            self.path = os.environ["HOME"] + time.strftime("%Y%m%d%H%M%S",time.gmtime())
        os.mkdir(self.path)
        self.fileNameGenerator = uniqueFileNameGenerator(self.path + "tmpfile")
        self.fileMd5sum = {}
    
    def localFileAdd(self,srcPath):
        newname = self.fileNameGenerator.next()
        shutil.copy(srcPath,newname)
        self.fileMd5sum[newname] = md5sum(newname)
        return newname

    def fileNameGenerate(self):
        return self.fileNameGenerator.next()
        
    def filesMd5sum(self):
        for fileName in os.listdir(self.path):
            if fileName not in self.fileMd5sum.keys():
                self.fileMd5sum[self.path + fileName] = md5sum(self.path + fileName)
        
    def __del__(self):
        for i in os.listdir(self.path):
            os.remove(self.path + i)
        os.rmdir(self.path)
