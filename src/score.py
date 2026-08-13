def calculate_score(analysis):
    # Skora 0'dan başlıyoruz, güçlü özellikler geldikçe puan ekleyeceğiz.
    score = 0

    # Uzun parola için daha fazla puan veriyoruz.
    if analysis["length"] >= 12:
        score += 25
    elif analysis["length"] >= 8:
        score += 15
    else:
        score += 5

    # Parolada kaç farklı karakter türü kullanıldığını hesaplıyoruz.
    character_types = sum([
        analysis["has_lowercase"],
        analysis["has_uppercase"],
        analysis["has_digit"],
        analysis["has_special"]
    ])

    # Daha fazla karakter çeşidi, daha geniş bir karakter havuzu demek.
    score += character_types * 5

    # Entropy yükseldikçe parolanın tahmin edilmesi zorlaşıyor.
    if analysis["entropy"] >= 60:
        score += 30
    elif analysis["entropy"] >= 40:
        score += 20
    elif analysis["entropy"] >= 28:
        score += 10

    # Yaygın bir parola olması ciddi bir güvenlik problemi.
    if analysis["is_common"]:
        score -= 30

    # Tekrar veya sıralı yapı varsa puan düşürüyoruz.
    if analysis["patterns"]["has_pattern"]:
        score -= 20

    # Skoru 0-100 arasında tutuyoruz.
    score = max(0, min(score, 100))

    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Moderate"
    else:
        strength = "Weak"

    return {
        "score": score,
        "strength": strength
    }