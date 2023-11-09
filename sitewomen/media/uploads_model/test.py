def from_10_to_any(number_after_f, to_number_f):
    translate_number = ""
    while number_after_f != 0:
        if to_number_f < 9:
            remainder = number_after_f % to_number_f
            number_after_f = number_after_f // to_number_f
            translate_number += str(remainder)
        else:
            list_16 = [10, 11, 12, 13, 14, 15]
            list_ABCDEF = ["A", "B", "C", "D", "E", "F"]
            remainder = number_after_f % to_number_f
            if remainder in list_16:
                index = list_16.index(remainder)
                remainder = list_ABCDEF[index]
            number_after_f = number_after_f // to_number_f
            translate_number += str(remainder)
    else:
        translate_number += str(number_after_f)
    return translate_number[-2::-1]


n = int(input())
print(from_10_to_any(n, 2))
print(from_10_to_any(n, 8))
print(from_10_to_any(n, 16))
