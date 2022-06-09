import read_pat_info
import argparse
# Press the green button in the gutter to run the script.
import reg_4DCT

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pat", required=True,
                        help="patient info file folder,check /u/ysheng/MyAIXd/projects/patient/commands/01-prepare4Ddata/patient_info.txt for format.")
    #parser.add_argument("-p","--mpos", required=False , nargs='?',  const="default_directory", help="write to .mpos file, following by directory and file name or default the same path as .daf",  default="nompos")
    parser.add_argument("-r", "--reg", required=False, action='store_true',
                        help="Regstration based on 4D cts, necessary info in patient: id, name, ct folder. makesure 00 is the reference image")
    parser.add_argument("-s","--showfigs", required=False,  action='store_true', help="show daf and related figures", default="False")
    parser.add_argument("-m","--mbr", nargs='?',required=False, help="machine beam record .xml file path")
    parser.add_argument("-t", "--timeoffset", required=False, type=int, nargs='+',
                        help="Time offset in msec,to adjust results in ~250ms level that was added to system determined timeoffset value;multiple values are acceptable, e.g. -t 250 -250 100",
                        default=250)
    parser.add_argument("-w", "--writetxt", required=False, action='store_true', help="write all data in txt for plot",
                        default="False")
    parser.add_argument("-l", "--lmdout", required=False, nargs='?',
                        help="write to .lmdout file directory, following by directory and file name or default the same path as MBR .xml")
    parser.add_argument("-i", "--initialspot", required=False, type=int, nargs='+',
                        help="Time offset of the first spot of each spill in .msec., default 10ms", default=10)
    parser.add_argument("-z", "--showdebug", required=False, type=int, help="show all figures for debug. MBR time shift by the given value")
    args = parser.parse_args()

    patinfo=read_pat_info.class_readpat_info(args.pat)
    patinfo.fun_readpat_info()
    if args.reg:
        reg_cts=reg_4DCT.class_reg_4DCT(patinfo)
        reg_cts.fun_auto_reg_4DCT()