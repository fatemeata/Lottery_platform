# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comp2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import Res1_rc  # image of post which wanted to do the process
import sys
import qdarkstyle
import os
import instaloader
import pandas as pd
from collections import Counter
from itertools import islice
import numpy as np
import random
import time
import csv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QFile
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi


class ProcessThread(QThread):
    def __init__(self, UI):
        QThread.__init__(self)
        self.UI = UI

    def __del__(self):
        self.wait()

    def stop(self):
        self.terminate()

    def strat(self):
        print("START!!!!!!!!!")


def get_data():
    window.PT = ProcessThread(window)
    show_data(window)
    window.PT.start()
    # window.run.setText("قرعه کشی مجدد")
    # window.PT.finished.connect(done)
    # window.run.clicked.disconnect(get_data)
    # window.run.clicked.connect(window.PT.stop)
    # process()


def select_winners():
    first, second, third = process()
    first = "1. نفر اول:  @" + first
    second = "2. نفر دوم:  @" + second
    third = "3. نفر سوم:  @" + third
    first = '<span style=\" margin-top: 10 px;\">%s</span>' % first
    window.winners_log.setStyleSheet("QTextBrowser { padding-left:10; padding-top:10; "
                                     "padding-bottom:10; padding-right:10}")
    window.winners_log.append(first)
    window.winners_log.append(second)
    window.winners_log.append(third)

    window.run.clicked.disconnect(select_winners)


def hide_data(window):
    window.Main_widget.setVisible(False)


def show_data(window):
    window.Main_widget.setVisible(True)
    window.comment_text.setText("3134")
    window.like_text.setText("552")


def process():
    comment_file = "D:/final_comments.csv"
    like_file = "D:/likes_finals.txt"

    data_comments = read_comments_file(comment_file)
    data_likes = read_list_of_likes(like_file)

    data_sh = shuffle_data(data_comments)
    data_wdup = drop_duplicate(data_sh)
    data_final = drop_more_than_one_tagged(data_wdup)
    first_winner, data_wfirst = get_winner(data_final, data_likes)
    print("First Winner: ", first_winner)
    second_winner, data_wsecond = get_winner(data_wfirst, data_likes)
    print("Second Winner: ", second_winner)
    third_winner, data_wthird = get_winner(data_wsecond, data_likes)
    print("Third Winner: ", third_winner)
    return first_winner, second_winner, third_winner


def login(USER, PASSWORD):
    L = instaloader.Instaloader()
    L.login(USER, PASSWORD)


def read_comments_file(file):
    return (pd.read_csv(file, engine='python'))  # raw data


def read_list_of_likes(file):
    with open(file, 'r') as f:
        x = f.read().splitlines()
    return x


def shuffle_data(data):
    return (data.sample(frac=1).reset_index(drop=True))


def drop_duplicate(data):
    return (data.drop_duplicates(subset=['comment_owner', 'comment_text']).reset_index(drop=True))


def drop_more_than_one_tagged(data):
    for index, row in data.iterrows():  # delete comments with more than one @
        counts = Counter(row['comment_text'])
        if (counts['@'] > 1):
            data = data.drop([index])
    return data.reset_index(drop=True)


def get_winner(data, liked_list):  ##TODO: check the winner liked the post
    random_num = generate_random_number(len(data))
    winner = data['comment_owner'].loc[random_num]

    if winner in liked_list:
        # print("1. First data shape: ", data.shape)
        for index, row in data.iterrows():
            if (row['comment_owner'] == winner):
                data = data.drop([index])
        data = data.reset_index(drop=True)
    # print("2. Second data shape: ", data.shape)
    else:
        for index, row in data.iterrows():
            if row['comment_owner'] == winner:
                data = data.drop([index])
        data = data.reset_index(drop=True)
        get_winner(data, liked_list)
    return winner, data


def generate_random_number(limit):
    return random.randint(0, limit)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def setupWindow(window):
    # connect signals and slots in here
    hide_data(window)
    window.start.clicked.connect(get_data)
    window.run.clicked.connect(select_winners)
    app_icon = QIcon(resource_path("Logo.png"))
    window.setWindowIcon(app_icon)
    # window.second_run.clicked.connect(select_second_Winner)
    # window.third_run.clicked.connect(select_third_Winner)
    # print(window.comp_image.isVisible())
    value = window.Main_widget.isVisible()
    print(value)


if __name__ == "__main__":
    print("START PROGRAM!")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())
    ui_file = QFile("comp3.ui")
    ui_file.open(QFile.ReadOnly)
    window = loadUi(ui_file)

    ui_file.close()
    setupWindow(window)
    window.show()

    sys.exit(app.exec_())
