import CRC16

test_value = [1, 1, 1, 42, 2]

ret = CRC16.crc16_ccitt(test_value, 5)

print(bin(ret))
print(hex(ret))
