# anime1.me_Subscription_Manager

这个Python脚本允许您轻松管理您的动漫订阅。它使用一个JSON文件来存储您正在关注的动漫信息，并提供添加、修改、删除订阅以及使用Aria2 JSON-RPC服务器更新动漫剧集的选项。

## 先决条件

确保已安装以下依赖项：

* Python 3.x
* pip install `seleniumwire`
* pip install `selenium`
* Chrome浏览器
* [[ChromeDriver](https://chromedriver.chromium.org/downloads)]（请将ChromeDriver路径正确配置在脚本中）
* Aria2 并启用了JSON-RPC

## 配置

1. 打开脚本文件（`main.py`），在文件开头设置以下变量：

```
# Aria2 JSON-RPC服务器地址和密钥
aria2_jsonrpc_url = "http://xxx:6800/jsonrpc"
secret_token = "xxx"
```

2. 打开脚本文件（`download.py`），设置以下变量：

```
service = Service("C:\\app\\chromedriver.exe")`#ChromeDriver改为你的路径
dir = f"/xxx/动漫/{name}/S0{season}"#aria2下载路径
```

## 使用方法

运行脚本并按照屏幕上的提示进行操作：

* **1.关注新动漫**
  * 输入动漫链接、名称和季数以进行关注。脚本将自动分配一个ID。
  * 订阅信息保存到`anime_subscribe.json`文件中。
  * 同时触发新关注动漫的相应更新。
* **2.修改现有订阅**
  * 输入要管理的动漫ID，查看和删除现有订阅。
  * 删除订阅将同时删除相应的剧集信息文件。
* **3.更新动漫剧集**
  * 查看所有已订阅动漫的列表，选择更新全部或指定动漫，输入其ID。
  * 可选择指定要下载的剧集，或让脚本自动确定。
* **q: 退出程序**

## 注意

* 脚本使用Aria2下载剧集，请确保Aria2正在运行且JSON-RPC服务器可访问。
* 剧集信息存储在`ep`目录中，文件以`id.anime_name.json`格式命名。
* 脚本将持续运行，直到选择退出（选项 'q'）。
