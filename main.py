import os
import sys
from PyQt6.QtCore import QProcess, QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class ScrpycpyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI SCRCPY")
        #self.get_asset_path(f"assets/icons/logos.png")
        self.resize(420, 560)

        self.process = QProcess(self)
        self.init_ui()
        self.load_stylesheet()

    def get_asset_path(self, relative_path):
        """Mendukung pembacaan aset saat running .py maupun setelah di-build .exe"""
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def load_icon(self, icon_name):
        """Fungsi pembantu untuk memuat ikon PNG dari folder assets/icons/"""
        icon_path = self.get_asset_path(f"assets/icons/{icon_name}.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 1. Header (Logo PNG + Title)[cite: 1]
        header_layout = QHBoxLayout()

        lbl_logo = QLabel()
        logo_path = self.get_asset_path("assets/icons/logos.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            lbl_logo.setPixmap(pixmap)

        title_box = QVBoxLayout()
        lbl_title = QLabel("guiscrcpy")
        lbl_title.setObjectName("lbl_title")
        lbl_subtitle = QLabel("Build 3.9 by srevinsaju")
        lbl_subtitle.setObjectName("lbl_subtitle")

        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_subtitle)

        header_layout.addWidget(lbl_logo)
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # 2. Checkbox Grid Options[cite: 1]
        grid_layout = QGridLayout()

        self.chk_bottom_panel = QCheckBox("Bottom Panel")
        self.chk_side_panel = QCheckBox("Side Panel")
        self.chk_swipe_panel = QCheckBox("Swipe Panel")

        self.chk_fullscreen = QCheckBox("Fullscreen")
        self.chk_fullscreen.setIcon(self.load_icon("fullscreen"))

        self.chk_keep_off = QCheckBox("Keep display off")
        self.chk_show_touches = QCheckBox("Show touches")
        self.chk_record = QCheckBox("Record screen")
        self.chk_always_top = QCheckBox("Always on Top")
        self.chk_lock_rot = QCheckBox("Lock Rotation")

        # Set default checked[cite: 1]
        self.chk_bottom_panel.setChecked(True)
        self.chk_side_panel.setChecked(True)
        self.chk_swipe_panel.setChecked(True)

        grid_layout.addWidget(self.chk_bottom_panel, 0, 0)
        grid_layout.addWidget(self.chk_fullscreen, 0, 1)
        grid_layout.addWidget(self.chk_record, 0, 2)
        grid_layout.addWidget(self.chk_side_panel, 1, 0)
        grid_layout.addWidget(self.chk_keep_off, 1, 1)
        grid_layout.addWidget(self.chk_always_top, 1, 2)
        grid_layout.addWidget(self.chk_swipe_panel, 2, 0)
        grid_layout.addWidget(self.chk_show_touches, 2, 1)
        grid_layout.addWidget(self.chk_lock_rot, 2, 2)

        main_layout.addLayout(grid_layout)

        # 3. Quick Icon Bar (Wifi, Setting, Restart, Android) & Rotation Combo[cite: 1]
        icon_bar_layout = QHBoxLayout()

        btn_wifi = QPushButton()
        btn_wifi.setIcon(self.load_icon("wifi"))
        btn_wifi.setProperty("class", "btn-icon-small")

        btn_settings = QPushButton()
        btn_settings.setIcon(self.load_icon("setting"))
        btn_settings.setProperty("class", "btn-icon-small")

        btn_restart = QPushButton()
        btn_restart.setIcon(self.load_icon("restart"))
        btn_restart.setProperty("class", "btn-icon-small")

        btn_android = QPushButton()
        btn_android.setIcon(self.load_icon("android"))
        btn_android.setProperty("class", "btn-icon-small")

        self.combo_rotation = QComboBox()
        self.combo_rotation.addItems(
            ["Default Rotation", "0 Degree", "90 Degree", "180 Degree"]
        )

        icon_bar_layout.addWidget(btn_wifi)
        icon_bar_layout.addWidget(btn_settings)
        icon_bar_layout.addWidget(btn_restart)
        icon_bar_layout.addWidget(btn_android)
        icon_bar_layout.addStretch()
        icon_bar_layout.addWidget(self.combo_rotation)
        main_layout.addLayout(icon_bar_layout)

        # 4. Status Bar[cite: 1]
        self.lbl_status = QLabel("SCRCPY SERVER READY")
        self.lbl_status.setObjectName("status_bar")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lbl_status)

        # 5. Bitrate & Dimensions Dial[cite: 1]
        dial_layout = QHBoxLayout()
        self.dial_bitrate = QDial()
        self.dial_bitrate.setFixedSize(75, 75)
        self.dial_bitrate.setRange(2, 30)
        self.dial_bitrate.setValue(8)

        self.lbl_bitrate = QLabel("8000 KB/s")
        self.lbl_bitrate.setObjectName("lbl_bitrate")

        lbl_default = QLabel("DEFAULT")
        lbl_default.setObjectName("lbl_default")

        dial_layout.addWidget(self.dial_bitrate)
        dial_layout.addWidget(self.lbl_bitrate)
        dial_layout.addWidget(lbl_default)
        main_layout.addLayout(dial_layout)

        # 6. Flags Input Line[cite: 1]
        self.txt_flags = QLineEdit()
        self.txt_flags.setPlaceholderText(
            "Enter additional flags to pass to scrcpy"
        )
        main_layout.addWidget(self.txt_flags)

        # 7. Action Bar Buttons (Close, Reset, Github, Sound, Rocket)[cite: 1]
        action_layout = QHBoxLayout()

        btn_close = QPushButton()
        btn_close.setIcon(self.load_icon("close"))
        btn_close.setProperty("class", "btn-danger")
        btn_close.clicked.connect(self.close)

        btn_reset = QPushButton("RESET")
        btn_reset.setIcon(self.load_icon("reset"))
        btn_reset.setProperty("class", "btn-cyan")

        btn_github = QPushButton()
        btn_github.setIcon(self.load_icon("github"))
        btn_github.setProperty("class", "btn-cyan")

        btn_audio = QPushButton()
        btn_audio.setIcon(self.load_icon("sound"))
        btn_audio.setProperty("class", "btn-purple")

        self.btn_start = QPushButton(" START SCRCPY")
        self.btn_start.setIcon(self.load_icon("rocket"))
        self.btn_start.setIconSize(QSize(20, 20))
        self.btn_start.setProperty("class", "btn-start")
        self.btn_start.clicked.connect(self.toggle_scrcpy)

        action_layout.addWidget(btn_close)
        action_layout.addWidget(btn_reset)
        action_layout.addWidget(btn_github)
        action_layout.addWidget(btn_audio)
        action_layout.addWidget(self.btn_start)
        main_layout.addLayout(action_layout)

        # 8. Progress Bar[cite: 1]
        progress = QProgressBar()
        progress.setValue(100)
        progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(progress)

        self.setLayout(main_layout)

        # Signals
        self.dial_bitrate.valueChanged.connect(self.update_bitrate_label)
        self.process.finished.connect(self.on_finished)

    def load_stylesheet(self):
        qss_path = self.get_asset_path("assets/style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())

    def update_bitrate_label(self, value):
        self.lbl_bitrate.setText(f"{value * 1000} KB/s")

    def get_scrcpy_path(self):
        scrcpy_bin = self.get_asset_path("scrcpy/scrcpy.exe")
        if os.path.exists(scrcpy_bin):
            return scrcpy_bin
        return "scrcpy"

    def toggle_scrcpy(self):
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.terminate()
        else:
            args = []

            if self.chk_fullscreen.isChecked():
                args.append("-f")
            if self.chk_keep_off.isChecked():
                args.append("-S")
            if self.chk_show_touches.isChecked():
                args.append("-t")
            if self.chk_always_top.isChecked():
                args.append("--always-on-top")

            bitrate_val = f"{self.dial_bitrate.value()}M"
            args.extend(["-b", bitrate_val])

            extra_flags = self.txt_flags.text().strip()
            if extra_flags:
                args.extend(extra_flags.split())

            scrcpy_bin = self.get_scrcpy_path()
            self.process.start(scrcpy_bin, args)

            self.lbl_status.setText("SCRCPY SERVER RUNNING")
            self.btn_start.setText(" STOP SCRCPY")

    def on_finished(self):
        self.lbl_status.setText("SCRCPY SERVER READY")
        self.btn_start.setText(" START SCRCPY")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrpycpyApp()
    window.show()
    sys.exit(app.exec())
