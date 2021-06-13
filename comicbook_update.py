import re
import requests
from bs4 import BeautifulSoup

def main():
    #紀錄有更新再進行記錄更新
    update_flag = False

    # 文件檔紀錄要抓取的漫畫位置
    with open("read.txt", 'r', encoding="utf-8") as f:
        content_list = f.read().splitlines()
    f.close()

    #讀取line_notify 權杖
    with open("Line_notify.txt", 'r', encoding="utf-8") as ntf:
        ntf_Group = ntf.read().splitlines()
    ntf.close()
    
    combooksave =[]
    # 把每一行的漫畫都抓出來並分開
    for i in content_list:
        combook = i.split(',')
        #進行資料更新
        newcomic = send_update(combook[0], combook[1], combook[2],ntf_Group)
        if newcomic != "None" :
            combook[2] = newcomic 
            update_flag = True
        combooksave .append( [combook[0], combook[1], combook[2]])
    #沒更新就跳出
    if update_flag == False: return None,print("END")

    # 寫回更新項目
    file = open('read.txt', 'w', encoding="utf-8")
    for i in combooksave:
        file.writelines(i[0]+","+i[1]+","+i[2]+"\n")
    file.close()
    print("END")

#漫畫名稱 , 漫畫網路位置 , 最新更新的集數


def send_update(bookname, bookrul, bookold,ntf_Group):
    #抓取漫畫網頁
    response = requests.get(bookrul)
    soup = BeautifulSoup(response.text, "html.parser")

    #抓取最新集數
    booknew = soup.findAll('a', attrs={"class": "fed-btns-info fed-rims-info fed-part-eone", "href": re.compile(".html")}, limit=1)[0].get('title')

    #沒有新集數，跳出
    if bookold == booknew:
        return "None"
    #抓取最新集數html位置
    comichref = soup.findAll('a', attrs={"class": "fed-btns-info fed-rims-info fed-part-eone", "href": re.compile(".html")}, limit=1)[0].get('href')
        
    #將發送的 notify key 填入 發送
    for group in ntf_Group:
        headers = {
            "Authorization": "Bearer " + group.split(',')[0],
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {"message": bookname + ","+booknew + "  "+"https://www.cocomanhua.com"+comichref}
        r = requests.post("https://notify-api.line.me/api/notify",
                        headers=headers, params=params)
        print(r.status_code)  # 200

    return booknew


if __name__ == '__main__':
    main()
