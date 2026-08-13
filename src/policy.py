def evaluate_policy(analysis):
    # Başlangıçta parolayı uygun kabul ediyoruz.
    passed = True
    issues = []

    # Çok kısa parolaları direkt sorun olarak kabul ediyoruz.
    if analysis["length"] < 8:
        passed = False
        issues.append("Password is too short.")

    # En az üç farklı karakter grubu kullanılmasını istiyoruz.
    character_types = sum([
        analysis["has_lowercase"],
        analysis["has_uppercase"],
        analysis["has_digit"],
        analysis["has_special"]
    ])

    if character_types < 3:
        passed = False
        issues.append("Use at least three different character types.")

    # Yaygın bir parola kullanılıyorsa bunu önemli bir zayıflık sayıyoruz.
    if analysis["is_common"]:
        passed = False
        issues.append("Password is commonly used.")

    # Basit tekrar veya sıralı yapı varsa parolanın tahmin edilmesi kolaylaşabilir.
    if analysis["patterns"]["has_pattern"]:
        passed = False
        issues.append("Password contains a predictable pattern.")

    return {
        "passed": passed,
        "issues": issues
    }