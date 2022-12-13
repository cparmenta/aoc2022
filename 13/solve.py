FILENAME = 'input'

def compare(left, right):
    print(f' * Compare {left} vs {right}')
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

with open(FILENAME) as file:
    packet_1 = file.readline()
    packet_2 = file.readline()
    _ = file.readline() # Blank line
    packet_index = 1
    sum_correct = 0

    while packet_1 != '':
        print(f'\n == Pair {packet_index} ==')
        packet_1 = eval(packet_1)
        packet_2 = eval(packet_2)

        if compare(packet_1, packet_2):
            sum_correct += packet_index

        packet_1 = file.readline()
        packet_2 = file.readline()
        _ = file.readline() # Blank line
        packet_index += 1

print(f'{sum_correct = }')
