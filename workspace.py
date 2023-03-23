from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
import threading  # 线程模块
import serial  # 导入串口模块
from control import *

# 配置串口
portx = "COM2"
bps = 9600
# 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
timex = 0.5
ser = serial.Serial(portx, bps, timeout=timex)  # 开启串口通信


class Software:

    def __init__(self):
        # 动态导入ui界面
        self.ui = QUiLoader().load('main.ui')
        self.ui.writeButton.clicked.connect(self.writeVal)
        self.ui.readButton.clicked.connect(self.readVal)

    def writeVal(self):  # 写数据
        val = self.ui.val.text()
        add_d = self.ui.add_D.text()
        add_r = self.ui.add_R.text()
        # print(type(add_r))
        # add_r = '0000'
        datatype=getType(self.ui.buttonGroup.checkedButton().text())#int1，float2
        if val != "":
            if(datatype==1):
                ser.write(newwriteframe(add_d,add_r,int(val),1))
                # print(newwriteframe(add_d,add_r,int(val),1))
            else:
                writefloat(ser,add_d,add_r,float(val))

    def readVal(self):  # 读数据
        val = self.ui.val.text()
        add_d = self.ui.add_D.text()
        add_r = self.ui.add_R.text()

        datatype=getType(self.ui.buttonGroup.checkedButton().text())#int1，float2

        # result=ser.write(newread('1','0000',1)) # int填1，float填2
        ser.write(newreadframe(add_d,add_r,datatype)) # int填1，float填2

        # 停止、等待数据，这一步非常关键。timeout压根没用
        time.sleep(1)
        count=ser.inWaiting()

        # 数据的接收
        if count>0:
            data=ser.read(count)
            if data!=b'':
                if datatype == 1:
                    self.ui.val.setText(str(byte2int(data[3:-2])))
                else:
                    time.sleep(0.5)
                    self.ui.val.setText(str(byte2float(data[3:-2])))

app = QApplication([])
software = Software()
software.ui.show()


app.exec_()
