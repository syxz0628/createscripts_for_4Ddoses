import os


class class_dafmbr():
    def __init__(self, dafpath):
        self.dafpath = dafpath

    def fun_writename(self):
        mbrfiles = []
        daffiles = []
        print("write daf and mbr information to :")
        print(self.dafpath[:self.dafpath.rfind('/')])
        filename = self.dafpath + 'dafmbrinfo.txt'
        path_list = os.listdir(self.dafpath)
        with open(filename, 'w+') as writedafmbr:

            for foldername in path_list:
                writedafmbr.write(foldername + os.linesep)
                daffilepath = self.dafpath + foldername + '/'
                try:
                    dafmbrfiles = os.listdir(daffilepath)
                except:
                    continue
                for dafmbrs in dafmbrfiles:
                    if dafmbrs.endswith('.xml') == True:
                        mbrfiles.append(dafmbrs)
                    elif dafmbrs.endswith('.daf') == True:
                        daffiles.append(dafmbrs)
                    else:
                        pass

                writedafmbr.writelines((temp1 + ' ') for temp1 in daffiles)
                writedafmbr.writelines((temp1 + ' ') for temp1 in mbrfiles)

                writedafmbr.writelines(os.linesep + os.linesep)
                mbrfiles = []
                daffiles = []

if __name__ == '__main__':
    mbr = class_dafmbr(r'C:\Users\carbon\Desktop\01-GSI-all_in_one\Motion_patient_data\daf_mbr\\')
    mbr.fun_writename()