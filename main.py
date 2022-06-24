import sys
import dafmbr_lmdout
import read_CT_info
import read_motion_info
import argparse
# Press the green button in the gutter to run the script.
import reg_4DCT
import voi_4D
import voi_ave2p00
import dose_recon_3D
import dose_recon_4D
import temp_write_planinfo

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pat", required=True,
                        help="patient info file folder,check /u/ysheng/MyAIXd/projects/patient/commands/patient_info.txt for format.")
    parser.add_argument("-a", "--a20", required=False, action='store_true',
                        help="Generate/Print exec for reg and generate vois for phase 00 from average 3D vois. Necessary info in patient: id, name, ct folder. sh file written in /patient/commands/01-prepare4Ddata/03_3Dvois_ave_phase00.sh")
    parser.add_argument("-r", "--reg", required=False, action='store_true',
                        help="Generate/Print Regstration commandlines based on 4D cts, necessary info in patient: id, name, ct folder. makesure 00 is the reference image")
    parser.add_argument("-v", "--voi", required=False, action='store_true',
                        help="Generate/Print exec for generate 4D vois from trafo and 3D vois. Necessary info in patient: id, name, ct folder and write to exec file path. makesure 00 is the reference image")
    parser.add_argument("-m", "--motionpath", required=False, nargs='?',
                        help="path to motion info folder, required if -L, -T, -F exist")
    parser.add_argument("-L", "--lmdoutsh", required=False, action='store_true',
                        help="write script to generate the lmdout info for each plans.")
    parser.add_argument("-T", "--ThreeDrec", required=False, action='store_true',
                        help="Generate 3D plans exec files and sh file.")
    parser.add_argument("-F", "--FourDrec", required=False, action='store_true',
                        help="Generate 4D plans exec files and sh file.")
    parser.add_argument("-t", "--temp", required=False, action='store_true',
                        help="Write some tempinfo.")
    # parser.add_argument("-s","--showfigs", required=False,  action='store_true', help="show daf and related figures", default="False")
    # parser.add_argument("-m","--mbr", nargs='?',required=False, help="machine beam record .xml file path")
    # parser.add_argument("-t", "--timeoffset", required=False, type=int, nargs='+',
    #                     help="Time offset in msec,to adjust results in ~250ms level that was added to system determined timeoffset value;multiple values are acceptable, e.g. -t 250 -250 100",
    #                     default=250)
    # parser.add_argument("-w", "--writetxt", required=False, action='store_true', help="write all data in txt for plot",
    #                     default="False")
    # parser.add_argument("-l", "--lmdout", required=False, nargs='?',
    #                     help="write to .lmdout file directory, following by directory and file name or default the same path as MBR .xml")
    # parser.add_argument("-i", "--initialspot", required=False, type=int, nargs='+',
    #                     help="Time offset of the first spot of each spill in .msec., default 10ms", default=10)
    # parser.add_argument("-z", "--showdebug", required=False, type=int, help="show all figures for debug. MBR time shift by the given value")
    args = parser.parse_args()

    CTinfo=read_CT_info.class_readpat_info(args.pat)
    CTinfo.fun_readpat_info()
    if args.a20:
        voi_3D=voi_ave2p00.class_gen_ave_00_vois(CTinfo)
        voi_3D.fun_preparefile()
        voi_3D.fun_gen_ph00_vois_exec()
    if args.reg:
        reg_cts=reg_4DCT.class_reg_4DCT(CTinfo)
        reg_cts.fun_auto_reg_4DCT(args.pat)
    if args.voi:
        voi_4D=voi_4D.class_gen_4D_vois(CTinfo)
        voi_4D.fun_preparefolder()
        voi_4D.fun_gen_4D_vois()
    if args.motionpath!=None:
        dafmbrdata=read_motion_info.class_readmotion_info(args.motionpath)
        dafmbrdata.fun_readpat_motion_info()
    if args.lmdoutsh and args.motionpath!=None: # output lmdout sh
        creatlmdoutsh=dafmbr_lmdout.class_dafmbr_lmdout_script(CTinfo,dafmbrdata)
        creatlmdoutsh.fun_create_lmdout_sh()
    elif args.lmdoutsh:
        print('Path 2 file for patient plan and motion paramters "-m" is necessary for output the lmdout file ')
        sys.exit()
    if args.ThreeDrec and args.motionpath!=None:  # output 3D plan exec file.
        dose_recon_3D_exec=dose_recon_3D.class_dose_recon_3D(CTinfo,dafmbrdata)
        dose_recon_3D_exec.fun_create_3D_dose_recon_exec()
        dose_recon_3D_exec.fun_create_3D_dose_run_sh()
    elif args.ThreeDrec:
        print('Path 2 file for patient plan and motion paramters "-m" is necessary for generate the 3D plan')
        sys.exit()
    if args.FourDrec and args.motionpath!=None:  # output 3D plan exec file.
        dose_recon_4D_exec=dose_recon_4D.class_dose_recon_4D(CTinfo,dafmbrdata)
        dose_recon_4D_exec.fun_create_4D_dose_recon_exec()
        #dose_recon_4D_exec.fun_create_4D_dose_run_sh()
    elif args.ThreeDrec:
        print('Path 2 file for patient plan and motion paramters "-m" is necessary for generate the 3D plan')
        sys.exit()
    if args.temp:
        tempinfo=temp_write_planinfo.class_temp(CTinfo, dafmbrdata)
        tempinfo.fun_tempwrite()
