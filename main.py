# -*- coding: utf-8 -*-
import sys, os, logging
from collections import OrderedDict
from getopt import getopt
from json5 import loads
from BiliClient import BiliApi
import sendmsg
#from push_message import webhook


main_version = (0, 1, 0)
main_version_str = '.'.join(map(str, main_version))


def init_log(log_file: str, log_console: bool):
    '''初始化日志参数'''
    try:
        logger_raw = logging.getLogger()
        logger_raw.setLevel(logging.INFO)
        formatter_log = logging.Formatter(
            "[%(asctime)s] [%(levelname)s]: %(message)s")
        if log_file:
            file_handler = logging.FileHandler(log_file,
                                               encoding='utf-8')  #输出到日志文件
            file_handler.setFormatter(formatter_log)
            logger_raw.addHandler(file_handler)
        if log_console:
            console_handler = logging.StreamHandler(stream=sys.stdout)  #输出到控制台
            console_handler.setFormatter(formatter_log)
            logger_raw.addHandler(console_handler)
        return None
    except Exception as e:
        print(f'初始化日志参数异常，原因为{str(e)}，退出程序')
        sys.exit(1)


def init_message(configData: dict):
    '''初始化消息推送'''
    try:
        init_log(configData["log_file"], configData["log_console"])
        #if configData["webhook"]["enable"]:
            #webhook.set(configData["webhook"])
    except Exception as e:
        print(f'初始化消息推送异常，原因为{str(e)}，退出程序')
        sys.exit(1)


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
        logging.info(f'当前程序版本为v{main_version_str},配置文件版本为v{config_version}')
    else:
        logging.warning(
            f'当前程序版本为v{main_version_str},配置文件版本为v{config_version},版本不匹配可能带来运行问题'
        )
        #webhook.addMsg(f'当前配置版本不匹配，请尽快更新\n\n')
    run_user_tasks(configData["users"], configData["default"],
                   configData.get("http_header", None))
    #webhook.send()


def run_user_tasks(
        user: dict,  #用户配置
        default: dict,  #默认配置
        header: dict = None) -> None:
    with BiliApi(header) as biliapi:
        try:
            if not user["cookieDatas"]["SESSDATA"] or not user["cookieDatas"][
                    "bili_jct"] or not user["cookieDatas"]["DedeUserID"]:
                logging.warning(f'账户参数未正确配置,请检查配置文件')
                return
            if not biliapi.login_by_cookie(user["cookieDatas"]):
                logging.warning(
                    f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效，跳过此账户后续操作'
                )
                return
        except Exception as e:
            logging.warning(
                f'登录验证id为{user["cookieDatas"]["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续操作'
            )
            return

        show_name = user.get("show_name", "")
        if show_name:
            biliapi.name = show_name

        logging.info(
            f'{biliapi.name}: 等级{biliapi.level},经验{biliapi.myexp},剩余硬币{biliapi.mycoin}'
        )

        sendmsg.send_msg_task(biliapi, default['send_msg'], 1479861)


def main(**kwargs):
    try:
        configData = load_config(kwargs.get("config", None))
    except Exception as e:
        print(f'配置加载异常，原因为{str(e)}，退出程序')
        sys.exit(1)

    if 'log' in kwargs:
        configData["log_file"] = kwargs["log"]

    init_message(configData)  #初始化消息推送
    start(configData)  #启动任务


if __name__ == "__main__":
    kwargs = {}
    opts, args = getopt(sys.argv[1:], "hvc:l:", ["configfile=", "logfile="])
    for opt, arg in opts:
        if opt in ('-c', '--configfile'):
            kwargs["config"] = arg
        elif opt in ('-l', '--logfile'):
            kwargs["log"] = arg
    main(**kwargs)