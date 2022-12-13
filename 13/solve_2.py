from functools import cmp_to_key

FILENAME = 'input'

def compare(left, right):
    result = None
    if isinstance(left, int) and isinstance(right, int):
        result = left <= right
    elif isinstance(left, list) and isinstance(right, list):
        if left and right:
            if left[0] == right[0]:
                result = compare(left[1:], right[1:])
            else:
                result = compare(left[0], right[0])
        else:
            result = not left
    else:
        left_l = [left] if isinstance(left, int) else left
        right_l = [right] if isinstance(right, int) else right
        result = compare(left_l, right_l)
    return result

def compare2(left, right):
    if left == right:
        return 0
    else:
        return -1 if compare(left, right) else 1

list_packets = []
with open(FILENAME) as file:
    packet_1 = file.readline()
    packet_2 = file.readline()
    _ = file.readline() # Blank line
    packet_index = 1

    while packet_1 != '':
        print(f'\n == Pair {packet_index} ==')
        list_packets.append(eval(packet_1))
        list_packets.append(eval(packet_2))

        packet_1 = file.readline()
        packet_2 = file.readline()
        _ = file.readline() # Blank line
        packet_index += 1


# Append divider packets, I hope they are unique...
list_packets.append([[2]])
list_packets.append([[6]])

list_packets.sort(key=cmp_to_key(compare2))

print('list_packets sorted:')
for packet in list_packets:
    print(packet)

divider_idx_1 = list_packets.index([[2]]) + 1
divider_idx_2 = list_packets.index([[6]]) + 1

print(f'Answer = {divider_idx_1 * divider_idx_2 = }')
