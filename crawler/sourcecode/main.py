import khu_crawler
import cau_crawler
import pandas as pd
import time

def bring_file_to_df(filename,df):
    f=pd.read_excel(filename)
    df=df.append(f,ignore_index=True)
    return df
if __name__=="__main__":
    khu_crawler.run()
    cau_crawler.run()
    file_names=[]
    df = pd.DataFrame(
        columns=["Univ", "Field", "College", "Major", "Continent", "Country", "Foreign Univ", "Semester", "Info"])

    print("읽어올 파일 이름 입력. 입력 끝나면 q 입력")
    i=input()
    while (1):
        if i=="q":
            break
        else:
            if not (i.endswith(".xls")):
                print("올바른 파일 형식 아님. 다시 입력: ")
                i=input()
            else:
                file_names.append(i)

    for file_name in file_names:
            df=bring_file_to_df(file_name,df)

    n = time.localtime()
    s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)
    df.to_excel(s+".xls",index=False)
    print("파일 저장 완료")
