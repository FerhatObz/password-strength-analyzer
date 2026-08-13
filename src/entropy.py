import math


def calculate_entropy(length, charset_size):
    # Boş parola veya karakter havuzu yoksa entropy hesaplayamayız.
    if length == 0 or charset_size == 0:
        return 0

    # Entropy formülünü Python'da uyguluyoruz.
    entropy = length * math.log2(charset_size)

    return entropy