import win32ui
import win32gui
import win32con
import numpy
import cv2
import traceback
import logging


def screen_shot(hwnd, pos_lt=None, pos_rb=None, file_name=None):
    """
    在窗口指定区域内截图（支持后台窗口）
        :param hwnd: 窗口句柄
        :param pos_lt: (x,y) 截图区域的左上角坐标, 若为 None 则截取整个窗口
        :param pos_rb: (x,y) 截图区域的右下角坐标, 若为 None 则截取整个窗口
        :param file_name: 截图文件的保存路径
        :return: 若 file_name 为空则返回 RGB 数据
    """
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    client_pos = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
    client_to_window_x = client_pos[0] - window_rect[0]
    client_to_window_y = client_pos[1] - window_rect[1]
    if pos_lt is None or pos_rb is None:
        pos_lt = (0, 0)
        pos_rb = (client_rect[2], client_rect[3])
    w = pos_rb[0] - pos_lt[0]
    h = pos_rb[1] - pos_lt[1]
    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, w, h)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (w, h), srcdc,
                 (pos_lt[0] + client_to_window_x, pos_lt[1] + client_to_window_y),
                 win32con.SRCCOPY)
    if file_name is not None:
        bmp.SaveBitmapFile(memdc, file_name)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return
    else:
        signedIntsArray = bmp.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def compare_image(img_template, img_cmp):
    """
    查找图片（在待比较图中查找模板图）
        :param img_template: 模板图片
        :param img_cmp: 待比较图片
        :return: (max_val, max_loc) max_val为相关性，越接近1越好，max_loc为得到的坐标
    """
    try:
        res = cv2.matchTemplate(img_template, img_cmp, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val, max_loc
    except Exception:
        logging.warning('compare_image failed')
        logging.warning(traceback.format_exc())
        return 0, 0


def find_image(hwnd, img_template_path, pos_lt=None, pos_rb=None):
    """
    在窗口中找图
        :param hwnd: 窗口句柄
        :param img_template_path: 模板图片文件路径
        :param pos_lt: 截图区域的左上角坐标, 若为 None 则截取整个窗口
        :param pos_rb: 截图区域的右下角坐标, 若为 None 则截取整个窗口
        :return: (max_val, max_loc, img_size)
                max_val: 为相关性，越接近1越好
                max_loc: (x, y) 为得到的坐标
                img_size: (w, h) 模板图片尺寸
    """
    img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
    img_cmp = screen_shot(hwnd, pos_lt, pos_rb)
    _, w, h = img_template.shape[::-1]
    img_size = (w, h)
    max_val, max_loc = compare_image(img_template, img_cmp)
    return max_val, max_loc, img_size


def show_img(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
