import crc

test_value = [1, 1, 1, 42, 2]

ret = crc.crc16_ccitt(test_value, 5)

print(bin(ret))
print(hex(ret))
