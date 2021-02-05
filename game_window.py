# -*- coding:utf-8 -*-
import win32gui
import win32con
import time
import random
import logging


def find_window(wnd_class, wnd_title):
    """
    查找窗口
    :param wnd_class: 窗口类名
    :param wnd_title: 窗口标题
    :return: 窗口句柄
    """
    hwnd = win32gui.FindWindow(wnd_class, wnd_title)
    return hwnd


def find_window_list(title):
    """
    获取指定标题名的窗口句柄
    :param title: 窗口标题
    :return: 窗口句柄列表
    """
    hwnd_list = list()
    ret_list = list()
    win32gui.EnumWindows(_enum_window_callback, hwnd_list)
    for hwnd in hwnd_list:
        if win32gui.GetWindowText(hwnd) == title:
            ret_list.append(hwnd)
    return ret_list


def _enum_window_callback(hwnd, hwnd_list):
    if win32gui.IsWindow(hwnd) \
            and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd):
        hwnd_list.append(hwnd)


def dump_window_info(hwnd):
    """
    打印指定窗口的详细信息
    :param hwnd: 窗口句柄
    """
    title = win32gui.GetWindowText(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    pos = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
    logging.info('hwnd: %s, title: %s, pos: %s, client_rect: %s' % (hwnd, title, pos, client_rect))


def shake_window(hwnd):
    """
    抖动窗口
    :param hwnd: 窗口句柄
    """
    x, y, w, h = win32gui.GetWindowRect(hwnd)
    for i in range(3):
        win32gui.SetWindowPos(
            hwnd, None, x + random.randint(-5, 5), y - random.randint(-5, 5), 0, 0,
            win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)  # 实现更改当前窗口位置
        time.sleep(0.1)
        win32gui.SetWindowPos(
            hwnd, None, x, y, 0, 0,
            win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)  # 将窗口恢复至初始位置
        time.sleep(0.1)


def move_window(hwnd, x, y, w, h):
    """
    移动并窗口并重设窗口大小
    :param hwnd: 窗口句柄
    :param x: 窗口起始坐标 x
    :param y: 窗口起始坐标 y
    :param w: 窗口宽
    :param h: 窗口高
    :return:
    """
    win32gui.MoveWindow(hwnd, x, y, w, h, True)

