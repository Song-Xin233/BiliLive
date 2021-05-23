from typing import Dict, Any, Optional
from requests.sessions import Session
import time
_default_headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    'Connection': 'keep-alive'
}


class BiliApi:
    def __init__(self, headers: Optional[Dict[str, str]]):
        if not headers:
            headers = _default_headers
        self._session = Session()
        self._session.headers.update(headers)
        self._session.trust_env = True
        self._islogin = False
        self._show_name = None

    def login_by_cookie(self,
                        cookieData,
                        checkBanned=True,
                        strict=False) -> bool:
        '''
        登录并获取账户信息
        cookieData dict 账户cookie
        checkBanned bool 检查是否被封禁
        strict bool 是否严格限制cookie在.bilibili.com域名之下
        '''
        if strict:
            from yarl import URL
            self._session.cookies.update(cookieData,
                                         URL('https://.bilibili.com'))
        else:
            self._session.cookies.update(cookieData)

        self.refreshInfo()
        if not self._islogin:
            return False

        if 'bili_jct' in cookieData:
            self._bili_jct = cookieData["bili_jct"]
        else:
            self._bili_jct = ''

        self._isBanned = None
        if checkBanned:
            code = (self.likeCv(10743282))["code"]
            if code != 0 and code != 65006 and code != -404:
                self._isBanned = True
                import warnings
                warnings.warn(f'{self._name}:账号异常，请检查bili_jct参数是否有效或本账号是否被封禁')
            else:
                self._isBanned = False

        return True

    @property
    def banned(self):
        '''是否账号被异常封禁'''
        return self._isBanned

    @property
    def islogin(self):
        '''是否登录'''
        return self._islogin

    @property
    def myexp(self) -> int:
        '''获取登录的账户的经验'''
        return self._exp

    @property
    def mycoin(self) -> int:
        '''获取登录的账户的硬币数量'''
        return self._coin

    @property
    def vipType(self) -> int:
        '''获取登录的账户的vip类型'''
        return self._vip

    @property
    def name(self) -> str:
        '''获取用于显示的用户名'''
        return self._show_name

    @name.setter
    def name(self, name: str) -> None:
        '''设置用于显示的用户名'''
        self._show_name = name

    @property
    def username(self) -> str:
        '''获取登录的账户用户名'''
        return self._name

    @property
    def uid(self) -> int:
        '''获取登录的账户uid'''
        return self._uid

    @property
    def level(self) -> int:
        '''获取登录的账户等级'''
        return self._level

    def refreshInfo(self):
        '''刷新账户信息(需要先登录)'''
        ret = self.getWebNav()
        if ret["code"] != 0:
            self._islogin = False
            return

        self._islogin = True
        self._name = ret["data"]["uname"]
        self._uid = ret["data"]["mid"]
        self._vip = ret["data"]["vipType"]
        self._level = ret["data"]["level_info"]["current_level"]
        self._verified = ret["data"]["mobile_verified"]
        self._coin = ret["data"]["money"]
        self._exp = ret["data"]["level_info"]["current_exp"]
        if not self._show_name:
            self._show_name = self._name

    def xliveRoomInit(self, rid: int = 1):
        '''
        获取房间初始化信息(房间短id转长id)
        id int 直播间id
        '''
        url = f'https://api.live.bilibili.com/room/v1/Room/room_init?id={rid}'
        with self._session.get(url) as r:
            return r.json()

    def xliveMsgSend(
        self,
        roomid: int,
        msg: str,
        color: int = 16777215,
        fontsize: int = 25,
        mode: int = 1,
        bubble: int = 0,
    ):
        '''
        直播间发送消息
        roomid int 直播间id
        msg str 要发送的消息
        color int 字体颜色
        fontsize int 字体大小
        mode int 发送模式，应该是控制滚动，底部这些
        bubble int 未知
        '''
        url = 'https://api.live.bilibili.com/msg/send'
        post_data = {
            "color": color,
            "fontsize": fontsize,
            "mode": mode,
            "msg": msg,
            "rnd": int(time.time()),
            "roomid": roomid,
            "bubble": bubble,
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
        }
        with self._session.post(url, data=post_data) as r:
            return r.json()

    def likeCv(self, cvid: int, type=1) -> Dict:
        '''
        点赞专栏
        cvid int 专栏id
        type int 类型
        '''
        url = 'https://api.bilibili.com/x/article/like'
        post_data = {"id": cvid, "type": type, "csrf": self._bili_jct}
        with self._session.post(url, data=post_data) as r:
            return r.json()

    def getWebNav(self) -> Dict[str, Any]:
        '''取导航信息'''
        url = "https://api.bilibili.com/x/web-interface/nav"
        with self._session.get(url) as r:
            ret = r.json()
        return ret

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()