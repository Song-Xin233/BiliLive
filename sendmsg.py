import logging
from time import sleep
from BiliClient import BiliApi
#from push_message import webhook

def send_msg_task(biliapi: BiliApi, msg: str, roomid: int = 1):
    rid = roomid
    retry = 2
    while retry:
        sleep(5)
        try:
            ret = biliapi.xliveRoomInit(roomid)
        except Exception as e:
            logging.warning(f'{biliapi.name}:获取房间{rid}的真实id异常，原因为{str(e)}')
        else:
            if ret['code'] == 0:
                rid = ret['data']['room_id']
            else:
                logging.warning(f'{biliapi.name}:获取房间{rid}的真实id失败，错误信息为{ret["message"]}')

        try:
            ret = biliapi.xliveMsgSend(rid, msg)
        except Exception as e:
            logging.warning(f'{biliapi.name}:在直播房间{rid}发送消息异常，原因是{str(e)}，重试')
            retry -= 1
        else:
            if ret['code'] == 0:
                if ret['message'] == '':
                    logging.info(f'{biliapi.name}:在直播间{rid}发送信息成功')
                    #webhook.addTitle('Love lulu success')
                    #webhook.addMsg(f'{biliapi.name}:在直播间{rid}发送信息成功\n\n')
                    break
                else:
                    logging.warning(f'{biliapi.name}:在直播间{rid}发送信息失败，错误信息为{ret["message"]}，重试')
                    retry -= 1
            else:
                logging.warning(f'{biliapi.name}:在直播间{rid}发送信息失败，错误信息为{ret["message"]}，跳过')
                #webhook.addTitle('Love lulu failure')
                #webhook.addMsg(f'{biliapi.name}:在直播间{rid}发送信息失败，错误信息为{ret["message"]}，跳过\n\n')
                break