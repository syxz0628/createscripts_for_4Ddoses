class class_readmotion_info:
    def __init__(self, motion_info_path):
        self.motion_info_path = motion_info_path
        self.planNumber=[]
        self.patientID=[]
        self.patientName=[]
        self.ctName=[]
        self.planName=[]
        self.ion_info=[] # S3C carbon/3mm RIFI, S6C carbon/6mm RiFI, S1H, SPHIC Proton.
        self.hult=[] # prostate/head
        self.fieldNo = [] # number of portals
        self.beamName=[] # 2D data set [plan][beam]
        self.path2Plan=[] #
        self.couch=[]#
        self.gantry=[]#
        self.targetX=[]#
        self.targetY = []  #
        self.targetZ = []  #
        self.bolus=[] #
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
                self.ion_info.append(basicinfo[5])
                self.hult.append(basicinfo[6])
                self.fieldNo.append(basicinfo[7])
                self.beamName.append([])
                self.path2Plan.append([])
                self.couch.append([])
                self.gantry.append([])
                self.targetX.append([])
                self.targetY.append([])
                self.targetZ.append([])
                self.bolus.append([])
                for fieldi in range (0,int(self.fieldNo[-1])):
                    self.beamName[-1].append(basicinfo[8 + fieldi * 8])
                    self.path2Plan[-1].append(basicinfo[9 + fieldi * 8])
                    self.couch[-1].append(basicinfo[10 + fieldi * 8])
                    self.gantry[-1].append(basicinfo[11 + fieldi * 8])
                    self.targetX[-1].append(basicinfo[12 + fieldi * 8])
                    self.targetY[-1].append(basicinfo[13 + fieldi * 8])
                    self.targetZ[-1].append(basicinfo[14 + fieldi * 8])
                    self.bolus[-1].append(basicinfo[15 + fieldi * 8])

                self.dafinfo.append([])
                self.mbrinfo.append([])
                for useinfo in basicinfo[7:]:
                    if useinfo.endswith('.daf'):
                        self.dafinfo[-1].append(useinfo)
                    elif useinfo.endswith('.xml'):
                        self.mbrinfo[-1].append(useinfo)