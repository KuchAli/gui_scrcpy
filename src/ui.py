import os
import webbrowser
from PyQt6.QtCore import QProcess, QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDial,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from src.utils import AppUtils


class ScrpycpyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI SCRCPY")
        self.resize(420, 560)

        self.setWindowIcon(AppUtils.load_icon("logos"))

        self.process = QProcess(self)
        self.bitrate_kbps = 8000

        self.init_ui()
        self.load_stylesheet()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 1. Header
        header_layout = QHBoxLayout()
        lbl_logo = QLabel()
        
        # path logo langsung mengarah ke assets/icons/logos.png di luar src
        logo_path = AppUtils.get_asset_path("assets/icons/logos.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            lbl_logo.setPixmap(pixmap)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title_box.setContentsMargins(0,0,0,0)
        title_box.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )

        lbl_title = QLabel("GUI SCRCPY")
        lbl_title.setObjectName("lbl_title")
        lbl_subtitle = QLabel("Build 1.0 by Mister K")
        lbl_subtitle.setObjectName("lbl_subtitle")

        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_subtitle)

        header_layout.addWidget(lbl_logo)
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        #checkbox options grid
        grid_layout = QGridLayout()
        self.chk_bottom_panel = QCheckBox("Bottom Panel")
        self.chk_side_panel = QCheckBox("Side Panel")
        self.chk_swipe_panel = QCheckBox("Swipe Panel")

        self.chk_fullscreen = QCheckBox("Fullscreen")
        #self.chk_fullscreen.setIcon(AppUtils.load_icon("fullscreen"))

        self.chk_keep_off = QCheckBox("Keep display off")
        self.chk_show_touches = QCheckBox("Show touches")
        self.chk_record = QCheckBox("Record screen")
        self.chk_always_top = QCheckBox("Always on Top")
        self.chk_lock_rot = QCheckBox("Lock Rotation")

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

        #quick icon bar
        icon_bar_layout = QHBoxLayout()

        btn_wifi = QPushButton()
        btn_wifi.setIcon(AppUtils.load_icon("wifi"))
        btn_wifi.setProperty("class", "btn-icon-small")
        btn_wifi.setToolTip("Koneksi Wireless Debugging (Wi-Fi)")
        btn_wifi.clicked.connect(self.connect_wifi)

        btn_settings = QPushButton()
        btn_settings.setIcon(AppUtils.load_icon("setting"))
        btn_settings.setProperty("class", "btn-icon-small")
        btn_settings.setToolTip("Buka Pengaturan (Isi Flag Line dulu)")
        btn_settings.clicked.connect(self.open_settings)

        btn_restart = QPushButton()
        btn_restart.setIcon(AppUtils.load_icon("restart"))
        btn_restart.setProperty("class", "btn-icon-small")
        btn_restart.setToolTip("Restart ADB")
        btn_restart.clicked.connect(self.restart_adb)

        btn_android = QPushButton()
        btn_android.setIcon(AppUtils.load_icon("android"))
        btn_android.setProperty("class", "btn-icon-small")
        btn_android.setToolTip("Adb Connect")
        btn_android.clicked.connect(self.adb_connect)

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

        #status bar
        status_box = QVBoxLayout()
        status_box.setSpacing(4)

        #label penanda
        self.title_status = QLabel("STATUS BAR:")
        self.title_status.setObjectName("title_status")
        self.title_status.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #64748b;"
        )

       
        self.lbl_status = QLabel("SCRCPY SERVER READY")
        self.lbl_status.setObjectName("status_bar")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #digabung ke layout
        status_box.addWidget(self.title_status)
        status_box.addWidget(self.lbl_status)
        main_layout.addLayout(status_box)

        #bitrate dial
        dial_layout = QHBoxLayout()
        self.dial_bitrate = QDial()
        self.dial_bitrate.setFixedSize(75, 75)
        self.dial_bitrate.setRange(1000, 30000)
        self.dial_bitrate.setSingleStep(1000)
        self.dial_bitrate.setValue(8000)

        self.btn_bitrate = QPushButton("8000 KB/s")
        self.btn_bitrate.setObjectName("lbl_bitrate")
        self.btn_bitrate.clicked.connect(self.manual_set_bitrate)

        self.btn_default = QPushButton("DEFAULT")
        self.btn_default.setObjectName("lbl_default")
        self.btn_default.clicked.connect(self.reset_to_default)

        dial_layout.addWidget(self.dial_bitrate)
        dial_layout.addWidget(self.btn_bitrate)
        dial_layout.addWidget(self.btn_default)
        main_layout.addLayout(dial_layout)

        #additional flags line
        self.txt_flags = QLineEdit()
        self.txt_flags.setPlaceholderText(
            "Enter additional flags to pass to scrcpy"
        )
        main_layout.addWidget(self.txt_flags)

        #action bar
        action_layout = QHBoxLayout()

        btn_close = QPushButton()
        btn_close.setIcon(AppUtils.load_icon("close"))
        btn_close.setProperty("class", "btn-danger")
        btn_close.setToolTip("Keluar dari program")
        btn_close.clicked.connect(self.close)

        btn_reset = QPushButton("RESET")
        btn_reset.setIcon(AppUtils.load_icon("reset"))
        btn_reset.setProperty("class", "btn-cyan")
        btn_reset.setToolTip("Reset Semua")
        btn_reset.clicked.connect(self.reset_all_inputs)

        btn_github = QPushButton()
        btn_github.setIcon(AppUtils.load_icon("github"))
        btn_github.setProperty("class", "btn-cyan")
        btn_github.setToolTip("Buka Profil GitHub KuchAli")
        btn_github.clicked.connect(
            self.open_github
        ) 

        btn_audio = QPushButton()
        btn_audio.setIcon(AppUtils.load_icon("sound"))
        btn_audio.setProperty("class", "btn-purple")
        btn_audio.setToolTip("Atur volume")
        btn_audio.clicked.connect(self.show_volume_menu)

        self.btn_start = QPushButton(" START SCRCPY")
        self.btn_start.setIcon(AppUtils.load_icon("rocket"))
        self.btn_start.setIconSize(QSize(20, 20))
        self.btn_start.setProperty("class", "btn-start")
        self.btn_start.setToolTip("Mulai SCRCPY")
        self.btn_start.clicked.connect(self.toggle_scrcpy)

        action_layout.addWidget(btn_close)
        action_layout.addWidget(btn_reset)
        action_layout.addWidget(btn_github)
        action_layout.addWidget(btn_audio)
        action_layout.addWidget(self.btn_start)
        main_layout.addLayout(action_layout)

        #progress bar
        self.progress = QProgressBar()
        self.progress.setValue(100)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.progress)

        self.setLayout(main_layout)

        #signal
        self.dial_bitrate.valueChanged.connect(self.update_bitrate_from_dial)
        self.process.finished.connect(self.on_finished)

    def load_stylesheet(self):
        # path stylesheet langsung mengarah ke assets/style.qss di luar src
        qss_path = AppUtils.get_asset_path("assets/style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())

    def connect_wifi(self):
        if AppUtils.setup_wireless_adb(self):
            self.lbl_status.setText("CONNECTED VIA WIRELESS")

    def update_bitrate_from_dial(self, value):
        self.bitrate_kbps = value
        self.btn_bitrate.setText(f"{self.bitrate_kbps} KB/s")

    def manual_set_bitrate(self):
        val, ok = QInputDialog.getInt(
            self,
            "Ubah Bitrate",
            "Masukkan nilai Bitrate (KB/s):",
            self.bitrate_kbps,
            500,
            50000,
            500,
        )
        if ok:
            self.bitrate_kbps = val
            self.dial_bitrate.setValue(val)
            self.btn_bitrate.setText(f"{self.bitrate_kbps} KB/s")

    def reset_to_default(self):
        self.bitrate_kbps = 8000
        self.dial_bitrate.setValue(8000)
        self.btn_bitrate.setText("8000 KB/s")
        self.combo_rotation.setCurrentIndex(0)

    def reset_all_inputs(self):
        self.reset_to_default()
        self.chk_bottom_panel.setChecked(True)
        self.chk_side_panel.setChecked(True)
        self.chk_swipe_panel.setChecked(True)
        self.chk_fullscreen.setChecked(False)
        self.chk_keep_off.setChecked(False)
        self.chk_show_touches.setChecked(False)
        self.chk_record.setChecked(False)
        self.chk_always_top.setChecked(False)
        self.chk_lock_rot.setChecked(False)
        self.txt_flags.clear()

    def open_settings(self):
        QMessageBox.information(
            self,
            "Setting",
            "Gunakan kolom 'Enter additional flags' untuk argumen kustom.",
        )

    def restart_adb(self):
        adb_bin = AppUtils.get_adb_path()
        adb_proc = QProcess(self)
        adb_proc.start(adb_bin, ["kill-server"])
        adb_proc.waitForFinished()
        adb_proc.start(adb_bin, ["start-server"])
        self.lbl_status.setText("ADB SERVER RESTARTED")

    def adb_connect(self):
        """Mengeksekusi perintah ADB dari folder scrcpy untuk mengecek & mengkoneksikan perangkat"""
        adb_bin = AppUtils.get_adb_path()
        proc = QProcess(self)

        # Jalankan perintah 'adb devices' untuk melihat daftar HP yang terhubung
        proc.start(adb_bin, ["devices"])
        proc.waitForFinished()

        output = proc.readAllStandardOutput().data().decode("utf-8").strip()

        # Cek hasil output dari terminal ADB
        lines = output.splitlines()
        connected_devices = [
            line for line in lines[1:] if line.strip() and "device" in line
        ]

        if connected_devices:
            # Mengambil ID perangkat pertama yang terdeteksi
            device_id = connected_devices[0].split()[0]
            self.lbl_status.setText(f"ADB CONNECTED: {device_id}")
            QMessageBox.information(
                self,
                "ADB Status",
                f"Perangkat terhubung!\nDevice ID: {device_id}",
            )
        else:
            self.lbl_status.setText("NO DEVICE DETECTED")
            QMessageBox.warning(
                self,
                "ADB Status",
                "Perangkat tidak ditemukan!\nPastikan kabel USB terpasang & USB Debugging di HP aktif.",
            )

    def open_github(self):
        webbrowser.open("https://github.com/KuchAli/gui_scrcpy")

    def show_volume_menu(self):
        """Menampilkan menu dropdown untuk Volume Up, Volume Down, dan Mute"""
        from PyQt6.QtWidgets import QMenu

        menu = QMenu(self)

        # Opsi Menu Volume
        vol_up_action = menu.addAction("🔊 Volume Up (+)")
        vol_down_action = menu.addAction("🔉 Volume Down (-)")
        mute_action = menu.addAction("🔇 Mute / Unmute")

        # Jalankan menu di posisi tombol audio
        action = menu.exec(
            self.sender().mapToGlobal(self.sender().rect().bottomLeft())
        )

        # Cek opsi mana yang diklik
        if action == vol_up_action:
            self.change_volume("up")
        elif action == vol_down_action:
            self.change_volume("down")
        elif action == mute_action:
            self.change_volume("mute")

    def change_volume(self, action_type):
        """Mengirim perintah Keycode ADB untuk mengubah volume HP"""
        adb_bin = AppUtils.get_adb_path()
        proc = QProcess(self)

        # Keycode ADB standar Android untuk Volume
        keycodes = {
            "up": "24",  # KEYCODE_VOLUME_UP
            "down": "25",  # KEYCODE_VOLUME_DOWN
            "mute": "164",  # KEYCODE_VOLUME_MUTE
        }

        if action_type in keycodes:
            code = keycodes[action_type]
            proc.start(adb_bin, ["shell", "input", "keyevent", code])
            self.lbl_status.setText(f"VOLUME {action_type.upper()}")


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

            args.extend(["-b", f"{self.bitrate_kbps}K"])

            rot_idx = self.combo_rotation.currentIndex()
            if rot_idx > 0:
                rot_val = (rot_idx - 1) * 90
                args.extend(["--lock-video-orientation", str(rot_val)])
            elif self.chk_lock_rot.isChecked():
                args.append("--lock-video-orientation")

            extra_flags = self.txt_flags.text().strip()
            if extra_flags:
                args.extend(extra_flags.split())

            scrcpy_bin = AppUtils.get_scrcpy_path()
            self.process.start(scrcpy_bin, args)

            self.lbl_status.setText("SCRCPY SERVER RUNNING")
            self.btn_start.setText(" STOP SCRCPY")

    def on_finished(self):
        self.lbl_status.setText("SCRCPY SERVER READY")
        self.btn_start.setText(" START SCRCPY")