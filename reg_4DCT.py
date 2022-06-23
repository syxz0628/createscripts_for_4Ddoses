import os

class class_reg_4DCT():
    def __init__(self,patinfo):
        self.patinfo=patinfo
        self.fileversion = 1.0
    def fun_auto_reg_4DCT(self,path2patinfo):
        print("start registrate 4D CTs for all patients listed in patinfo.txt")
        print(self.patinfo.patientName)
        if path2patinfo.rfind('/')!=-1:
            regshfile=path2patinfo[:path2patinfo.rfind('/')]+'02_CreatePlastimatch4D.sh'
        else:
            regshfile = '/u/ysheng/MyAIXd/projects/patient/commands/02_CreatePlastimatch4D.sh'
        with open(regshfile,'w+') as createplastimath:
            for patientNo in range(0,len(self.patinfo.patientName)):
                createplastimath.writelines("#trying plastimatch in: "+self.patinfo.patientName[patientNo]+os.linesep)
                FDctdir='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(self.patinfo.patientID[patientNo]) + '/' + \
                            str(self.patinfo.ctName[patientNo]) + '/' + 'ctx/'
                refCTname = FDctdir + str(self.patinfo.patientName[patientNo]) + '_00.nrrd'
                outputname='./' + str(self.patinfo.patientID[patientNo]) + '/' + \
                            str(self.patinfo.ctName[patientNo]) + '/' + 'Reg/'
                execommand = 'python /u/motion/Software/RegistrationScript/createPlastimatchScript.py F ' + refCTname + ' -D ' + FDctdir + ' -O ' + outputname + ' -n ' + \
                             str(self.patinfo.patientName[patientNo]) + ' -t bspline -S -p 32'
                rmcommand='rm -rf '+outputname+'*'
                createplastimath.writelines(rmcommand+os.linesep+execommand+os.linesep)
                #tmp = os.popen(execommand).readlines()
                createplastimath.writelines("#finished plastimatch for: "+self.patinfo.patientName[patientNo]+os.linesep+os.linesep)