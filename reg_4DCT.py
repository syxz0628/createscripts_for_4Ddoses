import os

class class_reg_4DCT():
    def __init__(self,patinfo):
        self.patinfo=patinfo
        self.fileversion = 1.0
    def fun_auto_reg_4DCT(self):
        print("start registrate 4D CTs for all patients listed in patinfo.txt")
        print(self.patinfo.patientName)
        for patientNo in range(0,len(self.patinfo.patientName)):
            print("trying plastimatch in: ",self.patinfo.patientName[patientNo])
            FDctdir='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(self.patinfo.patientID[patientNo]) + '/' + \
                        str(self.patinfo.ctName[patientNo]) + '/' + 'ctx/'
            refCTname = FDctdir + str(self.patinfo.patientName[patientNo]) + '_00.nrrd'
            outputname='./' + str(self.patinfo.patientID[patientNo]) + '/' + \
                        str(self.patinfo.ctName[patientNo]) + '/' + 'Reg/'
            execommand = 'python /u/motion/Software/RegistrationScript/createPlastimatchScript.py F ' + refCTname + ' -D ' + FDctdir + ' -O ' + outputname + ' -n ' + \
                         str(self.patinfo.patientName[patientNo]) + ' -t bspline -S -p 32'
            print(execommand)
            #tmp = os.popen(execommand).readlines()
            print("finished plastimatch in: ",self.patinfo.patientName[patientNo])