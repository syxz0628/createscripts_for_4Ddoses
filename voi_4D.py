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
    def fun_gen_4D_vois(self):
        print("start generate 4D vois command that could be run in TRiP")
        print(self.patinfo.patientName)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for patientNo in range(0,len(self.patinfo.patientName)):
            print("#trying 4D voi in: ",self.patinfo.patientName[patientNo])
            data_path = '/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + str(
                self.patinfo.patientID[patientNo]) + '/' + str(self.patinfo.ctName[patientNo]) + '/'
            read_trafo= 'trafo \''+data_path+'Reg/'+str(self.patinfo.patientName[patientNo])+'\' / r select(bw)'
            read_3Dvoi= 'voi \''+data_path+'vois/3D/Average/'+str(self.patinfo.patientName[patientNo])+'\' / r'
            voisine2='voi * / create4D voistate(0) maxthreads(16)'
            write_4Dvoi='voi / write bin prefix(\''+data_path+'vois/4D/'
            print(read_trafo)
            print(read_3Dvoi)
            print(voisine2)
            print(write_4Dvoi)
            #tmp = os.popen(execommand).readlines()
            print("#finished 4D voi: ",self.patinfo.patientName[patientNo],self.patinfo.ctName[patientNo])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")