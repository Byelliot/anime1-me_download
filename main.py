import json
import os
import all_video_url

# aria2 JSON-RPC 服务器地址和密钥
aria2_jsonrpc_url = "http://xxx:6800/jsonrpc"
secret_token = "xxx"

# 获取脚本文件的目录
script_directory = os.path.dirname(os.path.abspath(__file__))

# 构建JSON文件的完整路径
json_file_path = os.path.join(script_directory, "anime_subscribe.json")

# 如果JSON文件已存在，尝试加载现有数据，如果不存在则创建一个空列表
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as existing_file:
        anime_subscribe = json.load(existing_file)
else:
    anime_subscribe = []


while True:
    choice = input("请选择（1: 关注动漫 2: 关注修改 3: 更新动漫  q: 退出）：")

    if choice == '1':
        anime_link = input("请输入需要关注的动漫链接：")
        anime_name = input("请输入动漫名称：")
        season = input("请输入第几季：")
        # 找到最小可用数字
        id = 0
        anime_ids = [anime_info["id"] for anime_info in anime_subscribe]

        while True:
            id += 1
            if id not in anime_ids:
                break
        new_anime_info = {
            "id": id,
            "anime_link": anime_link,
            "anime_name": anime_name,
            "season": season
        }
        # 将新的动漫信息添加到现有列表
        anime_subscribe.append(new_anime_info)
        # 将更新后的信息以JSON格式保存到文件
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(anime_subscribe, json_file, ensure_ascii=False, indent=4)
            print(f"文件已保存到：{json_file_path}")
            all_video_url.update(id,anime_name,'season',anime_link,aria2_jsonrpc_url,secret_token,1,0)
            print(f"关注动漫：ID：{id}，{anime_name}，第{season}季,链接：{anime_link}")

    elif choice == '2':
        while True:
            # 读取anime_subscribe.json中所有关注的动漫信息
            if len(anime_subscribe) == 0:
                print("你还没有关注任何动漫。")
                break  # 如果没有关注的动漫，直接退出循环返回上一级菜单
            else:
                print("已关注的动漫列表：")
                for anime_info in anime_subscribe:
                    print(f"ID: {anime_info['id']}, 动漫名称: {anime_info['anime_name']}, 第{anime_info['season']}季, 链接: {anime_info['anime_link']}")

            delete_choice = input("是否需要删除关注的动漫？(y/n): ")
            if delete_choice.lower() == 'y':
                id_to_delete = input("请输入要删除的动漫的ID: ")
                id_to_delete = int(id_to_delete)  # 将输入的ID转换为整数
                # 查找要删除的动漫信息并删除
                updated_anime_subscribe = [anime_info for anime_info in anime_subscribe if anime_info['id'] != id_to_delete]

                # 如果没有找到匹配的ID，提示用户
                if len(updated_anime_subscribe) == len(anime_subscribe):
                    print(f"找不到ID为{id_to_delete}的关注动漫。")
                else:
                    anime_subscribe = updated_anime_subscribe
                    with open(json_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(anime_subscribe, json_file, ensure_ascii=False, indent=4)
                    # 获取ep目录的路径
                    ep_directory = os.path.join(os.path.dirname(__file__), 'ep')
                    files_in_ep = os.listdir(ep_directory)
                    for file_name in files_in_ep:
                        if file_name.endswith('.json'):
                            # 提取文件名中的ID部分，假设文件名格式为：id.anime_name.json
                            file_id = int(file_name.split('.')[0])
                            if file_id == id_to_delete:
                                # 找到匹配的JSON文件，删除它
                                file_path = os.path.join(ep_directory, file_name)
                                os.remove(file_path)
    
                    print(f"ID为{id_to_delete}的动漫已成功删除。")
            else:
                break  # 如果用户不再想删除，退出循环返回上一级菜单

    elif choice == '3':
        for anime_info in anime_subscribe:
                print(f"ID: {anime_info['id']}, 动漫名称: {anime_info['anime_name']}, 链接: {anime_info['anime_link']}, 第{anime_info['season']}季")
        update_choice = input("请选择需要更新的动画（输入ID）或输入 'a' 全部更新： ")
        if update_choice.lower() == 'a':
            # 全部更新动漫
            for anime_info in anime_subscribe:
                print(f"正在更新动漫 ID: {anime_info['id']} - {anime_info['anime_name']}")
                all_video_url.update(anime_info['id'],anime_info['anime_name'],anime_info['season'],anime_info['anime_link'],aria2_jsonrpc_url,secret_token,0,0)
                print(f"动漫 ID: {anime_info['id']} - {anime_info['anime_name']} 更新完成")
        else:
            # 更新指定动漫
            update_choice = int(update_choice)
            for anime_info in anime_subscribe:
                if anime_info['id'] == update_choice:
                    ep = input("输入要下载的集数 或 输入 a 自动判断")
                    
                    if ep.lower() == 'a':
                        print(f"正在更新动漫 ID: {anime_info['id']} - {anime_info['anime_name']}")
                        all_video_url.update(anime_info['id'],anime_info['anime_name'],anime_info['season'],anime_info['anime_link'],aria2_jsonrpc_url,secret_token,0,0)
                        print(f"动漫 ID: {anime_info['id']} - {anime_info['anime_name']} 更新完成")
                        break
                    else:
                        #print(ep)
                        print(f"正在更新动漫 ID: {anime_info['id']} - {anime_info['anime_name']}")
                        all_video_url.update(anime_info['id'],anime_info['anime_name'],anime_info['season'],anime_info['anime_link'],aria2_jsonrpc_url,secret_token,0,ep)
                        print(f"动漫 ID: {anime_info['id']} - {anime_info['anime_name']} 更新完成")
                        break
            else:
                print(f"找不到ID为 {update_choice} 的动漫。")

    elif choice.lower() == 'q':
        print("结束程序")
        break  # 退出程序