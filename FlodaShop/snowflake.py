# @Time: 2021-5-12  15:22
# @Author: chalmer
# @File: snowflake.py
# @software: PyCharm
import time


class SnowFlake(object):
    """雪花算法"""

    def __init__(self, init_time='2020-01-01 0:0:0', roomID=None, serverID=None):
        """
        :param init_time: 默认以2020年1月1日为起始时间，进行保存的时间戳为当前时间与起始时间的差值
        :param roomID:  机房ID，默认为1，最大值为2^5=32(不含32）
        :param serverID: 服务器ID,默认为1，最大值为2^5=32(不含32）
        """
        print(time.mktime(time.strptime(init_time, "%Y-%m-%d %H:%M:%S")))
        self.init_time = str(time.mktime(time.strptime(init_time, "%Y-%m-%d %H:%M:%S"))).split('.')[0]

        self.roomID = roomID if roomID else 1
        self.serverID = serverID if serverID else 1
        self.now_time = str(time.time()).split('.')[0]  # 当前时间的时间戳（精确到秒）
        self.count = 0  # 每秒范围内的时间序列计数器

    # 根据当前时间及预设的机房ID,服务器ID生成雪花ID
    def CreateSnowID(self):
        now_time = str(time.time()).split('.')[0]  # 当前时间的时间戳

        # 时间戳部分
        # 计算当前时间与起始时间的差值，精确到秒。切割掉小数点后的部分,然后转换为二进制数，再填充0至41位
        differenct_time = int(self.now_time) - int(self.init_time)  # 时间差值
        timestamp = bin(differenct_time)[2:].zfill(41)
        # print('differenct_time:', differenct_time)
        # print('timestamp:', timestamp)

        # 机器ID部分
        roomID = bin(self.roomID)[2:].zfill(5)  # 机房ID
        serverID = bin(self.serverID)[2:].zfill(5)  # 服务器ID

        # 序列号部分
        if self.count <= 4090:
            if now_time != self.now_time:
                self.now_time = now_time
            self.count += 1
        else:
            self.count = 1
            time.sleep(1)
        # print(self.count)
        serial_number = bin(self.count)[2:].zfill(12)
        # print('serial_number:', serial_number)

        # 合成雪花ID
        print(('0' + str(timestamp) + str(roomID) + str(serverID) + str(serial_number)))
        snowID = int(('0' + str(timestamp) + str(roomID) + str(serverID) + str(serial_number)), 2)
        return snowID

    # 根据雪花ID解析出创建时间等信息
    def AnalysisSnowID(self, snowID):
        binID = bin(snowID)[2:].zfill(64)  # 转为二进制后再填充0至64位
        timestamp = int(binID[1:42], 2)
        roomID = int(binID[42:47], 2)  # 机房ID
        serverID = int(binID[47:52], 2)  # 服务器ID
        serial_number = int(binID[52:], 2)  # 秒级时间序列号

        ID_time = time.localtime(int(self.init_time) + timestamp)
        print(ID_time)
        ID_time = time.strftime("%Y-%m-%d %H:%M:%S", ID_time)
        data = {
            'create_time': ID_time,
            '机房ID': roomID,
            '服务器ID': serverID,
            '时间序列号': serial_number
        }
        return data


maker_one = SnowFlake(roomID=1, serverID=1)
print(maker_one.CreateSnowID())