# oding = utf-8
# -*- coding:utf-8 -*-

# 由YBB(Yubadboy)编写，其所有权归属Yubadboy，Yubadboy有权对代码做修改

from decimal import Decimal

import json,re,hashlib
import selenium.common.exceptions
import selenium.webdriver.support.ui as ui
from selenium import webdriver

# 获取预算和开始网站
budget = float(input("Budget:"))

# 这两项千万不要动
buffGetUrl = "https://buff.163.com/market/csgo#tab=selling&max_price={}&page_num={}"
igxeSearchUrl = "https://www.igxe.cn/market/csgo?keyword={}"

# 读取配置文件
with open("config.json", "r") as configFile:
    config = json.load(configFile)

# 这项是MicrosoftWebDriver（Edge驱动）的路径
executable_path = config["executable_path"]

# 这两项是网易buff的cookie，可在登录时查看network找到
buffCookie1 = {"name": "session",
               "value": config["cookies"]["session"]}
buffCookie2 = {"name": "csrf_token",
               "value": config["cookies"]["csrf_token"]}

way=config["way"]
pageNum = config["pageNum"]
jewelryNum=config["jewelryNum"]

minDisparity=config["minDisparity"]
count = 1
jewelryCount = 1

minStockA=config["minStockA"]
minStockB=config["minStockB"]

gotJewelry=[]

def getBuffDriver():
    driver = webdriver.Edge(executable_path=executable_path)
    driver.get(buffGetUrl.format(budget, count))
    driver.add_cookie(buffCookie1)
    driver.add_cookie(buffCookie2)
    driver.get(buffGetUrl.format(budget, count))
    driver.refresh()
    return driver


def setBuffDriverGoto(driver, budget, count):
    driver.get(buffGetUrl.format(budget, count))
    driver.refresh()


def getIgxeDriver():
    driver = webdriver.Edge(executable_path=executable_path)
    return driver


def setIgxeDriverGoto(driver, name):
    driver.get(igxeSearchUrl + name)
    driver.refresh()


def getBuffCommission(price):
    commission = float(Decimal(str(price)) * Decimal("0.01"))
    return commission


def getIgxeCommission(price):
    commission = float(Decimal(str(price)) * Decimal("0.025"))
    if commission > 100:
        return 100
    return commission


def dataPrint(buffDriver, igxeDriver):
    global jewelryCount
    if way=="page" and count>pageNum:
        return 1
    buffWait = ui.WebDriverWait(buffDriver, 10)
    buffWait.until(
        lambda WaitDriver: buffDriver.find_element_by_class_name("card_csgo").find_elements_by_tag_name("li"))
    eleList = buffDriver.find_element_by_class_name("card_csgo").find_elements_by_tag_name("li")
    for eleGoods in eleList:
        if way=="num" and jewelryCount>jewelryNum:
            return 1
        href = eleGoods.find_element_by_tag_name("a").get_attribute("href")
        title = eleGoods.find_element_by_tag_name("a").get_attribute("title")
        stock = eleGoods.find_element_by_tag_name("p").find_element_by_tag_name("span").text.strip()
        price = eleGoods.find_element_by_tag_name("p").find_element_by_tag_name("strong").text.strip()[2:]
        try:
            abrase = eleGoods.find_element_by_css_selector(".tag").text.strip()
        except selenium.common.exceptions.NoSuchElementException:
            abrase = "该物品无磨损信息"
        buffResult = [href, title, stock, price, abrase]
        if hashlib.md5(buffResult[0].encode("utf-8")).hexdigest() in gotJewelry:
            continue
        setIgxeDriverGoto(igxeDriver, buffResult[1])
        igxeWait = ui.WebDriverWait(igxeDriver, 10)
        try:
            igxeWait.until(lambda WaitDriver: igxeDriver.find_element_by_class_name("market").find_element_by_class_name(
                "container").find_element_by_class_name("list").find_element_by_tag_name("a"))
        except selenium.common.exceptions.TimeoutException:
            continue
        secondGoods = igxeDriver.find_element_by_class_name("market").find_element_by_class_name(
            "container").find_element_by_class_name(
            "list").find_elements_by_tag_name("a")
        SecondGoods = None
        for goods in secondGoods:
            if goods.find_element_by_class_name("name").text == buffResult[1]:
                SecondGoods = goods
        if SecondGoods is None:
            continue
        href = SecondGoods.get_attribute("href")
        title = buffResult[1]
        stock = SecondGoods.find_element_by_class_name("info").find_element_by_class_name("stock").text.strip()[
                3:] + "件在售"
        price = SecondGoods.find_element_by_class_name("info").find_element_by_class_name("price").text.replace("\n",
                                                                                                                "").strip()[
                1:5]
        abrase = buffResult[4]
        igxeResult = [href, title, stock, price, abrase]
        buffPrice = float(buffResult[3])
        igxePrice = float(igxeResult[3])
        profit = float(Decimal(str(max(buffPrice, igxePrice))) - Decimal(str(min(buffPrice, igxePrice))))
        if profit < minDisparity:
            continue
        if buffPrice == igxePrice:
            continue
        elif buffPrice > igxePrice:
            fromResult = igxeResult
            toResult = buffResult
            commissionFunc = getBuffCommission
            fromPlatform = "IGXE"
            toPlatform = "BUFF"
        else:
            fromResult = buffResult
            toResult = igxeResult
            commissionFunc = getIgxeCommission
            fromPlatform = "BUFF"
            toPlatform = "IGXE"
        if int(re.sub("\D", "", fromResult[2]))<minStockA or int(re.sub("\D", "", toResult[2]))<minStockB:
            continue
        commission = Decimal(str(commissionFunc(toResult[3])))
        netProfit = float(Decimal(str(profit)) - commission)
        print("=" * 50)
        print("第一平台数据（进货方）", fromPlatform)
        print("物品名称：", fromResult[1])
        print("物品价格：", fromResult[3])
        print("物品磨损：", fromResult[4])
        print("物品在售数量：", fromResult[2])
        print("物品链接：", fromResult[0])
        print("-" * 40)
        print("第二平台数据（出货方）", toPlatform)
        print("物品名称：", toResult[1])
        print("物品价格：", toResult[3])
        print("物品磨损：", toResult[4])
        print("物品在售数量：", toResult[2])
        print("物品链接：", toResult[0])
        print("-" * 40)
        print("利润：", profit)
        print("净利润：", netProfit)
        print("手续费：", commission)
        jewelryCount+=1
        gotJewelry.append(hashlib.md5(buffResult[0].encode("utf-8")).hexdigest())
    return 0


# 获取物品链接
buffDriver = getBuffDriver()
igxeDriver = getIgxeDriver()

while 1:
    if count > 1:
        setBuffDriverGoto(buffDriver, budget, count)
    if dataPrint(buffDriver, igxeDriver):
        break
    count += 1
print("=" * 50)
buffDriver.close()
igxeDriver.close()
