import time
import psutil
from gi.repository import Gtk, GLib, Pango
import gi
from system_monitor import SystemMonitor
gi.require_version('Gtk', '3.0')

# Stałe
UPDATE_INTERVAL = 3  # Interwał aktualizacji w sekundach


class OknoMenu(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "O programie", parent, 0)

        self.set_default_size(50, 100)
        self.set_border_width(10)
        text = 'System Monitor to prosta aplikacja do monitorowania różnych\nwskaźników systemowych, takich jak użycie procesora,\nużycie pamięci, aktywność sieciowa, użycie dysku.'

        label = Gtk.Label(label=text)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class MojeOkno(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Monitor Systemu")
        self.set_default_size(400, 400)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        grid.set_border_width(10)
        self.add(grid)

        self.monitor_object = SystemMonitor()
        self.create_menu()

        # Sekcja CPU
        cpu_title = self.create_title_label("CPU")
        grid.attach(cpu_title, 0, 1, 1, 1)

        # Etykiety dla informacji o CPU
        self.label_CPU_percent = self.create_info_label("Użycie procesora: -%")
        grid.attach(self.label_CPU_percent, 0, 2, 1, 1)
        self.label_cpu_freq = self.create_info_label(
            "Częstotliwość procesora: - MHz")
        grid.attach(self.label_cpu_freq, 0, 3, 1, 1)
        self.label_cpu_count = self.create_info_label("Liczba procesorów: -")
        grid.attach(self.label_cpu_count, 0, 4, 1, 1)

        # Sekcja Sieci
        network_title = self.create_title_label("Sieć")
        grid.attach(network_title, 0, 7, 1, 1)

        # Etykiety dla informacji o sieci
        self.label_sent_network = self.create_info_label(
            "Wysłane dane sieciowe: - bajtów")
        grid.attach(self.label_sent_network, 0, 8, 1, 1)
        self.label_recv_network = self.create_info_label(
            "Odebrane dane sieciowe: - bajtów")
        grid.attach(self.label_recv_network, 0, 9, 1, 1)

        # Sekcja Dysku
        disk_title = self.create_title_label("Dysk")
        grid.attach(disk_title, 2, 1, 1, 1)

        # Etykiety dla informacji o dysku
        self.label_total_disk = self.create_info_label(
            'Całkowita przestrzeń dysku: -GB')
        grid.attach(self.label_total_disk, 2, 2, 1, 1)
        self.label_free_disk = self.create_info_label(
            'Wolna przestrzeń dysku: -GB')
        grid.attach(self.label_free_disk, 2, 3, 1, 1)
        self.label_used_disk = self.create_info_label(
            "Zajęta przestrzeń dysku: -GB")
        grid.attach(self.label_used_disk, 2, 4, 1, 1)

        # Sekcja Pamięci
        mem_title = self.create_title_label("Pamięć")
        grid.attach(mem_title, 2, 7, 1, 1)

        # Etykiety dla informacji o pamięci
        self.label_total_memory = self.create_info_label(
            'Całkowita pamięć: -GB')
        grid.attach(self.label_total_memory, 2, 8, 1, 1)
        self.label_available_memory = self.create_info_label(
            'Dostępna pamięć: -GB')
        grid.attach(self.label_available_memory, 2, 9, 1, 1)
        self.label_percent_memory = self.create_info_label(
            "Procent wykorzystanej pamięci: -GB")
        grid.attach(self.label_percent_memory, 2, 10, 1, 1)
        self.label_used_memory = self.create_info_label(
            "Wykorzystanie pamięci: -%")
        grid.attach(self.label_used_memory, 2, 11, 1, 1)

        self.update_labels()
        GLib.timeout_add_seconds(UPDATE_INTERVAL, self.update_labels)

    def create_title_label(self, text):
        label = Gtk.Label(label=text)
        label.set_halign(Gtk.Align.START)
        label.set_use_markup(True)
        label.modify_font(Pango.FontDescription("bold"))
        return label

    def create_info_label(self, text):
        label = Gtk.Label(label=text)
        label.set_halign(Gtk.Align.START)
        return label

    def update_labels(self):
        start = psutil.net_io_counters()
        time.sleep(1)
        system_info = self.monitor_object.collect_data(start)

        cpu_percent = str(system_info['cpu_percent'])
        cpu_freq = str(system_info['cpu_freq'])
        cpu_count = str(system_info['cpu_count'])
        recv_network = str(system_info['recv_network'])
        sent_network = str(system_info['sent_network'])
        total_disk = str(system_info['total_disk'])
        free_disk = str(system_info['free_disk'])
        used_disk = str(system_info['used_disk'])
        percent_disk = str(system_info['percent_disk'])
        total_memory = str(system_info['total_memory'])
        available_memory = str(system_info['available_memory'])
        percent_memory = str(system_info['percent_memory'])
        used_memory = str(system_info['used_memory'])

        self.label_CPU_percent.set_text(f"Użycie CPU: {cpu_percent} %")
        self.label_cpu_freq.set_text(f"Częstotliwość CPU: {cpu_freq} MHz")
        self.label_cpu_count.set_text(f"Liczba CPU: {cpu_count}")

        self.label_total_memory.set_text(f"Całkowita pamięć: {total_memory}")
        self.label_available_memory.set_text(
            f"Dostępna pamięć: {available_memory}")
        self.label_percent_memory.set_text(
            f"Procent wykorzystanej pamięci: {percent_memory} %")
        self.label_used_memory.set_text(
            f"Wykorzystanie pamięci: {used_memory}")

        self.label_total_disk.set_text(
            f"Całkowita przestrzeń dysku: {total_disk}")
        self.label_free_disk.set_text(f"Wolna przestrzeń dysku: {free_disk}")
        self.label_used_disk.set_text(f"Zajęta przestrzeń dysku: {used_disk}")

        self.label_recv_network.set_text(
            f"Odebrane dane sieciowe: {float(recv_network):.2f} Mb/s")
        self.label_sent_network.set_text(
            f"Wysłane dane sieciowe: {float(sent_network):.2f} Mb/s")

        return True

    def create_menu(self):
        menubar = Gtk.MenuBar()

        about_menu = Gtk.MenuItem(label="O programie")
        about_menu.connect("activate", self.on_about_clicked)
        menubar.append(about_menu)

        grid = self.get_children()[0]
        grid.attach(menubar, 0, 0, 4, 1)

    def on_about_clicked(self, widget):

        dialog = OknoMenu(self)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.run()
        dialog.destroy()


win = MojeOkno()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
