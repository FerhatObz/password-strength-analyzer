from src.entropy import calculate_entropy


def load_common_passwords():
    # Yaygın parolaları dosyadan okuyup bellekte tutuyoruz.
    with open("data/common_passwords.txt", "r", encoding="utf-8") as file:
        return {line.strip() for line in file if line.strip()}


def analyze_password(password):
    # Parolada en az bir küçük harf var mı diye kontrol ediyoruz.
    has_lowercase = any(char.islower() for char in password)

    # Parolada büyük harf var mı?
    has_uppercase = any(char.isupper() for char in password)

    # Parolada rakam var mı?
    has_digit = any(char.isdigit() for char in password)

    # Harf veya rakam olmayan karakterleri özel karakter kabul ediyoruz.
    has_special = any(not char.isalnum() for char in password)

    # Entropy hesabında kullanacağımız karakter havuzunu oluşturuyoruz.
    charset_size = 0

    if has_lowercase:
        charset_size += 26

    if has_uppercase:
        charset_size += 26

    if has_digit:
        charset_size += 10

    if has_special:
        charset_size += 32

    # Karakter havuzu hazır olduktan sonra entropy hesaplıyoruz.
    entropy = calculate_entropy(len(password), charset_size)

    # Yaygın parola listesini yüklüyoruz.
    common_passwords = load_common_passwords()

    # Büyük/küçük harf farkını ortadan kaldırarak karşılaştırıyoruz.
    is_common = password.lower() in common_passwords

    return {
        "length": len(password),
        "has_lowercase": has_lowercase,
        "has_uppercase": has_uppercase,
        "has_digit": has_digit,
        "has_special": has_special,
        "charset_size": charset_size,
        "entropy": entropy,
        "is_common": is_common
    }