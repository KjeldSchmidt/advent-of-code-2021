from dataclasses import dataclass
from typing import Union

import numpy as np
transmission = "620080001611562C8802118E34"


@dataclass
class Packet:
    full_body: str
    length: int
    type: int
    content: str
    version: int
    decoded_content: Union[int, list["Packet"]]


def char_to_bits(char) -> str:
    dec = ord(char)
    if 48 <= dec <= 57:
        num = dec - 48
    elif 65 <= dec <= 70:
        num = dec - 55
    else:
        raise ValueError()

    return np.binary_repr(num, width=4)


def get_version_number(packet) -> str:
    return packet[:3]


def get_type_id(packet) -> str:
    return packet[3:6]


def extract_first_packet(packet_string: str) -> Packet:
    if get_type_id(packet_string) == "100":
        return extract_literal_packet(packet_string)

    length_type_id = packet_string[6]
    subpacket_length_bit_count = 11 if length_type_id == "1" else 15
    subpacket_length_string = packet_string[7:7 + subpacket_length_bit_count]
    if subpacket_length_string == "":
        raise NotImplementedError
    subpacket_length = int(subpacket_length_string, 2)

    sub_packet_bodies = packet_string[7 + subpacket_length_bit_count:]
    if length_type_id == "0":
        decoded_content = get_sub_packets_by_length(sub_packet_bodies, subpacket_length)
    else:
        decoded_content = get_sub_packets_by_count(sub_packet_bodies, subpacket_length)

    content = "".join(map(lambda x: x.full_body, decoded_content))
    length = 7 + len(content) + subpacket_length_bit_count
    packet = Packet(
        version=int(packet_string[:3], 2),
        type=int(packet_string[3:6], 2),
        full_body=packet_string[:length],
        content=content,
        decoded_content=decoded_content,
        length=length
    )

    return packet


def get_sub_packets_by_length(packet_bodies: str, length: int) -> list[Packet]:
    sub_packets = []
    while sum(map(lambda x: x.length, sub_packets)) != length:
        new_sub_packet = extract_first_packet(packet_bodies)
        sub_packets.append(new_sub_packet)
        packet_bodies = packet_bodies[new_sub_packet.length:]

    return sub_packets


def get_sub_packets_by_count(packet_bodies, count) -> list[Packet]:
    sub_packets = []
    while len(sub_packets) != count:
        new_sub_packet = extract_first_packet(packet_bodies)
        sub_packets.append(new_sub_packet)
        packet_bodies = packet_bodies[new_sub_packet.length:]

    return sub_packets


def extract_literal_packet(packet_string: str) -> Packet:
    continue_bit_index = 6

    content_to_decode = []
    while packet_string[continue_bit_index] == "1":
        content_to_decode.append(packet_string[continue_bit_index + 1:continue_bit_index + 5])
        continue_bit_index += 5

    content_to_decode.append(packet_string[continue_bit_index + 1:continue_bit_index + 5])
    content_to_decode = "".join(content_to_decode)
    decoded_content = int(content_to_decode, 2)

    packet = Packet(
        version=int(packet_string[:3], 2),
        type=4,
        full_body=packet_string[:continue_bit_index + 5],
        content=packet_string[6:continue_bit_index + 5],
        decoded_content=decoded_content,
        length=continue_bit_index+5
    )

    return packet


def packets_from_hex(transmission) -> Packet:
    transmission = "".join([char_to_bits(char) for char in transmission])
    return extract_first_packet(transmission)


def version_sum(packet: Packet) -> int:
    if packet.type == 4:
        return packet.version
    else:
        return packet.version + sum(map(version_sum, packet.decoded_content))


def calculate_packet_value(packet: Packet) -> int:
    operations = {
        0: np.sum,
        1: np.prod,
        2: np.min,
        3: np.max,
        5: lambda x: 1 if x[0] > x[1] else 0,
        6: lambda x: 1 if x[0] < x[1] else 0,
        7: lambda x: 1 if x[0] == x[1] else 0,
    }

    if packet.type == 4:
        return packet.decoded_content
    else:
        child_values: list[int] = list(map(calculate_packet_value, packet.decoded_content))
        return operations[packet.type](child_values)


def dev():
    packet = packets_from_hex(open("16-input.txt", "r").readline().strip())
    print("Solution part 1:")
    print(version_sum(packet))
    print("Solution part 2:")
    print(calculate_packet_value(packet))


def tests():
    assert packets_from_hex("D2FE28") == Packet(
        full_body="110100101111111000101",
        length=21,
        type=4,
        version=6,
        decoded_content=2021,
        content="101111111000101"
    )
    assert version_sum(packets_from_hex("620080001611562C8802118E34")) == 12
    assert version_sum(packets_from_hex("C0015000016115A2E0802F182340")) == 23
    assert version_sum(packets_from_hex("A0016C880162017C3686B18A3D4780")) == 31
    assert version_sum(packets_from_hex("8A004A801A8002F478")) == 16

    assert calculate_packet_value(packets_from_hex("C200B40A82")) == 3
    assert calculate_packet_value(packets_from_hex("04005AC33890")) == 54
    assert calculate_packet_value(packets_from_hex("D8005AC2A8F0")) == 1


tests()
dev()
