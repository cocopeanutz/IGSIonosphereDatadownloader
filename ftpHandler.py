from ftplib import FTP
from ftplib import FTP_TLS
# cddis.nasa.gov/gnss/products/ionex/2020/256/esrg2560.20i.Z
# FTP
# ftps = FTP('cddis.nasa.gov')
# print(ftps.login())


# FTPS
def connectFTP_TLS():
    ftps = FTP_TLS('gdc.cddis.eosdis.nasa.gov')
    print(ftps.login(passwd='edobiasa@gmail.com'))
    print(ftps.prot_p())
    return ftps
def connectFTP():
    ftps = FTP('cddis.nasa.gov')
    print(ftps.login())
    return ftp

# def getFtpList()
# print(ftps.nlst('gnss/products/ionex/2020/256'))
# def callbackdata(data):
#     print('callback Called')
