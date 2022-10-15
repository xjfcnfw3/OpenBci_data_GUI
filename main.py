import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, freqz
from setting import SettingApp


# 데이터 전처리 부분
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs  # 나이트퀴스트 주파수 계산
    normal_cutoff = cutoff / nyq  # 디자인 필터
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a  # 필터 계수를 반환(분자와 분모)


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 250.0  # sample rate(샘플링 속도)
cutoff = 5  # 필터의 차단 주파수(Hz)
df = None


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 현재 저장되어 있는 정보
        self.setting_time = False  # 주어진 시간(시작 ~ 끝)을 사용할 지 나타 내는 변수
        self.line = False  # 그래프에 주어진 시간과 그 시간 동안 최대 최소 값으로 사각형을 그릴 것인지를 나타내는 변수
        self.endTime = 0  # 끝
        self.startTime = 0  # 시작
        self.time = None  # 실험 최대 시간 ex)스쿼트 30초
        self.experiment_title = None  # 실험 제목
        self.address = []  # csv 파일 주소

        self.layout = QGridLayout(self)
        self.toolbar = QGridLayout(self)
        self.status = QWidget()
        self.status.setStyleSheet("background-color: white;")

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        self.layout.addLayout(self.toolbar, 0, 0, 1, 3)
        self.layout.addWidget(self.canvas, 1, 0, 2, 3)
        self.layout.addWidget(self.status, 3, 0, 1, 3)

        self.initStatus(self.status)
        self.initUI()

    def initUI(self):
        self.file()
        self.information()

        self.setWindowTitle('openBci_gui')
        self.resize(2500, 1500)
        self.center()
        self.show()

    # 파일 관련 창 입니다. (open 다이어 그램 버튼, 주소)
    def file(self):
        btn_file = QPushButton('open', self)
        btn_file.clicked.connect(self.open_file)
        self.address_lb = QLabel("open")
        self.toolbar.addWidget(btn_file, 0, 0, 0, 1)
        self.toolbar.addWidget(self.address_lb, 0, 1, 0, 2)

    # 파일을 열고 실험 정보를 setting 창을 불러 오고 그에 대한 정보를 받는 함수
    def open_file(self):
        win = SettingApp()
        r = win.showModal()
        if r:
            print(win.address, "ok")
            self.setter(win.address, win.experiment_title, win.time, win.startTime, win.endTime, win.setting_time,
                        win.line)
            # df = pd.read_csv(self.address, header=None)
            df = self.set_df()
            self.draw(df)

    def setter(self, address, experiment_title, time, startTime, endTime, setting_time, line):
        self.address = address
        self.experiment_title = experiment_title
        self.time = time
        self.startTime = startTime
        self.endTime = endTime
        self.setting_time = setting_time
        self.line = line
        self.setInformation(address[0], experiment_title, time, startTime, endTime)

    # 입력된 정보를 바탕으로 정보 창을 수정
    def setInformation(self, address, experiment_title, time, startTime, endTime):
        self.address_lb.setText(address)
        self.title_lb.setText(f'experiment_title : {experiment_title}')
        self.time_lb.setText(f'time : {time}')
        self.start_input.setText(str(startTime))
        self.end_input.setText(str(endTime))

    # 선택한 실험에 대한 정보 출력.
    def information(self):
        # layout, groupBox make
        information_group = QGroupBox(self)
        information_Box = QGridLayout(self)
        # 각종 정보 위젯
        start_lb = QLabel("Start")
        end_lb = QLabel("End")
        self.title_lb = QLabel("experiment")
        self.time_lb = QLabel("Time")
        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        redraw_btn = QPushButton("redraw")
        redraw_btn.clicked.connect(self.redraw)
        # 위젯 추가
        information_Box.addWidget(self.title_lb, 0, 0)
        information_Box.addWidget(self.time_lb, 0, 1)
        information_Box.addWidget(start_lb, 0, 2)
        information_Box.addWidget(self.start_input, 0, 3)
        information_Box.addWidget(QLabel('~'), 0, 4)
        information_Box.addWidget(end_lb, 0, 5)
        information_Box.addWidget(self.end_input, 0, 6)
        information_Box.addWidget(redraw_btn, 0, 7)

        information_group.setLayout(information_Box)
        self.toolbar.addWidget(information_group, 0, 4, 0, 5)

    # 전달 받은 변수로 상태 창을 그리는 함수
    def setStatus(self, i, min_data, max_data):
        min_lb = QLabel(f'Min: {min_data}')
        max_lb = QLabel(f"Max: {max_data}")
        subtract_lb = QLabel(f'Subtract: {max_data - min_data}')

        min_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
        max_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
        subtract_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))

        self.channels[i].addWidget(max_lb, 1, 0)
        self.channels[i].addWidget(min_lb, 2, 0)
        self.channels[i].addWidget(subtract_lb, 3, 0)

    # 맨 아래의 상태 창을 초기화 하는 함수
    def initStatus(self, status):
        status.layout = QGridLayout(status)
        status.layout.setContentsMargins(0, 0, 0, 0)

        channel1 = QGridLayout(status)
        channel2 = QGridLayout(status)
        channel3 = QGridLayout(status)
        channel4 = QGridLayout(status)
        channel5 = QGridLayout(status)
        channel6 = QGridLayout(status)
        channel7 = QGridLayout(status)
        channel8 = QGridLayout(status)

        self.channels = [channel1, channel2, channel3, channel4, channel5, channel6, channel7, channel8]
        for channel in self.channels:
            group = QGroupBox()
            label = QLabel(f'channel{self.channels.index(channel) + 1}')
            min_lb = QLabel("Min")
            max_lb = QLabel("Max")
            subtract_lb = QLabel("Subtract")

            group.setStyleSheet("QGroupBox{border: 5px solid black;}")
            label.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
            min_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
            max_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
            subtract_lb.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))

            channel.addWidget(label, 0, 0)
            channel.addWidget(max_lb, 1, 0)
            channel.addWidget(min_lb, 2, 0)
            channel.addWidget(subtract_lb, 3, 0)

            group.setLayout(channel)
            index = self.channels.index(channel)
            status.layout.addWidget(group, index//4, index%4)

    def redraw(self):
        self.startTime = int(self.start_input.text())
        self.endTime = int(self.end_input.text())
        df = self.set_df()
        self.draw(df)

    # 창을 화면 중앙에 배치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def draw_plot(self, i, ch):
        # 이렇게 작성하면 그래프가 작게나와 주석 처리함
        # if i > 4:
        #     idx = i + 4
        # else:
        #     idx = i
        idx = i
        self.draw_lowpass_plot(ch, idx)

    # 초당 250 인덱스가 출력
    def draw_lowpass_plot(self, ch, idx):
        # Demonstrate the use of the filter.
        # First make some data to be filtered.
        T = 5.0  # seconds
        n = int(T * fs)  # total number of samples
        t = np.linspace(0, T, n, endpoint=False)
        # Filter the data, and plot both the original and filtered signals.
        y = butter_lowpass_filter(ch, cutoff, fs, order)

        if self.setting_time:
            startTime = self.startTime * 250
            endTime = self.endTime * 250
            min_data = round(min(y[startTime: endTime]), 3)
            max_data = round(max(y[startTime: endTime]), 3)
            # if idx > 4:
            #     self.setStatus(idx - 5, min_data, max_data)
            # else:
            #     self.setStatus(idx - 1, min_data, max_data)
            self.setStatus(idx - 1, min_data, max_data)

        # ax = plt.subplot(4, 4, idx+4)
        plt.subplot(2, 4, idx)
        plt.plot(y, 'g-', linewidth=2, label='filtered data')

        max_time = 250 * self.time
        y_max = max(y[500:max_time])
        y_min = min(y[500:max_time])

        if self.setting_time and self.line:
            startTime = self.startTime * 250
            endTime = self.endTime * 250
            # min_data = min(y[startTime: endTime])
            # max_data = max(y[startTime: endTime])
            # ax.add_patch(
            #     patches.Rectangle(
            #         (startTime, min_data),  # (x, y) coordinates of left-bottom corner point
            #         endTime - startTime, max_data - min_data,  # width, height
            #         edgecolor='red',
            #         fill=False
            #     ))
            plt.vlines(startTime, y_min, y_max, color="red", linewidth=2)
            plt.vlines(endTime, y_min, y_max, color="red", linewidth=2)
            font = {'family': 'Arial',
                     'color': 'blue',
                     'style': 'italic',
                     'size': 14}
            plt.text(startTime, y_max - (y_max - y_min) * 0.1, str(self.startTime)+'s', fontdict=font)
            plt.text(endTime, y_max - (y_max - y_min) * 0.1, str(self.endTime)+'s', fontdict=font)
        #############################################
        plt.title("Original data")
        plt.title("Lowpass Filter data")
        plt.grid()

        plt.plot([1, 2, 4], 'g-', linewidth=2)
        plt.xlim(100, max_time)

        plt.ylim(y_min, y_max)

    # 여기서 위젯에 그리기 위한 코드를 추가 했습니다.
    def draw(self, df):
        self.fig = plt.figure()
        plt.subplots_adjust(hspace=0.3, wspace=0.35)
        print(df)
        for i in range(8):
            ch = df[i]
            self.draw_plot(i + 1, ch)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas, 1, 0, 2, 3)

    def set_df(self):
        sub_df = pd.read_csv(self.address[0], header=None)
        sub_df = sub_df[:250 * self.time]
        df = sub_df
        for file in self.address[1:]:
            sub_df = pd.read_csv(file, header=None)
            sub_df = sub_df[:250 * self.time]
            df += sub_df
        df /= len(self.address)
        return df


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
