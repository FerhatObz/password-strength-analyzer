from getpass import getpass

from src.analyzer import analyze_password


def show_analysis(result):
    print("\nPassword Analysis")
    print("-----------------")

    print(f"Length: {result['length']}")
    print(f"Character Set Size: {result['charset_size']}")
    print(f"Entropy: {result['entropy']:.2f} bits")

    common_status = "Yes" if result["is_common"] else "No"
    print(f"Common Password: {common_status}")

    pattern_status = "Yes" if result["patterns"]["has_pattern"] else "No"
    print(f"Pattern Detected: {pattern_status}")

    policy_status = "Passed" if result["policy"]["passed"] else "Failed"
    print(f"Policy: {policy_status}")

    print(f"Score: {result['score']['score']}/100")
    print(f"Strength: {result['score']['strength']}")

    if result["policy"]["issues"]:
        print("\nIssues:")
        for issue in result["policy"]["issues"]:
            print(f"- {issue}")


def main():
    # Parolayı normal input yerine getpass ile alıyoruz.
    password = getpass("Password: ")

    # Girilen parolayı analiz motorumuza gönderiyoruz.
    result = analyze_password(password)

    show_analysis(result)


if __name__ == "__main__":
    main()