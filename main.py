# -*- coding: utf-8 -*-
import sys, os
from collections import OrderedDict
from getopt import getopt
from BiliClient import BiliApi
import sendmsg
from json5 import loads

main_version = (0, 0, 1)
main_version_str = '.'.join(map(str, main_version))


def load_config(path: str) -> OrderedDict:
    '''加载配置文件'''
    if path:
        with open(path, 'r', encoding='utf-8') as fp:
            return loads(fp.read(), object_pairs_hook=OrderedDict)
    else:
        for path in ('./config/config.json', './config.json',
                     '/etc/BiliExp/config.json', 'config.json'):
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as fp:
                    return loads(fp.read(), object_pairs_hook=OrderedDict)
        raise RuntimeError('未找到配置文件')


def start(configData: dict):
    '''开始任务'''
    config_version = configData.get('version', '0.0.0')
    if tuple(map(int, config_version.strip().split('.'))) == main_version:
        print(f'当前程序版本为v{main_version_str},配置文件版本为v{config_version}')
    else:
        print(
            f'当前程序版本为v{main_version_str},配置文件版本为v{config_version},版本不匹配可能带来额外问题'
        )
    run_user_tasks(configData["users"], configData["default"],
                   configData.get("http_header", None))


def run_user_tasks(
        user: dict,  #用户配置
        default: dict,  #默认配置
        header: dict = None) -> None:
    with BiliApi(header) as biliapi:
        try:
            if not biliapi.login_by_cookie(user["cookieDatas"]):
                print(
                    f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效，跳过此账户后续操作'
                )
                return
        except Exception as e:
            print(
                f'登录验证id为{user["cookieDatas"]["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续操作'
            )
            return

        show_name = user.get("show_name", "")
        if show_name:
            biliapi.name = show_name

        print(
            f'{biliapi.name}: 等级{biliapi.level},经验{biliapi.myexp},剩余硬币{biliapi.mycoin}'
        )

        sendmsg.send_msg_task(biliapi, default['send_msg'], 1479861)


def main(*args, **kwargs):
    try:
        configData = load_config(kwargs.get("config", None))
    except Exception as e:
        print(f'配置加载异常，原因为{str(e)}，退出程序')
        sys.exit(6)

    if 'log' in kwargs:
        configData["log_file"] = kwargs["log"]

    #启动任务
    start(configData)


if __name__ == "__main__":
    kwargs = {}
    opts, args = getopt(sys.argv[1:], "hvc:l:", ["configfile=", "logfile="])
    for opt, arg in opts:
        if opt in ('-c', '--configfile'):
            kwargs["config"] = arg
        elif opt in ('-l', '--logfile'):
            kwargs["log"] = arg
    main(**kwargs)