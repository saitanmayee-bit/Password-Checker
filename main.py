def check_password(password):
    score = 0
    suggestions = []
    warnings = []

    if not password:
        return 0, "Invalid", ["Enter a password."], []

    # 1. Length checks
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Aim for at least 12 characters.")

    # 2. Character variety
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)

    if has_upper and has_lower:
        score += 1
    else:
        suggestions.append("Use uppercase and lowercase letters.")

    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        suggestions.append("Consider including a number.")

    if any(not ch.isalnum() and not ch.isspace() for ch in password):
        score += 1
    else:
        suggestions.append("Consider including a special character.")

    # 3. Normalize for common-password checks
    normalized = "".join(ch for ch in password.lower() if ch.isalnum())

    common_passwords = {
        "password",
        "password123",
        "123456",
        "123456789",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "letmein",
        "welcome",
        "welcome123",
        "iloveyou",
        "abc123",
        "monkey",
        "dragon",
        "football",
        "princess",
        "sunshine",
        "login",
        "secret",
    }

    common_terms = {
        "password",
        "qwerty",
        "letmein",
        "welcome",
        "iloveyou",
        "admin",
        "monkey",
        "dragon",
        "football",
        "princess",
        "sunshine",
    }

    is_common = normalized in common_passwords or any(
        term in normalized for term in common_terms
    )

    if is_common:
        warnings.append(
            "This is a commonly used password or contains a common password phrase."
        )
        suggestions.append("Avoid common words and familiar password phrases.")

    # 4. Detect keyboard patterns
    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qwert",
        "werty",
        "asdfg",
        "sdfgh",
        "zxcvb",
        "12345",
        "98765",
    ]

    if any(pattern in normalized for pattern in keyboard_patterns):
        warnings.append("A predictable keyboard or number pattern was detected.")
        suggestions.append("Avoid keyboard walks and number sequences.")

    # 5. Detect ascending/descending letter or number sequences
    sequence_found = False

    for i in range(len(normalized) - 2):
        a, b, c = normalized[i : i + 3]

        same_type = (a.isdigit() and b.isdigit() and c.isdigit()) or (
            a.isalpha() and b.isalpha() and c.isalpha()
        )

        if same_type:
            values = [ord(a), ord(b), ord(c)]

            if (values[1] == values[0] + 1 and values[2] == values[1] + 1) or (
                values[1] == values[0] - 1 and values[2] == values[1] - 1
            ):
                sequence_found = True
                break

    if sequence_found:
        warnings.append("A predictable sequence was detected.")
        suggestions.append("Avoid consecutive letters or numbers such as abc or 321.")

    # 6. Detect repeated characters
    repeated = any(
        password[i] == password[i + 1] == password[i + 2]
        for i in range(len(password) - 2)
    )

    if repeated:
        warnings.append("Repeated characters were detected.")
        suggestions.append("Avoid repeating the same character three or more times.")

    # 7. Base rating
    if score <= 2:
        rating = "Weak"
    elif score == 3:
        rating = "Moderate"
    elif score == 4:
        rating = "Strong"
    else:
        rating = "Very Strong"

    # 8. Apply warning limits
    if is_common:
        rating = "Weak"
    elif warnings and rating in ("Strong", "Very Strong"):
        rating = "Moderate"

    return score, rating, suggestions, warnings
