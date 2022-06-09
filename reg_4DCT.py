import os

class class_reg_4DCT():
    def __init__(self,patinfo):
        self.patinfo=patinfo
        self.fileversion = 1.0
    def fun_auto_reg_4DCT(self):
        print("start registrate 4D CTs for all patients listed in patinfo.txt")
        print(self.patinfo.patientName)
        for patientNo in range(0,len(self.patinfo.patientName)):
            FDctdir='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + self.patinfo.patientID[patientNo] + '/' + \
                        self.patinfo.ctName[patientNo] + '/' + 'ctx/'
            refCTname = FDctdir + self.patinfo.patientName[patientNo] + '_00.nrrd'
            outputname='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + self.patinfo.patientID[patientNo] + '/' + \
                        self.patinfo.ctName[patientNo] + '/' + 'Reg/'
            execommand = 'python /u/motion/Software/RegistrationScript/createPlastimatchScript.py F ' + refCTname + ' -D ' + FDctdir + ' -O ' + outputname + ' -n ' + \
                         self.patinfo.patientName[patientNo] + ' -t bspline -S -p 32'
            tmp = os.popen(execommand).readlines()