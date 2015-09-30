import os
from RSAtools import RSAtools
from fileUtils import FileUtils

if __name__ == '__main__' :
    rsa = RSAtools()
    fileUtil = FileUtils()
    rsaClient = rsa.generateRSAkey(1024)
    rsaCommercant = rsa.generateRSAkey(1024)
    rsaBanque = rsa.generateRSAkey(1024)

    """n,e,d"""
    clientpk = open('clientPk','w')
    clientpk.write(str(rsaClient [0])+' '+str(rsaClient [1]))
    clientpk.close()
    clientsk = open('clientSk','w')
    clientsk.write(str(rsaClient [0])+' '+str(rsaClient [2]))
    clientsk.close()
    commercantpk = open('commercantPk','w')
    commercantpk.write(str(rsaCommercant [0])+' '+str(rsaCommercant [1]))
    commercantpk.close()
    commercantsk = open('commercantSk','w')
    commercantsk.write(str(rsaCommercant [0])+' '+str(rsaCommercant [2]))
    commercantsk.close()
    banquepk = open('banquePk','w')
    banquepk.write(str(rsaBanque [0])+' '+str(rsaBanque [1]))
    banquepk.close()
    banquesk = open('banqueSk','w')
    banquesk.write(str(rsaBanque [0])+' '+ str(rsaBanque [2]))
    banquesk.close()
    clientpkencode = str(rsa.encrypt_sk_str(fileUtil.recupKey('banqueSk'), fileUtil.recupLine('clientPk')))
    clientpkencodefile = open('clientPkEncode','w')
    clientpkencodefile.write(clientpkencode)
    clientpkencodefile.close()

    