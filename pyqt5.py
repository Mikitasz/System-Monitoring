import time
import psutil
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit,
    QDialog, QHBoxLayout, QGridLayout, QMainWindow, QAction
)
from system_monitor import SystemMonitor


class OknoMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu')
        self.setGeometry(600, 600, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        opis_label = QLabel("Opis", self)
        opis_label.setStyleSheet(
            "font-size: 16px; color: #333; font-weight: bold; ")
        layout.addWidget(opis_label)

        opis_tekst = QTextEdit(self)
        opis_tekst.setReadOnly(True)
        opis_tekst.setText(
            "Monitor Systemu to prosta aplikacja do monitorowania różnych wskaźników systemowych, takich jak użycie procesora, użycie pamięci, aktywność sieciowa, użycie dysku.")
        layout.addWidget(opis_tekst)

        self.setLayout(layout)


class MojeOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monitor Systemu')
        self.setGeometry(700, 200, 400, 400)
        self.timer_count = 0
        self.initUI()
        self.monitor_object = SystemMonitor()

    def initUI(self):
        layout = QGridLayout()

        cpu_sekcja = QVBoxLayout()
        cpu_sekcja.setSpacing(10)
        self.dodaj_tytul_sekcji(cpu_sekcja, 'CPU')
        self.label_uzyt_proc = self.dodaj_etykiete_sekcji(
            cpu_sekcja, 'Użycie procesora: -%')
        self.label_czest_proc = self.dodaj_etykiete_sekcji(
            cpu_sekcja, 'Częstotliwość procesora: - MHz')
        self.label_liczba_cpu = self.dodaj_etykiete_sekcji(
            cpu_sekcja, "Liczba procesorów: -")

        siec_sekcja = QVBoxLayout()
        siec_sekcja.setSpacing(10)
        self.dodaj_tytul_sekcji(siec_sekcja, 'Sieć')
        self.label_wysl_siec = self.dodaj_etykiete_sekcji(
            siec_sekcja, 'Wysłana sieć: - bajtów')
        self.label_odebr_siec = self.dodaj_etykiete_sekcji(
            siec_sekcja, 'Odebrana sieć: - bajtów')

        self.timer = 1
        self.monitor = SystemMonitor()

        # self.plot_widget = pg.PlotWidget()
        # self.setup_plot_widget()

        dysk_sekcja = QVBoxLayout()
        dysk_sekcja.setSpacing(10)
        self.dodaj_tytul_sekcji(dysk_sekcja, 'Dysk')
        self.label_total_dysk = self.dodaj_etykiete_sekcji(
            dysk_sekcja, 'Pojemność: -Gb')
        self.label_dost_dysk = self.dodaj_etykiete_sekcji(
            dysk_sekcja, 'Dostępno: -Gb')
        self.label_wykorz_dysk = self.dodaj_etykiete_sekcji(
            dysk_sekcja, "Wykorzystano: -GB")
        #self.label_proc_dysk = self.dodaj_etykiete_sekcji(
       #     dysk_sekcja, "Ile jest zajęte: -%")

        pamiec_sekcja = QVBoxLayout()
        pamiec_sekcja.setSpacing(10)
        self.dodaj_tytul_sekcji(pamiec_sekcja, 'Pamięć')
        self.label_total_pamiec = self.dodaj_etykiete_sekcji(
            pamiec_sekcja, 'Całkowita: -Gb')
        self.label_dost_pamiec = self.dodaj_etykiete_sekcji(
            pamiec_sekcja, 'Dostępno: -Gb')
        self.label_proc_pamiec = self.dodaj_etykiete_sekcji(
            pamiec_sekcja, "Ile jest zajęte: -GB")
        self.label_wykorz_pamiec = self.dodaj_etykiete_sekcji(
            pamiec_sekcja, "Wykorzystano: -%")

        layout.addLayout(cpu_sekcja, 0, 0)
        layout.addLayout(siec_sekcja, 1, 0)
      #  layout.addWidget(self.plot_widget, 2, 0, 2, 2)
        layout.addLayout(dysk_sekcja, 0, 1)
        layout.addLayout(pamiec_sekcja, 1, 1)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 0)

        centralny_widget = QWidget()
        centralny_widget.setLayout(layout)
        self.setCentralWidget(centralny_widget)

        self.setStyleSheet("background-color: #f9f9f9;")
        self.update_label()

        pasek_menu = self.menuBar()
        akcja_opisu = QAction('Opis', self)
        akcja_opisu.triggered.connect(self.otworz_menu)
        pasek_menu.addAction(akcja_opisu)

    def dodaj_tytul_sekcji(self, layout, tytul):
        tytul_sekcji = QLabel(tytul, self)
        tytul_sekcji.setStyleSheet(
            "font-size: 18px; color: #333; font-weight: bold;")
        layout.addWidget(tytul_sekcji)

    def dodaj_etykiete_sekcji(self, layout, tekst):
        etykieta = QLabel(tekst, self)
        layout.addWidget(etykieta)
        return etykieta

    def setup_plot_widget(self):
        self.plot_widget.setBackground('#f9f9f9')
        self.plot_widget.setMaximumHeight(110)
        self.plot_widget.setMaximumWidth(350)
        self.plot_data_x = []
        self.plot_data_y = []
        self.plot_data_x2 = []
        self.plot_data_y2 = []
        self.pen = pg.mkPen(width=3, color=(255, 0, 0))
        self.pen2 = pg.mkPen(width=3, color=(0, 0, 255))
        self.timer_count = 0

    def update_label(self):
        start = psutil.net_io_counters()
        time.sleep(self.timer)
        system_info = self.monitor.collect_data(start)

        self.label_uzyt_proc.setText(
            f"Użycie procesora: {system_info['cpu_percent']} %")
        self.label_czest_proc.setText(
            f"Częstotliwość procesora: {system_info['cpu_freq']} MHz")
        self.label_liczba_cpu.setText(
            f"Liczba procesorów: {system_info['cpu_count']}")

        self.label_total_pamiec.setText(
            f"Całkowita pamięć: {system_info['total_memory']} Gb")
        self.label_dost_pamiec.setText(
            f"Dostępna pamięć: {system_info['available_memory']} Gb")
        self.label_proc_pamiec.setText(
            f"Procent wykorzystanej pamięci: {system_info['percent_memory']} %")
        self.label_wykorz_pamiec.setText(
            f"Wykorzystanie pamięci: {system_info['used_memory']} ")

        self.label_total_dysk.setText(
            f"Całkowita przestrzeń dysku: {system_info['total_disk']} Gb")
        self.label_dost_dysk.setText(
            f"Wolna przestrzeń dysku: {system_info['free_disk']} Gb")
        self.label_wykorz_dysk.setText(
            f"Zajęta przestrzeń dysku: {system_info['used_disk']} Gb")
      #  self.label_proc_dysk.setText(
        #   f"Ile jest zajęte: {system_info['percent_disk']:.02f} %")

        self.label_odebr_siec.setText(
            f"Odebrane dane sieciowe: {system_info['recv_network']:.2f} Mb/s")
        self.label_wysl_siec.setText(
            f"Wysłane dane sieciowe: {system_info['sent_network']:.2f} Mb/s")

        # self.plot_data_x.append(self.timer_count)
       # self.plot_data_y.append(int(system_info['recv_network']))
       # self.plot_data_x2.append(self.timer_count)
       # self.plot_data_y2.append(int(system_info['sent_network']))
        # self.plot_widget.plot(
        #    self.plot_data_x, self.plot_data_y, pen=self.pen, clear=True)
      #  self.plot_widget.plot(
        #    self.plot_data_x2, self.plot_data_y2, pen=self.pen2)

        self.timer_count += 3
        QTimer.singleShot(3000, self.update_label)

    def otworz_menu(self):
        okno_menu = OknoMenu()
        okno_menu.exec_()


if __name__ == '__main__':
    app = QApplication([])
    okno = MojeOkno()
    okno.show()
    app.exec_()
