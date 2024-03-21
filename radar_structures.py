import struct

class RawScanline:
    def __init__(self, data):
        (
            self.headerLen,
            self.status,
            self.scan_number,
            self.u00,
            self.large_range,
            self.angle,
            self.heading,
            self.small_range,
            self.rotation,
            self.u02,
            self.u03,
            self.data,
        ) = struct.unpack("=BBHHhHHhHiI1024H", data)

class RawSector:
    def __init__(self, data):
        (
            self.stuff,
            self.scanline_count,
            self.scanline_size,
            scanlines,
        ) = struct.unpack(f"=5sBH{self.scanline_count * len(RawScanline(b''))}", data)
        self.lines = [RawScanline(scanline) for scanline in scanlines]

class IPAddress:
    def __init__(self, data):
        self.address, self.port = struct.unpack("=IH", data)

class RadarReport_b201:
    def __init__(self, data):
        (
            self.id,
            self.serialno,
            addr0_data,
            self.u1,
            addr1_data,
            self.u2,
            addr2_data,
            self.u3,
            addr3_data,
            self.u4,
            addr4_data,
            self.u5,
            addrDataA_data,
            self.u6,
            addrSendA_data,
            self.u7,
            addrReportA_data,
            self.u8,
            addrDataB_data,
            self.u9,
            addrSendB_data,
            self.u10,
            addrReportB_data,
            self.u11,
            addr11_data,
            self.u12,
            addr12_data,
            self.u13,
            addr13_data,
            self.u14,
            addr14_data,
            self.u15,
            addr15_data,
            self.u16,
            addr16_data,
        ) = struct.unpack(
            "=H16s6sB12s6sB4s6sB10s6sB4s6sB10s6sB4s6sB4s6sB10s6sB4s6sB4s6sB10s6sB4s6sB4s6sB10s",
            data,
        )
        self.addr0 = IPAddress(addr0_data)
        self.addr1 = IPAddress(addr1_data)
        self.addr2 = IPAddress(addr2_data)
        self.addr3 = IPAddress(addr3_data)
        self.addr4 = IPAddress(addr4_data)
        self.addrDataA = IPAddress(addrDataA_data)
        self.addrSendA = IPAddress(addrSendA_data)
        self.addrReportA = IPAddress(addrReportA_data)
        self.addrDataB = IPAddress(addrDataB_data)
        self.addrSendB = IPAddress(addrSendB_data)
        self.addrReportB = IPAddress(addrReportB_data)
        self.addr11 = IPAddress(addr11_data)
        self.addr12 = IPAddress(addr12_data)
        self.addr13 = IPAddress(addr13_data)
        self.addr14 = IPAddress(addr14_data)
        self.addr15 = IPAddress(addr15_data)
        self.addr16 = IPAddress(addr16_data)

class RadarReport_c402:
    def __init__(self, data):
        (
            self.id,
            self.range,
            self.skip1,
            self.mode,
            self.gain_auto,
            self.skip2,
            self.gain,
            self.sea_clutter_auto,
            self.skip3,
            self.sea_clutter,
            self.skip4,
            self.rain_clutter,
            self.skip5,
            self.interference_rejection,
            self.skip6,
            self.target_expansion,
        ) = struct.unpack("=HLIB3xB3xBL4xB11xB3xB", data)

class RadarReport_c404:
    def __init__(self, data):
        (
            self.what,
            self.command,
            self.field2,
            self.bearing_alignment,
            self.field8,
            self.antenna_height,
            self.unknown,
            self.lights,
        ) = struct.unpack("=BBIHHHxB7xB", data)

class RadarReport_c408:
    def __init__(self, data):
        (
            self.what,
            self.command,
            self.sea_state,
            self.local_interference_rejection,
            self.scan_speed,
            self.sls_auto,
            self.field6,
            self.field7,
            self.field8,
            self.side_lobe_suppression,
            self.field10,
            self.noise_rejection,
            self.target_separation,
            self.field11,
            self.auto_sea_clutter_nudge,
            self.field13,
            self.field14,
            self.doppler_state,
            self.doppler_speed,
        ) = struct.unpack("=BBBBBBBBBBHBBbBBBH", data)

class RangeCmd:
    def __init__(self, range_value=None):
        self.cmd = 0xC103
        if range_value is not None:
            self.range = range_value
        else:
            self.range = 0

    def pack(self):
        return struct.pack("=HI", self.cmd, self.range)

class BearingAlignmentCmd:
    def __init__(self, bearing_alignment=None):
        self.cmd = 0xC105
        if bearing_alignment is not None:
            self.bearing_alignment = bearing_alignment
        else:
            self.bearing_alignment = 0

    def pack(self):
        return struct.pack("=HH", self.cmd, self.bearing_alignment)

class GainCmd:
    def __init__(self, gain_auto=0, gain=0):
        self.cmd = 0xC106
        self.sub_cmd = 0
        self.gain_auto = gain_auto
        self.gain = gain

    def pack(self):
        return struct.pack("=HHIB", self.cmd, self.sub_cmd, self.gain_auto, self.gain)

class SeaClutterCmd:
    def __init__(self, sea_clutter_auto=0, sea_clutter=0):
        self.cmd = 0xC106
        self.sub_cmd = 0x02
        self.sea_clutter_auto = sea_clutter_auto
        self.sea_clutter = sea_clutter

    def pack(self):
        return struct.pack(
            "=HHIIB", self.cmd, self.sub_cmd, self.sea_clutter_auto, self.sea_clutter
        )

class RainClutterCmd:
    def __init__(self, rain_clutter=0):
        self.cmd = 0xC106
        self.sub_cmd = 0x04
        self.blank = 0
        self.rain_clutter = rain_clutter

    def pack(self):
        return struct.pack("=HHIIB", self.cmd, self.sub_cmd, self.blank, self.rain_clutter)

class SidelobeSuppressionCmd:
    def __init__(self, sls_auto=0, sidelobe_suppression=0):
        self.cmd = 0xC106
        self.sub_cmd = 0x05
        self.sls_auto = sls_auto
        self.sidelobe_suppression = sidelobe_suppression

    def pack(self):
        return struct.pack(
            "=HHIIB", self.cmd, self.sub_cmd, self.sls_auto, self.sidelobe_suppression
        )

class EnumCmd:
    def __init__(self, cmd, value):
        self.cmd = cmd
        self.value = value

    def pack(self):
        return struct.pack("=HB", self.cmd, self.value)

class AutoSeaClutterNudgeCmd:
    def __init__(self, nudge):
        self.cmd = 0xC111
        self.sub_cmd = 0x01
        self.nudge1 = nudge
        self.nudge2 = nudge
        self.tail = 0x04

    def pack(self):
        return struct.pack("=HBbbB", self.cmd, self.sub_cmd, self.nudge1, self.nudge2, self.tail)

class DopplerSpeedCmd:
    def __init__(self, speed):
        self.cmd = 0xC124
        self.speed = speed

    def pack(self):
        return struct.pack("=HH", self.cmd, self.speed)

class AntennaHeightCmd:
    def __init__(self, height_mm):
        self.cmd = 0xC130
        self.one = 1
        self.height_mm = height_mm

    def pack(self):
        return struct.pack("=HII", self.cmd, self.one, self.height_mm)

class HaloHeadingPacket:
    def __init__(self, data):
        (
            self.marker,
            self.u00,
            self.counter,
            self.u01,
            self.u02,
            self.u03,
            self.epoch,
            self.u04,
            self.u05a,
            self.u05b,
            self.u06,
            self.heading,
            self.u07,
        ) = struct.unpack("=4s4sH26s2s2sQQ4s4sBH5s", data)

class HaloMysteryPacket:
    def __init__(self, data):
        (
            self.marker,
            self.u00,
            self.counter,
            self.u01,
            self.u02,
            self.u03,
            self.epoch,
            self.u04,
            self.u05a,
            self.u05b,
            self.u06,
            self.u07,
            self.mystery1,
            self.mystery2,
            self.u08,
        ) = struct.unpack("=4s4sH26s2s2sQQ4s4sBBHH2s", data)