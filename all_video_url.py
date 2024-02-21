from selenium import webdriver

import re
import json
import os
import download

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')

def update(id,name,season,url,aria2_jsonrpc_url,secret_token,sta,epp):

    # 创建存储JSON文件的目录路径
    folder_path = os.path.join(os.path.dirname(__file__), 'ep')
    os.makedirs(folder_path, exist_ok=True)
    json_file_name = f"{id}.{name}.json"
    json_file_path = os.path.join(folder_path, json_file_name)

    # 如果JSON文件已存在，尝试加载现有数据，如果不存在则创建一个空列表
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as existing_file:
            update_anime_ep_info = json.load(existing_file)
    else:
        update_anime_ep_info = []

    # 创建一个Chrome浏览器实例（请确保已经安装Chrome浏览器和Chromedriver）
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)  
    all_links = driver.find_elements(by="css selector", value="h2.entry-title a")

    # 遍历所有链接元素并获取其href属性值
    for link in all_links:
        video_url = link.get_attribute("href")
        ep_name = re.sub(r'[^\u4e00-\u9fa5]+', '', link.get_attribute("text"))
        ep = re.search(r'\[(.*?)\]', link.get_attribute("text")).group(1)

        # 检查是否已存在相同的ep
        if not any('ep' in info and info['ep'] == ep for info in update_anime_ep_info):
            new_anime_ep_info = {
                "ep": ep,
                "video_url": video_url,
                "ep_name": ep_name,
                "download": 0, 
            }
            # 更新对应ep的信息
            update_anime_ep_info.append(new_anime_ep_info)

    # 将更新后的信息以JSON格式保存到文件
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(update_anime_ep_info, json_file, ensure_ascii=False, indent=4)
    if sta == 1:
        return 1
    # 检查并输出下载状态
    for ep_info in update_anime_ep_info:

        if ep_info.get('ep') == epp and epp != 0:
            print("开始下载",epp)
            print(f"{ep_info.get('ep_name')} - {ep_info.get('ep')} - {ep_info.get('video_url')} - 下载状态：{ep_info.get('download')}")
            retry = 0
            while retry < 3:
                result = download.dl(name, season, ep_info.get('video_url'), aria2_jsonrpc_url, secret_token)
                if result == 1:
                    # 下载成功，更新下载状态为1
                    ep_info['download'] = 1
                    # 将更新后的信息以JSON格式保存到文件
                    with open(json_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(update_anime_ep_info, json_file, ensure_ascii=False, indent=4)
                    break  # 退出循环
                else:
                    print("下载失败，正在重试...")
                    retry += 1

        download_sta = "No" if 'download' in ep_info and ep_info.get("download", 0) == 0 else "Yes"
        #if download_sta == "Yes":
            #print(f"{ep_info.get('ep_name')} - {ep_info.get('video_url')} - 下载状态： {download_sta}")
        if download_sta == "No":
            print("开始下载还未下载的视频")
            print(f"{ep_info.get('ep_name')} - {ep_info.get('ep')} - {ep_info.get('video_url')} - 下载状态： {download_sta}")
            retry = 0
            while retry < 3:
                result = download.dl(name, season, ep_info.get('video_url'), aria2_jsonrpc_url, secret_token)
                if result == 1:
                    # 下载成功，更新下载状态为1
                    ep_info['download'] = 1
                    # 将更新后的信息以JSON格式保存到文件
                    with open(json_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(update_anime_ep_info, json_file, ensure_ascii=False, indent=4)
                    break  # 退出循环
                else:
                    print("下载失败，正在重试...")
                    retry += 1

    # 关闭浏览器
    #driver.quit()
