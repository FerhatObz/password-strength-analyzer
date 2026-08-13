def has_repeated_characters(password):
    # Aynı karakter sürekli tekrar ediyorsa parolanın yapısı tahmin edilebilir.
    if len(password) < 3:
        return False

    return len(set(password)) == 1


def has_repeated_sequence(password):
    # "ababab" veya "123123" gibi kendini tekrar eden yapıları yakalamaya çalışıyoruz.
    length = len(password)

    for size in range(1, length // 2 + 1):
        if length % size != 0:
            continue

        part = password[:size]
        repeat_count = length // size

        if part * repeat_count == password:
            return True

    return False


def has_sequential_characters(password):
    # 123456 veya abcdef gibi sıralı karakterleri kontrol ediyoruz.
    if len(password) < 3:
        return False

    for i in range(len(password) - 2):
        first = ord(password[i])
        second = ord(password[i + 1])
        third = ord(password[i + 2])

        if second == first + 1 and third == second + 1:
            return True

        if second == first - 1 and third == second - 1:
            return True

    return False


def analyze_patterns(password):
    # Üç farklı pattern kontrolünün sonucunu tek yerde topluyoruz.
    repeated_characters = has_repeated_characters(password)
    repeated_sequence = has_repeated_sequence(password)
    sequential_characters = has_sequential_characters(password)

    return {
        "repeated_characters": repeated_characters,
        "repeated_sequence": repeated_sequence,
        "sequential_characters": sequential_characters,
        "has_pattern": (
            repeated_characters
            or repeated_sequence
            or sequential_characters
        )
    }