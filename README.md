# CSGOJewelryDisparity
一个获取中国饰品网饰品差价并且显示的软件

## 介绍
该软件可以从两个CSGO饰品交易平台(buff,igxe)寻找目标饰品。目前支持Microsoft Edge(Chromium)
### 目标
Target Get Num 目标饰品数
Target Disparity 目标差价
Target Stock 目标库存/在售

## 配置cookie
请在config.json内配置相应参数
### 参数
#### executable_path
MicrosoftWebDriver.exe路径。
#### cookies
两个cookie，请打开网络然后登录，找到包含该两个cookie的文件获取cookie。
#### way
获取方式，num为获取一定数量，page为获取一定页数
#### pageNum
当你的way为page时，该数据表示页数
#### jewelryNum
当你的way为num时，该数据表示饰品数量
#### minDisparity
最小差价
#### minStockA
进货方最小库存/在售
#### minStockB
出货方最小库存/在售

## 开始使用
1.首先保证电脑中有抖音哥最爱语言(蟒蛇)，版本尽量为3.x，安装selenium库。

2.运行main.py

3.输入预算

4.等待

## 作者联系方式
QQ:2025677540

Bilibili:宇badboy