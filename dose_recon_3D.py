import os


class class_dose_recon_3D():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
        self.path2patientEXE = '/u/ysheng/MyAIXd/projects/patients/'
        self.path2patientData = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/'
    def fun_create_3D_dose_recon_exec(self):
        print("start create 3D dose reconstruction exec for all plans listed in patient_motioninfo.txt")
        for specific_plan in range(0, len(self.motioninfo.planName)):
            print('start to write 3D plan: ' + self.motioninfo.planName[specific_plan] + ' for patient:' +
                  self.motioninfo.patientName[specific_plan])
            # selection of beam base data
            if self.motioninfo.ion_info[specific_plan]=='S3C':
                Plan_basedata='exec "/u/ysheng/MyAIXd/projects/basedata/EXEC/SPHIC_12C_RIFI3mm.exec" \n'
            elif self.motioninfo.ion_info[specific_plan]=='S6C':
                Plan_basedata = 'exec "/u/ysheng/MyAIXd/projects/basedata/EXEC/SPHIC_12C_RIFI6mm.exec" \n'
            elif self.motioninfo.ion_info[specific_plan]=='S1H':
                Plan_basedata = 'exec "/u/ysheng/MyAIXd/projects/basedata/EXEC/SPHIC_1H.exec" \n'
            # selection of HULT
            if self.motioninfo.hult[specific_plan] == 'prostate':
                Plan_hult = 'hlut "/u/ysheng/MyAIXd/projects/basedata/SPHIC/SPHIC_HLUT/CTAWP66960_RT_Prostata_1.hlut" / read \n'
            elif self.motioninfo.hult[specific_plan] == 'head':
                Plan_hult = 'hlut "/u/ysheng/MyAIXd/projects/basedata/SPHIC/SPHIC_HLUT/CTAWP66960_RT_Head_Neck_D30s_1.hlut" / read \n'
            # selection of rbe model
            Plan_rbe_Table='rbe  "/u/motion/AIXd/user/motion/Data/TRiP98DATA/chordom*.rbe" / read \n'
            # selection of CT (Average for 3D plan)
            Plan_ct = 'ct "' + self.path2patientData + self.motioninfo.patientID[specific_plan] + '/' + \
                      self.motioninfo.ctName[specific_plan] + '/ctx/Average/' + self.motioninfo.patientName[
                          specific_plan] + '" / read \n'
            # selection of voi
             # get voi info from CTinfo:
            for ctinfocount in range(0, len(self.ctinfo.patientID)):
                if self.ctinfo.patientID[ctinfocount]==self.motioninfo.patientID[specific_plan]:
                    if self.ctinfo.ctName[ctinfocount]==self.motioninfo.ctName[specific_plan]:
                        Plan_targetname=",".join(i for i in self.ctinfo.targetName[ctinfocount])
                        Plan_oarname=",".join(i for i in self.ctinfo.oarName[ctinfocount])
                        Plan_external=self.ctinfo.external[ctinfocount]
                        break
             # set voi (average for 3D plan)
            Plan_voi = 'voi "' + self.path2patientData + self.motioninfo.patientID[specific_plan] + '/' + \
                      self.motioninfo.ctName[specific_plan] + '/vois/3D/Average/' + self.motioninfo.patientName[
                          specific_plan] + '" / read select('+Plan_targetname+','+Plan_oarname+','+Plan_external+') \n'
             # set target voi
            Plan_set_target_voi='voi "'+self.ctinfo.targetName[ctinfocount][0]+'" / targetset \n'
            # set rbe model
            Plan_rbe_model='rbe "'+self.ctinfo.external[ctinfocount]+'" / alias(chordom02) \n'
            # set plan dose
            Plan_setdose='plan / dose(3) targettissue(chordom02) residualtissue(chordom02) \n'
            # set field information
            Plan_fieldinfo=''
            for temp in range(0, int(self.motioninfo.fieldNo[specific_plan])):
                Plan_fieldinfo = Plan_fieldinfo+'field ' + str(temp + 1) + ' / read file(' + self.path2patientData + \
                                 self.motioninfo.patientID[specific_plan] + '/' + \
                                 self.motioninfo.path2Plan[specific_plan][temp] + '/' + \
                                 self.motioninfo.beamName[specific_plan][temp] + '.rst) couch(' + \
                                 self.motioninfo.couch[specific_plan][temp] + ') gantry(' + \
                                 self.motioninfo.gantry[specific_plan][temp] +') target(' + \
                                 self.motioninfo.targetX[specific_plan][temp] + ',' + \
                                 self.motioninfo.targetY[specific_plan][temp] + ',' + \
                                 self.motioninfo.targetZ[specific_plan][temp] + ') doseext(1.4862) noreg'
                if self.motioninfo.bolus[specific_plan][temp]!='0':
                    Plan_fieldinfo=Plan_fieldinfo+'bolus('+self.motioninfo.bolus[specific_plan][temp]+')'
                Plan_fieldinfo=Plan_fieldinfo+'\n'
            # set dose information
            Plan_doseinfo=''
            write2dosepath=self.path2patientEXE+self.motioninfo.patientID[specific_plan]+'/3Ddose/dose/'+ \
                           self.motioninfo.planName[specific_plan]+'/'
            for temp in range(0, int(self.motioninfo.fieldNo[specific_plan])):
                Plan_doseinfo=Plan_doseinfo+'dose "'+write2dosepath+self.motioninfo.beamName[specific_plan][temp]+\
                              '" / field('+str(temp+1)+') '+'voi('+self.ctinfo.external[ctinfocount]+') '+\
                              'maxthreads(30) direct calculate alg(msdb) bio bioalg(ld) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
            Plan_doseinfo = Plan_doseinfo +'dose "'+write2dosepath+'total" / field(*) '+'voi('+self.ctinfo.external[ctinfocount]+') '+\
                              'maxthreads(30) direct calculate alg(msdb) bio bioalg(ld) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
            # set DVH export information
            Plan_dvh='dvh  "'+write2dosepath+'total.bio" / calculate export(gd) bio\n'
            # write to specific exec file in each patient folder
            createexec = self.path2patientEXE + self.motioninfo.patientID[specific_plan]+'/3Ddose/exec/'+ \
                       self.motioninfo.planName[specific_plan]+'/'+self.motioninfo.planName[specific_plan]+'.exec'
            with open(createexec, 'w+') as writeexec:
                writeexec.writelines(Plan_basedata+Plan_hult+Plan_rbe_Table+Plan_ct+Plan_voi)
                writeexec.writelines(Plan_set_target_voi+Plan_rbe_model+Plan_setdose)
                writeexec.writelines(Plan_fieldinfo+Plan_doseinfo+Plan_dvh+'quit')
    def fun_create_3D_dose_run_sh(self):
        print("start generating the running sh file")
        createsh='/u/ysheng/MyAIXd/projects/patients/commands/05_run3Dexec.sh'
        headinfo='echo \'This script will run all 3D dose reconstruct plans\' \n'
        with open (createsh,'w+') as writesh:
            writesh.writelines(headinfo)
            for specific_plan in range(0, len(self.motioninfo.planName)):
                planheadinfo = 'echo \'Running the plan:' + self.motioninfo.planName[
                    specific_plan] + ' for patient:' + self.motioninfo.patientName[specific_plan] + '\'\n'
                cd2execfolder='cd '+self.path2patientEXE + self.motioninfo.patientID[specific_plan]+'/3Ddose/exec/'+ \
                       self.motioninfo.planName[specific_plan]+'/ \n'
                runexec='runtrip.sh '+self.motioninfo.planName[specific_plan]+'.exec -l \n\n'
                writesh.writelines(planheadinfo+cd2execfolder+runexec)
        print('running file generated in :')
        print('/u/ysheng/MyAIXd/projects/patients/commands/05_run3Dexec.sh')