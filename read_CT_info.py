class class_readpat_info:
    def __init__(self, pat_info_path):
        self.pat_info_path = pat_info_path
        self.fileversion = 1.0
        self.numbernumber=[]
        self.patientID=[]
        self.patientName=[]
        self.ctName=[]
        self.oarName=[]
        self.targetName=[]
        self.plannumber=[]
        self.external=[]
    def fun_readpat_info(self):
        countlines=0
        with open(self.pat_info_path) as patfile:
            for lineinfo in patfile.readlines():
                countlines+=1
                if lineinfo[0]=='#' or lineinfo[0]=='N':
                    continue
                basicinfo=lineinfo.split()
                self.patientID.append(basicinfo[1])
                self.patientName.append(basicinfo[2])
                self.ctName.append(basicinfo[3])
                self.plannumber.append([])
                self.oarName.append([])
                self.targetName.append([])
                for useinfo in basicinfo[4:]:
                    if useinfo.isdigit(): # digital means plan number coresponding to daf and plan info file
                        self.plannumber[-1].append(useinfo)
                    elif 'TV' in useinfo and not('ung' in useinfo): # oar and target
                        self.targetName[-1].append(useinfo)
                    elif useinfo == basicinfo[-1]:
                        self.external.append(useinfo)
                    else:
                        self.oarName[-1].append(useinfo)



