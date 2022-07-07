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
        self.dose_analysis_script_path='python3 /u/ysheng/MyAIXd/projects/doseanalysis_TRiP/main.py '
        self.dose_analysis_filename=self.path2patientEXE+'commands/07_dose_analysis.sh'
        self.path2datafiles=[]


    def fun_create_dose_analysis_sh(self):
        print("start create dose analysis sh for all plans listed in patient_motioninfo.txt")

        with open (self.dose_analysis_filename,'w+') as analysis_file:
            for specific_plan in range(0, len(self.motioninfo.planName)):
                print('start to write plan: ' + self.motioninfo.planName[specific_plan] + ' for patient:' +
                      self.motioninfo.patientName[specific_plan])
                analysis_file.writelines('# paitent: '+self.motioninfo.patientName[specific_plan]+ ' plan: '+self.motioninfo.planName[specific_plan]+'\n')
                #analysis_file.writelines('mkdir '+self.path2patientEXE+self.motioninfo.patientID[specific_plan]+'/dose_ana_'+self.folderlist[0]+'_'+self.folderlist[1]+'\n')
                targetname='' # write target name in one line
                for targeti in self.motioninfo.targets[specific_plan]:
                    targetname=targetname+targeti+','
                targetname=targetname[:-1]
                targetdose = ''# write target dose in one line
                for targeti in self.motioninfo.prescribdose[specific_plan]:
                    targetdose = targetdose + targeti + ','
                targetdose = targetdose[:-1]
                oarname = ''  # write oarname in one line
                for ctinfocount in range(0, len(self.ctinfo.patientID)):
                    if self.ctinfo.patientID[ctinfocount] == self.motioninfo.patientID[specific_plan]:
                        if self.ctinfo.ctName[ctinfocount] == self.motioninfo.ctName[specific_plan]:
                            oarname = ",".join(i for i in self.ctinfo.oarName[ctinfocount])

                folderl = '' # give name for the dose txt
                for s in self.folderlist:
                    folderl = folderl + s + '_'
                analysis_file.writelines(
                    self.dose_analysis_script_path + '-i ' + self.motioninfo.patientID[specific_plan] +
                    ' -p ' + self.motioninfo.planName[specific_plan] +
                    ' -t ' + targetname +  # list of target
                    ' -d ' + targetdose +  # list of pd
                    ' -o ' + oarname +
                    ' -f ' + self.motioninfo.fractions[specific_plan] +
                    ' -s ' + folderl+
                    ' -g ')
                for folder in self.folderlist:
                    if folder == '3Ddose':  # /u/ysheng/MyAIXd/projects/patients/ID/folder/
                        if '1H' in self.motioninfo.ion_info[specific_plan]:
                            analysis_file.writelines(self.path2patientEXE+self.motioninfo.patientID[specific_plan]+ '/'+ folder+ '/dose/'+ self.motioninfo.planName[specific_plan]+'/total.phys.dvh.gd,')
                        else:
                            analysis_file.writelines(self.path2patientEXE+self.motioninfo.patientID[specific_plan]+ '/'+ folder+ '/dose/'+ self.motioninfo.planName[specific_plan]+'/total.bio.dvh.gd,')
                    else:
                        filename=''
                        for dafinfo in self.motioninfo.dafinfo[specific_plan]:
                            filename=filename+self.path2patientEXE+self.motioninfo.patientID[specific_plan]+'/'+folder+'/dose/'+self.motioninfo.planName[specific_plan]
                            if '1H' in self.motioninfo.ion_info[specific_plan]:
                                filename=filename+'/'+str(dafinfo[:-4])+'/total.phys.dvh.gd,'
                            else:
                                filename=filename+'/'+str(dafinfo[:-4])+'/total.bio.dvh.gd,'
                analysis_file.writelines(filename[:-1])
                analysis_file.write('\n')
                self.path2datafiles.append(self.path2patientEXE+self.motioninfo.patientID[specific_plan]+'/dose_ana_'+folderl+self.motioninfo.patientID[specific_plan]+'_'+self.motioninfo.planName[specific_plan]+'.txt')
        combine_log_name = '/u/ysheng/MyAIXd/projects/patients/commands/dose_compare_logs/00_total.txt'
        related_funs.fun_copy_combine_logfiles( self.dose_analysis_filename,'a+', combine_log_name, self.path2datafiles)