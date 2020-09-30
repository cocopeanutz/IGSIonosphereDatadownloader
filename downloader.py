import os
import errno

def createDir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
def downloadFile(filename, ftps):
    localFilename = 'data/' + filename
    createDir(localFilename)
    localfile = open(localFilename, 'wb')
    ftps.retrbinary('RETR ' + filename, localfile.write)
# 101, 202, 303 not a directory why?
