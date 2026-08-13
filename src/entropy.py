import math


def calculate_entropy(length, charset_size):
    # Boş parola veya karakter havuzu yoksa hesap yapmanın anlamı yok.
    if length == 0 or charset_size == 0:
        return 0

    # README'de anlattığımız L × log2(K) formülünü uyguluyoruz.
    entropy = length * math.log2(charset_size)

    return entropy