def verify_passport(passport_number: str) -> dict:
    """
    Temporary stub for passport verification.
    Replace with Interswitch API integration.
    """

    if passport_number.endswith("0"):
        return {
            "status": "failed",
            "reason": "Passport could not be verified"
        }

    return {
        "status": "verified",
        "reference": "INTSW-123456"
    }
