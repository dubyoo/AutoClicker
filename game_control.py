# -*- coding:utf-8 -*-
import win32api
import win32gui
import win32con
import random
import time
import logging
from vk_code import VK_CODE


def sleep(sleep_time, variable_time=0):
    """
    随机睡眠一段时间，单位是 ms
    :param sleep_time: 睡眠时间
    :param variable_time: 如果不为 0，则睡眠从 sleep_time 到 sleep_time + variable_time 之间的随机时间
    """
    slp = random.randint(sleep_time, sleep_time + variable_time)
    time.sleep(slp / 1000)


def get_cursor_pos(hwnd=None):
    """
    获取鼠标坐标值
    :param hwnd: 窗口句柄，为空时返回屏幕坐标，不为空时返回窗口内坐标
    :return: pos = (x, y)
    """
    pos = win32api.GetCursorPos()
    if hwnd is not None:
        pos = win32gui.ScreenToClient(hwnd, pos)
    return pos


def set_cursor_pos(pos):
    """
    设置鼠标到目标位置
    :param pos: (x, y) 鼠标坐标
    """
    win32api.SetCursorPos(pos)


def click(pos, pos_end=None):
    """
    在屏幕指定区域内模拟鼠标点击（不支持后台）
    :param pos: (x, y) 鼠标点击的坐标
    :param pos_end: (x, y) 如果不为空，则点击从左上 pos 到右下 pos_end 区域内的随机坐标
    """
    x = pos[0] if pos_end is None else random.randint(pos[0], pos_end[0])
    y = pos[1] if pos_end is None else random.randint(pos[1], pos_end[1])
    logging.debug("click in position (%d, %d)" % (x, y))
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def click_bg(hwnd, pos, pos_end=None):
    """
    在窗口中指定区域内模拟鼠标点击（支持后台窗口）
    :param hwnd: 窗口句柄
    :param pos: (x, y) 鼠标点击的坐标
    :param pos_end: (x, y) 如果不为空，则点击从左上 pos 到右下 pos_end 区域内的随机坐标
    """
    x = pos[0] if pos_end is None else random.randint(pos[0], pos_end[0])
    y = pos[1] if pos_end is None else random.randint(pos[1], pos_end[1])
    long_position = win32api.MAKELONG(x, y)
    logging.debug("background click in position (%d, %d)" % (x, y))
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


def key_press(key):
    """
    模拟键盘按键
    :param key: 按键
    """
    logging.debug("key input %s" % key)
    win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


def key_press_bg(hwnd, key):
    """
    向窗口发送模拟键盘按键（支持后台窗口）
    :param hwnd: 窗口句柄
    :param key: 按键
    """
    logging.debug("background key input %s" % key)
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, VK_CODE[key], 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, VK_CODE[key], 0)

