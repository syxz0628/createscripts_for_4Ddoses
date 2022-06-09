class class_readpat_info:
    def __init__(self, pat_info_path):
        self.pat_info_path = pat_info_path
        self.fileversion = 1.0
        self.numbernumber=[]
        self.patientID=[]
        self.patientName=[]
        self.ctName=[]
        self.dafName=[]
        self.MBRName=[]
    def fun_readpat_info(self):
        countlines=0
        with open(self.pat_info_path) as patfile:
            for lineinfo in patfile.readlines():
                countlines+=1
                if lineinfo[0]=='#':
                    continue
                basicinfo=lineinfo.split()
                self.patientID.append(basicinfo[1])
                self.patientName.append(basicinfo[2])
                self.ctName.append(basicinfo[3])
                self.dafName.append([])
                self.MBRName.append([])
                for dafs in basicinfo[4:]:
                    if dafs.isdigit():
                        self.dafName[-1].append(dafs)
                    else:
                        self.MBRName[-1].append(dafs)


