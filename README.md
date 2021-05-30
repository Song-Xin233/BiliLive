PS: 尽管这个项目目前所属为SSXX-233，但是大部分（99%）功能为忆佬(GOOD-AN)所实现  
感谢忆佬的帮助和支持！  
~~感谢ssxx每日对忆佬的督促23333~~

## 项目功能
本项目主要为了在UP主幽蓝伊梦的直播间发送消息(作用是点亮粉丝牌和增加亲密度)

## 使用方法

1. 先下载项目到本地计算机
2. 安装 python3.7+，安装方法自行谷歌
3. [requirements.txt](requirements.txt) 是所需第三方模块，执行 `pip install -r requirements.txt` 安装模块
4. [config.json](config.json) 是配置文件，里面有说明
5. Python 和需要模块安装完毕后直接 **cmd** 运行 `python ./main.py`

## cookieDatas获取方法

1. 使用谷歌或者其他类似的浏览器打开并登录bilibili
2. 按F12打开开发者工具
3. 菜单栏选择application
4. 下方弹出的窗口选择Cookies，然后选择任意一项
5. 分别找到 SESSDATA，bili_jct，DedeUserID 填入配置文件对应处
