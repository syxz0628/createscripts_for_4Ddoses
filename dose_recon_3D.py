class class_dose_recon_3D():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
    def fun_create_3D_dose_recon_exec(self):
        print("start create 3D dose reconstruction exec for all plans listed in patient_motioninfo.txt")
        path2patient='/u/ysheng/MyAIXd/projects/patients/'
        createsh='/u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/04_makemposlmdout_local.sh'
        for specific_plan in range(0, len(self.motioninfo.planName)):
            with open(createsh, 'w+') as writesh:
                for patientNo in range(0, len(self.motioninfo.planNumber)):
                    patientIDstringMotion='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + self.motioninfo.patientID[patientNo]
                    patientIDstringLocal='/u/ysheng/MyAIXd/projects/patients/' + self.motioninfo.patientID[patientNo]
