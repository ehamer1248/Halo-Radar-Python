import socket
import struct
import threading
import time
import sys
from radar_structures import *

class AddressSet:
    def __init__(self):
        self.label = ""
        self.data = None
        self.send = None
        self.report = None
        self.interface = None

    def __str__(self):
        return f"{self.label}: data: {ip_address_to_string(self.data.address)}:{self.data.port}, report: {ip_address_to_string(self.report.address)}:{self.report.port}, send: {ip_address_to_string(self.send.address)}:{self.send.port}, interface: {ip_address_to_string(self.interface)}"

class Radar:
    def __init__(self, addresses):
        self.m_addresses = addresses
        self.m_exit_flag = False
        self.m_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.m_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.m_send_address = (self.m_addresses.interface, 0)
        self.m_send_socket.bind(self.m_send_address)
        self.m_send_address = (socket.inet_ntoa(struct.pack("!I", self.m_addresses.send.address)), self.m_addresses.send.port)
        self.send_heartbeat()

    def start_threads(self):
        self.m_data_thread = threading.Thread(target=self.data_thread)
        self.m_report_thread = threading.Thread(target=self.report_thread)
        self.m_data_thread.start()
        self.m_report_thread.start()

    def data_thread(self):
        # Implement data thread functionality
        pass

    def report_thread(self):
        # Implement report thread functionality
        pass


    def create_listener_socket(self, interface, mcast_address, port):
        # Implement listener socket creation
        pass

    def process_data(self, scanlines):
        # Implement data processing logic
        pass

    def send_command_raw(self, data, size):
        self.m_send_socket.sendto(data, self.m_send_address)

    def send_heartbeat(self):
        data1 = bytes([0xa0, 0xc1])
        self.send_command_raw(data1, len(data1))

        data2 = bytes([0x03, 0xc2])
        self.send_command_raw(data2, len(data2))

        data3 = bytes([0x04, 0xc2])
        self.send_command_raw(data3, len(data3))

        data4 = bytes([0x05, 0xc2])
        self.send_command_raw(data4, len(data4))

        self.m_last_heartbeat = time.monotonic()

    def check_heartbeat(self):
        elapsed = time.monotonic() - self.m_last_heartbeat
        if elapsed > 1.0:
            self.send_heartbeat()
            return True
        return False

    def send_command_key_value(self, key, value):
        if key == "status":
            if value == "transmit":
                data1 = bytes([0x00, 0xc1, 0x01])
                self.send_command_raw(data1, len(data1))
                data2 = bytes([0x01, 0xc1, 0x01])
                self.send_command_raw(data2, len(data2))
            elif value == "standby":
                data1 = bytes([0x00, 0xc1, 0x01])
                self.send_command_raw(data1, len(data1))
                data2 = bytes([0x01, 0xc1, 0x00])
                self.send_command_raw(data2, len(data2))

        if key == "range":
            cmd = RangeCmd()
            cmd.range = float(value) * 10
            self.send_command_raw(cmd)

        if key == "bearing_alignment":
            cmd = BearingAlignmentCmd()
            cmd.bearing_alignment = float(value) * 10
            self.send_command_raw(cmd)

        if key == "gain":
            cmd = GainCmd()
            if value == "auto":
                cmd.gain_auto = 1
            else:
                cmd.gain = float(value) * 255 / 100
            self.send_command_raw(cmd)

        if key == "sea_clutter":
            cmd = SeaClutterCmd()
            if value == "auto":
                cmd.sea_clutter_auto = 1
            else:
                cmd.sea_clutter = float(value) * 255 / 100
            self.send_command_raw(cmd)

        if key == "rain_clutter":
            cmd = RainClutterCmd()
            cmd.rain_clutter = float(value) * 255 / 100
            self.send_command_raw(cmd)

        if key == "sidelobe_suppression":
            cmd = SidelobeSuppressionCmd()
            if value == "auto":
                cmd.sls_auto = 1
            else:
                cmd.sidelobe_suppression = float(value) * 255 / 100
            self.send_command_raw(cmd)

        lmh_map = {
            "off": 0,
            "low": 1,
            "medium": 2,
            "high": 3
        }

        if key == "interference_rejection":
            cmd = EnumCmd(0xc108, lmh_map[value])
            self.send_command_raw(cmd)

        if key == "sea_state":
            cmd = EnumCmd(0xc10b, 0)
            if value == "moderate":
                cmd.value = 1
            if value == "rough":
                cmd.value = 2
            self.send_command_raw(cmd)

        if key == "scan_speed":
            cmd = EnumCmd(0xc10f, 0)
            if value == "medium":
                cmd.value = 1
            if value == "high":
                cmd.value = 3
            self.send_command_raw(cmd)

        if key == "mode":
            cmd = EnumCmd(0xc110, 0)
            if value == "harbor":
                cmd.value = 1
            if value == "offshore":
                cmd.value = 2
            if value == "weather":
                cmd.value = 4
            if value == "bird":
                cmd.value = 5
            self.send_command_raw(cmd)

        if key == "auto_sea_clutter_nudge":
            cmd = AutoSeaClutterNudgeCmd(float(value))
            self.send_command_raw(cmd)

        if key == "target_expansion":
            cmd = EnumCmd(0xc112, lmh_map[value])
            self.send_command_raw(cmd)

        if key == "noise_rejection":
            cmd = EnumCmd(0xc121, lmh_map[value])
            self.send_command_raw(cmd)

        if key == "target_separation":
            cmd = EnumCmd(0xc122, lmh_map[value])
            self.send_command_raw(cmd)

        if key == "doppler_mode":
            cmd = EnumCmd(0xc123, 0)
            if value == "normal":
                cmd.value = 1
            if value == "approaching_only":
                cmd.value = 2
            self.send_command_raw(cmd)

        if key == "doppler_speed":
            cmd = DopplerSpeedCmd(float(value) * 100)
            self.send_command_raw(cmd)

        if key == "antenna_height":
            cmd = AntennaHeightCmd(float(value) * 1000)
            self.send_command_raw(cmd)

        if key == "lights":
            cmd = EnumCmd(0xc131, lmh_map[value])
            self.send_command_raw(cmd)

    def state_updated(self):
        # Implement state update logic
        pass


def scan():
    return scan(get_local_addresses())

def scan(addresses):
    ret = []
    for a in addresses:
        print(f"local interface: {ip_address_to_string(a)}", file=sys.stderr)
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if listen_sock < 0:
            print("socket error", file=sys.stderr)
            continue

        listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listen_sock.settimeout(1)

        listen_address = ('', 6878)
        try:
            listen_sock.bind(listen_address)
        except socket.error as e:
            print(f"bind error: {e}", file=sys.stderr)
            listen_sock.close()
            continue

        mreq = struct.pack("4sL", socket.inet_aton("236.6.7.5"), socket.INADDR_ANY)
        listen_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        send_address = (socket.inet_ntoa(struct.pack("!I", a)), 0)
        try:
            send_sock.bind(send_address)
        except socket.error as e:
            print(f"bind error: {e}", file=sys.stderr)
            listen_sock.close()
            send_sock.close()
            continue

        data = struct.pack("!H", 0xb101)
        send_address = ("236.6.7.5", 6878)
        try:
            send_sock.sendto(data, send_address)
        except socket.error as e:
            print(f"sendto error: {e}", file=sys.stderr)
            listen_sock.close()
            send_sock.close()
            continue

        count = 0
        while count < 3:
            try:
                in_data, from_addr = listen_sock.recvfrom(1024)
                nbytes = len(in_data)
                if nbytes > 0:
                    print(f"{nbytes} bytes", file=sys.stderr)
                    print(f"is it {RadarReport_b201.size} bytes and start with b201?", file=sys.stderr)
                    if nbytes == RadarReport_b201.size and in_data[:2] == b'\xb2\x01':
                        b201 = RadarReport_b201.from_buffer_copy(in_data)
                        asa = AddressSet()
                        asa.label = "HaloA"
                        asa.data = b201.addrDataA
                        asa.send = b201.addrSendA
                        asa.report = b201.addrReportA
                        asa.interface = a
                        ret.append(asa)
                        asb = AddressSet()
                        asb.label = "HaloB"
                        asb.data = b201.addrDataB
                        asb.send = b201.addrSendB
                        asb.report = b201.addrReportB
                        asb.interface = a
                        ret.append(asb)
                        break
            except socket.timeout:
                pass
            count += 1

        listen_sock.close()
        send_sock.close()
        if ret:
            break

    return ret

def get_local_addresses():
    local_addresses = []
    try:
        for interface in socket.if_nameindex():
            ifname = interface[1]
            addr = socket.inet_ntoa(fcntl.ioctl(
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15].encode())
            )[20:24])
            local_addresses.append(ip_address_from_string(addr))
    except OSError:
        pass
    return local_addresses

def ip_address_to_string(address):
    return socket.inet_ntoa(struct.pack("!I", address))

def ip_address_from_string(address_str):
    return struct.unpack("!I", socket.inet_aton(address_str))[0]