from time import sleep
from BiliClient import BiliApi


def send_msg_task(biliapi: BiliApi, msg: str, roomid: int = 1):
    rid = roomid
    retry = 2
    while retry:
        sleep(5)
        try:
            ret = biliapi.xliveRoomInit(roomid)
        except Exception as e:
            print(f'{biliapi.name}:获取房间{rid}的真实id异常，原因为{str(e)}')
        else:
            if ret['code'] == 0:
                rid = ret['data']['room_id']
            else:
                print(f'{biliapi.name}:获取房间{rid}的真实id失败，错误信息为{ret["message"]}')

        try:
            ret = biliapi.xliveMsgSend(rid, msg)
        except Exception as e:
            print(f'{biliapi.name}:在直播房间{rid}发送消息异常，原因是{str(e)}，重试')
            retry -= 1
        else:
            if ret['code'] == 0:
                if ret['message'] == '':
                    print(f'{biliapi.name}:在直播间{rid}发送信息成功')
                    break
                else:
                    print(
                        f'{biliapi.name}:在直播间{rid}发送信息失败，错误信息为{ret["message"]}，重试'
                    )
                    retry -= 1
            else:
                print(
                    f'{biliapi.name}:在直播间{rid}发送信息失败，错误信息为{ret["message"]}，跳过')
                break