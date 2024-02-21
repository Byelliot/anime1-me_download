#from selenium import webdriver
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from time import sleep

import urllib.request
import json
import re

# 创建 Chrome 选项
chrome_options = webdriver.ChromeOptions()

# 添加你需要的 Chrome 选项，例如禁用 GPU 加速
chrome_options.add_argument('--disable-gpu')

# 创建 SeleniumWire 选项
seleniumwire_options = {
    'addr': '127.0.0.1',  # 这是一个示例，你可能需要根据需要调整
}

#读取视频保存路径

def dl(name,season,url,aria2_jsonrpc_url,secret_token):
    # 设置 Selenium Wire 的 WebDriver
    options = {
        'disable_encoding': True  # 禁用请求编码
    }

    # 初始化 WebDriver
    service = Service("C:\\app\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, seleniumwire_options=seleniumwire_options, options=chrome_options)
    
    dir = f"/动漫/{name}/S0{season}"

    #下载部分
    driver.get(url)
    print("U:", url)
    # 模拟点击播放按钮
    play_button_selector = '.vjs-big-play-button'
    play_button = driver.find_element(By.CSS_SELECTOR, play_button_selector)
    play_button.click()

    # 尝试获取视频 URL
    sleep(5)
    try:
        # 这里假设视频是通过 <video> 标签嵌入的
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_url = video_element.get_attribute('src')
    except Exception as e:
        print("获取视频 URL 失败:", e)
        video_url = None
        return 0

    if video_url:
        print("找到的视频 URL:", video_url)
        target_url = video_url
    else:
        print("未能找到视频 URL")
        return 0

    try:
        # 尝试打开视频URL
        driver.set_page_load_timeout(1)
        driver.get(video_url)
        cookie_v = ""
        for request in driver.requests:
            if request.url == target_url:  # 检查请求的URL是否是我们要找的那个
                cookie_v = request.headers.get('Cookie')  # 保存cookie值
                #print(cookie_v)
                print("cookie成功获取",cookie_v)
                break  # 找到后退出循环
    except TimeoutException:
        print("切断连接以获取cookie")
        cookie_v = ""
        for request in driver.requests:
            if request.url == target_url:  # 检查请求的URL是否是我们要找的那个
                cookie_v = request.headers.get('Cookie')  # 保存cookie值
                #print(cookie_v)
                print("cookie成功获取",cookie_v)
                break  # 找到后退出循环
        

    #使用aria2下载视频
    #视频 URL 和下载文件名
    def remove_a_b_from_filename(url):
        # Extracting the filename from the URL
        filename = url.split('/')[-1]
        # Removing 'a' and 'b' from the filename
        cleaned_filename = re.sub('[ab]', '', filename)
        return cleaned_filename   
      
    file_name = remove_a_b_from_filename(video_url)
    download_file_name = file_name  # 这里设置你想要的文件名

    # 构造 JSON-RPC 请求
    header = f"Cookie: {cookie_v}"
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer','method': 'aria2.addUri','params': [f"token:{secret_token}", [video_url], {'out': download_file_name,'dir': dir,'header': header}]})

    # 发送请求
    req = urllib.request.Request(url=aria2_jsonrpc_url,data=jsonreq.encode('utf-8'),headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(req) as c:
        response = c.read().decode('utf-8')

    #print(response)
    print("成功推送到Aria2下载")
    return 1
    # 关闭浏览器
    #driver.quit()
