# -*- coding: utf-8 -*-
# 哔哩哔哩自动完成任务 V2.0.0
# 本程序可以实时获取B站私信新消息，并向您发送通知。

import requests
import win32gui
import win32con
import os
import sys
import time
import base64

appdata = os.getenv ("Appdata") # 获取环境变量Appdata的值
TEMP = os.getenv ("TEMP") # 获取环境变量TEMP的值
true = True
false = False
null = None
已输出的消息 = []

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
        
        # base64解码 ballontip.ico，存放于%TEMP%
        ballontip = base64.b64decode("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LzMvMzMzMzMzMzMzNkBAQDYzMy8zLzMzMzMzSHx/e3BdPTMzMzMzMzMzMzMzMzMzd3x6cmNGMzMzMzMzNkBCQDozMzMzMzMzMzYzUf///////25AMzNwbjM2M1J8TTM2////////d00zM1t3QEZCRn9nMzMzMzUzNTMzW///fEh3////TTb/dzn/YGD/UjZD////SGz///9kNm7/PXd3S/9sMzYzNjU1NTYzY///dzM2bP//f0j/bkb/XWT/VT1V////NjZb////Q33/NnxwUf9sNjM2MzY2NjY2Z///bj9dev//fFv/ZFX/TWf/XUZV//98P1Fw////Uv96Nv9uWP9sNjY2NjY2NjY2cP////////93Rmr/W2D/Rm7/Wz9c/////////3xVTf9yQP9nXf9sNjY2NjY2NjY2d///gYF6Z002Nnf/UWf/P3D/UTZk/////3puWDo2Y/9sTf9kZP9sNjY2NjY2NjY5f/9YRjY2Ojo6Ov//RnD/Onf/UTZu/2A2NjY2NjY6cP9jW/9dZ/9sNjY2Njo6Ojo9//9PRjk5OkZGSGpuPXp/NmNnSDZ3/1s2Ojo6P0JGZ25PZP9cXW5YOjo6OjY6NjpI//9LRjk5OklGWGJjQIF6OmNYQDp8/1E2PUBGS0lLZ1s/bP9RYlxPOjY6Njo6OjlY/4FGSTk5OkJJam57S/93P3x0TT///09JSElJRklYd3pGdP9NdHBnOjo6Ojo6Ojpj/3xJSTo6Ojo6dG50WP90S3x0T03//09LRklJQj9dbP86fP9Ld3JnOjo6Ojo6PTpt/3tLST06PTo6S0tRWP9uQFFNQFv//0ZGRj8/PT1CSVg9/3xLXFFJPTo9Ojo9Oj13/3pLSz86PTo9Ojo6Y/9kOjo9Omf//0A6PTo9OT05PTpG/3tLS0I6Oj05PTo/Oj2B/3dLSz89Oj06PT06av9dPz06PW7//0A6PTo9Oj06PT1P/3dLS0I9PTo9Oj06P0b//3pLS0I9PT0/Oj89Z4FbOj89PXv//0I/PT86Pz09Oj1UfHBLS0A9PT09PT0/P0///3pLS0I/PT0/PT09PTo/Pz09P3///0Y9PT0/Oj89Pz0/Qk9LS0A9PT09PT09Pz9GY3JLT0s/Pz8/Pz8/Pz8/Pz8/Pz9YcEY/Pz8/Pz8/Pz8/S09MTz8/Pz0/Pz8/Pz8/P0lPT09LSUJCQkJAQD8/Pz8/Pz8/Pz8/QEBAQkJCRkZLT09NST8/Pz8/Pz8/Pz8/P0BLT09PT09PT09PT09PT09PT09PTU9PTU9PT09PT09PT09PQD8/Pz8/P0BAQEBAQEBGTE9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0xCQkBCP0I/QEBAQkBCQEA/QktPT09PT09PT09PT09PT09PT09PT09PT09PT09PS0JAQD9CQEBCP0BAQEBCQEJCQj9CQkZJSUlPT1FPT0tLS09LTVFPT1FLS0ZJRkJCQkBCQEJAQkBAQkJGQEZAQkJCQkJCQkJCQkZPT09RS0JCQkJCQktRT09PRkJCQkJCQkJCQkJCQkJCQkZAQkJCQkJCQkJCQkJCQk9RUU9PQkJCQkJCQkJPUVFPT0JCQkJCQkJCQkJCQkJCRk9CRkJGQkJGQkJGQkJCS09UT1RJQkJCQkJCQkZJT1RUT0lCQkJCQkJCQkJCQkJCT2NGQkJCRkJCRkJCSUJGSVJSVExCSUJGRkZGQkJJTFJUUklCSUJGRkZGRkZGRkJGYwBCRkZCRkZCRkZCSUJCQktMTEVCRUJCQkJCSUJFQkxPSUJFQklCQkJCQkJCSUJCAABdRkJJQkZCSUJJQklGRUVFRUVFRUlFSUlFRUVFRUVCSUVFQklCSUlFSUVFQkliAAAAT0lCSUlFRUVFSUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFSUVFRUVFRUVFSUwAAAAAAE9JSUVFSUVJRUVJRUlFSUVJRUlFSUVJRUlFSUVJRUlFRUVJRUlFSUVJTAAAAAAAAABiRUlFRUlFRUVFRUlFRUVFRUlFRUVFRUlFRUlFSUVFSUlFSUVFSUViAAAAAAAAAAAAAGRUSUlJSUlJSUVJSUlJSUVJSUlJSUVJSUVJSUlJSUVJSUlUZAAAAAAAAPwAAAAAPwAA8AAAAAAPAADgAAAAAAcAAMAAAAAAAwAAgAAAAAABAACAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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/v6KVP//j1v+/o9b//+PW/7+j1v+/o9b/v6PW///j1v+/o9b/v6PW///j1v+/o9b/v6PW///j1v+/o9b/v6PW///j1v+/o9b/v6PW///j1v+/o9b/v6PW///j1v+/o9b//+PW/7+j1v+/o9b//+PW/z+fFPT/mJImf9HO2D+MzM1/jMzM/84M0L+MzM0/jMzM/87M03+dTf9/nY3/vl3Of//dzn//3c5//93Of//dzn//3c5//93Of//gUf//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//fEbw/2A4uv9NNoD/OjRI/zIyMv8zMzP/YzjD/3c5//94O///eDv+/ng7/v54O///eDv+/ng7/v5+Q///kFz+/pFd/v6RXf//kV3+/pFd//+RXf7+kV3+/pFd/v6RXf//kFz+/o9b/v6OWf//jVj+/o1X/v6MV///jFb+/oxW/v6MVv//jFb+/oxX/v6NV///jVj+/o5Z/v6PW///kFz+/pFd//+RXf7+kV3+/pFd//+RXf7+kV3+/pFd//+RXf7+kFz+/n1C//94O/7+eDv+/mw62v9ZOKH+ZjnI/ng7/v55PP//eTz//3k8//95PP//eTz//3k8//+MVv//kl7//5Je//+SXv//jVj//4JJ//9/RP//fUL//3s///96Pf//eTz//3k8//95PP//eTz//3k8//95PP//eTz//3k8//95PP//eTz//3k8//95PP//eTz//3k8//95PP//eTz//3k9//97P///fUH//39E//+CSf//jVj//5Je//+SXv//kl7//4tV//95PP//eTz//3k8//95PP//eTz//3k8//96Pf//ej3+/no9/v56Pf//ej3+/n1B/v6TX///k1/+/pNf/v6OWf//ez7+/no9//96Pf7+ej3+/no9/v56Pf//ej3+/no9/v56Pf//ej3+/no9/v56Pf//ej3+/no9/v56Pf//ej3+/no9/v56Pf//ej3+/no9/v56Pf//ej3+/no9//96Pf7+ej3+/no9//96Pf7+ez/+/o9a//+TX/7+k1/+/pNf//98QP7+ej3+/no9//96Pf7+ej3+/no9/v57P///ez/+/ns//v57P///ez/+/oNJ/v6UYf//lGH+/pRh/v6FTf//ez/+/ns///97P/7+ez/+/ns//v57P///ez/+/ns//v57P///ez/+/ns//v57P///ez/+/ns//v57P///ez/+/ns//v57P///ez/+/ns//v57P///ez/+/ns///97P/7+ez/+/ns///97P/7+ez/+/oZO//+UYf7+lGH+/pRh//+CSP7+ez/+/ns///97P/7+ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/oVM/v6UYf//lGH+/pRh/v6DSf//ez/+/nxA//97P/7+ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/ns//v58QP//ez/+/nxA//97P/7+ez/+/nxA//97P/7+ez/+/oNK//+UYf7+lGH+/pRh//+ETP7+ez/+/nxA//97P/7+ez/+/ns//v59Qv//fUL//31C//99Qv//fUL//5xu///x6///9O///+7m///Zx///uZn//49c//99Qv//fUL//31C//99Qv//fUL//31C//99Qv//fUL//31C//99Qv//fUL//31C//99Qv//fUL//+fc///y7P//7eX//97P///Dp///m27//35C//99Qv//fUL//31C//99Qv//fUL//4JJ//+VY///lWL//5Vj//+IUP//fUL//31C//99Qv//fUL//31C//9/RP//fkP+/n5D/v5/RP//fkP+/quE/v7//////v7+/v7+/v7+/v///v7+/v79///Xxf7+k2H+/n5D/v5+Q///2cf+/tbD/v5/RP//gEX+/n9E/v6nfv//8+7+/qR6/v5/RP//g0r+/v7+/v7//////v7+/v7+/v7//////v7+/ujd//+le/7+fkP+/n5D//+3lv7+49b+/pZl//+XZf7+l2X+/plo///07/7+ybD+/n9E//9+Q/7+fkP+/n5D/v5/RP//fkP+/n5D/v5/RP//fkP+/raU/v7//////v7+/vPu/v6cb///59z+/v/////+/v7++vj+/qV7/v6DSv///Pv+/uXa/v6KVf///fz+/r+h/v69n////v7+/qiA/v5/RP//l2b+/v7+/v7//////v7+/qB1/v7Tv////v7+/v/////+/v7+xKj+/n9E///Yxv7+/v7+/o9c///m2/7+5dn+/qJ1///+/v7+0Lv+/n9E//9+Q/7+fkP+/n9E/v6ARv//gEb//4BG//+ARv//gEb//8Gk/////////////+XZ//+BR///hEv//9K9//////////////Xw//+dcP///////9bD//+cbv///////7yc///Irv///////7GN//+RXf//rof//////////////v3//4VM//+ARv//s5D///7+/////////v7//5tt///y6////Pv//4NJ///07///3c3//6qB////////0bz//4BG//+ARv//gEb//4BG//+CSP//gkj+/oJI/v6CSP//gkj+/s22/v7//////v7+/tnH/v6QXf//uJj+/u3l///+/v7+/v7+/vTv/v64l////v7+/seu/v6th////v7+/qV8/v7JsP///v7+/rqZ/v6ZaP//sIv+/v7+/v7/////9fD+/pBc/v6shv//39D+/v7+///+/v7+/v7+/qmA///+/v7+7+f+/oZN///+/f7+1cH+/rOO///+/v7+0r3+/oJI//+CSP7+gkj+/oJI/v6DSf//g0n+/oNJ/v6DSf//g0n+/tnI/v7//////v7+/vz7/v7+/v///v7+/v/////+/v7+5tr+/ppr/v7PuP///v7+/riY/v6/ov///v7+/ppr/v7Tvv///v7+/rmY/v6RXf//t5b+/v7+/v7//////v3+/v39/v7//////v7+/v/////z7f7+r4n+/qd////+/v7+4NH+/pVj///+/v7+zbX+/rua///+/v7+0r3+/oNJ//+CSP7+gkj+/oJI/v6DSv//g0r//4NK//+DSv//g0r//+fd/////////Pv///39///6+P//6+H//864//+kev//hEr//4NK///o3f///////6qC///LtP///////5Fd///czP///////6yF//+ESv//xqz////////8+////fz///z6///w6f//18X//7GN//+IUP//g0r//8Gk////////0bv//6R6////////xan//8Om////////0r7//4NK//+DSv//g0r//4NK//+FTP//hUz+/oVM/v6FTP//hUz+/vbz/v7/////so3+/ptr/v6FTP//hUz+/oVM//+HT/7+iFD+/olT/v78+////v7+/pxu/v7byv///v7+/ohR/v7m2v///v7+/qyG/v6FTP//1cL+/v7+/v7Bpf//hU3+/oVN/v6FTP//hUz+/oVM//+FTP7+h1D+/tvL///+/v7+wqb+/rSS///+/v7+vZ3+/suy///+/v7+077+/oVM//+FTP7+hUz+/oVM/v6GTv//hk7+/oZO/v6GTv//jVn+/v7+/v7/////qH3+/pxr/v6GTv//hk7+/ohR//+ba/7+nGz+/qBy/v7Ru///2Mb+/o1Y/v7q4P//9/P+/oZO/v7Cpv//zLX+/pxv/v6GTv//5dn+/v7+/v60kv//hk7+/oZO/v6GTv//h0/+/o5Z//+XZf7+nWz+/sit///Vwf7+qID+/sSo///+/v7+tpL+/ryb///Tv/7+s4/+/oZO//+GTv7+hk7+/oZO/v6HT///h0///4dP//+HT///nnH////////+/v//oHL//51u//+HT///h0///41X//+ebv//nm7//7KN//+/oP//waL//5Vj///59v//7eT//4dP//++n///so///5Vk//+HT///9fH///////+pgv//h1D//41Y//+VY///nG3//55u//+ebv//oHL//862//+0kf//kF3//9O/////////rob//76e//+6mf//qID//4dP//+HT///h0///4dP//+IUP//iFD+/ohQ/v6IUP//sIv+/v7+/v759v//nm/+/p5v/v6IUf//iFD+/ohR//+VYv7+nW7+/tC5/v7byv//7eX+/qV5/v7/////59z+/pJe/v708P//39D+/qR5/v6QXP///v7+/v7+/v6of///nW3+/p5v/v6eb///nm/+/p5v//+eb/7+sYz+/uTY///v6P7+mGj+/uLU///+/v7+pnv+/uLV///dzP7+ybD+/ohQ//+IUP7+iFD+/ohQ/v6KUv//iVL+/olS/v6JUv//wqX+/v7+/v7z7v//n3D+/p9w/v6LVP//iVL+/olS//+JUv7+i1T+/t/R/v7Yxv//4tT+/rKM/v7/////4NH+/qJ2/v7y7P//4tT+/qV7/v6id////v7+/v7+/v6pgP//n3D+/p9w/v6fcP//n3D+/ppp//+SX/7+upn+/tXB///7+f7+jVf+/vHq///9/P7+oHL+/urg///dzP7+yrH+/opS//+KUv7+ilL+/opS/v6LVP//i1T//4tU//+LVP//1MD////////v6P//oHL//6By//+NV///ilP//4pT//+KU///ilP//55w//+hdf//qYH//7WS////////18P//5Ri//+qgf//pnv//5Nf//+1kv////////////+cbf//nW7//5pp//+TYP//jVf//4tU//+LVP//lWP//51u//+1kv//jVf///38///28v//oHL//7iX//+shP//nnD//4tU//+LVP//i1T//4tU//+LVP//i1T+/otU/v6LVP//5tv+/v7+/v7t5P//oXT+/qF0/v6PWv//i1T+/otU//+LVP7+i1T+/otU/v6LVP//i1T+/r6f/v7/////xqz+/otU/v6LVP//i1T+/otU/v7Hrf///v7+/v7+/v6VY///i1T+/otU/v6LVP//i1T+/otU//+LVP7+i1T+/otU//+LVP7+mmr+/v/////u5/7+oXT+/qF0//+WZP7+i1T+/otU//+LVP7+i1T+/otU/v6MVv//jFb+/oxW/v6NV///+fb+/v7+/v7s4///oXX+/qF1/v6SXv//jFb+/oxW//+MVv7+jFb+/oxW/v6MVv//jFb+/s21/v7/////vZ7+/oxW/v6MVv//jFb+/oxW/v7byv///v7+/v7+/v6UYv//jFb+/oxW/v6MVv//jFb+/oxW//+MVv7+jFb+/oxW//+MVv7+qYD+/v/////n2/7+oXX+/qF1//+VY/7+jFb+/oxW//+MVv7+jFb+/oxW/v6NWP//jVj//41Y//+cbv/////////////s4///onb//6J2//+UYv//jVj//41Y//+NWP//jVj//41Y//+NWP//jVj//8y0///28v//tJH//41Y//+NWP//jVj//41Y///v5/////////////+WZf//jVj//41Y//+NWP//jVj//41Y//+NWP//jVj//41Y//+NWP//roj///Ls///ezv//onb//6J2//+UYv//jVj//41Y//+NWP//jVj//41Y//+OWf//jln+/o5Z/v6pgf///fz+/v7+/v7u5///onf+/qJ3/v6YaP//jln+/o5Z//+OWf7+jln+/o5Z/v6OWf//jln+/o5Z/v6OWf//j1r+/o5Z/v6OWf//jln+/pBd/v718P///v7+/v7+/v6Zaf//jln+/o5Z/v6OWf//jln+/o5Z//+OWf7+jln+/o5Z//+OWf7+jln+/pho//+jd/7+onf+/qJ3//+TYP7+jln+/o5Z//+OWf7+jln+/o5Z/v6PW///j1v//49b//+PW///mmv//8Gk///g0f//pHj//6R4//+idv//kl///5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+SX///so7//9rJ//+cbv//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kFz//5Bc//+QXP//kl///6J2//+keP//pHj//6N4//+RXf//j1v//49b//+PW///j1v//49b//+QXP//kFz+/pBc/v6QXP//kFz+/pBc/v6ecP//pXr+/qV6/v6lev//o3j+/pxt//+Zaf7+mGf+/pdl/v6VY///lGL+/pNg/v6SX///kl7+/pFe/v6RXf//kV3+/pFd/v6RXf//kV3+/pFd/v6RXf//kl7+/pJf/v6TYP//lGH+/pVj//+WZf7+mGf+/plp//+cbf7+o3f+/qV6//+lev7+pXr+/p5w//+QXP7+kFz+/pBc//+QXP7+kFz+/pBc/v6SXv//kl7+/pJe/v6SXv//kl7+/pJe/v6UYv//pHn+/qZ7/v6me///pnv+/qZ7//+me/7+pnv+/qZ7/v6me///pnv+/qZ7/v6me///pnv+/qZ7/v6me///pXr+/qV6/v6lev//pXr+/qV7/v6me///pnv+/qZ7/v6me///pnv+/qZ7//+me/7+pnv+/qZ7//+me/7+pnv+/qZ7//+me/7+pHn+/pRi//+SXv7+kl7+/pJe//+SXv7+kl7+/pJe/v6TYP//k2D//5Ng//+TYP//k2D//5Ng//+TYP//mGf//6V6//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+mfP//pnz//6Z8//+lev//mGf//5Ng//+TYP//k2D//5Ng//+TYP//k2D//5Ng//+UYf//lGH+/pRh/v6UYf//lGH+/pRh/v6UYf//lGH+/pZk/v6gcv//pnz+/qd+//+nfv7+p37+/qd+/v6nfv//p33+/qd9/v6nff//p33+/qd9/v6nff//p33+/qd9/v6nff//p37+/qd9/v6nff//p33+/qd9/v6nff//p33+/qd+//+nfv7+p37+/qd+//+nfv7+pn3+/qBz//+WZP7+k2D+/pRh//+TYP7+k2D+/pRh//+TYP7+k2D+/pNg/v6UYv//lGL+/pRi/v6UYv//lGL+/pRi/v6UYv//lGL+/pRi/v6UYv//lWL+/phm//+Zaf7+m2v+/pxt/v6db///pHn+/qd+/v6nfv//p37+/qd+/v6hdf//oXX+/qF1/v6idv//onb+/qJ2/v6nfv//p37+/qd+/v6nfv//o3j+/p5w//+cbv7+m2z+/ppq//+YZ/7+lWP+/pRi//+UYv7+lGL+/pRi//+UYv7+lGL+/pRi//+UYv7+lGL+/pRi/v6WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+aaf//qH///6h///+of///qH///6F0//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+idv//qH///6h///+of///p37//5lo//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+WZP//lmT//5Zk//+XZf/5l2X+/pdl/v6XZf//l2X+/pdl/v6XZf//l2X+/pdl/v6XZf//l2X+/pdl//+XZf7+l2X+/pdm/v6nff//qoH+/qqB/v6qgf//qH7+/phm/v6XZf//lmT+/pZk/v6XZf//lmT+/pZk/v6YZ///qH/+/qqB/v6qgf//qoH+/qZ7//+XZf7+l2X+/pdl//+XZf7+l2X+/pdl//+XZf7+l2X+/pdl//+XZf7+l2X+/pdl//+XZf7+l2X+/pdl/vmXZf/Ul2b+/pdm/v6XZv//l2b+/pdm/v6XZv//l2b+/pdm/v6XZv//l2b+/pdm//+XZv7+l2b+/p5v/v6rgv//q4L+/quC/v6rgv//nW7+/pdm/v6XZv//l2b+/pdm/v6XZv//l2b+/pdm/v6XZv//nnD+/quC/v6rgv//q4L+/quC//+cbf7+l2b+/pdm//+XZv7+l2b+/pdm//+XZv7+l2b+/pdm//+XZv7+l2b+/pdm//+XZv7+l2b+/pdl/tSVZfiSmWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5xs//+rgv//q4L//6uC//+jd///mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//6V5//+rgv//q4L//6qB//+ba///mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5lo//+ZaP//mWj//5dn/JJoRqwxmWj+/plo/v6aaf//mWj+/plo/v6aaf//mWj+/plo/v6aaf//mWj+/ppp//+ZaP7+mWj+/plo/v6fcP//pnv+/qR3/v6aaf//mWj+/plo/v6aaf//mWj+/plo/v6aaf//mWj+/plo/v6aaf//mWj+/ppq/v6keP//pnv+/p5v//+ZaP7+mWj+/ppp//+ZaP7+mWj+/ppp//+ZaP7+mWj+/ppp//+ZaP7+mWj+/ppp//+ZaP7+mWj+/m9LuDEAAAAAmWj9qJpp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp//+aaf7+mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp/v6aaf//mmn+/ppp//+aaf7+mmn+/ppp//+aaf7+mmn+/ppp//+aaf7+mmn+/ppp//+aaf7+mmn+/ppp//+aaf7+mmn+qAAAAAAAAAAAWT2RFJxr/+Cca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca///nGv//5xr//+ca//gYEKdFAAAAAAAAAAAAAAAAG9MtSSdbf/gnW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t//+dbf7+nW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t/v6dbf//nW3+/p1t//+dbf7+nW3+/p1t//+dbf7+nW3+/p1t//+dbf7+nW3+/p1t//+dbf7+nW3+/p1t/+B0UL4kAAAAAAAAAAAAAAAAAAAAAAAAAABcQJUUnW39qJ1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p5u//+dbf7+nW3+/p1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p1t/v6ebv//nW3+/p5u//+dbf7+nW3+/p5u//+dbf7+nW3+/p5u//+dbf7+nW3+/p5u//+dbf7+nW3+qGFEnRQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG9NszGcbfuSnm/+1J5v/vmeb///nm/+/p5v//+eb/7+nm/+/p5v/v6eb///nm/+/p5v/v6eb///nm/+/p5v/v6eb///nm/+/p5v/v6eb///nm/+/p5v/v6eb///nm/+/p5v/v6eb///nm/+/p5v//+eb/7+nm/+/p5v//+eb/7+nm/+/p5v//+eb/75nm/+1Jxt/JJyT7gxAAAAAAAAAAAAAAAAAAAAAAAAAAD4AAAAAB8AAOAAAAAABwAAwAAAAAADAACAAAAAAAEAAIAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAQAAgAAAAAABAADAAAAAAAMAAOAAAAAABwAA+AAAAAAfAAA=")
        with open(TEMP + "\\ballontip.ico", "wb") as f:
            f.write(ballontip)

        iconPathName = os.path.abspath(os.path.join( sys.path[0], TEMP + "\\ballontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(self.hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "bili-msg-helper")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                         (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                          hicon, "bili-msg-helper",msg,200,title))
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
            用户选择 = input ("输入1立即使用上次的配置，输入2则重新配置 [1/2] ")
            if 用户选择 == "1" or 用户选择 == "2": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环
        
        if 用户选择 == "1": # 使用上次的配置
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
    token = " "
    print ("是否将接收到的通知推送到您的手机？（现仅支持运行iOS/iPadOS的苹果设备）")
    while True: # 一直循环
        用户选择 = input ("输入1表示“是”，输入2表示“否” [1/2] ")
        if 用户选择 == "1" or 用户选择 == "2": # 用户的选择有效
            break # 跳出循环
        print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环

    if 用户选择 == "1":
        print("步骤1：打开APP Store，安装“Chanify”，完成后打开“Chanify”，允许通知，创建账号（点击即可创建，无需输入任何手机号的信息）\n步骤2：打开Safari浏览器，输入“chanify://action/token/default”并回车\n步骤3：跳转到“Chanify”后会自动复制token，将其粘贴于下方")
        token = input("请输入token：")
        while token == "":
            token = input("您没有输入内容，放弃设置推送到手机请输入1，或请输入token：")
            if token == "1":
                token = " "
                break
    with open (appdata + "\\bilimsghelperdata.txt", "at") as file:
        file.write (SESSDATA + "\n" + bili_jct + "\n" + token)
    main () # 跳转到主程序
    
    
def main (): # 主程序
    with open (appdata + "\\bilimsghelperdata.txt", "rt") as x:
        line = x.read ().splitlines () # 读取内容，并分割每行

    try: # 异常调试
        SESSDATA = line[0] # 读取第1行内容：Cookie（SESSDATA）
        bili_jct = line[1] # 读取第2行内容：Cookie（bili_jct）
        token = line[2] # 读取第3行内容：token

    except: # 如果读取配置文件异常，执行except内的操作
        fix ()
        return
        
    headers = {"Cookie": "SESSDATA=" + SESSDATA + "; bili_jct=" + bili_jct, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}

    # 获取API返回值（验证Cookie是否失效）  
    用户登录数据 = eval(requests.get ("https://api.bilibili.com/x/web-interface/nav", headers = headers).text) # 获取当前用户登录信息
    UID = str(用户登录数据.get("data").get("mid")) # 获取当前账号UID

    if 用户登录数据 ["code"] != 0: # 账号未登录（-101），请求错误（-400），或者是其他原因导致的失败
        print ("cookie已失效或填写不正确！")
        if os.path.exists (appdata + "\\bilimsghelperdata.txt"): # 如果配置存在
            os.remove (appdata + "\\bilimsghelperdata.txt") # 删除配置文件
        Cookie () # 重新输入Cookie
        return
        
    时间戳_短 = eval(requests.get("http://api.bilibili.com/x/report/click/now",headers=headers).text).get("data").get("now")
    时间戳_长 = str(时间戳_短 * 1000000)
    
    w.ShowWindow("开始运行","开始运行！")
    print ()

    while True: # 无条件一直循环
        消息列表数据 = eval(requests.get("https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts=" + 时间戳_长 + "&build=0&mobi_app=web",headers=headers).text) # 获取消息列表
        
        if 消息列表数据.get("code") != 0: # 如果“消息列表数据”的状态码不是“0”，报错
            print("错误：" + 消息列表数据.get("message"))
        
        if 用户登录数据.get("code") != 0: # 如果“用户登录数据”的状态码不是“0”，报错
            print("错误：" + 用户登录数据.get("message"))
            
        else:
            if 消息列表数据.get("data").get("session_list") != None: # 如果有新消息
                for i in range(len(消息列表数据.get("data").get("session_list"))):
                    tallker_id = str(消息列表数据.get("data").get("session_list")[i].get("talker_id")) # 获取消息发送者UID
                    私信聊天数据 = eval(requests.get("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?talker_id=" + tallker_id + "&session_type=1&size=20&build=0&mobi_app=web",headers=headers).text) # 获取私信聊天记录
                    # 获取“消息列表数据”和“私信聊天数据”后，获取当前时间戳，作为临时暂存变量，传递给新一轮的“时间戳_短”和“时间戳_长”
                    临时时间戳_短 = eval(requests.get("http://api.bilibili.com/x/report/click/now",headers=headers).text).get("data").get("now")
                    临时时间戳_长 = str(int(time.time() * 1000000)) # 获取当前时间戳，去除小数点
        
                    if 私信聊天数据.get("code") != 0: # 如果状态码不是“0”，报错
                        print("错误：" + 私信聊天数据.get("message"))

                    else:
                        新消息数 = 0
                        while 私信聊天数据.get("data").get("messages")[新消息数].get("timestamp") >= 时间戳_短:
                            新消息数 += 1
                            
                        for num in range(新消息数 -1,-1,-1):
                            sender_uid = str(私信聊天数据.get("data").get("messages")[num].get("sender_uid"))
                            sender_info = eval(requests.get("https://api.bilibili.com/x/space/acc/info?mid=" + sender_uid,headers=headers).text)           
                            if sender_info.get("code") != 0: # 如果“sender_info”的状态码不是“0”，报错
                                print("错误：" + sender_info.get("message"))
                            else:    
                                sender_name = str(sender_info.get("data").get("name"))
                                        
                                if (sender_uid == UID) or (int(私信聊天数据.get("data").get("messages")[num].get("timestamp")) < round(float(时间戳_短))) or (私信聊天数据.get("data").get("messages")[num].get("msg_key") in 已输出的消息): # 如果消息是当前账号发送的 或 消息时间戳小于本地时间戳 或msg_key存在于变量“已输出的消息”
                                    continue # 跳过本次循环，直接进行下一轮循环
                                else:
                                    if 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 1: # 纯文本
                                        content = str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("content","[未知]")) # 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                        
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 2: # 图片
                                        content = "[图片] " + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("url","[未知]")) # 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                    
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 5: # 撤回消息
                                        content = "撤回了一条消息"
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                        
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 6: # 自定义表情
                                        content = "[自定义表情] " + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("url","[未知]")) # 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                        
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 7: # 分享稿件（除了直播）
                                        if eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("source") == 2: # 相簿
                                            content = "分享了相簿 ID" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("id","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        elif eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("source") == 5: # 视频
                                            content = "分享了视频 av" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("id","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        elif eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("source") == 6: # 专栏
                                            content = "分享了专栏 cv" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("id","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        elif eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("source") == 16: # 番剧/纪录片
                                            content = "分享了" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("source_desc","[未知]")) + " ep" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("id","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        else:
                                            content = "分享了[未知内容]"
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                    
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 10: # 通知消息
                                        details = ""
                                        for details_num in range(len(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("modules"))):
                                            details = details + "                      " + eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("modules")[details_num].get("title") + "：" + eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("modules")[details_num].get("detail") + "\n"
                                        content = "[通知消息] 标题：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]")) + "\n           内容：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("text","[未知]")) + "\n           详细信息：\n" + details + "\n           " + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("jump_uri_config").get("text","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("jump_uri_config").get("all_uri","[未知]")) + "\n"
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：\n" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                        
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 11: # 发布视频
                                        content = "发布了视频 " + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("bvid","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                    
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 12: # 发布专栏
                                        content = "发布了专栏 cv" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("rid","[未知]")) + "：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]"))# 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                    
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 13: # 卡片消息（abnormal-card）
                                        content =  "[卡片消息] 标题：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]")) + "\n           图片：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("pic_url","[未知]")) + "\n           跳转链接：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("jump_url","[未知]")) # 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：\n" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text                                                                                                                                               
                                        
                                    elif 私信聊天数据.get("data").get("messages")[num].get("msg_type") == 14: # 分享直播
                                        content = "分享了" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("author","[未知]")) + "的直播：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("title","[未知]")) + "（链接：" + str(eval(私信聊天数据.get("data").get("messages")[num].get("content")).get("url","[未知]")).replace("\\","") + "）"# 获取消息
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text
                                    else:
                                        content = "未知类型"
                                        已输出的消息.append(私信聊天数据.get("data").get("messages")[num].get("msg_key"))
                                        消息时间戳 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(私信聊天数据.get("data").get("messages")[num].get("timestamp")))
                                        w.ShowWindow(sender_name + "（UID" + sender_uid + "）",content)
                                        print(("[" + 消息时间戳 + "] " + sender_name + "（UID" + sender_uid + "）：" + content).encode('gbk', 'replace').decode('gbk')) # 将无法解码的字符转换为“?”
                                        requests.post("https://api.chanify.net/v1/sender/" + token,data={'title':sender_name + "（UID" + sender_uid + "）",'text':content,'sound':1}).text

        try:
            时间戳_短 = 临时时间戳_短
            时间戳_长 = 临时时间戳_长
            del 临时时间戳_短,临时时间戳_长 # 删除变量
            
        except:
            时间戳_短 = eval(requests.get("http://api.bilibili.com/x/report/click/now",headers=headers).text).get("data").get("now")
            时间戳_长 = str(时间戳_短 * 1000000)
        
        time.sleep(5)
        
        
# 程序开始运行时，运行以下代码
while True: # 一直循环
    if isConnected () == true: # 网络是否连接正常
        check ()
    else:
        print ("无法连接到互联网，这会使任务无法完成！请检查网络是否正常！（按Enter键重试）")
        os.system ("pause >nul")
