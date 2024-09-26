import sys
import json
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class User:
    def __init__(self, member_id, member_password, name, phone_number):
        self.member_id = member_id
        self.member_password = member_password
        self.name = name
        self.phone_number = phone_number


class Auth:
    @staticmethod
    def send_request(url, data):
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"HTTP 요청 중 오류 발생: {e}"}

    @staticmethod
    def signup(user):
        data = {
            'member_id': user.member_id,
            'member_password': user.member_password,
            'name': user.name,
            'phone_number': user.phone_number
        }

        return Auth.send_request("http://domain.com/CafeProject/cafe_signup.php", data)

    @staticmethod
    def login(member_id, member_password):
        data = {
            'member_id': member_id,
            'member_password': member_password
        }
        response = Auth.send_request("http://jdomain.com/CafeProject/cafe_login.php", data)

        if 'error' in response:
            return response['error']

        if response.get('status') == 'success':
            account_status = response.get('account_status')
            if account_status == 'banned':
                return "로그인 실패: 계정이 차단되었습니다. \n\n관리자 문의 010-1111-1111"
            elif account_status == 'suspended':
                suspension_end_date = response.get('suspension_end_date')
                suspension_end_date_formatted = suspension_end_date.split(' ')[0]
                return f"로그인 실패: 계정이 일시정지 상태입니다. \n\n해지일: {suspension_end_date_formatted}"
            else:
                return "로그인 성공!"
        else:
            return "로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다."


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("회원 프로그램")
        self.setGeometry(1200, 300, 300, 200)
        self.layout = QVBoxLayout()
        title_label = QLabel("스터디카페 시스템")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        self.login_button = QPushButton("로그인")
        self.login_button.setFont(QFont("Arial", 14))
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 10px;")
        self.login_button.clicked.connect(self.show_login)

        self.signup_button = QPushButton("회원가입")
        self.signup_button.setFont(QFont("Arial", 14))
        self.signup_button.setStyleSheet("background-color: #2196F3; color: white; border: none; border-radius: 5px; padding: 10px;")
        self.signup_button.clicked.connect(self.show_signup)

        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)

        self.login_view = None
        self.signup_view = None
        self.menu_view = None
        self.member_id = None


    def show_login(self):
        if self.login_view is None:
            self.login_view = LoginView(self)
        self.login_view.show()
        self.hide()

    def show_signup(self):
        if self.signup_view is None:
            self.signup_view = SignupView(self)
        self.signup_view.show()
        self.hide()

    def show_menu(self):
        if self.menu_view is None:
            self.menu_view = MenuView(self)
        self.menu_view.show()
        self.hide()


class LoginView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("로그인")
        self.setGeometry(1200, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("아이디:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("비밀번호:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("로그인")
        self.back_button = QPushButton("뒤로가기")
        self.back_button.clicked.connect(self.go_back)
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def go_back(self):
        self.parent.show()
        self.close()

    def login(self):
        member_id = self.username_input.text()
        member_password = self.password_input.text()

        response = Auth.login(member_id, member_password)

        if response.strip() == "로그인 성공!":
            QMessageBox.information(self, "Login", "로그인 성공!", QMessageBox.Ok)

            self.parent.member_id = member_id
            self.parent.show_menu()
            self.close()
        else:
            QMessageBox.warning(self, "Login", response)


class SignupView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("회원가입")
        self.setGeometry(1200, 300, 300, 300)

        layout = QVBoxLayout()

        self.username_label = QLabel("아이디:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("비밀번호:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.name_label = QLabel("이름:")
        self.name_input = QLineEdit()
        self.phone_label = QLabel("전화번호:")
        self.phone_input = QLineEdit()

        self.signup_button = QPushButton("회원가입")
        self.back_button = QPushButton("뒤로가기")
        self.back_button.clicked.connect(self.go_back)
        self.signup_button.clicked.connect(self.signup)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def go_back(self):
        self.parent.show()
        self.close()

    def signup(self):
        member_id = self.username_input.text()
        member_password = self.password_input.text()
        name = self.name_input.text()
        phone_number = self.phone_input.text()

        user = User(member_id, member_password, name, phone_number)
        response = Auth.signup(user)

        if response.get('status') == 'success':
            QMessageBox.information(self, "Sign Up", "회원가입 성공!")
            self.parent.show()
            self.close()  
        else:
            QMessageBox.warning(self, "Sign Up", response.get('error', '회원가입 실패\n\n해당 아이디가 중복 사용중 입니다.'))

####################################################################################################

class MenuView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("메인화면")
        self.setGeometry(1200, 300, 300, 300)

        layout = QVBoxLayout()

        self.label = QLabel("관리자 공지사항 : 자리 비울때 퇴실 부탁드립니다.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.seat_button = QPushButton("좌석 예약하기")
        self.seat_button.clicked.connect(self.show_seat_app)
        layout.addWidget(self.seat_button)

        self.exit_button = QPushButton("퇴실하기")
        self.exit_button.clicked.connect(self.exit_cafe)
        layout.addWidget(self.exit_button)

        self.back_button = QPushButton("로그아웃")
        self.back_button.clicked.connect(self.logout)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def show_seat_app(self):
        self.seat_app = SeatApp(self.parent.member_id)
        self.seat_app.show()

    def exit_cafe(self):
        response = QMessageBox.question(
            self,
            "퇴실 확인",
            "퇴실하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if response == QMessageBox.Yes:
            #사용자의 좌석 정보 가져오기
            response = requests.get('http://domain.com/CafeProject/seat.php')
            seat_data = json.loads(response.text)  # JSON 파싱

            #사용자의 예약 좌석 찾기
            user_seat = None
            for seat in seat_data:
                if seat['user_id'] == self.parent.member_id and seat['status'] == 'true':
                    user_seat = seat
                    break

            if user_seat:
                #퇴실 업데이트
                data = {
                    'id': user_seat['id'],
                    'status': 'false',
                    'scheduled_end_time': 'null',
                }

                #퇴실
                try:
                    update_response = requests.post('http://domain.com/CafeProject/update_seat.php',
                                                    data=data)
                    update_response.raise_for_status()
                    update_result = update_response.json()

                    if update_result.get('success'):
                        QMessageBox.information(self, "퇴실 완료", "퇴실되었습니다.")
                        self.parent.show()
                        self.close()
                    else:
                        QMessageBox.warning(self, "퇴실 실패", "퇴실에 실패했습니다.") 
                except requests.RequestException as e:
                    QMessageBox.critical(self, "오류", f"퇴실 요청 중 오류가 발생했습니다: {e}")
            else:
                QMessageBox.warning(self, "오류", "사용자의 예약 정보가 없습니다.")

    def logout(self):
        self.parent.show()
        self.close()



class SeatApp(QWidget):
    def __init__(self, member_id):
        super().__init__()
        self.member_id = member_id
        self.initUI()
        self.seat_data = []

    def initUI(self):
        self.layout = QVBoxLayout()

        self.get_seat_data()

        self.seat_info_label = QLabel(self)
        self.update_seat_info()
        self.layout.addWidget(self.seat_info_label)

        for seat in self.seat_data:
            scheduled_end_time = seat['scheduled_end_time']
            if scheduled_end_time is not None:
                button_text = f"좌석 {seat['id']} (종료 시간: {scheduled_end_time})"
            else:
                button_text = f"좌석 {seat['id']}"

            button = QPushButton(button_text)
            button.setEnabled(seat['status'] == 'false')
            button.clicked.connect(lambda checked, seat_id=seat['id']: self.confirm_selection(seat_id)) 
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.setWindowTitle('좌석선택')
        self.show()

    def get_seat_data(self):
        response = requests.get('http://domain.com/CafeProject/seat.php')
        self.seat_data = json.loads(response.text)

    def confirm_selection(self, seat_id):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('좌석 선택')
        msg_box.setText(f'해당 좌석 {seat_id}을(를) 선택하시겠습니까?')
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.No)

        response = msg_box.exec_()

        if response == QMessageBox.Yes:

            data = {
                'id': seat_id,
                'status': 'true',
                'user_id': self.member_id
            }

            #입실
            try:
                update_response = requests.post('http://domain.com/CafeProject/update_seat.php', data=data)
                update_response.raise_for_status()
                update_result = update_response.json()

                if update_result.get('success'):
                    QMessageBox.information(self, "예약 성공", f"좌석 {seat_id}이(가) 예약되었습니다.")
                    self.close()
                else:
                    QMessageBox.warning(self, "예약 실패", "좌석 예약에 실패했습니다.")
            except requests.RequestException as e:
                QMessageBox.critical(self, "오류", f"예약 요청 중 오류가 발생했습니다: {e}")

    def update_seat_info(self):
        total_seats = len(self.seat_data)
        available_seats = sum(1 for seat in self.seat_data if seat['status'] == 'false')

        seat_info = f"사용 가능 {available_seats}/{total_seats}"
        self.seat_info_label.setText(seat_info)

        self.seat_info_label.setAlignment(Qt.AlignRight)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
