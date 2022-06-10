import os
class class_gen_4D_vois():
    def __init__(self,patinfo):
        self.patinfo=patinfo
        self.fileversion = 1.0
    def fun_preparefolder(self):
        print("start preparing such as generate 4D folder, remove patient.vdx")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for patientNo in range(0, len(self.patinfo.patientName)):
            data_path = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(
                self.patinfo.patientID[patientNo]) + '/' + str(self.patinfo.ctName[patientNo]) + '/'
            generate4D='mkdir '+data_path+'vois/4D/'
            vdxfile = data_path + 'vois/3D/Average/' + str(self.patinfo.patientName[patientNo]) + '.vdx '
            changevdxfile= data_path + 'vois/3D/Average/' + str(self.patinfo.patientName[patientNo]) + '.vdxbackup'
            mvcommand='mv '+vdxfile+changevdxfile
            print(generate4D)
            print(mvcommand)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    def fun_gen_4D_vois(self,createvoiexec):
        print("start generate 4D vois command that could be run in TRiP")
        print(self.patinfo.patientName)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        runexec=createvoiexec+'03-4Dvois_motion.exec'
        with open(runexec, 'w+') as writesh:
            for patientNo in range(0,len(self.patinfo.patientName)):
                print("#trying 4D voi in: ",self.patinfo.patientName[patientNo])

                data_path = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(
                    self.patinfo.patientID[patientNo]) + '/' + str(self.patinfo.ctName[patientNo]) + '/'
                shell_del = 'shell rm '+data_path+'vois/4D/*'
                read_trafo= 'trafo \''+data_path+'Reg/'+str(self.patinfo.patientName[patientNo])+'\' / r select(bw)'
                read_3Dvoi= 'voi \''+data_path+'vois/3D/Average/'+str(self.patinfo.patientName[patientNo])+'\' / r'
                voisine2='voi * / create4D voistate(0) maxthreads(16)'
                write_4Dvoi='voi / write bin prefix(\''+data_path+'vois/4D/\')'
                print(shell_del)
                print(read_trafo)
                print(read_3Dvoi)
                print(voisine2)
                print(write_4Dvoi)
                #tmp = os.popen(execommand).readlines()
                print("#finished 4D voi: ",self.patinfo.patientName[patientNo],self.patinfo.ctName[patientNo])
                print()
                writesh.writelines(
                    shell_del + read_trafo + os.linesep + read_3Dvoi + os.linesep + voisine2 + os.linesep + write_4Dvoi + os.linesep + os.linesep)
                # createfilepath=data_path + 'vois/create4Dvois.exec'
                # with open(createfilepath,'w+') as writeexec:
                #     writeexec.writelines(
                #         read_trafo + os.linesep + read_3Dvoi + os.linesep + voisine2 + os.linesep + write_4Dvoi + os.linesep + 'quit')
                # cdtofolder= 'cd '+data_path+'vois/'+os.linesep
                # runtrip='runtrip.sh create4Dvois.exec -l'+os.linesep
                # cdoutfolder='cd ../../../'+os.linesep
                # printinfo='#finished '+self.patinfo.patientName[patientNo]+os.linesep+os.linesep
                # writesh.writelines(cdtofolder+runtrip+cdoutfolder+printinfo)
            writesh.write('quit')
        print("quit")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")