# -*- coding: utf-8 -*-
# 哔哩哔哩自动完成任务 V1.0.0
# 本程序可以实时获取B站私信新消息，并向您发送通知。

import requests
import win32gui
import win32con
import os
import sys
import time

appdata = os.getenv ("Appdata") # 获取环境变量Appdata的值
true = True
false = False
null = None

class WindowsBalloonTip:
    def __init__(self):
        message_map = {win32con.WM_DESTROY: self.OnDestroy,}
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        self.hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        self.classAtom = win32gui.RegisterClass(wc)

    def ShowWindow(self, title, msg):
        # 创建窗口
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( self.classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, self.hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(self.hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                         (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)


    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # 终止消息

w = WindowsBalloonTip()

def isConnected (): # 判断网络是否连接正常
    try: # 异常调试
        requests.get ("https://www.bilibili.com/")
    except: # 如果requests请求异常，执行except内的操作
        return False
    return True

def fix (): # 异常修复
    print ()
    print ("程序的配置损坏，这通常是因为程序意外关闭导致的！")
    print ("请重新填写数据（填写好的数据将会被记录，以方便下次使用）")
    print ()
    if os.path.exists (appdata + "\\bilimsghelperdata.txt"): # 如果配置存在
        os.remove (appdata + "\\bilimsghelperdata.txt") # 删除配置文件
    
    Cookie () # 跳转到设置
        
def check (): # 检查配置文件是否存在，并检查Cookie是否失效
    if (os.path.exists (appdata + "\\bilimsghelperdata.txt")): # 配置文件存在
        print ("是否使用上次的配置？")
        
        while True: # 一直循环
            c = input ("输入1立即使用上次的配置，输入2则重新配置 [1/2] ")
            if c == "1" or c == "2": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环
        
        if c == "1": # 使用上次的配置
            main () # 跳转到主程序
            
        else: # 重新配置
            if os.path.exists (appdata + "\\bilimsghelperdata.txt"): # 如果配置存在
                os.remove (appdata + "\\bilimsghelperdata.txt") # 删除配置文件
            
            print () # 输出空行
            print ("请填写数据（填写好的数据将会被记录，以方便下次使用）")
            Cookie () # 跳转到设置
        
    else: # 配置文件不存在
        print ("检测到第一次使用该程序，请先填写数据（填写好的数据将会被记录，以方便下次使用）")
        Cookie ()

def Cookie (): # 输入Cookie
    print ()
    SESSDATA = input ("请输入SESSDATA的值：")
    bili_jct = input ("请输入bili_jct的值：")
    with open (appdata + "\\bilimsghelperdata.txt", "at") as file:
        file.write (SESSDATA + "\n" + bili_jct)
    main () # 跳转到主程序
    
    
def main (): # 主程序
    appdata = os.getenv ("Appdata") # 获取环境变量Appdata的值
    with open (appdata + "\\bilimsghelperdata.txt", "rt") as x:
        line = x.read ().splitlines () # 读取内容，并分割每行

    try: # 异常调试
        SESSDATA = line[0] # 读取第1行内容：Cookie（SESSDATA）
        bili_jct = line[1] # 读取第2行内容：Cookie（bili_jct）

    except: # 如果读取配置文件异常，执行except内的操作
        fix ()
        return
        
    headers = {"Cookie": "SESSDATA=" + SESSDATA + "; bili_jct=" + bili_jct, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}

    # 获取API返回值（验证Cookie是否失效）  
    result = requests.get ("https://api.bilibili.com/x/web-interface/nav", headers = headers).text # 获取当前用户登录信息
    code = eval (result) ["code"] # 获取命令行返回值，并改变编码为“utf-8”，转换类型为“词典”，并获取API的返回值

    if code != 0: # 账号未登录（-101），请求错误（-400），或者是其他原因导致的失败
        print ("cookie已失效或填写不正确！")
        if os.path.exists (appdata + "\\bilimsghelperdata.txt"): # 如果配置存在
            os.remove (appdata + "\\bilimsghelperdata.txt") # 删除配置文件
        Cookie () # 重新输入Cookie
        return
        
    timestamp = str(int(time.time() * 1000000)) # 获取当前时间戳，去除小数点
    w.ShowWindow("开始运行","开始运行！")
    print ()

    while True: # 无条件一直循环
        data = eval(requests.get("https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts=" + timestamp + "&build=0&mobi_app=web",headers=headers).text) # 获取消息列表
        user = eval(requests.get('https://api.bilibili.com/x/web-interface/nav',headers=headers).text) # 获取当前账号UID

        if (data.get("code") != 0) or (user.get("code") != 0): # 如果data和user的状态码不是“0”，报错
            print("错误：" + data.get("message"))
            
        else:
            if data.get("data").get("session_list") != None: # 如果有新消息
                for i in range(len(data.get("data").get("session_list"))):
                    tallker_id = str(data.get("data").get("session_list")[i].get("talker_id")) # 获取消息发送者UID
                    session = eval(requests.get("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?talker_id=" + tallker_id + "&session_type=1&size=20&build=0&mobi_app=web",headers=headers).text) # 获取私信聊天记录
                    if session.get("code") != 0: # 如果状态码不是“0”，报错
                        print("错误：" + data.get("message"))
                    else:
                        for num in range(int(data.get("data").get("session_list")[i].get("unread_count")) -1,-1,-1):
                            if str(session.get("data").get("messages")[num].get("sender_uid")) == user: # 如果消息是当前账号发送的
                                continue # 跳过本次循环，直接进行下一轮循环
                            else:
                                try:
                                    content = str(eval(session.get("data").get("messages")[num].get("content")).get("content","[未知类型]")) # 获取消息
                                except:
                                    content = "撤回了一条消息"
                                sender_uid = str(session.get("data").get("messages")[num].get("sender_uid"))
                                ts = session.get("data").get("messages")[num].get("timestamp")
                                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                                w.ShowWindow("UID" + sender_uid,"[" + ts + "] " + content)
                                print("[" + ts + "] " + "UID" + sender_uid + "：" + content)
                                # post=requests.post("https://api.chanify.net/v1/sender/token",data={'content':"UID" + sender_uid + "：" + content}).text
                    
        timestamp = str(int(time.time() * 1000000))
        time.sleep(5)
        
        
# 程序开始运行时，运行以下代码
while True: # 一直循环
    if isConnected () == true: # 网络是否连接正常
        check ()
    else:
        print ("无法连接到互联网，这会使任务无法完成！请检查网络是否正常！（按Enter键重试）")
        os.system ("pause >nul")