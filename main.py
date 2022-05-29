# oding = utf-8
# -*- coding:utf-8 -*-

#由YBB(Yubadboy)编写，其所有权归属Yubadboy，Yubadboy有权对代码做修改

import selenium.common.exceptions
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from decimal import Decimal

#获取预算和开始网站
budget=float(input("Budget:"))

buffGetUrl="https://buff.163.com/market/csgo#tab=selling&max_price={}&page_num={}"
igxwSearchUrl="https://www.igxe.cn/market/csgo?keyword={}"
executable_path=r"E:\desktop\getstudio\meonly\CSGOJewelryDisparity\MicrosoftWebDriver.exe"
buffCookie1 = {"name": "session", "value": "1-CHPxUMorO2JbdtLvibfRwk_Zpf283zSVegR0R6KyhWgG2037919380"}
buffCookie2 = {"name": "csrf_token",
               "value": "IjhlZjhlMDgzY2M0MGMyZDExNTQ5ZGM2MTcwYTBhNDhkMGU4MDY1ZWUi.FXOVaA.IkH1nNGZZH6k6XuM5GQIofwcbf4"}

count=1

def getBuffDriver():
    driver=webdriver.Edge(executable_path=executable_path)
    driver.get(buffGetUrl.format(budget,count))
    driver.add_cookie(buffCookie1)
    driver.add_cookie(buffCookie2)
    driver.get(buffGetUrl.format(budget,count))
    driver.refresh()
    return driver

def getIgxeDriver():
    driver=webdriver.Edge(executable_path=executable_path)
    return driver

def setIgxeDriverGoto(driver,name):
    driver.get(igxwSearchUrl+name)
    driver.refresh()

#获取物品链接
buffDriver=getBuffDriver()
buffWait=ui.WebDriverWait(buffDriver,10)
buffWait.until(lambda WaitDriver:buffDriver.find_element_by_class_name("card_csgo").find_elements_by_tag_name("li"))
eleList = buffDriver.find_element_by_class_name("card_csgo").find_elements_by_tag_name("li")

igxeDriver=getIgxeDriver()

for eleGoods in eleList:
    href=eleGoods.find_element_by_tag_name("a").get_attribute("href")
    title=eleGoods.find_element_by_tag_name("a").get_attribute("title")
    stock=eleGoods.find_element_by_tag_name("p").find_element_by_tag_name("span").text.strip()
    price=eleGoods.find_element_by_tag_name("p").find_element_by_tag_name("strong").text.strip()[2:]
    try:
        abrase=eleGoods.find_element_by_css_selector(".tag").text.strip()
    except selenium.common.exceptions.NoSuchElementException:
        abrase="该物品无磨损信息"
    buffResult=[href,title,stock,price,abrase]

    setIgxeDriverGoto(igxeDriver,buffResult[1])
    igxeWait = ui.WebDriverWait(igxeDriver, 10)
    igxeWait.until(lambda WaitDriver: igxeDriver.find_element_by_class_name("market").find_element_by_class_name("container").find_element_by_class_name("list").find_element_by_tag_name("a"))
    secondGoods=igxeDriver.find_element_by_class_name("market").find_element_by_class_name("container").find_element_by_class_name(
        "list").find_elements_by_tag_name("a")
    SecondGoods=None
    for goods in secondGoods:
        if goods.find_element_by_class_name("name").text==buffResult[1]:
            SecondGoods=goods
    if SecondGoods is None:
        continue
    href=SecondGoods.get_attribute("href")
    title=buffResult[1]
    stock=SecondGoods.find_element_by_class_name("info").find_element_by_class_name("stock").text.strip()[3:]+"件在售"
    price=SecondGoods.find_element_by_class_name("info").find_element_by_class_name("price").text.replace("\n","").strip()[1:5]
    abrase=buffResult[4]
    igxeResult = [href, title, stock, price, abrase]

    buffPrice=float(buffResult[3])
    igxePrice=float(igxeResult[3])

    if buffPrice==igxePrice:
        continue
    elif buffPrice>igxePrice:
        fromResult=igxeResult
        toResult=buffResult
    else:
        fromResult = buffResult
        toResult = igxeResult
    print("="*50)
    print("第一平台数据（进货方）")
    print("物品名称：",fromResult[1])
    print("物品价格：",fromResult[3])
    print("物品磨损：",fromResult[4])
    print("物品在售数量：",fromResult[2])
    print("物品链接：",fromResult[0])
    print("-" * 40)
    print("第二平台数据（出货方）")
    print("物品名称：",toResult[1])
    print("物品价格：",toResult[3])
    print("物品磨损：",toResult[4])
    print("物品在售数量：",toResult[2])
    print("物品链接：",toResult[0])
    print("-" * 40)
    print("可赚差价（未含税）：",float(Decimal(str(max(buffPrice,igxePrice)))-Decimal(str(min(buffPrice,igxePrice)))))
print("="*50)
buffDriver.close()
igxeDriver.close()