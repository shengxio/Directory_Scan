import os, time,datetime
import pandas as pd
import numpy as np

from stat import *

def main():
    df_out          = getDIRdata(os.getcwd())
    df_xlsx         = df_out[(df_out.Category=='.xlsx')]
    df_csv          = df_out[(df_out.Category=='.csv')]
    col             = ['Date',
                       'Directory',
                       'Scanned By',
                       'Total Entities',
                       'Total Size']
    df_Rev          = pd.read_excel('Scan Summary.xlsx',sheet_name='summary')
    df_Rev          = df_Rev.append(pd.DataFrame(data = [[	datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"),
                                                            os.path.dirname(os.path.realpath(__file__)),
                                                            os.getlogin(),
                                                            df_out.shape[0],
                                                            df_out.sum()['Size']]],columns = col),ignore_index=True)
    writer = pd.ExcelWriter('Scan Log '+datetime.datetime.now().strftime('%y%m%d_%H%M%S')+'.xlsx', engine='xlsxwriter')
    df_out.to_excel(writer,sheet_name = 'Raw')
    writer.save()
	
    writer = pd.ExcelWriter('Data Log '+datetime.datetime.now().strftime('%y%m%d_%H%M%S')+'.xlsx', engine='xlsxwriter')
    df_xlsx.to_excel(writer,sheet_name = 'xlsx')
    df_csv.to_excel(writer,sheet_name = 'csv')
    writer.save()
	
    writer = pd.ExcelWriter('Scan Summary.xlsx', engine='xlsxwriter')
    df_Rev.to_excel(writer,sheet_name = 'summary')
    writer.save()

def getDIRdata(DIR,lvl = None):
    rootFolder      = os.path.basename(DIR)
    DIRls           = os.listdir(DIR)
    col             = [ 'Root',
                        'Entity',
                        'Category',
                        'Size',
                        'Date Creation',
                        'Date Last Access',
                        'Date Last Change']
    df_out          = pd.DataFrame(columns=col)
    for f in DIRls:
        pathname = os.path.join(DIR,f)
        mode =os.stat(pathname).st_mode
        if S_ISDIR(mode):
            df_raw = pd.DataFrame(data=[[rootFolder,
                                        f,
                                        'Subfolder',
                                        os.stat(pathname).st_size,
                                        time.asctime(time.localtime(os.stat(pathname).st_ctime)),
                                        time.asctime(time.localtime(os.stat(pathname).st_atime)),
                                        time.asctime(time.localtime(os.stat(pathname).st_mtime))]],columns=col)
            if lvl == None:
                df_raw = df_raw.append(getDIRdata(pathname),ignore_index=True)
            elif lvl !=None and lvl>0:
                df_raw = df_raw.append(getDIRdata(pathname,lvl-1),ignore_index=True)
        elif S_ISREG(mode):
            filename,file_ext = os.path.splitext(f)
            df_raw = pd.DataFrame(data=[[rootFolder,
                                        filename,
                                        file_ext,
                                        os.stat(pathname).st_size,
                                        time.asctime(time.localtime(os.stat(pathname).st_ctime)),
                                        time.asctime(time.localtime(os.stat(pathname).st_atime)),
                                        time.asctime(time.localtime(os.stat(pathname).st_mtime))]],columns=col)
        else:
            print('We don\'t know what ' +f+' is.')
        df_out=df_out.append(df_raw,ignore_index = True)
    return df_out

if __name__== '__main__':
    main()
