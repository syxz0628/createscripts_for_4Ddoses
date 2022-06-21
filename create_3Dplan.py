class class_create3Dplan():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
    def fun_create_3Dplan_exec(self):
        print("start create sh for all plans listed in patient_motioninfo.txt")
