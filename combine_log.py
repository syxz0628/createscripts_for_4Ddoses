import os

class class_combine_log :
    def __init__(self,ctinfo,motioninfo,path2logfiles):
        self.ctinfo=ctinfo
        self.motioninfo=motioninfo
        self.path2logfiles=path2logfiles
        self.fileversion = 1.0
    def fun_copy_logfiles(self):
        writeshname='/u/ysheng/MyAIXd/projects/patients/commands/062_combinelogs.sh'
        with open(writeshname, 'w+') as log_file:
            for logfilepath in self.path2logfiles:
                copyname = logfilepath.replace('/','_')
                copycommand='cp '+logfilepath+' '+copyname[35:]+'\n'
                log_file.writelines(copycommand)


