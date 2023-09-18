import sys
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer , QCoreApplication
from PyQt5.QtWidgets import QMessageBox ,QApplication ,QMainWindow ,QGraphicsDropShadowEffect
import cv2 
import requests
from rubik_solver import utils
import numpy as np
import subprocess

#############################################################################################################
blue = green = red = orange = white = yellow = 0
hsvColors = {'Blue': [blue, [0, 100, 100], [30, 255, 255]],
             'Green': [green, [30, 100, 100], [75, 255, 255]],
             'Red': [red, [118, 120, 120], [140, 255, 255]],
             'Orange': [orange, [100, 130, 130], [130, 255, 255]],
             'White': [white, [0, 0, 75], [180, 45, 255]],
             'Yellow': [yellow, [75, 100, 100], [100, 255, 255]]}

rgbColors = {'Blue': (255, 0, 0),
             'Green': (0, 255, 0),
             'Red': (0, 0, 255),
             'Orange': (0, 125, 255),
             'White': (255, 255, 255),
             'Yellow': (0, 255, 255)}
faces = {'Blue': 'b',
         'Green': 'g',
         'Red': 'r',
         'Orange': 'o',
         'White': 'w',
         'Yellow': 'y'}
#############################################################################################################

method = {
    '1' : ['สเเกนด้านสีเหลือง โดยด้านบนจะต้องเป็นด้านสีส้ม','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '2' : ['สเเกนด้านสีน้ำเงิน เเละด้านบนจะต้องเป็นด้านสีเหลือง','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '3' : ['สเเกนด้านสีแดง เเละด้านบนจะต้องเป็นด้านสีเหลือง','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '4' : ['สเเกนด้านสีเขียว เเละด้านบนจะต้องเป็นด้านสีเหลือง','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '5' : ['สเเกนด้านสีส้ม เเละด้านบนจะต้องเป็นด้านสีเหลือง','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '6' : ['สเเกนด้านสีขาว เเละด้านบนจะต้องเป็นด้านสีเเดง','จัดวางตำเเหน่งจากนั้นกดสเเกน'],
    '7' : ['ตรวจสอบสีเเต่ละด้านที่สเเกน','จากนั้นกดประมวลผล']
}

#############################################################################################################
def get_connected_ssid():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        lines = result.split('\n')
        for line in lines:
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                return ssid
    except subprocess.CalledProcessError:
        pass
    return "ไม่พบการเชื่อมต่อไร้สาย"

def list_available_cameras():
    camera_list = []
    for i in range(5): 
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) 
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                camera_list.append(f"Camera {i}")
            cap.release()
    return camera_list

class MainWindow(QMainWindow):
    def __init__(self):
        print("OpenCV version:", cv2.__version__)
        super(MainWindow,self).__init__()
        self.ui = loadUi("./ui/gui.ui",self)
        self.ui.setWindowTitle('โปรเเกรมหุ่นยนต์เเก้ไขรูบิค')
        self.ui.setWindowIcon(QIcon('./image/logo.png'))
        
        self.cam = cv2.VideoCapture(0)
        
        self.ui.btNext.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.ui.btExit.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.ui.video.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))        
        self.ui.btReset.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.ui.label_2.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.ui.result.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.ui.btRobot.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        
        self.available_cameras = list_available_cameras()
        if self.available_cameras:
            for camera in self.available_cameras:
                self.ui.comboBox.addItem(str(camera))
        
        else:
            print("ไม่พบกล้องที่ใช้งานได้")
            self.ui.comboBox.addItem("ไม่พบกล้องที่ใช้งานได้")
            
        self.dataColorRubik = [['' for i in range(9)] for j in range(6)]
        self.editColors_Colors = "default"
        self.ui.btExit.clicked.connect(self.Qmessage_appExit)
        self.ui.btNext.clicked.connect(self.nextCount)
        self.ui.btRobot.clicked.connect(self.Robot)
        self.ui.btReset.clicked.connect(self.Qmessage_reset)
        self.ui.btR.clicked.connect(self.on_btR_click)
        self.ui.btB.clicked.connect(self.on_btB_click)
        self.ui.btG.clicked.connect(self.on_btG_click)
        self.ui.btY.clicked.connect(self.on_btY_click)
        self.ui.btO.clicked.connect(self.on_btO_click)
        self.ui.btW.clicked.connect(self.on_btW_click)
        
        self.ui.y1.clicked.connect(self.y1_click)
        self.ui.y2.clicked.connect(self.y2_click)
        self.ui.y3.clicked.connect(self.y3_click)
        self.ui.y4.clicked.connect(self.y4_click)
        self.ui.y5.clicked.connect(self.y5_click)
        self.ui.y6.clicked.connect(self.y6_click)
        self.ui.y7.clicked.connect(self.y7_click)
        self.ui.y8.clicked.connect(self.y8_click)
        self.ui.y9.clicked.connect(self.y9_click)
        
        self.ui.b1.clicked.connect(self.b1_click)
        self.ui.b2.clicked.connect(self.b2_click)
        self.ui.b3.clicked.connect(self.b3_click)
        self.ui.b4.clicked.connect(self.b4_click)
        self.ui.b5.clicked.connect(self.b5_click)
        self.ui.b6.clicked.connect(self.b6_click)
        self.ui.b7.clicked.connect(self.b7_click)
        self.ui.b8.clicked.connect(self.b8_click)
        self.ui.b9.clicked.connect(self.b9_click)
        
        self.ui.r1.clicked.connect(self.r1_click)
        self.ui.r2.clicked.connect(self.r2_click)
        self.ui.r3.clicked.connect(self.r3_click)
        self.ui.r4.clicked.connect(self.r4_click)
        self.ui.r5.clicked.connect(self.r5_click)
        self.ui.r6.clicked.connect(self.r6_click)
        self.ui.r7.clicked.connect(self.r7_click)
        self.ui.r8.clicked.connect(self.r8_click)
        self.ui.r9.clicked.connect(self.r9_click)
        
        self.ui.g1.clicked.connect(self.g1_click)
        self.ui.g2.clicked.connect(self.g2_click)
        self.ui.g3.clicked.connect(self.g3_click)
        self.ui.g4.clicked.connect(self.g4_click)
        self.ui.g5.clicked.connect(self.g5_click)
        self.ui.g6.clicked.connect(self.g6_click)
        self.ui.g7.clicked.connect(self.g7_click)
        self.ui.g8.clicked.connect(self.g8_click)
        self.ui.g9.clicked.connect(self.g9_click)

        self.ui.o1.clicked.connect(self.o1_click)
        self.ui.o2.clicked.connect(self.o2_click)
        self.ui.o3.clicked.connect(self.o3_click)
        self.ui.o4.clicked.connect(self.o4_click)
        self.ui.o5.clicked.connect(self.o5_click)
        self.ui.o6.clicked.connect(self.o6_click)
        self.ui.o7.clicked.connect(self.o7_click)
        self.ui.o8.clicked.connect(self.o8_click)
        self.ui.o9.clicked.connect(self.o9_click)
        
        self.ui.w1.clicked.connect(self.w1_click)
        self.ui.w2.clicked.connect(self.w2_click)
        self.ui.w3.clicked.connect(self.w3_click)
        self.ui.w4.clicked.connect(self.w4_click)
        self.ui.w5.clicked.connect(self.w5_click)
        self.ui.w6.clicked.connect(self.w6_click)
        self.ui.w7.clicked.connect(self.w7_click)
        self.ui.w8.clicked.connect(self.w8_click)
        self.ui.w9.clicked.connect(self.w9_click)
        
        self.ui.comboBox.currentTextChanged.connect(self.changedCam)
        
        self.count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)
        self.ColorsRubik = {'b': 'background-color: rgb(0, 0, 167);border-radius:1px;',
                            'g': 'background-color: rgb(0, 160, 0);border-radius:1px;',
                            'r': 'background-color: rgb(208, 0, 0);border-radius:1px;',
                            'o': 'background-color: rgb(243, 162, 0);border-radius:1px;',
                            'w': 'background-color: rgb(255, 255, 255);border-radius:1px;',
                            'y': 'background-color: rgb(252, 252, 0);border-radius:1px;',
                            'default': 'background-color: rgb(230, 230, 230);border-radius:1px;'}
    # def changedCam(self):
    #     self.cam.release()
    #     camValue = self.spinBox.value()
    #     self.cam = cv2.cv2.VideoCapture(camValue)
    #     if self.cam.isOpened():
    #         print(f"สามารถเปิดกล้อง {camValue} ได้")
    #     else:
    #         self.cam = cv2.cv2.VideoCapture(0)
    #         print(f"ไม่สามารถเปิดกล้อง {camValue} ได้")
    #         QMessageBox.warning(self, "ไม่สำเร็จ",f"ไม่สามารถเปิดกล้อง {camValue} ได้!!\t")
  
    def changedCam(self):
        x = self.ui.comboBox.currentText()
        self.cam.release()
        self.cam = cv2.cv2.VideoCapture(int(x[-1]))
        if self.cam.isOpened():
            print(f"สามารถเปิดกล้อง {x[-1]} ได้")
        else:
            self.cam = cv2.cv2.VideoCapture(0)
            print(f"ไม่สามารถเปิดกล้อง {x[-1]} ได้")
            QMessageBox.warning(self, "ไม่สำเร็จ",f"ไม่สามารถเปิดกล้อง {x[-1]} ได้!!\t")
  
    def update_frame(self):
        img = self.cam.read()[1] 
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.count <=5:
                    x = 240 + 80 * j
                    y = 160 + 80 * i
                    bestColor = 'White'
                    bestValue = 0
                    for key in ['Blue', 'Green', 'Red', 'Orange', 'White', 'Yellow']:
                        color = hsvColors[key] 
                        color[0] = cv2.inRange(hsv[y - 25: y + 25, x - 25: x + 25], np.array(color[1]), np.array(color[2]))
                        cv2.morphologyEx(color[0], cv2.MORPH_OPEN, (1, 1), color[0])
                        cv2.morphologyEx(color[0], cv2.MORPH_CLOSE, (1, 1), color[0])
                        avg = np.average(color[0])
                        if avg > bestValue:
                            bestValue = avg
                            bestColor = key
                    
                        self.dataColorRubik[self.count][3 * i + j] = faces[bestColor]
                        cv2.rectangle(img, (x - 25, y - 25),(x + 25, y + 25), rgbColors[bestColor], 2)
                        #img[y - 30: y + 30, x - 30: x + 30] = cv2.addWeighted(img[y - 30: y + 30, x - 30: x + 30], 0.4, np.full((60, 60, 3), rgbColors[bestColor], dtype=np.uint8), 0.3, 0)
                        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
                        self.ui.label_5.setText(f'ขั้นตอนที่ {self.count +1}')
                        self.ui.label_6.setText(method[f'{self.count +1}'][0])
                        self.ui.label_8.setText(method[f'{self.count +1}'][1])
                    
                elif self.count == 6:
                    self.ui.label_5.setText(f'ขั้นตอนที่ {self.count +1}')
                    self.ui.label_6.setText(method[f'{self.count +1}'][0])
                    self.ui.label_8.setText(method[f'{self.count +1}'][1])
                    self.ui.btNext.setText('เรื่มประมวลผล')
                    self.btNext.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(0, 200, 0, 240), stop:1 rgba(24, 248, 12, 180));color:rgb(255, 255, 255);border-radius:5px;") 
                    # self.output = ''
                    # for face in range(6):
                    #     self.output += ''.join(self.dataColorRubik[face])
                    self.count += 1
                                           
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format_RGB888)
        self.ui.video.setPixmap(QPixmap.fromImage(image))
        
    def nextCount(self):
        if self.count <= 5:
            self.addColorsRubik()
            self.count += 1 
        else:
            print()
            self.dataColorRubik[0][4] = 'y'
            self.dataColorRubik[1][4] = 'b'
            self.dataColorRubik[2][4] = 'r'
            self.dataColorRubik[3][4] = 'g'
            self.dataColorRubik[4][4] = 'o'
            self.dataColorRubik[5][4] = 'w'
            print(f"rubik = {self.dataColorRubik}")
            self.cube = ''
            for face in range(6):
                self.cube += ''.join(self.dataColorRubik[face])

            print()
            print(f"cube : {self.cube}")
            try:
                self.solve = utils.solve(self.cube, 'Kociemba')
            except Exception as e:
                print()
                print(f"Error!!! : Rubik's color is wrong")
                QMessageBox.critical(self, "Error", "เกิดข้อผิดพลาด สีของรูบิคไม่ถูกต้อง \nกรุณาตรวจสอบด้านที่สเเกนเเละรีเซ็ตอีกครั้ง\t")
            else:
                self.solve = utils.solve(self.cube, 'Kociemba')
                self.cube_solve = ""
                for i in self.solve:
                    self.cube_solve += str(i)+" "
                self.ui.result.setText(f" ผลลัพท์: {self.cube_solve}")
                print()
                print(f"cube solve ===>  {self.cube_solve} <===")
                print()
                self.btNext.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(0, 200, 0, 80), stop:1 rgba(24, 248, 12, 80));color:rgb(255, 255, 255);border-radius:5px;") 
                self.ui.btNext.setEnabled(False)
                self.ui.btRobot.setEnabled(True)
                
                self.ui.y1.setEnabled(False)
                self.ui.y2.setEnabled(False)
                self.ui.y3.setEnabled(False)
                self.ui.y4.setEnabled(False)
                self.ui.y5.setEnabled(False)
                self.ui.y6.setEnabled(False)
                self.ui.y7.setEnabled(False)
                self.ui.y8.setEnabled(False)
                self.ui.y9.setEnabled(False)
                
                self.ui.b1.setEnabled(False)
                self.ui.b2.setEnabled(False)
                self.ui.b3.setEnabled(False)
                self.ui.b4.setEnabled(False)
                self.ui.b5.setEnabled(False)
                self.ui.b6.setEnabled(False)
                self.ui.b7.setEnabled(False)
                self.ui.b8.setEnabled(False)
                self.ui.b9.setEnabled(False)
                
                self.ui.r1.setEnabled(False)
                self.ui.r2.setEnabled(False)
                self.ui.r3.setEnabled(False)
                self.ui.r4.setEnabled(False)
                self.ui.r5.setEnabled(False)
                self.ui.r6.setEnabled(False)
                self.ui.r7.setEnabled(False)
                self.ui.r8.setEnabled(False)
                self.ui.r9.setEnabled(False)
            
                self.ui.g1.setEnabled(False)
                self.ui.g2.setEnabled(False)
                self.ui.g3.setEnabled(False)
                self.ui.g4.setEnabled(False)
                self.ui.g5.setEnabled(False)
                self.ui.g6.setEnabled(False)
                self.ui.g7.setEnabled(False)
                self.ui.g8.setEnabled(False)
                self.ui.g9.setEnabled(False)

                self.ui.o1.setEnabled(False)
                self.ui.o2.setEnabled(False)
                self.ui.o3.setEnabled(False)
                self.ui.o4.setEnabled(False)
                self.ui.o5.setEnabled(False)
                self.ui.o6.setEnabled(False)
                self.ui.o7.setEnabled(False)
                self.ui.o8.setEnabled(False)
                self.ui.o9.setEnabled(False)
                
                self.ui.w1.setEnabled(False)
                self.ui.w2.setEnabled(False)
                self.ui.w3.setEnabled(False)
                self.ui.w4.setEnabled(False)
                self.ui.w5.setEnabled(False)
                self.ui.w6.setEnabled(False)
                self.ui.w7.setEnabled(False)
                self.ui.w8.setEnabled(False)
                self.ui.w9.setEnabled(False)
                
                self.ui.btRobot.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.955, y1:0.363455, x2:0, y2:1, stop:0 rgba(84, 183, 108, 255), stop:0.75 rgba(114, 225, 112, 255));\n"
                "color:rgb(255, 255, 255);\n"
                "border-radius:5px;\n"
                "")

    def addColorsRubik(self):
        self.colors = self.dataColorRubik[self.count]
        if self.count == 0:
            self.ui.y1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.y2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.y3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.y4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.y6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.y7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.y8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.y9.setStyleSheet(self.ColorsRubik[self.colors[8]])
        if self.count == 1:
            self.ui.b1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.b2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.b3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.b4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.b6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.b7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.b8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.b9.setStyleSheet(self.ColorsRubik[self.colors[8]])
        if self.count == 2:
            self.ui.r1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.r2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.r3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.r4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.r6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.r7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.r8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.r9.setStyleSheet(self.ColorsRubik[self.colors[8]])
        if self.count == 3:
            self.ui.g1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.g2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.g3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.g4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.g6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.g7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.g8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.g9.setStyleSheet(self.ColorsRubik[self.colors[8]])
        if self.count == 4:
            self.ui.o1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.o2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.o3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.o4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.o6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.o7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.o8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.o9.setStyleSheet(self.ColorsRubik[self.colors[8]])
        if self.count == 5:
            self.ui.w1.setStyleSheet(self.ColorsRubik[self.colors[0]])
            self.ui.w2.setStyleSheet(self.ColorsRubik[self.colors[1]])
            self.ui.w3.setStyleSheet(self.ColorsRubik[self.colors[2]])
            self.ui.w4.setStyleSheet(self.ColorsRubik[self.colors[3]])
            self.ui.w6.setStyleSheet(self.ColorsRubik[self.colors[5]])
            self.ui.w7.setStyleSheet(self.ColorsRubik[self.colors[6]])
            self.ui.w8.setStyleSheet(self.ColorsRubik[self.colors[7]])
            self.ui.w9.setStyleSheet(self.ColorsRubik[self.colors[8]])
            
    def Robot(self):
        self.ui.btRobot.setEnabled(False)
        connected_ssid = get_connected_ssid()
        if connected_ssid == "Robot_Cube":
            try:
                response = requests.get(f'http://192.168.4.1/')
            except Exception as e:
                self.ui.btRobot.setEnabled(True)
                print()
                QMessageBox.critical(self, "Error", "ไม่สามารถส่งข้อมูลได้")
                print(f"Unable to send data")
                print()
            else:
                requests.get(f'http://192.168.4.1/control?result=START {self.cube_solve}STOP')
                QMessageBox.information(self, "สำเร็จ", "ส่งข้อมูลสำเร็จ หุ่นยนต์ทำงาน!!\t")
                print()
                print('successfully!!')
                print()
                self.reset()
        elif connected_ssid != "Robot_Cube" :
            print()
            print(f"Error!!!: Unable to send data ,Please connect to Wi-Fi : Robot_Cube")
            print()
            QMessageBox.critical(self, "Error", "ไม่สามารถส่งข้อมูลได้ \nกรุณาเชื่อมต่อ Wi-Fi : Robot_Cube\t")
            self.ui.btRobot.setEnabled(True)
            
        # try:
        #     response = requests.get(f'http://192.168.4.1/')
        # except Exception as e:
        #     print()
        #     print(f"Error!!!: Unable to send data ,Please connect to Wi-Fi : Robot_Cube")
        #     print()
        #     QMessageBox.critical(self, "Error", "ไม่สามารถส่งข้อมูลได้ \nกรุณาเชื่อมต่อ Wi-Fi : Robot_Cube\t")
        #     self.ui.btRobot.setEnabled(True)
        # else:
        #     requests.get(f'http://192.168.4.1/control?result=START {self.cube_solve}STOP')
        #     QMessageBox.information(self, "สำเร็จ", "ส่งข้อมูลสำเร็จ หุ่นยนต์ทำงาน!!\t")
        #     print()
        #     print('successfully!!')
        #     print()
        #     self.reset()

    def reset(self):
        self.count = 0
        self.dataColorRubik = [['' for i in range(9)] for j in range(6)]
        self.ui.result.setText(" ผลลัพท์:")
        self.ui.y1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y5.setStyleSheet(self.ColorsRubik['y'])
        self.ui.y6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.y9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b5.setStyleSheet(self.ColorsRubik['b'])
        self.ui.b6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.b9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r5.setStyleSheet(self.ColorsRubik['r'])
        self.ui.r6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.r9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g5.setStyleSheet(self.ColorsRubik['g'])
        self.ui.g6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.g9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o5.setStyleSheet(self.ColorsRubik['o'])
        self.ui.o6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.o9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w1.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w2.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w3.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w4.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w5.setStyleSheet(self.ColorsRubik['w'])
        self.ui.w6.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w7.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w8.setStyleSheet(self.ColorsRubik['default'])
        self.ui.w9.setStyleSheet(self.ColorsRubik['default'])
        self.ui.btNext.setEnabled(True)
        self.ui.btRobot.setEnabled(False)
        
        self.ui.y1.setEnabled(True)
        self.ui.y2.setEnabled(True)
        self.ui.y3.setEnabled(True)
        self.ui.y4.setEnabled(True)
        self.ui.y5.setEnabled(True)
        self.ui.y6.setEnabled(True)
        self.ui.y7.setEnabled(True)
        self.ui.y8.setEnabled(True)
        self.ui.y9.setEnabled(True)
        
        self.ui.b1.setEnabled(True)
        self.ui.b2.setEnabled(True)
        self.ui.b3.setEnabled(True)
        self.ui.b4.setEnabled(True)
        self.ui.b5.setEnabled(True)
        self.ui.b6.setEnabled(True)
        self.ui.b7.setEnabled(True)
        self.ui.b8.setEnabled(True)
        self.ui.b9.setEnabled(True)
        
        self.ui.r1.setEnabled(True)
        self.ui.r2.setEnabled(True)
        self.ui.r3.setEnabled(True)
        self.ui.r4.setEnabled(True)
        self.ui.r5.setEnabled(True)
        self.ui.r6.setEnabled(True)
        self.ui.r7.setEnabled(True)
        self.ui.r8.setEnabled(True)
        self.ui.r9.setEnabled(True)
    
        self.ui.g1.setEnabled(True)
        self.ui.g2.setEnabled(True)
        self.ui.g3.setEnabled(True)
        self.ui.g4.setEnabled(True)
        self.ui.g5.setEnabled(True)
        self.ui.g6.setEnabled(True)
        self.ui.g7.setEnabled(True)
        self.ui.g8.setEnabled(True)
        self.ui.g9.setEnabled(True)

        self.ui.o1.setEnabled(True)
        self.ui.o2.setEnabled(True)
        self.ui.o3.setEnabled(True)
        self.ui.o4.setEnabled(True)
        self.ui.o5.setEnabled(True)
        self.ui.o6.setEnabled(True)
        self.ui.o7.setEnabled(True)
        self.ui.o8.setEnabled(True)
        self.ui.o9.setEnabled(True)
        
        self.ui.w1.setEnabled(True)
        self.ui.w2.setEnabled(True)
        self.ui.w3.setEnabled(True)
        self.ui.w4.setEnabled(True)
        self.ui.w5.setEnabled(True)
        self.ui.w6.setEnabled(True)
        self.ui.w7.setEnabled(True)
        self.ui.w8.setEnabled(True)
        self.ui.w9.setEnabled(True)
        
        self.ui.btNext.setText('สเเกน')
        self.ui.btNext.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(55, 55, 140, 219), stop:1 rgba(21, 108, 152, 226));\n"
                                "color:rgb(255, 255, 255);\n"
                                "border-radius:5px;\n"
                                "\n"
                                "")
        self.ui.btRobot.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.955, y1:0.363455, x2:0, y2:1, stop:0 rgba(84, 183, 108, 100), stop:0.75 rgba(114, 225, 112, 100));\n"
                                "color:rgb(255, 255, 255);\n"
                                "border-radius:5px;\n"
                                "")
        print("")
        print('reset')
    
    def addColorsEdit(self,color):
        self.editColors_Colors = color
        self.ui.label_Colors.setStyleSheet(self.ColorsRubik[color])
    def on_btR_click(self):
        self.addColorsEdit("r")
    def on_btB_click(self):
        self.addColorsEdit("b")
    def on_btG_click(self):
        self.addColorsEdit("g")
    def on_btY_click(self):
        self.addColorsEdit("y")
    def on_btO_click(self):
        self.addColorsEdit("o")
    def on_btW_click(self):
        self.addColorsEdit("w")
        
    def editColors(self,pos):
        if pos == "y1":
            self.ui.y1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][0]= self.editColors_Colors
        if pos == "y2":
            self.ui.y2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][1]= self.editColors_Colors
        if pos == "y3":
            self.ui.y3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][2]= self.editColors_Colors
        if pos == "y4":
            self.ui.y4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][3]= self.editColors_Colors
        if pos == "y5":
            self.ui.y5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][4]= self.editColors_Colors
        if pos == "y6":
            self.ui.y6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][5]= self.editColors_Colors
        if pos == "y7":
            self.ui.y7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][6]= self.editColors_Colors
        if pos == "y8":
            self.ui.y8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][7]= self.editColors_Colors
        if pos == "y9":
            self.ui.y9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[0][8]= self.editColors_Colors
        if pos == "b1":
            self.ui.b1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][0]= self.editColors_Colors
        if pos == "b2":
            self.ui.b2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][1]= self.editColors_Colors
        if pos == "b3":
            self.ui.b3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][2]= self.editColors_Colors
        if pos == "b4":
            self.ui.b4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][3]= self.editColors_Colors
        if pos == "b5":
            self.ui.b5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][4]= self.editColors_Colors
        if pos == "b6":
            self.ui.b6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][5]= self.editColors_Colors
        if pos == "b7":
            self.ui.b7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][6]= self.editColors_Colors
        if pos == "b8":
            self.ui.b8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][7]= self.editColors_Colors
        if pos == "b9":
            self.ui.b9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[1][8]= self.editColors_Colors
        if pos == "r1":
            self.ui.r1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][0]= self.editColors_Colors
        if pos == "r2":
            self.ui.r2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][1]= self.editColors_Colors
        if pos == "r3":
            self.ui.r3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][2]= self.editColors_Colors
        if pos == "r4":
            self.ui.r4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][3]= self.editColors_Colors
        if pos == "r5":
            self.ui.r5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][4]= self.editColors_Colors
        if pos == "r6":
            self.ui.r6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][5]= self.editColors_Colors
        if pos == "r7":
            self.ui.r7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][6]= self.editColors_Colors
        if pos == "r8":
            self.ui.r8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][7]= self.editColors_Colors
        if pos == "r9":
            self.ui.r9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[2][8]= self.editColors_Colors
        if pos == "g1":
            self.ui.g1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][0]= self.editColors_Colors
        if pos == "g2":
            self.ui.g2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][1]= self.editColors_Colors
        if pos == "g3":
            self.ui.g3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][2]= self.editColors_Colors
        if pos == "g4":
            self.ui.g4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][3]= self.editColors_Colors
        if pos == "g5":
            self.ui.g5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][4]= self.editColors_Colors
        if pos == "g6":
            self.ui.g6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][5]= self.editColors_Colors
        if pos == "g7":
            self.ui.g7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][6]= self.editColors_Colors
        if pos == "g8":
            self.ui.g8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][7]= self.editColors_Colors
        if pos == "g9":
            self.ui.g9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[3][8]= self.editColors_Colors
        if pos == "o1":
            self.ui.o1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][0]= self.editColors_Colors
        if pos == "o2":
            self.ui.o2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][1]= self.editColors_Colors
        if pos == "o3":
            self.ui.o3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][2]= self.editColors_Colors
        if pos == "o4":
            self.ui.o4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][3]= self.editColors_Colors
        if pos == "o5":
            self.ui.o5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][4]= self.editColors_Colors
        if pos == "o6":
            self.ui.o6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][5]= self.editColors_Colors
        if pos == "o7":
            self.ui.o7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][6]= self.editColors_Colors
        if pos == "o8":
            self.ui.o8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][7]= self.editColors_Colors
        if pos == "o9":
            self.ui.o9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[4][8]= self.editColors_Colors
        if pos == "w1":
            self.ui.w1.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][0]= self.editColors_Colors
        if pos == "w2":
            self.ui.w2.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][1]= self.editColors_Colors
        if pos == "w3":
            self.ui.w3.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][2]= self.editColors_Colors
        if pos == "w4":
            self.ui.w4.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][3]= self.editColors_Colors
        if pos == "w5":
            self.ui.w5.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][4]= self.editColors_Colors
        if pos == "w6":
            self.ui.w6.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][5]= self.editColors_Colors
        if pos == "w7":
            self.ui.w7.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][6]= self.editColors_Colors
        if pos == "w8":
            self.ui.w8.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][7]= self.editColors_Colors
        if pos == "w9":
            self.ui.w9.setStyleSheet(self.ColorsRubik[self.editColors_Colors])
            self.dataColorRubik[5][8]= self.editColors_Colors

    def y1_click(self):
        self.editColors("y1")
    def y2_click(self):
        self.editColors("y2")
    def y3_click(self):
        self.editColors("y3")
    def y4_click(self):
        self.editColors("y4")
    def y5_click(self):
        self.editColors("y5")
    def y6_click(self):
        self.editColors("y6")
    def y7_click(self):
        self.editColors("y7")
    def y8_click(self):
        self.editColors("y8")
    def y9_click(self):
        self.editColors("y9")
    
    def b1_click(self):
        self.editColors("b1")
    def b2_click(self):
        self.editColors("b2")
    def b3_click(self):
        self.editColors("b3")
    def b4_click(self):
        self.editColors("b4")
    def b5_click(self):
        self.editColors("b5")
    def b6_click(self):
        self.editColors("b6")
    def b7_click(self):
        self.editColors("b7")
    def b8_click(self):
        self.editColors("b8")
    def b9_click(self):
        self.editColors("b9")
    
    def r1_click(self):
        self.editColors("r1")
    def r2_click(self):
        self.editColors("r2")
    def r3_click(self):
        self.editColors("r3")
    def r4_click(self):
        self.editColors("r4")
    def r5_click(self):
        self.editColors("r5")
    def r6_click(self):
        self.editColors("r6")
    def r7_click(self):
        self.editColors("r7")
    def r8_click(self):
        self.editColors("r8")
    def r9_click(self):
        self.editColors("r9")
    
    def g1_click(self):
        self.editColors("g1")
    def g2_click(self):
        self.editColors("g2")
    def g3_click(self):
        self.editColors("g3")
    def g4_click(self):
        self.editColors("g4")
    def g5_click(self):
        self.editColors("g5")
    def g6_click(self):
        self.editColors("g6")
    def g7_click(self):
        self.editColors("g7")
    def g8_click(self):
        self.editColors("g8")
    def g9_click(self):
        self.editColors("g9")
        
    def o1_click(self):
        self.editColors("o1")
    def o2_click(self):
        self.editColors("o2")
    def o3_click(self):
        self.editColors("o3")
    def o4_click(self):
        self.editColors("o4")
    def o5_click(self):
        self.editColors("o5")
    def o6_click(self):
        self.editColors("o6")
    def o7_click(self):
        self.editColors("o7")
    def o8_click(self):
        self.editColors("o8")
    def o9_click(self):
        self.editColors("o9")

    def w1_click(self):
        self.editColors("w1")
    def w2_click(self):
        self.editColors("w2")
    def w3_click(self):
        self.editColors("w3")
    def w4_click(self):
        self.editColors("w4")
    def w5_click(self):
        self.editColors("w5")
    def w6_click(self):
        self.editColors("w6")
    def w7_click(self):
        self.editColors("w7")
    def w8_click(self):
        self.editColors("w8")
    def w9_click(self):
        self.editColors("w9")

    
    def Qmessage_reset(self):
        reply = QMessageBox.question(self, 'ยืนยันการรีเซ็ต', 'คุณต้องการรีเซ็ตใช่หรือไม่?\t', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reset()
    
    def Qmessage_appExit(self):
        reply = QMessageBox.warning(self, 'ยืนยันออกจากโปรแกรม', 'คุณต้องการออกจากโปรแกรมใช่หรือไม่?\t', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCoreApplication.quit()
    
    def closeEvent(self, event):
        reply = QMessageBox.warning(self, 'ยืนยันออกจากโปรแกรม', 'คุณต้องการออกจากโปรแกรมใช่หรือไม่?\t', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
app = QApplication(sys.argv)
windown1 = MainWindow()
windown1.show()
sys.exit(app.exec_())