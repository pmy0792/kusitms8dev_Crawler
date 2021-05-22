import pandas as pd
import get_continent_and_code
import memoir_module
import save_to_file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

continent_df=get_continent_and_code.df()

def run():
    df=make_memoir_df()
    print(df)
    save_to_file.to_excel(df)

def awake_driver(URL):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver_path="C:/Users/user/Downloads/chromedriver/chromedriver.exe"

    driver=webdriver.Chrome(driver_path)
    driver.get(URL)
    driver.implicitly_wait(10)
    return driver

def make_memoir_df():
    URL="https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=1310&CONTENTS_NO=19&P_TAB_NO=7"
    driver=awake_driver(URL)
    page_num=find_page_num(driver)
    page_links=[URL+"#page{}".format(page) for page in range(1,page_num+1)]
    cau_df=scrape_pages(page_links,driver)
    return cau_df


def scrape_pages(page_links,driver):
    cau_df=pd.DataFrame(columns=["Univ","Field","College","Major","Continent","Country","Foreign Univ", "Semester","Info"])
    for idx, page_link in enumerate(page_links):
        print("\nscraping page {}...".format(idx+1))
        driver.get(page_link)
        time.sleep(2)
        post_table_len=len(driver.find_elements_by_css_selector("#tbody > tr"))
        
        for i in range(post_table_len):
            #row_items=driver.find_elements_by_xpath("//*[@id=\"tbody\"]/tr")[i]
            row_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[@id=\"tbody\"]/tr")))
            row_items = row_items[i]
            link= WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"tbody\"]/tr[{}]/td[4]/a".format(i+1))))
            link.click()
            memoir=make_memoir_obj(driver)
            cau_df=cau_df.append({"Univ":"CAU",
                        "Field":memoir.field,
                    "College":memoir.college,
                    "Major":memoir.major,
                    "Continent":memoir.continent,
                    "Country":memoir.country,
                    "Foreign Univ":memoir.ex_univ,
                    "Semester":memoir.semester,
                    "Info": memoir.info},
                        ignore_index=True)
            driver.back()
            driver.implicitly_wait(10)
    return cau_df

def scrape_a_post(i,driver):
    #row_items=driver.find_elements_by_xpath("//*[@id=\"tbody\"]/tr")[i]
    #print(row_items.text)

    row_items=WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//*[@id=\"tbody\"]/tr")))
    row_items=row_items[i]
    WebDriverWait(driver, 10).until(
                        EC.text_to_be_present_in_element(
                            (By.CLASS_NAME, "act_view")))
    link=row_items.find_elements_by_tag_name("td")[3].find_element_by_tag_name("a")
    link.click()
    driver.implicitly_wait(10)
    memoir=make_memoir_obj(driver)
    return memoir

def find_page_num(driver):
    num_of_post=int(driver.find_element_by_css_selector("#tbody > tr:nth-child(1) > td:nth-child(1)").text)
    page_num=num_of_post//10+1
    return page_num

def decide_continent_and_code(country):
    continent= continent_df[continent_df["Country"]==country]["Continent"]
    country_code=continent_df[continent_df["Country"]==country]["Code"]
    if len(continent)==0:
        return "etc","etc"
    else:
        return continent.values[0], country_code.values[0]

def make_memoir_obj(driver):
        head=WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=\"sendForm\"]/div/div[1]/table/tbody/tr[1]/td")))
        time.sleep(2)
        head_text=head.text
        print("head_text: ",head_text)
        country,ex_univ = map(str,head_text.split(' > ')[1:])
        continent, code=decide_continent_and_code(country)
        dptmt=driver.find_element_by_xpath("//*[@id=\"sendForm\"]/div/div[1]/table/tbody/tr[3]/td[1]").text.split()
        if len(dptmt)==0:
            college=None
            major=None
        elif len(dptmt)==1:
            college=dptmt[0]
            major=dptmt[0]
        else:
            college=dptmt[0]
            major=dptmt[1]
        semester=driver.find_element_by_xpath("//*[@id=\"sendForm\"]/div/div[1]/table/tbody/tr[3]/td[2]").text
        field=decide_field(college)
        driver_info_list=driver.find_elements_by_css_selector("#sendForm > div > div.lineList_tbW > table > tbody > tr")[3:]
        info_list=[d.text for d in driver_info_list]
        info="".join(info_list)
        memoir_obj=memoir_module.memoir("CAU",field,college,major,continent,country,ex_univ,semester,info)
        return memoir_obj

def decide_field(clg):
    engineering=["AI학과","소프트웨어학부","소프트웨어학과","융합교양학부","융합공학부","디지털이미징학과","바이오메디컬공학과","나노바이오소재공학과","전자전기공학부","전자전기공학과","발전전기학과","원자력학과","발전기계학과","기계공학과","화학신소재공학과","건축학과","건축공학과","건설환경플랜트공학과","도시시스템공학과","첨단소재공학과","에너지시스템공학부","기계공학부","사회기반시스템공학부","건축학부","화학신소재공학부","식품공학과","식품영양학과","동물생명공학과","식물생명공학과","생명자원공학부","식품공학부","시스템생명공학과","예술공학대학","생명공학대학","공과대학","창의ICT공과대학","소프트웨어대학"]
    nature=["자연과학대학","물리학과","화학과","생명과학과","수학과"]
    society=["광고홍보학과","국제물류학과","지식경영학부","산업보한학과","경영학과","경영학부","경제학과","경제학부","응용통계학과","사회과학대학","경영경제대학","정치국제학과","공공인재학부","심리학과","문헌정보학과","사회복지학부","미디어커뮤니케이션학부","도시계획·부동산학과","사회학과","디지털미디어콘텐츠학과","언론정보학과"]
    humanities=["인문대학","국어국문학과","영어영문학과","유럽문화학부","일본어문학과","중국어문학과","아시아문화학부","철학과","역사학과","독일어문학과","프랑스어문학과","러시아어문학과"]
    art_and_sports=["생활·레저스포츠과","스포츠산업과","골프과","TV방송연예과","전통예술학부","연희예술과","실용음악과","음악예술학과","관현악과","피아노과","성악과","작곡과","음악학부","패션학과","실내환경디자인학과","시각디자인학과","공예학과","산업디자인학과","미술학부","한국화학과","서양화학과","조소학과","공연영상창작학부","스포츠과학과","스포츠과학부","연극학과","영화학과","공간연출학과","예술대학","체육대학"]
    education=["사범대학","교육학과","유아교육과","영어교육과","체육교육과"]
    medicine=["간호학과","의과대학","약학대학","적십자간호대학","의학부","약학부"]
    if clg==None:
        return "etc"
    elif clg in engineering or "공학" in clg or "engineering" in clg or "소프트웨어" in clg:
        return "공학"
    elif clg in nature or "과학" in clg:
        return "자연과학"
    elif clg in society or "문헌" in clg or "신문" in clg or "글로벌" in clg or "광고" in clg or "국제" in clg or "사회" in clg or "도시" in clg or "미디어" in clg or "커뮤니케이션" in clg or "경영" in clg or "경제" in clg:
        return "사회과학"
    elif clg in humanities or "문과" in clg or "불어" in clg or "어문" in clg or "정치" in clg or "문학" in clg or "철학" in clg or "영어" in clg or "독어" in clg or "중국어" in clg or "일본어" in clg:
        return "인문대학"
    elif clg in art_and_sports or "패션" in clg or "스포츠" in clg or "디자인" in clg or "음악" in clg or "예술" in clg:
        return "예체능"
    elif clg in education:
        return "교육"
    elif clg in medicine or "간호" in clg:
        return "의약"
    else:
        print("분류에없는학과!!",clg)
        return "etc"

