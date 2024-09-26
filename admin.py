import sys
import json
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QComboBox, QHBoxLayout, QCheckBox, QScrollArea
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("관리자 프로그램")
        self.setGeometry(1200, 300, 575, 400)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(240, 240, 240))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.layout = QVBoxLayout()

        title_label = QLabel("회원 관리")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # member_id, name, phone_number, account_status, actions
        self.table.setHorizontalHeaderLabels(["선택", "ID", "이름", "전화번호", "상태"])
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; background-color: #f0f0f0;")

        self.scroll_area.setWidget(self.table)
        self.layout.addWidget(self.scroll_area)

        self.load_data()

        self.status_combo = QComboBox()
        self.status_combo.addItems(["정상", "일시정지", "차단"])
        self.layout.addWidget(self.status_combo)

        self.suspension_combo = QComboBox()
        self.suspension_combo.addItems(["7일", "15일", "30일", "무기한"])
        self.suspension_combo.setEnabled(False)
        self.layout.addWidget(self.suspension_combo)

        self.confirm_button = QPushButton("확인")
        self.confirm_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.confirm_button.clicked.connect(self.update_status)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)

        self.status_combo.currentIndexChanged.connect(self.update_date_edit_state)

    def load_data(self):
        response = requests.get("http://domain.com/CafeProject/cafe_user_list.php")
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        try:
            users = response.json()
            if 'error' in users:
                QMessageBox.critical(self, "Error", users['error'])
                return
        except requests.exceptions.JSONDecodeError:
            QMessageBox.critical(self, "Error", "서버 응답이 올바른 JSON 형식이 아닙니다.")
            return

        self.table.setRowCount(len(users))

        status_mapping = {
            "active": "정상",
            "suspended": "일시정지",
            "banned": "차단"
        }

        for row_idx, user in enumerate(reversed(users)):
            checkbox = QCheckBox()
            self.table.setCellWidget(row_idx, 0, checkbox)
            self.table.setItem(row_idx, 1, QTableWidgetItem(user['member_id']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(user['name']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(user['phone_number']))

            display_status = status_mapping.get(user['account_status'], user['account_status'])
            self.table.setItem(row_idx, 4, QTableWidgetItem(display_status))

            checkbox.stateChanged.connect(lambda state, idx=row_idx: self.select_user(idx, state))

    def select_user(self, row, state):
        current_status = self.table.item(row, 4).text()
        self.status_combo.setCurrentText(current_status)

        if state == Qt.Checked and current_status == '일시정지':
            self.suspension_combo.setEnabled(True)
        elif state == Qt.Unchecked:
            self.suspension_combo.setEnabled(False)

    def update_date_edit_state(self):
        if self.status_combo.currentText() == '일시정지':
            self.suspension_combo.setEnabled(True)
        else:
            self.suspension_combo.setEnabled(False)

    def update_status(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox.isChecked():
                member_id = self.table.item(row, 1).text()
                new_status = self.status_combo.currentText()

                if new_status == '일시정지':
                    selected_option = self.suspension_combo.currentText()
                    if selected_option != "무기한":
                        days = int(selected_option[:-1])
                        suspension_date = QDate.currentDate().addDays(days).toString("yyyy-MM-dd")
                    else:
                        suspension_date = None

                    data = {
                        'member_id': member_id,
                        'account_status': "suspended",
                        'suspension_end_date': suspension_date
                    }
                else:
                    data = {
                        'member_id': member_id,
                        'account_status': "active" if new_status == '정상' else "banned"
                    }

                response = requests.post("http://domain.com/CafeProject/update_user_status.php", data=data)
                if response.ok:
                    QMessageBox.information(self, "Success", f"{member_id}의 상태가 성공적으로 업데이트되었습니다!")
                else:
                    QMessageBox.warning(self, "Error", f"{member_id}의 상태 업데이트에 실패했습니다!\n서버 응답: {response.text}")

        self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
