import psutil

class SystemMonitor:
    def __init__(self):
        self.total_disk = 0
        self.free_disk = 0
        self.used_disk = 0

    @staticmethod
    def get_size(bytes_):
        """
        Returns size of bytes in a human-readable format
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        for unit in units:
            if bytes_ < 1024:
                return f"{bytes_:.2f} {unit}"
            bytes_ /= 1024
        return bytes_

    def collect_data(self, start_counters):
        self.total_disk = 0
        self.free_disk = 0
        self.used_disk = 0

        cpu_percent = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq().current
        cpu_count = psutil.cpu_count()

        end_counters = psutil.net_io_counters()
        sent = (end_counters.bytes_sent - start_counters.bytes_sent) / 1024**2
        recv = (end_counters.bytes_recv - start_counters.bytes_recv) / 1024**2

        disk_partitions = psutil.disk_partitions()
        for partition in disk_partitions:
            disk_usage = psutil.disk_usage(partition.device)
            self.total_disk += disk_usage.total
            self.free_disk += disk_usage.free
            self.used_disk += disk_usage.used

        percent_disk = (self.used_disk / self.total_disk) * 100
        self.total_disk = self.get_size(self.total_disk)
        self.free_disk = self.get_size(self.free_disk)
        self.used_disk = self.get_size(self.used_disk)
        write_bytes_disk = self.get_size(psutil.disk_io_counters().write_bytes)
        read_bytes_disk = self.get_size(psutil.disk_io_counters().read_bytes)

        memory = psutil.virtual_memory()
        total_mem = self.get_size(memory.total)
        available_mem = self.get_size(memory.available)
        percent_mem = memory.percent
        used_mem = self.get_size(memory.used)
        free_mem = self.get_size(memory.free)

        data = {
            "cpu_percent": cpu_percent,
            "cpu_freq": cpu_freq,
            "cpu_count": cpu_count,
            "sent_network": sent,
            "recv_network": recv,
            "total_disk": self.total_disk,
            "free_disk": self.free_disk,
            "used_disk": self.used_disk,
            "percent_disk": percent_disk,
            "write_bytes_disk": write_bytes_disk,
            "read_bytes_disk": read_bytes_disk,
            "total_memory": total_mem,
            "available_memory": available_mem,
            "percent_memory": percent_mem,
            "used_memory": used_mem,
            "free_memory": free_mem
        }

        return data
