import io
import os
import sys
import time
import string
import random
import qrcode
from PyQt6.QtCore import QProcess, QTimer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QInputDialog, QMessageBox)


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
    def load_pixmap(cls, icon_name):
        path = cls.get_asset_path(f"assets/icons/{icon_name}.png")
        return QPixmap(path) if os.path.exists(path) else QPixmap()


    @classmethod
    def load_icon(cls, icon_name):
       return QIcon(cls.load_pixmap(icon_name))

    @classmethod
    def get_scrcpy_path(cls):
        scrcpy_bin = cls.get_asset_path("scrcpy/scrcpy.exe")
        return scrcpy_bin if os.path.exists(scrcpy_bin) else "scrcpy"

    @classmethod
    def get_adb_path(cls):
        adb_bin = cls.get_asset_path("scrcpy/adb.exe")
        return adb_bin if os.path.exists(adb_bin) else "adb"

    @classmethod
    def _adb(cls, parent, args, timeout=10000):
        #menjalankan adb, return stdout + stderr (error adb sering di stderr)
        proc = QProcess(parent)
        proc.start(cls.get_adb_path(), args)
        proc.waitForFinished(timeout)
        out = proc.readAllStandardOutput().data().decode("utf-8", "ignore")
        err = proc.readAllStandardError().data().decode("utf-8", "ignore")
        return out + err

    @classmethod
    def _find_mdns(cls, parent, services_type, name=None):
        for line in cls._adb(parent, ["mdns", "services"]).splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[1].startswith(services_type):
                if name is None or parts[0] == name:
                    parts[2]
        return None

    #pairing

    @classmethod
    def pair_with_qr(cls, parent_widget):
        name = "ADB_WIFI_" + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        password = "".join(random.choices(string.digits, k=6))
        payload = f"WIFI:T:ADB;S:{name};P:{password};;"

        buf = io.BytesIO()
        qrcode.make(payload).save(buf, format="PNG")
        pix = QPixmap()
        pix.loadFromData(buf.getvalue())

        dlg = QDialog(parent_widget)
        dlg.setWindowTitle("Pairing via QR")
        lay = QVBoxLayout(dlg)
        lay.addWidget(
            QLabel(
                "HP: Opsi Developer → Wireless debugging →\n"
                "'Pair device with QR code', lalu scan QR ini."
            )
        )
        img = QLabel()
        img.setPixmap(pix.scaled(300, 300))
        lay.addWidget(img)
        status = QLabel("Menunggu scan...")
        lay.addWidget(status)

        result = {"ok": False}
        deadline = time.time() + 60
        timer = QTimer(dlg)

        def poll():
            if time.time() > deadline:
                timer.stop()
                status.setText("Timeout. Coba lagi atau pakai kode manual.")
                return
            addr = cls._find_mdns(parent_widget, "_adb-tls-pairing", name)
            if not addr:
                return
            timer.stop()
            status.setText("Pairing...")
            out = cls._adb(parent_widget, ["pair", addr, password])
            if "successfully paired" in out.lower():
                time.sleep(1.5)
                conn = cls._find_mdns(parent_widget, "_adb-tls-connect")
                if conn:
                    out = cls._adb(parent_widget, ["connect", conn])
                    result["ok"] = "connected" in out.lower()
                dlg.accept()
                if result["ok"]:
                    QMessageBox.information(parent_widget, "Sukses", out)
                else:
                    QMessageBox.warning(
                        parent_widget,
                        "Pairing berhasil, connect gagal",
                        out or "Port connect tidak ditemukan via mDNS.",
                    )
            else:
                status.setText(f"Gagal:\n{out}")

        timer.timeout.connect(poll)
        timer.start(1500)
        dlg.exec()
        timer.stop()
        return result["ok"]

    @classmethod
    def pair_with_code(cls, parent_widget):
        """Fallback kalau mDNS/QR tidak jalan (mis. di hotspot)."""
        addr, ok = QInputDialog.getText(
            parent_widget,
            "Pairing",
            "IP:Port dari 'Pair device with pairing code'\n"
            "(contoh 192.168.43.1:37123):",
        )
        if not ok or not addr.strip():
            return False
        code, ok = QInputDialog.getText(
            parent_widget, "Pairing", "Kode 6 digit:"
        )
        if not ok or not code.strip():
            return False

        out = cls._adb(parent_widget, ["pair", addr.strip(), code.strip()])
        if "successfully paired" not in out.lower():
            QMessageBox.warning(parent_widget, "Gagal pairing", out)
            return False

        conn, ok = QInputDialog.getText(
            parent_widget,
            "Connect",
            "IP:Port di layar utama Wireless debugging\n"
            "(BEDA dari port pairing):",
        )
        if not ok or not conn.strip():
            return False

        out = cls._adb(parent_widget, ["connect", conn.strip()])
        if "connected" in out.lower():
            QMessageBox.information(parent_widget, "Sukses", out)
            return True
        QMessageBox.warning(parent_widget, "Gagal", out)
        return False

    #kalo udah pernah pairing
    @classmethod
    def connect_direct(cls, parent_widget):
        ip_port, ok = QInputDialog.getText(
            parent_widget,
            "Wireless Debugging",
            "Masukkan IP:Port dari layar utama Wireless debugging\n"
            "(HP sudah pernah di-pair):",
        )
        if not ok or not ip_port.strip():
            return False

        out = cls._adb(parent_widget, ["connect", ip_port.strip()])
        if "connected" in out.lower() and "cannot" not in out.lower():
            QMessageBox.information(
                parent_widget, "Sukses", f"Berhasil terhubung ke {ip_port}!"
            )
            return True
        QMessageBox.warning(parent_widget, "Gagal", f"Gagal terhubung:\n{out}")
        return False

    
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