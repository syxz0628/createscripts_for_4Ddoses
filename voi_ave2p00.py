import os
class class_gen_ave_00_vois():
    def __init__(self,patinfo):
        self.patinfo=patinfo
        self.fileversion = 1.0
    def fun_preparefile(self):#generate file under: /u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/031_3Dvois-ave-phase00.sh
        print("start prepare files")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        cd2folder = 'cd /d/bio/medphys/PatienData/SPHIC_motion_mitigate/cmd/'
        print(cd2folder)
        shfilepath='/u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/031_3Dvois_ave_phase00.sh'
        with open (shfilepath,'wb') as shfilew:
            for patientNo in range(0, len(self.patinfo.patientName)):
                data_path = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(
                    self.patinfo.patientID[patientNo]) + '/' + str(self.patinfo.ctName[patientNo]) + '/'

                generate_folder1='mkdir '+data_path+'vois/3D/p00'
                generate_folder2 = 'mkdir ' + data_path + 'vois/ave2p00'

                hed2nrrd_fun = 'hed2nrrd.sh ' + data_path + 'ctx/Average/' + str(
                    self.patinfo.patientName[patientNo]) + '.hed'

                ln01nrrd = 'ln -s ' + data_path + 'ctx/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.nrrd ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_01.nrrd'
                ln01ctx = 'ln -s ' + data_path + 'ctx/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.ctx ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.ctx'

                ln00nrrd = 'ln -s ' + data_path + 'ctx/Average/' + str(
                    self.patinfo.patientName[patientNo]) + '.nrrd ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.nrrd'
                ln00ctx = 'ln -s ' + data_path + 'ctx/Average/' + str(
                    self.patinfo.patientName[patientNo]) + '.ctx ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.ctx'
                outputname='../' + str(self.patinfo.patientID[patientNo]) + '/' + \
                            str(self.patinfo.ctName[patientNo]) + '/vois/3D/p00/'
                regcommand = 'python /u/motion/Software/RegistrationScript/createPlastimatchScript.py F ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_00.nrrd' + ' -M ' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '_01.nrrd' + ' -O ' + outputname + ' -n ' + \
                             str(self.patinfo.patientName[patientNo]) + ' -t bspline -S -p 32'
                shfilew.writelines(generate_folder1+'/n')
                shfilew.writelines(generate_folder2+'/n')
                shfilew.writelines(hed2nrrd_fun+'/n')
                shfilew.writelines(ln00nrrd+'/n')
                shfilew.writelines(ln00ctx+'/n')
                shfilew.writelines(ln01nrrd+'/n')
                shfilew.writelines(ln01ctx+'/n')
                shfilew.writelines(regcommand+'/n')
            shfilew.writelines(cd2folder+'/n')
            shfilew.writelines('runtrip.sh 032_ave2ph00.exec')

    def fun_gen_ph00_vois_exec(self): # generate file under: /u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/032_ave2ph00.exec
        print("start generate ave to phase00 vois command that could be run in TRiP")
        print(self.patinfo.patientName)
        execfilepath='/u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/032_ave_phase00.sh'
        with open (execfilepath,'wb') as execfilew:
            for patientNo in range(0, len(self.patinfo.patientName)):
                data_path = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(
                    self.patinfo.patientID[patientNo]) + '/' + str(self.patinfo.ctName[patientNo]) + '/'
                shell_del = 'shell rm ' + data_path + 'vois/3D/p00/*'
                read_trafo = 'trafo \'' + data_path + 'vois/ave2p00/' + str(
                    self.patinfo.patientName[patientNo]) + '\' / r select(bw)'
                read_3Dvoi = 'voi \'' + data_path + 'vois/3D/Average/' + str(self.patinfo.patientName[patientNo]) + '\' / r'
                voisine2 = 'voi * / create4D voistate(0) maxthreads(16)'
                write_4Dvoi = 'voi / write bin prefix(\'' + data_path + 'vois/3D/p00/\')'
                execfilew.writelines("#start g 3D voi phase00 for: ", self.patinfo.patientName[patientNo],
                                     self.patinfo.ctName[patientNo])
                execfilew.writelines(shell_del+'/n')
                execfilew.writelines(read_trafo+'/n')
                execfilew.writelines(read_3Dvoi+'/n')
                execfilew.writelines(voisine2+'/n')
                execfilew.writelines(write_4Dvoi+'/n')
                # tmp = os.popen(execommand).readlines()
                execfilew.writelines("#finished 4D voi: ", self.patinfo.patientName[patientNo],
                                     self.patinfo.ctName[patientNo]+'/n')

            execfilew.writelines('quit')