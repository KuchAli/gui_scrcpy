import os
import sys
from PyQt6.QtCore import QProcess
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QInputDialog, QMessageBox


class AppUtils:
    @staticmethod
    def get_asset_path(relative_path):
        """Mendapatkan path file aset di luar folder src"""
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            # os.path.dirname(os.path.dirname(...)) dipakai untuk naik 1 folder ke luar dari 'src'
            base_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        return os.path.join(base_path, relative_path)

    @classmethod
    def load_icon(cls, icon_name):
        # Membaca dari assets/icons/ di luar src
        icon_path = cls.get_asset_path(f"assets/icons/{icon_name}.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    @classmethod
    def get_scrcpy_path(cls):
        scrcpy_bin = cls.get_asset_path("scrcpy/scrcpy.exe")
        return scrcpy_bin if os.path.exists(scrcpy_bin) else "scrcpy"

    @classmethod
    def get_adb_path(cls):
        adb_bin = cls.get_asset_path("scrcpy/adb.exe")
        return adb_bin if os.path.exists(adb_bin) else "adb"

    @classmethod
    def setup_wireless_adb(cls, parent_widget):
        ip_port, ok = QInputDialog.getText(
            parent_widget,
            "Wireless Debugging",
            "Masukkan Alamat IP & Port HP (Contoh: 192.168.1.15:5555):",
        )

        if ok and ip_port.strip():
            adb_bin = cls.get_adb_path()
            proc = QProcess(parent_widget)

            proc.start(adb_bin, ["connect", ip_port.strip()])
            proc.waitForFinished()

            output = proc.readAllStandardOutput().data().decode("utf-8")

            if "connected" in output.lower():
                QMessageBox.information(
                    parent_widget,
                    "Sukses",
                    f"Berhasil terhubung ke {ip_port}!",
                )
                return True
            else:
                QMessageBox.warning(
                    parent_widget,
                    "Gagal",
                    f"Gagal terhubung:\n{output}",
                )
        return False