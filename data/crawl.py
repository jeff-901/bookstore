import requests
import re
import random
import time
from bs4 import BeautifulSoup
import bs4
from fake_useragent import UserAgent

ua = UserAgent()

books = []
discounts = []
cookie = {
    "bid": "6183e2a207286",
    "_gcl_au": "1.1.1678734493.1636033188",
    "cid": "kypss95053",
    "pd": "B4MPDFMstRRagO9wOXmP3pNPoI",
    "stepsession": "YaCaCwo8DR4AAT5h8nYAAAAc",
    "ssid": "6183e2a207286.1637940082",
}
for i in range(10703023, 11000000):
    cookie["ssid"] = (
        "6183e2a207286.16379400" + str(random.randint(0, 9)) + str(random.randint(0, 9))
    )
    print(f"https://www.books.com.tw/products/00{i:08}", end="\r")
    time.sleep(0.5)
    flag = True
    while flag:
        try:
            res = requests.get(
                f"https://www.books.com.tw/products/00{i:08}",
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
                    "user-agent": ua.random,
                },
                cookies=cookie,
            )
            flag = False
        except:
            time.sleep(60)
            flag = True
    if res.status_code == 404:
        print(f"{i:08}: {res.status_code}", end="\r")
        continue
    else:
        retry = 0
        while res.status_code != 200 and retry < 3:
            time.sleep(60)
            try:
                res = requests.get(
                    f"https://www.books.com.tw/products/00{i:08}",
                    headers={"user-agent": ua.random},
                    cookies=cookie,
                )
            except:
                pass
            if res.status_code == 404:
                retry = 3
                break
            retry += 1
    if retry >= 3:
        continue
    try:
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "lxml")
        soup.prettify()
        book_id = i
        name = "None"
        author = "None"
        author_original = "None"
        translator = "None"
        publishing_date = "None"
        publishing_house = "None"
        price = "None"
        ISBN = "None"
        discount_price = "None"
        expire_date = "None"
        name = soup.find_all("div", class_="type02_p002")[0].h1.text
        # print(name)
        basic_information = soup.find_all("div", class_="type02_p003")[0].ul
        lis = basic_information.find_all("li", recursive=False)
        for li in lis:
            # print(li.children)
            children = [_ for _ in li.children]
            if len(children) == 1:
                if re.match("出版日期*", li.text):
                    publishing_date = li.text[5:]
                    # print(publishing_date)
                elif re.match("語言*", li.text):
                    language = li.text[3:]
                    # print(language)
            else:
                if re.match("原文作者", children[0]):
                    author_original = children[1].text
                    # print(author_original)
                elif re.match("譯者", children[0]):
                    translator = children[1].text
                    # print(translator)
                elif re.match("出版社", children[0]):
                    publishing_house = children[1].text
                    # print(publishing_house)
                else:
                    if (
                        len(children) > 2
                        and type(children[2]) == bs4.element.NavigableString
                        and re.match("作者", children[2].strip())
                    ):
                        author = children[3].text
                        if "," in author:
                            raise Exception()
        price_ul = soup.find_all("ul", class_="price")[0]
        price_ul_len = len(price_ul.find_all("li", recursive=False))
        price = price_ul.find_all("li", recursive=False)[0].em.text
        # print(price)
        if price_ul_len > 1:
            discount_price = (
                price_ul.find_all("li", recursive=False)[1]
                .find_all("strong", recursive=False)[1]
                .b.text
            )
            # print(discount_price)
            try:
                expire_date = price_ul.find_all("li", recursive=False)[2].text
                if expire_date[:4] == "優惠期限":
                    expire_date = expire_date[5:]
                    expire_date = expire_date.replace("年", "/")
                    expire_date = expire_date.replace("月", "/")
                    expire_date = expire_date.replace("日", "")

                    expire_date = expire_date.replace("止", "")
                    discounts = [str(book_id), discount_price, expire_date]
                else:
                    discount = [str(book_id), discount_price, ""]
                    # print(expire_date)
            except:
                discounts = [str(book_id), discount_price, ""]

        detail_div = soup.find_all("h3", text="詳細資料")[0].parent.div
        if detail_div.ul.li.text[:4] == "ISBN":
            ISBN = detail_div.ul.li.text[5:]
        else:
            raise Exception()
        # print(ISBN)
        book = [
            str(book_id),
            ISBN,
            name,
            author,
            author_original,
            translator,
            publishing_house,
            publishing_date,
            price,
        ]

        with open("book.csv", "r") as f:
            data = f.read()
        with open("book.csv", "w") as f:
            f.write(data)
            f.write(",".join(book) + "\n")
        with open("discount.csv", "r") as f:
            data = f.read()
        with open("discount.csv", "w") as f:
            f.write(data)
            f.write(",".join(discount) + "\n")
    except Exception as e:
        # raise e
        # break
        pass
