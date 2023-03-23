import struct
import serial
import binascii,time
import logging
import crcmod
 
#生成CRC16-MODBUS校验码
def crc16Add(read):  
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "") #消除空格
    readcrcout = hex(crc16(binascii.unhexlify(data))).upper()
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
    crc_data = "".join(str_list) #用""把数组的每一位结合起来  组成新的字符串
    # print(crc_data)
    read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4] #把源代码和crc校验码连接起来
    # print('CRC16校验:', crc_data[4:] + ' ' + crc_data[2:4])
    # print(read)
    return read


# data 数据 num 长度/字节数
def int2byte(data,num):
    return data.to_bytes(num,"big")

def byte2int(data):
    return int.from_bytes(data, byteorder='big')

def float2byte(data):
    return struct.pack('f',data)

def byte2float(data):
    return struct.unpack('f',data)[0]

# address:寄存器起始地址    num:寄存器数量
def newreadframe(add_d,add_r,num):
    frame = add_d+'03'
    # frame = '01 03'
    frame+=add_r
    frame=bytes.fromhex(frame)
    frame+=int2byte(num,2)   
    frame = crc16Add(str(binascii.b2a_hex(frame))[2:-1])
    return bytes.fromhex(frame)

# address:寄存器起始地址    x:设置数值
def newwriteframe(add_d,add_r,x,type):
    frame = add_d+'06'
    # frame = '01 06'
    frame+=add_r
    frame=bytes.fromhex(frame)
    if type == 1:
        frame+=int2byte(x,2) 
    else:
        frame+=float2byte(x) 
    frame = crc16Add(str(binascii.b2a_hex(frame))[2:-1])
    return bytes.fromhex(frame)

def getType(type):
    if type == '整型':
        return 1
    else:
        return 2

def writeint(ser,add_d,add_r,x,type):

    frame = add_d+'06'
    # frame = '01 06'
    frame+=add_r
    frame=bytes.fromhex(frame)
    if type == 1:
        frame+=int2byte(x,2) 
    else:
        frame+=float2byte(x)
    frame = bytes.fromhex(crc16Add(str(binascii.b2a_hex(frame))[2:-1]))
    ser.write(frame)
    # return bytes.fromhex(frame)

def writefloat(ser,add_d,add_r,x):
    # frame = '01 06'
    frame = add_d+'06'
    frame1 = frame+add_r
    frame2 = frame+add_r[:3]+str(int(add_r[3])+1)

    frame1=bytes.fromhex(frame1)
    frame2=bytes.fromhex(frame2)
    
    frame1=frame1+float2byte(x)[0:2]  
    frame1 = bytes.fromhex(crc16Add(str(binascii.b2a_hex(frame1))[2:-1]))
    ser.write(frame1)

    time.sleep(0.5)

    frame2=frame2+float2byte(x)[2:4]  
    frame2 = bytes.fromhex(crc16Add(str(binascii.b2a_hex(frame2))[2:-1]))
    ser.write(frame2)




# # 配置串口基本参数并建立通信
# ser = serial.Serial('COM2', 9600, timeout=0.5)

# # 串口发送数据
# # result=ser.write(newread('1','0000',1.5))
# # result=ser.write(newwriteframe('1','0002',1.5,2))

# # writefloat(ser,"1","0000",0.5)
# writeint(ser,"01","0000",33,1)

# # 停止、等待数据，这一步非常关键。timeout压根没用
# time.sleep(0.5)
# count=ser.inWaiting()

# # 数据的接收
# if count>0:
#     data=ser.read(count)
#     if data!=b'':
#         # 将接受的16进制数据格式如b'h\x12\x90xV5\x12h\x91\n4737E\xc3\xab\x89hE\xe0\x16'
#         #                      转换成b'6812907856351268910a3437333745c3ab896845e016'
#         #                      通过[]去除前后的b'',得到我们真正想要的数据 
#         print("receive",str(data)[2:-1])

#         print(data)
#         print(data[3:-2])
#         print(byte2int(data[3:-2]))

# # 关闭串口
# ser.close()
