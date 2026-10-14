import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QFileDialog, QGridLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt


# ================= صفحة تسجيل الدخول =================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("GYM PRO")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 36px; margin-bottom: 30px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم (admin أو user)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور (123)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("تسجيل الدخول")
        login_btn.clicked.connect(self.check_login)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "123":
            main_window.setCurrentIndex(1)
            self.clear_inputs()
        elif username == "user" and password == "123":
            main_window.setCurrentIndex(2)
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة.")

    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()


# ================= صفحة الكابتن (المدير) =================
class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- القائمة الجانبية ---
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #111111; border-left: 2px solid #e50914;")
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("لوحة الكابتن")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("border: none; margin-bottom: 20px;")

        btn_add_member = QPushButton("إضافة مشترك")
        btn_add_equip = QPushButton("إضافة جهاز رياضي")
        btn_assign_course = QPushButton("تخصيص كورس")

        logout_btn = QPushButton("تسجيل الخروج")
        logout_btn.setStyleSheet("background-color: #333333; margin-top: 20px;")
        logout_btn.clicked.connect(lambda: main_window.setCurrentIndex(0))

        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(btn_add_member)
        sidebar_layout.addWidget(btn_add_equip)
        sidebar_layout.addWidget(btn_assign_course)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(logout_btn)

        # --- منطقة المحتوى ---
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #070707; padding: 20px; border: none;")

        # 1. واجهة إضافة مشترك
        page_member = QWidget()
        layout_member = QVBoxLayout(page_member)
        layout_member.addWidget(QLabel("إضافة حساب مشترك جديد"))
        layout_member.addWidget(QLineEdit(placeholderText="الاسم الكامل"))
        layout_member.addWidget(QLineEdit(placeholderText="اسم المستخدم (اليوزر)"))
        layout_member.addWidget(QLineEdit(placeholderText="كلمة المرور"))
        save_member_btn = QPushButton("إنشاء الحساب")
        save_member_btn.clicked.connect(lambda: QMessageBox.information(self, "نجاح", "تم إنشاء حساب المشترك بنجاح!"))
        layout_member.addWidget(save_member_btn)
        layout_member.addStretch()

        # 2. واجهة إضافة جهاز (مع فتح الملفات)
        page_equip = QWidget()
        layout_equip = QVBoxLayout(page_equip)
        layout_equip.addWidget(QLabel("إضافة جهاز رياضي جديد"))

        self.eq_name = QLineEdit(placeholderText="اسم الجهاز (مثال: سحب ظهر أمامي)")
        layout_equip.addWidget(self.eq_name)

        # أزرار اختيار الملفات
        btn_img = QPushButton("📁 اختيار صورة الجهاز")
        btn_img.clicked.connect(self.choose_image)
        self.lbl_img = QLabel("لم يتم اختيار صورة")
        self.lbl_img.setStyleSheet("font-size: 12px; color: #a7a7a7;")

        btn_vid = QPushButton("🎥 اختيار فيديو توضيحي")
        btn_vid.clicked.connect(self.choose_video)
        self.lbl_vid = QLabel("لم يتم اختيار فيديو")
        self.lbl_vid.setStyleSheet("font-size: 12px; color: #a7a7a7;")

        layout_equip.addWidget(btn_img)
        layout_equip.addWidget(self.lbl_img)
        layout_equip.addWidget(btn_vid)
        layout_equip.addWidget(self.lbl_vid)

        save_eq_btn = QPushButton("حفظ الجهاز في النظام")
        save_eq_btn.clicked.connect(
            lambda: QMessageBox.information(self, "نجاح", f"تم إضافة جهاز: {self.eq_name.text()}"))
        layout_equip.addWidget(save_eq_btn)
        layout_equip.addStretch()

        # 3. واجهة الكورسات
        page_course = QWidget()
        layout_course = QVBoxLayout(page_course)
        layout_course.addWidget(QLabel("تخصيص كورس للمشتركين"))
        layout_course.addWidget(QLineEdit(placeholderText="اسم المشترك أو اليوزر"))
        layout_course.addWidget(QLineEdit(placeholderText="اسم الكورس (مثال: تنشيف)"))
        save_course_btn = QPushButton("حفظ الكورس")
        save_course_btn.clicked.connect(lambda: QMessageBox.information(self, "نجاح", "تم تخصيص الكورس بنجاح!"))
        layout_course.addWidget(save_course_btn)
        layout_course.addStretch()

        # إضافة الصفحات
        self.content_stack.addWidget(page_member)
        self.content_stack.addWidget(page_equip)
        self.content_stack.addWidget(page_course)

        # ربط الأزرار
        btn_add_member.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        btn_add_equip.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        btn_assign_course.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)
        self.setLayout(main_layout)

    def choose_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "اختر صورة الجهاز", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.lbl_img.setText(file_name)

    def choose_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "اختر فيديو التمرين", "", "Videos (*.mp4 *.avi)")
        if file_name:
            self.lbl_vid.setText(file_name)


# ================= صفحة المشترك =================
class MemberWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # --- الهيدر (الاسم، الكورس، الستريك، تسجيل الخروج) ---
        header_layout = QHBoxLayout()

        info_layout = QVBoxLayout()
        name_lbl = QLabel("أهلاً بك يا بطل: User")
        name_lbl.setStyleSheet("font-size: 24px;")
        course_lbl = QLabel("الكورس الحالي: ضخامة عضلية")
        course_lbl.setStyleSheet("color: #a7a7a7; font-size: 16px;")
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(course_lbl)

        self.streak_btn = QPushButton("🔥\nسجل حضورك")
        self.streak_btn.setFixedSize(100, 70)
        self.streak_btn.setStyleSheet("background-color: #ff8a00; border-radius: 10px;")
        self.streak_btn.clicked.connect(self.record_streak)

        logout_btn = QPushButton("خروج")
        logout_btn.setFixedSize(80, 40)
        logout_btn.setStyleSheet("background-color: #333333;")
        logout_btn.clicked.connect(lambda: main_window.setCurrentIndex(0))

        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.streak_btn)
        header_layout.addWidget(logout_btn)

        # --- أقسام العضلات (Grid) ---
        muscles_lbl = QLabel("تصفح الأجهزة والتمارين:")
        muscles_lbl.setStyleSheet("margin-top: 10px;")

        grid_layout = QGridLayout()
        muscles = ["الصدر", "الظهر", "أكتاف", "كارديو", "رجل", "سواعد", "بطن", "ذراع"]

        row, col = 0, 0
        for muscle in muscles:
            btn = QPushButton(muscle)
            btn.setStyleSheet("background-color: #151515; border: 1px solid #e50914; padding: 15px;")
            grid_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:  # 4 أزرار في كل سطر
                col = 0
                row += 1

        # --- تسجيل التمرين ---
        workout_layout = QVBoxLayout()
        workout_layout.addWidget(QLabel("تسجيل أوزان تمرين اليوم (سجل خاص بك):"))

        inputs_layout = QHBoxLayout()
        self.weight_in = QLineEdit(placeholderText="الوزن (كغم)")
        self.sets_in = QLineEdit(placeholderText="السيتات")
        self.reps_in = QLineEdit(placeholderText="التكرار (الدفعات)")

        inputs_layout.addWidget(self.weight_in)
        inputs_layout.addWidget(self.sets_in)
        inputs_layout.addWidget(self.reps_in)

        save_workout_btn = QPushButton("حفظ السجل للكابتن")
        save_workout_btn.clicked.connect(self.save_workout)

        # التجميع النهائي لصفحة المشترك
        main_layout.addLayout(header_layout)
        main_layout.addWidget(muscles_lbl)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.addLayout(workout_layout)
        main_layout.addLayout(inputs_layout)
        main_layout.addWidget(save_workout_btn)

        self.setLayout(main_layout)

    def record_streak(self):
        self.streak_btn.setText("تم الحضور ✔")
        self.streak_btn.setStyleSheet("background-color: #28a745; border-radius: 10px;")
        self.streak_btn.setEnabled(False)
        QMessageBox.information(self, "عاش وحش", "تم تسجيل حضورك لليوم بنجاح! يتفعل الزر بعد 12 ساعة.")

    def save_workout(self):
        if not self.weight_in.text() or not self.sets_in.text() or not self.reps_in.text():
            QMessageBox.warning(self, "نقص البيانات", "يرجى كتابة الوزن والسيتات والتكرار.")
            return
        QMessageBox.information(self, "تم", "تم تسجيل تمرينك بنجاح! سيظهر في سجلات الكابتن.")
        self.weight_in.clear()
        self.sets_in.clear()
        self.reps_in.clear()


# ================= التجميع والتشغيل الأساسي =================
app = QApplication(sys.argv)

main_window = QStackedWidget()
main_window.setWindowTitle("Gym Pro System")
main_window.resize(800, 600)

# التصميم العام (CSS بداخل بايثون)
main_window.setStyleSheet("""
    QWidget { background-color: #070707; font-family: Arial; color: white; }
    QLabel { color: #e50914; font-size: 20px; font-weight: bold; }
    QLineEdit { background-color: #151515; color: white; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 12px; font-size: 15px; margin-bottom: 10px; }
    QLineEdit:focus { border: 1px solid #e50914; }
    QPushButton { background-color: #e50914; color: white; border-radius: 8px; padding: 12px; font-size: 15px; font-weight: bold; border: none; }
    QPushButton:hover { background-color: #a6070e; }
    QMessageBox { background-color: #151515; color: white; }
    QMessageBox QPushButton { padding: 5px 20px; }
""")

login_page = LoginWindow()
admin_page = AdminWindow()
member_page = MemberWindow()

main_window.addWidget(login_page)  # Index 0
main_window.addWidget(admin_page)  # Index 1
main_window.addWidget(member_page)  # Index 2

main_window.show()
sys.exit(app.exec())