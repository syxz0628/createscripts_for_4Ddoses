import dafmbr_lmdout
import read_CT_info
import read_motion_info
import argparse
# Press the green button in the gutter to run the script.
import reg_4DCT
import voi_4D
import voi_ave2p00

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pat", required=True,
                        help="patient info file folder,check /u/ysheng/MyAIXd/projects/patient/commands/01-prepare4Ddata/patient_info.txt for format.")
    parser.add_argument("-r", "--reg", required=False, action='store_true',
                        help="Generate/Print Regstration commandlines based on 4D cts, necessary info in patient: id, name, ct folder. makesure 00 is the reference image")
    parser.add_argument("-v", "--voi", required=False, action='store_true',
                        help="Generate/Print exec for generate 4D vois from trafo and 3D vois. Necessary info in patient: id, name, ct folder and write to exec file path. makesure 00 is the reference image")
    parser.add_argument("-a", "--a20", required=False, action='store_true',
                        help="Generate/Print exec for reg and generate vois for phase 00 from average 3D vois. Necessary info in patient: id, name, ct folder. sh file written in /patient/commands/01-prepare4Ddata/03_3Dvois_ave_phase00.sh")
    parser.add_argument("-m", "--motionpath", required=False, nargs='?',
                        help="write script to generate the lmdout info for each plans.")

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
    if args.reg:
        reg_cts=reg_4DCT.class_reg_4DCT(CTinfo)
        reg_cts.fun_auto_reg_4DCT()
    if args.voi:
        voi_4D=voi_4D.class_gen_4D_vois(CTinfo)
        voi_4D.fun_preparefolder()
        voi_4D.fun_gen_4D_vois()
    if args.a20:
        voi_3D=voi_ave2p00.class_gen_ave_00_vois(CTinfo)
        voi_3D.fun_preparefile()
        voi_3D.fun_gen_ph00_vois_exec()
    if args.motionpath!=None:
        dafmbrdata=read_motion_info.class_readmotion_info(args.motionpath)
        dafmbrdata.fun_readpat_motion_info()
        creatlmdoutsh=dafmbr_lmdout.class_dafmbr_lmdout_script(CTinfo,dafmbrdata)