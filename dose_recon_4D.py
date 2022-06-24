import sys
import os


class class_dose_recon_4D():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
        self.path2patientEXE = '/u/ysheng/MyAIXd/projects/patients/'
        self.path2patientData = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/'
    def fun_create_4D_dose_recon_exec(self):
        print("start create 4D dose reconstruction exec for all plans listed in patient_motioninfo.txt")
        for specific_plan in range(0, len(self.motioninfo.planName)):
            print('start to write 4D plan: ' + self.motioninfo.planName[specific_plan] + ' for patient:' +
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
                      self.motioninfo.ctName[specific_plan] + '/ctx/' + self.motioninfo.patientName[
                          specific_plan] + '" / read state(10) refstate(0) \n'
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
                      self.motioninfo.ctName[specific_plan] + '/vois/4D/' + self.motioninfo.patientName[
                          specific_plan] + '" / read select('+Plan_targetname+','+Plan_oarname+','+Plan_external+') \n'
             # set target voi
            Plan_set_target_voi='voi "'+self.ctinfo.targetName[ctinfocount][0]+'" / targetset \n'
            # set TRAFO
            Plan_trafo = 'trafo "' + self.path2patientData + self.motioninfo.patientID[specific_plan] + '/' + \
                      self.motioninfo.ctName[specific_plan] + '/Reg/' + self.motioninfo.patientName[
                          specific_plan] + '" / read select(movref) \n'
            # set rbe model
            Plan_rbe_model='rbe "'+self.ctinfo.external[ctinfocount]+'" / alias(chordom02) \n'
            # set plan dose
            Plan_setdose='plan / dose(3) targettissue(chordom02) residualtissue(chordom02) \n'
            ######
            ###### set field information, write field before dose information.
            ######
            Plan_field_info=[] #Plan_field_info[field1, field2,...]
            for specific_daf in range(0, len(self.motioninfo.dafinfo[specific_plan])):
                Path2motion = self.path2patientEXE + self.motioninfo.patientID[
                    specific_plan] + '/4DdoseRecon/motion/' + self.motioninfo.planName[specific_plan] + '_' + \
                                   self.motioninfo.dafinfo[specific_plan][specific_daf][:-4]
                Path2motion_mpos = Path2motion + '/mpos/' + \
                                   self.motioninfo.dafinfo[specific_plan][specific_daf][:-4] + '.mpos'
                motion_lmdout_folder = Path2motion + '/lmdout/'
                path_list = os.listdir(motion_lmdout_folder)
                # write each filed info for specific daf file.
                for specific_field in range(0, int(self.motioninfo.fieldNo[specific_plan])):
                    print('#start write daf: ', self.motioninfo.dafinfo[specific_plan][specific_daf])
                    print('##start write field: ', str(specific_field))
                    # write one field information
                    Plan_field_info.append('field ' + str(specific_field + 1) + ' / read rst(' + self.path2patientData + \
                                     self.motioninfo.patientID[specific_plan] + '/' + \
                                     self.motioninfo.path2Plan[specific_plan][specific_field] + '/' + \
                                     self.motioninfo.beamName[specific_plan][specific_field] + '.rst) couch(' + \
                                     self.motioninfo.couch[specific_plan][specific_field] + ') gantry(' + \
                                     self.motioninfo.gantry[specific_plan][specific_field] +') target(' + \
                                     self.motioninfo.targetX[specific_plan][specific_field] + ',' + \
                                     self.motioninfo.targetY[specific_plan][specific_field] + ',' + \
                                     self.motioninfo.targetZ[specific_plan][specific_field] + ') doseext(1.4862) noreg ')
                    # write bolus information to one field
                    if self.motioninfo.bolus[specific_plan][specific_field]=='0':
                        Plan_field_info[-1] = Plan_field_info[-1]+'bolus(0) \n'
                    else:
                        Plan_field_info[-1] = Plan_field_info[-1] + 'bolus(' + self.motioninfo.bolus[specific_plan][specific_field] + ') \n'
                    # write motion mpos information to one field
                    Plan_field_info[-1] = Plan_field_info[-1]+'field ' + str(specific_field + 1) + ' / motion(' + Path2motion_mpos + \
                                     ') isexternal stateal(pb) statedir(x) statelimits(-108,-72,-36,0,36,72,108,144,180,216,252)\n'
                    # write motion lmdout information to one field
                    path2rst=self.path2patientData + \
                                     self.motioninfo.patientID[specific_plan] + '/' + \
                                     self.motioninfo.path2Plan[specific_plan][specific_field] + '/' + \
                                     self.motioninfo.beamName[specific_plan][specific_field] + '.rst'
                    [FirstEnergy_rst,LastEnergy_rst]=self.fun_get_rst_first_end_energy(path2rst)
                    for lmdoutfilename in path_list:
                        if lmdoutfilename.endswith('.lmdout') == False:
                            continue
                        if (FirstEnergy_rst in lmdoutfilename) and (LastEnergy_rst in lmdoutfilename):
                            path_list.remove(lmdoutfilename)
                            correct_lmdoutfilename=lmdoutfilename
                            break
                    try:
                        Path2motion_lmdout = Path2motion + '/lmdout/' + correct_lmdoutfilename
                    except:
                        print('ERROR:cannot match rst energy with lmdout/MBR energy for patient:')
                        print(self.motioninfo.patientName[specific_plan])
                        print('Plan name:')
                        print(self.motioninfo.planName[specific_plan])
                        sys.exit()
                    # write motion lmdout information to one field
                    Plan_field_info[-1] = Plan_field_info[-1] + 'field ' + str(specific_field + 1) + ' / spill(' + Path2motion_lmdout+')\n'
                    # write create to one field
                    Plan_field_info[-1] = Plan_field_info[-1] + 'field ' + str(specific_field + 1) + ' create \n\n'
                ######
                ###### set dose information, write in exec after field.
                ######
                Plan_doseinfo = ''
                write2dosepath = self.path2patientEXE + self.motioninfo.patientID[specific_plan] + '/4DdoseRecon/dose/' + \
                                 self.motioninfo.planName[specific_plan] + '/' + self.motioninfo.dafinfo[specific_plan][specific_daf][:-4]+'/'

                for temp in range(0, int(self.motioninfo.fieldNo[specific_plan])):
                    if self.motioninfo.ion_info[specific_plan] == 'S3C' or self.motioninfo.ion_info[specific_plan] == 'S6C':
                        Plan_doseinfo = Plan_doseinfo + 'dose "' + write2dosepath + \
                                        self.motioninfo.beamName[specific_plan][
                                            temp] + \
                                        '" / field(' + str(temp + 1) + ') ' + 'voi(' + self.ctinfo.external[
                                            ctinfocount] + ') ' + \
                                        'maxthreads(30) direct calculate alg(msdb) bio bioalg(ld) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
                    elif self.motioninfo.ion_info[specific_plan] == 'S1H':
                        Plan_doseinfo = Plan_doseinfo + 'dose "' + write2dosepath + \
                                        self.motioninfo.beamName[specific_plan][
                                            temp] + \
                                        '" / field(' + str(temp + 1) + ') ' + 'voi(' + self.ctinfo.external[
                                            ctinfocount] + ') ' + \
                                        'maxthreads(30) direct calculate alg(msdb) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
                if self.motioninfo.ion_info[specific_plan] == 'S3C' or self.motioninfo.ion_info[
                    specific_plan] == 'S6C':
                    Plan_doseinfo = Plan_doseinfo + 'dose "' + write2dosepath + 'total" / field(*) ' + 'voi(' + \
                                    self.ctinfo.external[ctinfocount] + ') ' + \
                                    'maxthreads(30) direct calculate alg(msdb) bio bioalg(ld) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
                    # set DVH export information
                    Plan_dvh = 'dvh  "' + write2dosepath + 'total.bio" / calculate export(gd) bio\n'
                elif self.motioninfo.ion_info[specific_plan] == 'S1H':
                    Plan_doseinfo = Plan_doseinfo + 'dose "' + write2dosepath + 'total" / field(*) ' + 'voi(' + \
                                    self.ctinfo.external[ctinfocount] + ') ' + \
                                    'maxthreads(30) direct calculate alg(msdb) nosvv norbe write datatype(float) subsample(3,3,3,mm) \n'
                    # set DVH export information
                    Plan_dvh = 'dvh  "' + write2dosepath + 'total.phys" / calculate export(gd)\n'
                ######
                # write to specific exec file in each patient folder
                # each daf write an exec
                ######
                createexec = self.path2patientEXE + self.motioninfo.patientID[specific_plan]+'/4DdoseRecon/exec/' + \
                             self.motioninfo.planName[specific_plan]+'/'+ self.motioninfo.dafinfo[specific_plan][specific_daf][:-4] + \
                             '/'+self.motioninfo.planName[specific_plan]+'.exec'
                with open(createexec, 'w+') as writeexec:
                    writeexec.writelines(Plan_basedata+Plan_hult+Plan_rbe_Table+Plan_ct+Plan_voi)
                    writeexec.writelines(Plan_set_target_voi+Plan_rbe_model+Plan_setdose)
                    writeexec.writelines('\n'+temp for temp in Plan_field_info)
                    writeexec.writelines(Plan_doseinfo+Plan_dvh+'quit')
    def fun_create_4D_dose_run_sh(self):
        print("start generating the running sh file")
        createsh='/u/ysheng/MyAIXd/projects/patients/commands/06_run4Dexec_local.sh'
        headinfo='echo \'This script will run all 4D dose reconstruct plans\' \n'
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
        print('/u/ysheng/MyAIXd/projects/patients/commands/05_run3Dexec_motion.sh')

    def fun_get_rst_first_end_energy(self,path2rst):
        slice_Energy = []
        with open(path2rst) as rstfile:
            alllines = rstfile.readlines()
            for sline in alllines:
                if ('submachine#' in sline):
                    submachineinfo = sline.split()
                    slice_Energy.append(submachineinfo[2])
        return slice_Energy[0],slice_Energy[-1]