class class_readmotion_info:
    def __init__(self, motion_info_path):
        self.motion_info_path = motion_info_path
        self.planNumber=[]
        self.patientID=[]
        self.patientName=[]
        self.ctName=[]
        self.planName=[]
        self.planParameter=[]
        self.dafinfo=[]
        self.mbrinfo=[]
    def fun_readpat_motion_info(self):
        countlines=0
        with open(self.motion_info_path) as planmotionfile:
            for lineinfo in planmotionfile.readlines():
                countlines+=1
                if lineinfo[0]=='#' or lineinfo[0]=='N':
                    continue
                basicinfo=lineinfo.split()
                self.planNumber.append(basicinfo[0])
                self.patientID.append(basicinfo[1])
                self.patientName.append(basicinfo[2])
                self.planName.append(basicinfo[3])
                self.ctName.append(basicinfo[4])
                self.planParameter.append([])
                self.dafinfo.append([])
                self.mbrinfo.append([])
                for useinfo in basicinfo[5:]:
                    if useinfo.endswith('.daf'):
                        self.dafinfo[-1].append(useinfo)
                    elif useinfo.endswith('.xml'):
                        self.mbrinfo[-1].append(useinfo)
                    else:
                        self.planParameter[-1].append(useinfo)