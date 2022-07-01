import os

class class_combine_log :
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
    def fun_combine_logfiles(self):
        for patientNo in range(0, len(self.motioninfo.planNumber)):
            patientIDstringMotion = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + self.motioninfo.patientID[
                patientNo]
            patientIDstringLocal = '/u/ysheng/MyAIXd/projects/patients/' + self.motioninfo.patientID[patientNo]
            for dafNo in self.motioninfo.dafinfo[patientNo]:
                printinfo1 = '#For patient:' + self.motioninfo.patientName[patientNo] + ' plan:' + \
                             self.motioninfo.planName[patientNo] + ' daf:' + dafNo
                daffolder = patientIDstringLocal + '/4DdoseRecon/exec/' + self.motioninfo.planName[
                    patientNo] + '/' + dafNo[:-4]+'/'
                path_list = os.listdir(daffolder)
                for anyfilename in path_list:
                    print(anyfilename)
                    if anyfilename.endswith('.log'):
                        copyname = '/u/ysheng/MyAIXd/projects/patients/commands/TRiP-logs/' + \
                                   self.motioninfo.patientName[patientNo] + '_' + self.motioninfo.planName[
                                       patientNo] + '_' + '_' + dafNo[:-4] + '.log'
                        copycommand='cp '+daffolder+anyfilename+' '+copyname
                        val=os.system(copycommand)
                        print(val)

