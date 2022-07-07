import os
import sys
def fun_copy_combine_logfiles(write_sh_name,writetype,combine_log_name,path2logfiles):
    #write_sh_name = '/u/ysheng/MyAIXd/projects/patients/commands/062_combine_TRiP_4D_logs.sh'
    #combine_log_name = '/u/ysheng/MyAIXd/projects/patients/commands/TRiP_logs/00_total.log'
    combine_log_path=combine_log_name[:combine_log_name.rfind('/')+1]
    with open(write_sh_name, writetype) as log_file:
        # delete log files in combine_log_path
        log_file.writelines('rm ' + combine_log_path + '* -rf\n')
        for logfilepath in path2logfiles:
            copyname = logfilepath.replace('/', '_')
            copycommand = 'cp ' + logfilepath + ' ' + combine_log_path + copyname[35:] + '\n'
            log_file.writelines(copycommand)

        log_file.writelines(
            'find ' + combine_log_path + ' -name "*.log" | xargs cat > ' + combine_log_name + '\n')
        log_file.writelines(
            'find ' + combine_log_path + ' -name "*.txt" | xargs cat > ' + combine_log_name + '\n')
        log_file.writelines('echo log file merged in: ' + combine_log_name)