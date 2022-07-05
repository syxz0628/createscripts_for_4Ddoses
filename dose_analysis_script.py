import os
import related_funs

class class_dose_analysis():
    def __init__(self,ctinfo,motioninfo,folderlist):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.folderlist=folderlist
        self.fileversion = 1.0
        self.path2patientEXE = '/u/ysheng/MyAIXd/projects/patients/'
        self.path2patientData = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/'
        self.dose_analysis_script_path='python3 /u/ysheng/MyAIXd/projects/doseanalysis/main.py '
        self.path2logfiles=[]
    def fun_create_dose_analysis_sh(self):
        print("start create dose analysis sh for all plans listed in patient_motioninfo.txt")
        dose_analysis_filename=self.path2patientEXE+'commands/07_dose_analysis.txt'
        with open (dose_analysis_filename,'w+') as analysis_file:
            for specific_plan in range(0, len(self.motioninfo.planName)):
                print('start to write plan: ' + self.motioninfo.planName[specific_plan] + ' for patient:' +
                      self.motioninfo.patientName[specific_plan])
                analysis_file.writelines('# paitent: ',self.motioninfo.patientName[specific_plan], ' plan: ',self.motioninfo.planName[specific_plan])
                for folder in self.folderlist:
                    if folder=='3Ddose': # /u/ysheng/MyAIXd/projects/patients/ID/folder/
                        analysis_file.writelines(self.dose_analysis_script_path, '-n ',self.motioninfo.patientName[specific_plan],
                                                 ' -p ',self.motioninfo.planName[specific_plan],
                                                 ' -t ',self.motioninfo.targets[specific_plan], # list of target
                                                 ' -d ',self.motioninfo.prescribdose[specific_plan], # list of pd
                                                 ' -f ',self.motioninfo.fractions[specific_plan],
                                                 ' -g ',self.path2patientEXE,
                                                 self.motioninfo.patientID[specific_plan], '/', folder, '/dose/', self.motioninfo.planName[specific_plan],'/total.bio.dvh.gd')
