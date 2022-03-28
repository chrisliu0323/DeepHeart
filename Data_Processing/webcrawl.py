import requests
from bs4 import BeautifulSoup
import time
import csv
from gittttt.Data_ETL_Automation.googlesheetAPI.connect_spreadsheet import df
from gittttt.Data_ETL_Automation.googlesheetAPI.connect_spreadsheet import data_range_start
from gittttt.Data_ETL_Automation.googlesheetAPI.connect_spreadsheet import data_range_end


### creat a csv file
date = time.strftime("%m%d" + "-" + "%H%M", time.localtime())
str_data_range_start = str(data_range_start)
str_data_range_end = str(data_range_end)
spec = str_data_range_start + "~" + str_data_range_end + "___" + date
path_csv = "C:\python\workspace\group4\\" + spec + ".csv"
with open(path_csv, "w", encoding='utf-8', newline="") as f:
    write_f = csv.writer(f)
    write_f.writerow(["label", "review"])


###write the text and label of data in the data ID range to the csv file
for data_ID in range(data_range_start, data_range_end + 1):

    #get url and rating from df
    str_data_ID = str(data_ID)

    url_df = df.loc[df['ID'] == str_data_ID, 'URL']
    url = url_df.iat[0]

    rating_df = df.loc[df['ID'] == str_data_ID, 'RATING']
    rating = rating_df.iat[0]

    #get the text from url using webcrawl
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    #crawl web data from online forum penpal
    def journal_to_json():
        a = soup.find("meta", attrs={'name': "description"})
        b = str(a)
        c = b[15:-22].strip()
        d = c.replace("\n", ",")
        return ''.join(d.split())


    #crawl web data from online forum ptt
    def ptt_to_json():
        a = soup.find(id='main-container').text
        b = a.split("--")[0]
        c = b.split("\n")[2:]
        for i in range(0, len(c)):
            if c[i] == "":
                c[i] = ","
        del c[-1]
        del c[-1]
        return "".join(c)


    #crawl web data from online forum dcard
    def dcard_to_json():
        a = soup.find('div', class_='phqjxq-0 iJJmxb').getText()
        b = a.replace("\n", ",")
        return ''.join(b.split())


    article = ""
    if "dcard" in url:
        article = dcard_to_json()
    elif "ptt" in url:
        article = ptt_to_json()
    elif "penpal" in url:
        article = journal_to_json()
    else:
        print("error")

    #store the rating and article text to the csv
    with open(path_csv, "a", encoding='utf-8', newline="") as f:
        write_f = csv.writer(f)
        write_f.writerow([rating, article])