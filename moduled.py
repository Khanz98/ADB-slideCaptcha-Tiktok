import os,time,sys
try:
 import threading,subprocess,base64,cv2,random,requests
 import numpy as np
 import cv2
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
  os.system("pip install requests")
  os.system("pip install pywin32")
  os.system("pip install psutil")
  os.system("pip install hashlib")
import threading,subprocess,base64,cv2,random,requests
import numpy as np
from datetime import datetime
import cv2
import json, win32gui, hashlib
import re
from sys import exit
from win32api import GetSystemMetrics
import psutil
import xml.etree.cElementTree as XML
sys.setrecursionlimit(10000)
# from md import *
from time import sleep


def bypass_slide(image):
    image = cv2.imread(image)
    # img = image[430:765, 102:648] # cắt chỗ có captcha # cut zone captcha
    img = image[350:590, 70:470]
    # img = image[400:1505, 80:1248]
    #cv2.imshow("a", img)
    #cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = cv2.Canny(gray, 200, 200, L2gradient=True)
    kernel = np.ones([23,23]) # Tạo kernel
    kernel[2:,2:] = -0.1
    im = cv2.filter2D(img3/255, -1, kernel)
    im1 = im[:,:125]
    y1,x1 = np.argmax(im1)//im1.shape[1], np.argmax(im1)%im1.shape[1] # Tìm vị trí 1 chính xác
    im2 = im[:,125:]
    y2,x2 = np.argmax(im2)//im2.shape[1], np.argmax(im2)%im2.shape[1] + 125 # Tìm vị trí 1 chính xác
    # cv2.rectangle(img, (x1,y1), (x1+50, y1+50), 255, 2)
    # cv2.rectangle(img, (x2,y2), (x2+50, y2+50), 255, 2)
    # plt.imshow(img)
    # plt.show()
    return x2-x1
fileRd = []
def randomFile(folder):
    time.sleep(3)
    for root, dirs, files in os.walk(r'{}'.format(folder)):
        for file in files:
            if file.endswith('.png'):
                fileRd.append(file)
            elif file.endswith('.jpg'):
                fileRd.append(file)
            elif file.endswith('.jpge'):
                fileRd.append(file)
    try:
        fileEnd = random.choice(fileRd)
        return {"status": "success", "path": r"{}/{}".format(folder, fileEnd), 'file': fileEnd} 
    except:
        return {"status": "error"}


class Connect(object):
    """
    Kết nối PC với điện thoại của bạn để Automatic rất dễ dàng
    Hãy lưu ý các tham số đầu vào cho các lớp và hàm
    Library By Tài Lê Official
    Welcome to Vietnamese
    """
    def __init__(self):
        """
        Turn on Application ADB
        Check List Device
        """
        # for proc in psutil.process_iter():
        #     if proc.name() == "adb.exe":
        #         try:
        #             subprocess.call('adb kill-server', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        #         except:
        #             pass
        getAllDevice = subprocess.check_output('adb devices')
    def reset(self):
        for proc in psutil.process_iter():
            if proc.name() == "adb.exe":
                try:
                    subprocess.call('adb kill-server', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                except:
                    pass
    def getDevices(self) -> list:
        Devices = []
        getAllDevice = subprocess.check_output('adb devices')
        listDevice = str(getAllDevice).split('\\r')
        for dv in listDevice:
            if '\\tdevice' in dv:
                try:
                    deviceSrial = dv.split('\\n')[1].split('\\t')[0]
                    Devices.append(deviceSrial)
                except:
                    pass
            else:
                pass
        if int(len(Devices)) == 0:
            return '0 connection'
        else:
            return Devices

    def showDevice(self,serial: str, width: int, height: int, x:int , y: int, title: str):
        """Hiển thị điện thoại của bạn lên màn hình máy tính"""
        subprocess.Popen(f'scrcpy -s {serial} --window-title "{title}" --window-x {x} --window-y {y} --window-width {width} --window-height {height}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

class ADB(object):
    """
    Class nhằm mục đích auto remote Phone của bạn
    """
    
    def checkImage(self, serial: str, image: str, *name_luong) -> dict:
        """
        Use OpenCV to find the picture in the frame. If the function exists, it will return x and y . coordinates
        Very useful in some cases
        Library By Tài Lê Official
        Welcome to VietNam
        """
        status = False
        if name_luong:
            name_luong = name_luong[0]
            mr = os.path.join(os.getcwd(), name_luong)
            if os.path.exists(mr)==False:
                os.mkdir(mr)
        try:
            #chụp ảnh r đẩy ảnh lên pc
            if name_luong:
                subprocess.call(f'adb -s {serial} shell screencap -p /sdcard/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                #time.sleep(2)
                subprocess.call(f'adb -s {serial} pull /sdcard/screen.png {name_luong}/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                large_image = cv2.imread(f"{name_luong}/screen.png") #đọc ảnh đc chụp ở phone r đẩy ra
            else:
                subprocess.call(f'adb -s {serial} shell screencap -p /sdcard/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                # time.sleep(2)
                subprocess.call(f'adb -s {serial} pull /sdcard/screen.png screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                large_image = cv2.imread(r"screen.png") #đọc ảnh đc chụp ở phone r đẩy ra
            ######
            #đọc ảnh đc đẩy ra và ảnh có sẵn
            method = cv2.TM_SQDIFF_NORMED
            small_image = cv2.imread(r"img/"+image) #đọc ảnh có sẵn ở thư mục img
            ########
            result = cv2.matchTemplate(small_image, large_image, method) # bắt đầu so sánh ảnh
            #đoạn này e ch học qua
            mn,_,mnLoc,_= cv2.minMaxLoc(result)
            min_val = cv2.minMaxLoc(result)[0]
            ######
        # đoạn này tạm bỏ qua
        except Exception as error:
            print('adb adb_click fail:',error)
            if name_luong:
                subprocess.call(f'adb -s {serial} shell screencap -p /sdcard/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                subprocess.call(f'adb -s {serial} pull /sdcard/screen.png {name_luong}/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                large_image = cv2.imread(f"{name_luong}/screen.png") #đọc ảnh đc chụp ở phone r đẩy ra
            else:
                subprocess.call(f'adb -s {serial} shell screencap -p /sdcard/screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                # time.sleep(2)
                subprocess.call(f'adb -s {serial} pull /sdcard/screen.png screen.png', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                large_image = cv2.imread(r"screen.png") #đọc ảnh đc chụp ở phone r đẩy ra
            ######
            #đọc ảnh đc đẩy ra và ảnh có sẵn
            time.sleep(1)
            method = cv2.TM_SQDIFF_NORMED
            small_image = cv2.imread(r"img/"+image) #đọc ảnh có sẵn ở thư mục img
            ########
            result = cv2.matchTemplate(small_image, large_image, method) # bắt đầu so sánh ảnh
            #đoạn này e ch học qua
            mn,_,mnLoc,_= cv2.minMaxLoc(result)
            min_val = cv2.minMaxLoc(result)[0]
        ###############
        #đoạn này cx tke nó là điều kiện để xem ảnh có trùng k. trùng thì click k thì bỏ trả về False
        thr = 0.02
        MPx,MPy = mnLoc
        trows,tcols = small_image.shape[:2]
        #print(x)
        ######
        if min_val <= thr :
            x=round(MPx+(tcols/2)) #lấy tọa độ x
            y=round(MPy+(trows/2)) #lấy tọa độ y
            status = True
        else:
            status = False
        if status == True:
            return {'status': "success", 'x': x, 'y': y}
    def excuteAdb(self, serial: str, command):
        """
        Excute ADB Command Shell
        Use command lines to control your adnroid
        """
        subprocess.call(f'adb -s {serial} {command}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def openApp(self,serial: str, packagename: str):
        """
        Open App From Packagename
        """
        subprocess.call(f'adb -s {serial} shell "monkey -p {packagename} -c android.intent.category.LAUNCHER 1"', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # def killApp(self,nameLd, packagename):
    #     """
    #     Stop/Kill Processed App From Packagename
    #     """
    #     subprocess.call(f'ldconsole killapp --name {nameLd} --packagename {packagename}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def resetServer(self):
        """
        Reset Server ADB
        """
        subprocess.call("adb kill-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        subprocess.call("adb start-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)
    
    def clearData(self, serial: str, packagename: str):
        """
        Clear all data app by packagename
        """
        subprocess.call(f'adb -s {serial} shell "pm clear {packagename}"', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def checkInstallApk(self, serial: str, packagename: str):
        """
        Check if the packagename of the app is installed
        Kiểm tra xem app đã cài đặt chưa bằng check list Packagename 
        """
        try:
            apps=subprocess.check_output('adb -s %s shell pm list packages'%(serial)).decode('utf8').strip().split('\r\r\r\n')
            app_check = False
            for i in apps:
                if packagename in i:
                    app_check=True
            return app_check
        except Exception as error:
                print('error check_installapped:',error)

    def pushFile(self, serial: str, fromPc: str, to: str):
        """
        Đẩy file vào Android
        Push files to android
        """
        cmd = f'adb -s {serial} push \\"{fromPc}\\" \\"{to}\\""'
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def installApk(self,serial: str, link_app: str):
        """
        Cài đặt apk từ PC
        Install apk app from Commputer
        """
        cmd = f'adb -s {serial} install "{link_app}"'
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def changeProxy(self, serial: str, ip: int, port: int):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {serial} shell settings put global http_proxy {ip}:{port}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remProxy(self, serial: str):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {serial} shell settings put global http_proxy :0', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def inputTap(self,serial: str , x: int, y: int):
        """
        Input tap click
        Click theo tọa độ x, y
        """
        subprocess.call(f'adb -s {serial} shell input tap {x} {y}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def inputSwipe(self, serial: str, x: int, y: int, finishX: int, finishY: int, *dur: int):
        if dur:
            subprocess.call(f'adb -s {serial} shell input swipe {x} {y} {finishX} {finishY} {dur[0]}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.call(f'adb -s {serial} shell input swipe {x} {y} {finishX} {finishY}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def inputText(self, serial: str, text: str):
        charsb64 = str(base64.b64encode(text.encode('utf-8')))[1:]
        subprocess.call('adb -s %s shell am broadcast -a ADB_INPUT_B64 --es msg %s '%(serial,charsb64), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # subprocess.call('adb -s %s "shell input text \\"%s\\"" '%(serial,text))

    def inputKeyEvent(self,serial: str, key: int):
        subprocess.call(f'adb -s {serial} shell input keyevent {key}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def killApp(self, serial: str, packagename: str):
        subprocess.call(f"adb -s {serial} shell am force-stop {packagename}")

    def startLink(self, sr: str, action: str, packagename: str):
        subprocess.call(f"adb -s {sr} shell am start -a android.intent.action.VIEW -d {action} {packagename}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    #DUMP XML
    def dumpXml(self, serial: str):
        srdev = serial
        serial = hashlib.md5(bytes(str(serial), 'utf-8-sig')).hexdigest()
        if os.path.exists(f"{os.getcwd()}\\{serial}\\ui.xml") == False:
            mr = os.path.join(os.getcwd(), serial)
            if os.path.exists(mr)==False:
                os.mkdir(mr)
            open(f"{os.getcwd()}\\{serial}\\ui.xml", "w+")
        self.serial = serial
        subprocess.call(f'adb -s {srdev} shell \"uiautomator dump /sdcard/uidump.xml\"')
        subprocess.call(f'adb -s {srdev} pull /sdcard/uidump.xml "{os.getcwd()}\\{serial}\\ui.xml"', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def getElement(self, attrib, name):
        try:
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2])-int(coord[0]))/2.0 + int(coord[0])
                    Ypoint = (int(coord[3])-int(coord[1]))/2.0 + int(coord[1])
                    return Xpoint, Ypoint
        except:
            pass
    
    def getTextByChar(self, name):
        attrib = "text"
        try:
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if name in elem.attrib[attrib]:
                    text = elem.attrib["text"]
                    return text
        except:
            pass

    def findElementByContentV2(self, name):
        attrib = "content-desc"
        try:
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if name in elem.attrib[attrib]:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2])-int(coord[0]))/2.0 + int(coord[0])
                    Ypoint = (int(coord[3])-int(coord[1]))/2.0 + int(coord[1])
                    return Xpoint, Ypoint
        except:
            pass
    
    def findElementByContentV1(self, name):
        attrib = "content-desc"
        try:
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if name in elem.attrib[attrib]:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2])-int(coord[0]))/2.0 + int(coord[0])
                    Ypoint = (int(coord[3])-int(coord[1]))/2.0 + int(coord[1])
                    return Xpoint, Ypoint
        except:
            pass


    def getElements(self, attrib, name):
        try:
            list = []
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2])-int(coord[0]))/2.0 + int(coord[0])
                    Ypoint = (int(coord[3])-int(coord[1]))/2.0 + int(coord[1])
                    list.append((Xpoint, Ypoint))
            return list
        except:
            pass

    def getText(self, attrib, name):
        try:
            self.pattern = re.compile(r"\d+")
            tree = XML.ElementTree(file=f"{os.getcwd()}\\{self.serial}\\ui.xml")
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    text = elem.attrib["text"]
                    return text
        except:
            pass
    def findText(self,attr, name):
        return self.getText(attr, name)


    def findElementByName(self, name):
        return self.getElement("text", name)

    def findElementsByName(self, name):
        return self.getElements("text", name)

    def findElementByClass(self, className):
        return self.getElement("class", className)

    def findElementsByClass(self, className):
        return self.getElements("class", className)

    def findElementById(self, id):
        return self.getElement("resource-id",id)

    def findElementsById(self, id):
        return self.getElements("resource-id",id)

def slideCaptcha(sr, adb):
    adb.dumpXml(sr)
    checktext = adb.findElementByName("Làm mới")
    print(checktext)
    if checktext:
        # adb.excuteAdb(sr, "adb shell screencap -p /sdcard/cap.png")
        # adb.excuteAdb(sr, f"adb pull /sdcard/cap.png {sr}/captcha.png")
        check = adb.checkImage(sr, "keo.png", sr)
        if check['status'] == "success":
            captcha = bypass_slide(f"{sr}/screen.png")
            adb.inputSwipe(sr, round(check['x']), round(check['y']), int(check['x'])+int(captcha), round(check['y']), 1000)
        return True
    else:
        return False

# adb = ADB()
# sr = "52005d83eaa63585"
# slideCaptcha(sr, adb)
a = Connect()
Devices = a.getDevices()
thread_count = len(Devices)
print(Devices)

class starts(threading.Thread):
    def __init__(self, nameLD,min_sleep,max_sleep, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep
    def run(self):
        min_sleep = self.min_sleep
        max_sleep = self.max_sleep
        device = self.device
        d = ADB()
        #d.remProxy(device)
        slideCaptcha(device, d)
        
        #d.inputTap(device,100,200)
        #d.changeProxy(device,'120.0.0.1',1654)


min_sleep = int(input(">> Nhập số min sleep (s): "))
max_sleep = int(input(">> Nhập số max sleep (s): "))
def main(m):
        device = Devices[m]
        for i in range(m, 10000, thread_count):
                run = starts(device,min_sleep,max_sleep,device,)
                run.run()

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()
        