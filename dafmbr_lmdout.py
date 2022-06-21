import os
import re
import xml.dom.minidom
import xml.etree.ElementTree
class class_dafmbr_lmdout_script():
    def __init__(self,ctinfo,motioninfo):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.fileversion = 1.0
    def fun_create_lmdout_exec(self):
        print("start create sh for all plans listed in patient_motioninfo.txt")
        print(self.motioninfo.patientName)
        path2script='python3 /u/ysheng/MyAIXd/projects/Daf_mbr2mpos_lmdout/main.py -d '
        createsh='/u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/04_makemposlmdout_local.sh'
        with open(createsh, 'w+') as writesh:
            for patientNo in range(0, len(self.motioninfo.planNumber)):
                patientIDstringMotion='/d/bio/medphys/PatienData/SPHIC_motion_mitigate/' + self.motioninfo.patientID[patientNo]
                patientIDstringLocal='/u/ysheng/MyAIXd/projects/patients/' + self.motioninfo.patientID[patientNo]

                for dafNo in self.motioninfo.dafinfo[patientNo]:
                    printinfo1 = '#For patient:' + self.motioninfo.patientName[patientNo] + ' plan:' + \
                                 self.motioninfo.planName[patientNo] + ' daf:' + dafNo
                    daffolder=patientIDstringLocal+ '/4DdoseRecon/motion/'+self.motioninfo.planName[patientNo]+'_'+dafNo[:-4]
                    removefolder='rm -rf '+patientIDstringLocal+ '/4DdoseRecon/motion/2021*'
                    generateDAFFolder = 'mkdir '+daffolder
                    cleanDAFFolder = 'rm -rf ' + daffolder+'/*'
                    generatelmdoutFolder='mkdir '+daffolder+'/lmdout'
                    generateMposFolder='mkdir '+daffolder+'/mpos'
                    # write prepareing folder info. 1. generate planname+daf, 2. generate lmdout and mpos
                    writesh.writelines(
                        printinfo1 + os.linesep + removefolder + os.linesep + generateDAFFolder + os.linesep + cleanDAFFolder + os.linesep + generatelmdoutFolder + os.linesep + generateMposFolder + os.linesep)
                    path2daf = patientIDstringMotion + '/Motion/daf/' + dafNo
                    mposfilename = daffolder + '/mpos/' + dafNo[:-4] + '.mpos'
                    NoofMBRinplan=0
                    for MBRNo in self.motioninfo.mbrinfo[patientNo]:
                        checkMBRdate = re.sub(r'_', '',MBRNo ) #check MBR belongs to the daf
                        if dafNo[:9] in checkMBRdate:
                            path2MBR=patientIDstringMotion+'/Motion/MBR/'+MBRNo
                            ETtree = xml.etree.ElementTree.ElementTree(file=path2MBR)
                            for elem in ETtree.iter(tag='IES'):
                                firstEnergy = elem.get('energy')
                                break
                            NoofMBRinplan+=1
                            lmdoutfilename = daffolder+'/lmdout/MBR_E'+str(firstEnergy)+'_0'+str(NoofMBRinplan)+'_'+checkMBRdate[:14]+'.lmdout'
                            writesh.writelines('#'+MBRNo+os.linesep)
                            writesh.writelines(
                                path2script + path2daf + ' -m ' + path2MBR + ' -l ' + lmdoutfilename + ' -o ' + mposfilename +' -g /u/ysheng/MyAIXd/projects/patients/commands/01-prepare4Ddata/lmdout_logfile.log'+ os.linesep)
                    NoofMBRinplan=0
                    writesh.write(os.linesep)
                    print('file \''+dafNo+'\' finished')



