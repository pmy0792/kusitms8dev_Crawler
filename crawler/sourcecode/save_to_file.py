#import xlwt
import time

def to_excel(df):
    #n=time.localtime()
    #s='%04d-%02d-%02d-%02d-%02d-%02d'%(n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)
    file_name=input("xls 파일로 저장합니다. 파일 이름 입력해주세요: (예: my_result.xls) ")
    df.to_excel("../{}.xls".format(file_name),index=False)
    #df.to_csv(s+"\\result.csv",index=False,encoding='utf-8-sig')
    