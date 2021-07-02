# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import requests
import os
import shutil
import ftplib
import pandas
import bs4
import re
import json

def downloadFile_HTTP(url:str, destination:str, filename:str):
    r = requests.get(url,stream=True)
    if not os.path.exists(destination):
        os.makedirs(destination)
    file_path = os.path.join(destination,filename)
    if r.ok:
        print("Saving", filename, "TO: === ",os.path.abspath(file_path))
        with open(file_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
    else:
        print("Download Failed status code {}\n{}".format(r.status_code, r.text))

def downloadFile_FTP(path:str,destination:str,filename:str):
    ftp = ftplib.FTP("ftp.cmegroup.com")
    ftp.login()
    root = "/span/data/"
    try:
        ftp.cwd(root+path)
        if not os.path.exists(destination):
            os.makedirs(destination)
        file_path = os.path.join(destination,filename)
    except OSError:
        print("Could not find or create error")
    except ftplib.error_perm:
        print("Could not find change to" + path)
    fileList = ftp.nlst()
    for file in fileList:
        if datetime.date.strftime(datetime.date.today() - datetime.timedelta(1),'%m%d') in file:
            if filename in file:
                try:
                    ftp.retrbinary("RETR " + file, open(os.path.join(destination, file), 'wb').write)
                except:
                    print("Could not download : " + file)






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #date time string mmdd
    dateStr_mmdd = datetime.date.strftime(datetime.date.today() - datetime.timedelta(1), '%m%d')
    dateStr_yyyymmdd = datetime.date.strftime(datetime.date.today()-datetime.timedelta(1),'%Y%m%d')
    dateStr_yymmdd = datetime.date.strftime(datetime.date.today() - datetime.timedelta(1),'%y%m%d')


    # ICUS File name
    # fileICUS_E = "NYB" + dateStr + "E.SP6.zip"

    file_name_ICUS_F = "NYB" + dateStr_mmdd + "F.SP6.zip"

   # ICEU soft Financial & soft commodities

    # fileICEU_Soft_Com_F = "FOX" + dateStr + "F.SP6.zip"
    # fileICEU_Equity_Op_F = "OPT" + dateStr + "F.SP6.zip"
    # fileICEU_Financial_F = "LIF" + dateStr + "F.SP6.zip"

   #ICEU file name
    # fileICEU_E = "IPE" + dateStr + "E.SP6.zip"
    # fileICEU_F = "IPE" + dateStr + "F.SP6.zip"


    url_ICUS = "https://www.theice.com/publicdocs/irm_files/icus/" + str(datetime.date.today().year) + "/" + \
              str(datetime.date.strftime(datetime.date.today(),'%m')) + "/";
    # url_ICEU_Financial_Soft_Com = "https://www.theice.com/publicdocs/irm_files/nyse/" + str(datetime.date.today().year) + "/" + \
    #                              str(datetime.date.strftime(datetime.date.today(),'%m')) + "/";
    # url_ICEU = "https://www.theice.com/publicdocs/irm_files/iceu/" + str(datetime.date.today().year) + "/" + \
    #           str(datetime.date.strftime(datetime.date.today(),'%m')) + "/";

   # File address
   # url_ICUS_E = url_ICUS + fileICUS_E
    url_ICUS_F = url_ICUS + file_name_ICUS_F

    # url_ICEU_Financial_Soft_Com_F = url_ICEU_Financial_Soft_Com + fileICEU_Soft_Com_F
    # url_ICEU_Equity_Op_F = url_ICEU_Financial_Soft_Com + fileICEU_Equity_Op_F
    # url_ICEU_Financial_F = url_ICEU_Financial_Soft_Com + fileICEU_Financial_F
    # url_ICEU_E = url_ICEU + fileICEU_E
    # url_ICEU_F = url_ICEU + fileICEU_F

   # Local file name
    folder_ICUS = "ICUS"
   # folder_ICEU = 'ICEU'
    shareFolderPath = "C:\\Esunny_Span\\" + datetime.date.strftime(datetime.date.today(),'%Y%m%d') + "\\"
    destination_ICUS = shareFolderPath + folder_ICUS
    # destination_ICEU = shareFolderPath + folder_ICEU

    if os.path.exists(shareFolderPath):

        shutil.rmtree(shareFolderPath)

    os.makedirs(shareFolderPath)

    r_euex = requests.get("https://www.eurexchange.com/exchange-en/data/clearing-files/risk-parameters/")
    r_euex.raise_for_status()
    soup = bs4.BeautifulSoup(r_euex.text,'html.parser')
    url_euex = "https://www.eurexchange.com" + soup.find(href=re.compile("IndicativePrismaMarginRequirements.xls")).get('href')


    file_name_asx = "asxclfendofdayriskparameterfile" + dateStr_yymmdd + ".zip"
    file_name_bmd = "bmd_" + dateStr_yyyymmdd + "_s.pa2"
    file_name_lme = "lme." + dateStr_yyyymmdd + ".s.dat.zip"
    file_name_hkf = "hkex." + dateStr_yyyymmdd + ".s.pa2.zip"
    file_name_cme = "cme." + dateStr_yyyymmdd + ".c.pa2.zip"
    file_name_sgx = "sgx." + dateStr_yyyymmdd + ".z.zip"
    file_name_jsc = "jsc" + dateStr_yyyymmdd + "_1700.zip"
    file_name_euex = "IndicativePrismaMarginRequirements.xls";



    downloadFile_FTP("asxclf", shareFolderPath,file_name_asx)
    downloadFile_FTP("bmdc",shareFolderPath,file_name_bmd)
    downloadFile_FTP("lme",shareFolderPath,file_name_lme)
    downloadFile_FTP("hkf",shareFolderPath,file_name_hkf)
    downloadFile_FTP("cme",shareFolderPath,file_name_cme)
    downloadFile_FTP("smx",shareFolderPath,file_name_sgx)
    downloadFile_FTP("jsc",shareFolderPath,file_name_jsc)

    #download ICEU
    # downloadFile_HTTP(url_ICEU_Financial_Soft_Com_F, shareFolderPath, fileICEU_Soft_Com_F)
    # downloadFile_HTTP(url_ICEU_Equity_Op_F, shareFolderPath, fileICEU_Equity_Op_F)
    # downloadFile_HTTP(url_ICEU_E, shareFolderPath, fileICEU_E)
    # downloadFile_HTTP(url_ICEU_F, shareFolderPath, fileICEU_F)
    # downloadFile_HTTP(url_ICEU_Financial_F, shareFolderPath, fileICEU_Financial_F)

    #download ICUS
   # downloadFile_HTTP(url_ICUS_E, shareFolderPath, fileICUS_E)
    downloadFile_HTTP(url_ICUS_F, shareFolderPath, file_name_ICUS_F)
    downloadFile_HTTP(url_euex,shareFolderPath,file_name_euex)

















