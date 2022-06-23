import os
class class_temp():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
    def fun_tempwrite(self):
        print("start create some info for all plans listed in patient_motioninfo.txt")
        tempfilepath='/u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/99_temp.sh'
        with open(tempfilepath,'w+') as writesh:
            for tempNumber in range(0, len(self.motioninfo.planName)):
                patientpath='mkdir /u/ysheng/MyAIXd/projects/patients/'
                rmfolder='rm /u/ysheng/MyAIXd/projects/patients/'
                Tddose =self.motioninfo.patientID[tempNumber]+'/3Ddose/dose/'
                Fddose=self.motioninfo.patientID[tempNumber]+'/4DdoseRecon/dose/'
                rmcommand3D=  rmfolder + Tddose+'* -rf'
                rmcommand4D = rmfolder + Fddose + '* -rf'
                mkdir3Ddose=patientpath+Tddose
                mkdir43Ddose = patientpath + Fddose
                mkdir3D=patientpath+Tddose+self.motioninfo.planName[tempNumber]
                mkdir4D = patientpath + Fddose + self.motioninfo.planName[tempNumber]
                writesh.writelines(rmcommand3D+os.linesep+rmcommand4D+os.linesep)
            for tempNumber in range(0, len(self.motioninfo.planName)):
                patientpath = 'mkdir /u/ysheng/MyAIXd/projects/patients/'
                rmfolder = 'rm /u/ysheng/MyAIXd/projects/patients/'
                Tddose = self.motioninfo.patientID[tempNumber] + '/3Ddose/dose/'
                Fddose = self.motioninfo.patientID[tempNumber] + '/4DdoseRecon/dose/'
                Tdexec = self.motioninfo.patientID[tempNumber] + '/3Ddose/exec/'
                Fdexec = self.motioninfo.patientID[tempNumber] + '/4DdoseRecon/exec/'
                dafexec=[]
                dafdose=[]
                for tempdafinfo in self.motioninfo.dafinfo[tempNumber]:
                    dafexec=patientpath+Fdexec+ self.motioninfo.planName[tempNumber]+tempdafinfo[:-4]
                    dafdose=patientpath + Fddose+tempdafinfo[:-4]
                mkdir3Ddose = patientpath + Tddose
                mkdir43Ddose = patientpath + Fddose
                mkdir3Dexec = patientpath + Tdexec
                mkdir43Dexec = patientpath + Fdexec
                mkdir3D = patientpath + Tddose + self.motioninfo.planName[tempNumber]
                mkdir4D = patientpath + Fddose + self.motioninfo.planName[tempNumber]
                mkdir3D2 = patientpath + Tdexec + self.motioninfo.planName[tempNumber]
                mkdir4D2 = patientpath + Fdexec + self.motioninfo.planName[tempNumber]
                writesh.writelines(
                     mkdir3Ddose + os.linesep + mkdir43Ddose + os.linesep + mkdir3D + os.linesep + mkdir4D + os.linesep+os.linesep)
                writesh.writelines(
                     mkdir3Dexec + os.linesep + mkdir43Dexec + os.linesep + mkdir3D2 + os.linesep + mkdir4D2 + os.linesep)
                for temp in range(0, len(dafexec)):
                    writesh.writelines(dafexec[temp]+os.linesep+dafdose[temp]+ os.linesep)
                writesh.writelines(os.linesep+os.linesep)
