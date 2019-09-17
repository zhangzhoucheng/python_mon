
##xpath 效率高，直接定位到某个元素，而soup直接一层层解析，效率慢点，但更灵活

##chromedriver.exe可以配置环境变量，或者py目录下
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from  selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import re
import math

#用xpath做解析，需要引用下列
from lxml import etree

class Login():
    def __init__(self):
        self.driver=webdriver.Chrome('../tool/chromedriver')
        self.driver.get("http://mail.163.com/")
    def login(self,username,pw):
        #element=WebDriverWait(self.driver,30,0.5).until(EC.presence_of_element_located((By.XPATH,"//*[@id='x-URS-iframe']")))
        #element = WebDriverWait(self.driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'x-URS-iframe')]")))
        source_txt=self.driver.page_source
        html=etree.HTML(source_txt.encode())
        frame_name=html.xpath("//iframe[contains(@id,'x-URS-iframe')]/@id")[0]
        self.driver.find_element(By.XPATH,"//*[@id='switchAccountLogin']").click()##需要先点击密码登陆

        self.driver.switch_to.frame(frame_name)#此处用switch to frame，是由于嵌入的元素直接捕捉不到。
        inputText=self.driver.find_element(By.XPATH,"//*[@id='account-box']//div[2]//input")##--).click()点击失败，由于元素在xpath外面
        inputText.send_keys(username)
        password=self.driver.find_element(By.XPATH,"//*[@id='login-form']//div//div[3]//div[2]//input[2]")
        password.send_keys(pw)
        password.send_keys(Keys.ENTER)
        time.sleep(0.5)#延迟移动鼠标，估计该element设置了延迟加载。
        ele_che=self.driver.find_element(By.XPATH, "//*[@class='ScapTcha']")##获取验证码元素
        loca=ele_che.location#位置
        action=ActionChains(self.driver)##获取driver 事件操作。
        action.move_to_element(ele_che).perform()#悬停在验证码触发框上
        time.sleep(0.7)#延迟加载，不然yidun_tips__answer 还没渲染
        ele_chi = self.driver.find_element(By.XPATH, "//*[@class='yidun_tips__answer']")  ##获取汉字
        ele_chi_list=re.split('\s+',ele_chi.text.replace('"',''))
        time.sleep(0.2)#延迟，不然下列点击不生效
        ele_chck_code_img=self.driver.find_element(By.XPATH, "//*[@class='yidun_panel']")#获取验证码图片
        ele_chi_list_kev={}
        i=0
        for it in ele_chi_list:
            ele_chi_list_kev[it]=[80+i*40,40+i*40]
            i+=1
        print(ele_chi_list_kev)
        for it in ele_chi_list:
            print(it)
            action.click(ele_chck_code_img)#<1>第一次点击，定位到该元素。

            action.pause(2)#，链式操作该步骤延时2s

            action.move_to_element_with_offset(ele_chck_code_img,ele_chi_list_kev[it][0],ele_chi_list_kev[it][1])
            #action.move_to_element_with_offset(ele_chck_code_img,80,40)#<2.0>移动元素，基于再次定位到ele_chck_code_img，去相对于其左上角位移80，40。
            #action.move_by_offset(80,40)#<2.1>如果上步骤'<2.0>'换成本步骤'<2.1>'，则是相对于'<1>' ('<1>'默认定位到元素中间）来说，往右下方移动80，40

            action.click()#<3>:此时不能用<1>一样代码去触发点击事件，因为看其源码知道，如果传参数，则会初始化点击中间，不传参数，则点击当前鼠标位置。

        action.perform()##action 是一个链式操作，perform 是统一提交。










    def logout(self):
        self.driver.find_element_by_link_text('退出').click()
        time.sleep(5)

log=Login()
log.login('idiot_jilidan@163.com','15856571830zz')

