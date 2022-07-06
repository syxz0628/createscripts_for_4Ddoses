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
        self.fractions=[]
        self.targets=[]
        self.prescribdose=[]
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
                self.fractions.append(basicinfo[8])
                self.dafinfo.append([])
                self.mbrinfo.append([])
                self.targets.append([])
                self.prescribdose.append([])
                for useinfo in range(0,len(basicinfo)):
                    if basicinfo[useinfo].endswith('.daf'):
                        self.dafinfo[-1].append(basicinfo[useinfo])
                    elif basicinfo[useinfo].endswith('.xml'):
                        self.mbrinfo[-1].append(basicinfo[useinfo])
                    elif 'TV' in basicinfo[useinfo]:
                        self.targets[-1].append(basicinfo[useinfo])
                        self.prescribdose[-1].append(basicinfo[useinfo+1])

                self.beamName.append([])
                self.path2Plan.append([])
                self.couch.append([])
                self.gantry.append([])
                self.targetX.append([])
                self.targetY.append([])
                self.targetZ.append([])
                self.bolus.append([])
                startfieldinfo=len(self.targets[-1])*2+9
                for fieldi in range (0,int(self.fieldNo[-1])):
                    self.beamName[-1].append(basicinfo[startfieldinfo + fieldi * 8])
                    self.path2Plan[-1].append(basicinfo[startfieldinfo+1 + fieldi * 8])
                    self.couch[-1].append(basicinfo[startfieldinfo+2 + fieldi * 8])
                    self.gantry[-1].append(basicinfo[startfieldinfo+3 + fieldi * 8])
                    self.targetX[-1].append(basicinfo[startfieldinfo+4 + fieldi * 8])
                    self.targetY[-1].append(basicinfo[startfieldinfo+5 + fieldi * 8])
                    self.targetZ[-1].append(basicinfo[startfieldinfo+6 + fieldi * 8])
                    self.bolus[-1].append(basicinfo[startfieldinfo+7 + fieldi * 8])
