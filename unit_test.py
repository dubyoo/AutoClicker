# -*- coding:utf-8 -*-
from game_control import *
from game_window import *
from game_image import *


def init_log():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s'
    )


def test_get_cursor_pos(hwnd=None):
    pos = (0, 0)
    while True:
        pos_new = get_cursor_pos(hwnd)
        if pos != pos_new:
            pos = pos_new
            logging.info(pos)
            sleep(500)


def test_move_window(hwnd):
    dump_window_info(hwnd)
    move_window(hwnd, 0, 0, 800, 600)
    dump_window_info(hwnd)


def test_screen_shot(hwnd):
    screen_shot(hwnd, (109, 225), (138, 258), 'images/arknights.bmp')


if __name__ == '__main__':
    init_log()
    hwnd = find_window('Qt5QWindowIcon', 'MuMu模拟器')
    # test_get_cursor_pos(hwnd)

    test_move_window(hwnd)
    sleep(500)

    # shake_window(hwnd)

    # img = screen_shot(hwnd, (109, 225), (138, 258))
    # show_img(img)

    # test_screen_shot(hwnd)

    max_val, max_loc, img_size = find_image(hwnd, 'images/arknights.bmp')
    logging.info('maxVal = %s, maxLoc = %s, img_size = %s' % (max_val, max_loc, img_size))
    click_bg(hwnd, (max_loc[0], max_loc[1]), (max_loc[0] + img_size[0], max_loc[1] + img_size[1]))
