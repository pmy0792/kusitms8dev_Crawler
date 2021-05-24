import requests
from bs4 import BeautifulSoup
import pandas as pd
import get_continent_and_code
import memoir_module
import save_to_file

continent_df=get_continent_and_code.df()

def run():
    df=make_memoir_df()
    save_to_file.to_excel(df)
    
def make_memoir_df():
    url="http://oiak.khu.ac.kr/program/memoirs.php?&perpage=15"
    df=scrape_pages(url)
    print(df)
    return df
    
def scrape_pages(url):
    df=pd.DataFrame(columns=["Univ","Field","College","Major","Continent","Country","Foreign Univ", "Semester","Info"])
    response=requests.get(url)
    result=response.text
    soup=BeautifulSoup(result,'html.parser')
    page_num=find_page_num(soup)
    for i in range(1, page_num+1):############
        print("Scraping page %s..."%i)
        page_url="http://oiak.khu.ac.kr/program/memoirs.php?&perpage=15"+"&page=%s"%i
        page_df=scrape_page(page_url)
        df=df.append(page_df,ignore_index=True)
    return df
        
def find_page_num(soup):
    max_num=soup.find('td').text
    print("max num: ",max_num)
    page_num=int(max_num)//15+1
    print("page num: ",page_num)
    return page_num

def scrape_page(url):
    response=requests.get(url)
    result=response.text
    soup=BeautifulSoup(result,'html.parser')
    
    post_list=soup.find('tbody').find_all('tr')

    df=pd.DataFrame(columns=["Univ","Field","College","Major","Continent","Country","Foreign Univ", "Semester","Info"])
    for post in post_list:
        memoir=make_memoir_obj(post)
        df=df.append({"Univ":"경희대학교",
                   "Field":memoir.field,
                   "College":memoir.college,
                   "Major":memoir.major,
                  "Continent":memoir.continent,
                  "Country":memoir.country,
                  "Foreign Univ":memoir.ex_univ,
                  "Semester":memoir.semester,
                  "Info": memoir.info},
                    ignore_index=True)
    return df

    
def make_memoir_obj(post):
    title=post.find('td',attrs={'class':'title'}).text.strip()
    left=title.find('[')
    right=title.find(']')
    country_str=title[left+1:right]
    continent, country = decide_continent_and_code(country_str)
    ex_univ=title[right+1:].lstrip()
    clg_and_major=post.find_all('td')[2].text.split(" ")
    if len(clg_and_major)==1:
        college="기타"
        major="기타"
    else:
        college=post.find_all('td')[2].text.split(" ")[0]
        major="".join(post.find_all('td')[2].text.split(" ")[1:])
    field=decide_field(major)
    date=post.find_all('td')[3].text
    semester=decide_semester(date)
    memoir_url="http://oiak.khu.ac.kr/program/" + post.find('a').attrs['href']
    response=requests.get(memoir_url)
    result=response.text
    soup=BeautifulSoup(result,'html.parser')
    info=""
    info_list=soup.find_all('tr')
    for i in info_list:
        s=i.text.replace("\r","").replace("\n","#")
        info+=s

    memoir_obj=memoir_module.memoir("경희대학교",field,college,major,continent,country,ex_univ,semester,info)
    return memoir_obj


def decide_semester(date):
    ymd=date.split(".")
    year=int(ymd[0])
    month=int(ymd[1])
    day=int(ymd[1])
    
    if 5<=month<=11:
        semester=1
    elif month<5 or month>11:
        semester=2
        year-=1
    
    result=str(year)+"-"+str(semester)
    return result
    
    
    
def decide_continent_and_code(country):
    continent= continent_df[continent_df["Country"]==country]["Continent"]
    country_code=continent_df[continent_df["Country"]==country]["Code"]
    if len(continent)==0:
        return "etc","etc"
    else:
        return continent.values[0], country_code.values[0]
    
def decide_field(major):
    clg1=["국어국문학과","사학과","철학과","응용영어통번역학과","영어영문학과","영어학부","영미어학부"]
    clg2=["법학부"]
    clg3=["국제통상·금융투자학과","국제통상·금융투자학과","경제학과","무역학과","정치외교학과","사회학과","미디어학과","행정학과","언론정보학과","회계ㆍ세무학과","국제교류과"]
    clg4=["경영학부","회계·세무학과","경영학과"]
    clg5=["관광학부","Hospitality경영학부","Hospitality경영학부 호텔경영학과","문화관광산업학과","조리산업학과","Hospitality경영학부 컨벤션경영학과","외식경영학과","Hospitality경영학부 조리·서비스경영학과","관광학부 문화관광콘텐츠학과","관광학부 관광학과"]
    clg6=["생물학과","화학과","물리학과","수학과","정보디스플레이학과","지리학과"]
    clg7=["식품영양학과","의상학과","아동가족학과","주거환경학과"]
    clg8=["의학과","의예과"]
    clg9=["한의예과","한의학과"]
    clg10=["치의학과","치의예과"]
    clg11=["한약학과","약과학과","약학과","약학과(2+4년제)"]
    clg12=["간호학과","간호학과(야)"]
    clg13=["작곡과","성악과","기악과"]
    clg14=["미술학부","미술학부 한국화","미술학부 회화","미술학부 조소"]
    clg15=["무용학부","무용학부 한국무용","무용학부 현대무용","무용학부 발레"]
    clg16=["자율전공학과"]
    clg17=["환경학및환경공학과","건축공학과","기계공학과","사회기반시스템공학과","화학공학과","건축학과","산업경영공학과","정보전자신소재공학과","원자력공학과"]
    clg18=["전자공학과","생체의공학과","전자·전파공학과"]
    clg19=["소프트웨어융합학과","컴퓨터공학과"]
    clg20=["우주과학과","응용화학과","응용물리학과","응용수학과"]
    clg21=["식물·환경신소재공학과","원예생명공학과","식품생명공학과","한방생명공학과","유전생명공학과","유전공학과","한방재료공학과"]
    clg22=["글로벌한국학과","국제학과"]
    clg23=["글로벌커뮤니케이션학부","글로벌커뮤니케이션학부 영미어문","한국어학과","일본어학과","중국어학과","러시아어학과","스페인어학과","프랑스어학과","글로벌커뮤니케이션학부 영미문화"]
    clg24=["도예학과","Post Modern음학학과","연극영화학과","산업디자인학과","환경조경디자인학과","의류디자인학과","디지털콘텐츠학과","시각디자인학과","시각정보디자인학과"]
    clg25=["태권도학과","체육학과","스포츠의학과","스포츠지도학과","골프산업학과","골프경영학과"]

    engineering=clg17+clg18+clg19+clg21
    nature=clg6+clg20
    society=clg2+clg3+clg4+clg5+clg22
    humanities=clg1+clg23
    art_sports=clg13+clg14+clg15+clg24+clg25
    medicine=clg8+clg9+clg10+clg11+clg12
    etc=clg7+clg16

    
    if major in engineering:
        return "공학"
    elif major in nature:
        return "자연과학"
    elif major in society:
        return "사회과학"
    elif major in humanities:
        return "인문대학"
    elif major in art_sports:
        return "예체능"
    elif major in medicine:
        return "의약"
    else:
        return "기타"

