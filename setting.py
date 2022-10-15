from PyQt5.QtWidgets import *
import sys

behav = ["Change legs",
         "Leg stretch(1)",
         "Leg stretch(2)",
         "Squat",
         "Leg raises (by each angle)",
         "Going up the stairs",
         "leg bend(1) (by each angle)",
         "leg bend(2) (by each angle)"]


class SettingApp(QDialog):
    def __init__(self):
        super().__init__()

        self.file_layout = QVBoxLayout()
        self.file_group = QGroupBox("file")

        # setting 창의 main layout
        self.layout = QVBoxLayout(self)

        #설정을 완료하게 되면 해당 변수의 값이 전달
        self.address = []
        self.experiment_title = "Change legs"
        self.line = False
        self.time = 45
        self.setting_time = False
        self.startTime = 0
        self.endTime = 0

        self.initUI()

    def initUI(self):
        self.get_file()
        self.select_experiment()
        self.set_time()
        self.set_line()
        self.buttons()

        self.center()
        self.setWindowTitle('Setting')
        # self.show()

    # 파일 주소값과 이에 대한 라벨을 출력하는 함수
    def get_file(self):
        self.layout.addStretch(1)

        fileBtn = QPushButton('open')
        fileBtn.clicked.connect(self.open_file)

        self.file_layout.addWidget(fileBtn)

        self.file_group.setLayout(self.file_layout)
        self.layout.addWidget(self.file_group)

    def file_block(self, address):
        block = QGroupBox()
        block.setStyleSheet("QGroupBox{border:0;}")

        layout = QGridLayout()

        address_lb = QLabel(address)
        button = QPushButton("-")
        button.clicked.connect(self.deleteAddress)

        layout.addWidget(address_lb, 0, 0, 1, 7)
        layout.addWidget(button, 0, 8, 1, 1)

        block.setLayout(layout)
        return block

    def deleteAddress(self):
        group = self.sender().parent()
        self.address.pop(group.parent().children().index(group)-2)
        group.deleteLater()
        print(self.address, len(self.address))

    # 맨 아래의 확인과 취소 버튼
    def buttons(self):
        self.layout.addStretch(1)
        buttons_layout = QGridLayout(self)

        btnOK = QPushButton("확인")
        btnCancel = QPushButton("취소")

        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel.clicked.connect(self.onCancelButtonClicked)

        buttons_layout.addWidget(btnOK)
        buttons_layout.addWidget(btnCancel)
        self.layout.addLayout(buttons_layout)

    # 시작과 끝 시간 설정
    def set_start_time(self, time):
        self.startTime = time

    def set_end_time(self, time):
        self.endTime = time

    # 시간 설정에 관한 위젯
    def set_time(self):
        self.layout.addStretch(1)
        self.time_group = QGroupBox("set time")
        self.time_group.setCheckable(True)
        self.time_group.setChecked(False)
        self.time_group.toggled.connect(self.check_group)

        time_layout = QHBoxLayout(self)

        start_layout = QVBoxLayout(self)
        start_label = QLabel("start time")
        self.start_input = QLineEdit(self)
        self.start_input.textChanged[str].connect(self.set_start_time)
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_input)
        time_layout.addLayout(start_layout)

        time_layout.addStretch(1)
        time_layout.addWidget(QLabel("~"))

        time_layout.addStretch(1)
        end_layout = QVBoxLayout(self)
        end_label = QLabel("end time")
        self.end_input = QLineEdit(self)
        self.end_input.textChanged[str].connect(self.set_end_time)
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.end_input)
        time_layout.addLayout(end_layout)

        self.time_group.setLayout(time_layout)
        self.layout.addWidget(self.time_group)

    # (시작 ~ 끝) 시간을 사용 할 것 인지에 대한 체크박스의 이벤트 함수
    def check_group(self):
        self.setting_time = self.time_group.isChecked()

    # 그래프에 사각형을 그릴지에 대한 체크 박스 이벤트 함수
    def check(self):
        checkBox = self.sender()
        self.line = checkBox.isChecked()

    # 그래프에 사각형을 그릴 지에 대한 체크박스 위젯
    def set_line(self):
        self.layout.addStretch(1)
        set_line_layout = QGridLayout(self)
        set_line_check = QCheckBox("set Line")
        set_line_check.stateChanged.connect(self.check)
        set_line_layout.addWidget(set_line_check)
        self.layout.addLayout(set_line_layout)

    # 실험 선택 위젯
    def select_experiment(self):
        self.layout.addStretch(1)
        radio_layout = QGridLayout(self)
        experiment_group = QGroupBox("select experiment")
        self.time_lb = QLabel(f'experiment time: {self.time}')
        self.btn1 = QRadioButton(behav[0])
        self.btn1.setChecked(True)
        self.btn2 = QRadioButton(behav[1])
        self.btn3 = QRadioButton(behav[2])
        self.btn4 = QRadioButton(behav[3])
        self.btn5 = QRadioButton(behav[4])
        self.btn6 = QRadioButton(behav[5])
        self.btn7 = QRadioButton(behav[6])
        self.btn8 = QRadioButton(behav[7])

        self.btn1.toggled.connect(self.onClicked)
        self.btn2.toggled.connect(self.onClicked)
        self.btn3.toggled.connect(self.onClicked)
        self.btn4.toggled.connect(self.onClicked)
        self.btn5.toggled.connect(self.onClicked)
        self.btn6.toggled.connect(self.onClicked)
        self.btn7.toggled.connect(self.onClicked)
        self.btn8.toggled.connect(self.onClicked)

        radio_layout.addWidget(self.btn1, 1, 0, 1, 1)
        radio_layout.addWidget(self.btn2, 1, 1, 1, 1)
        radio_layout.addWidget(self.btn3, 2, 0, 1, 1)
        radio_layout.addWidget(self.btn4, 2, 1, 1, 1)
        radio_layout.addWidget(self.btn5, 3, 0, 1, 1)
        radio_layout.addWidget(self.btn6, 3, 1, 1, 1)
        radio_layout.addWidget(self.btn7, 4, 0, 1, 1)
        radio_layout.addWidget(self.btn8, 4, 1, 1, 1)
        radio_layout.addWidget(self.time_lb, 5, 0, 1, 1)

        experiment_group.setLayout(radio_layout)
        self.layout.addWidget(experiment_group)

    # 각 실험의 라디오 버튼이 눌릴때 발생하는 이벤트 함수
    def onClicked(self):
        radioBtn = self.sender()
        # 각 실험 당 시간
        times = [45, 21, 20, 21, 45, 20, 35, 56]
        if radioBtn.isChecked():
            self.experiment_title = radioBtn.text()
            self.time = times[behav.index(radioBtn.text())]
            self.time_lb.setText(f'experiment time: {self.time}')

    # 파일 버튼에 대한 이벤트 함수
    def open_file(self):
        fname = QFileDialog.getOpenFileName(self)
        self.address.append(fname[0])
        self.file_layout.addWidget(self.file_block(fname[0]))
        print(self.address)

    # 맨 아래의 확인 버튼을 누를 때 이벤트 함수
    def onOKButtonClicked(self):
        time_str = ''
        if self.setting_time:
            time_str = f'start time : {self.startTime} ~ end time {self.endTime}\n'
        else:
            time_str = ''
        reply = QMessageBox.question(self, 'Message', f'your experiment : {self.experiment_title}\n'
                                                      f'experiment time : {self.time}\n' + time_str +
                                     f'set line = {self.line}',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        self.startTime = int(self.startTime)
        self.endTime = int(self.endTime)
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            return

    # 취소 버튼에 대한 이벤트 함수
    def onCancelButtonClicked(self):
        self.reject()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showModal(self):
        return super().exec_()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SettingApp()
#     sys.exit(app.exec_())
