from __future__ import annotations

from nigeria_network_detector.detector import detect_network, normalize_phone_number


class TestNormalizePhoneNumber:
    def test_local_format(self):
        result = normalize_phone_number("09050003328")
        assert result.valid
        assert result.national == "09050003328"
        assert result.e164 == "+2349050003328"

    def test_plus_234_format(self):
        result = normalize_phone_number("+2349050003328")
        assert result.valid
        assert result.national == "09050003328"
        assert result.e164 == "+2349050003328"

    def test_234_format_no_plus(self):
        result = normalize_phone_number("2349050003328")
        assert result.valid
        assert result.e164 == "+2349050003328"

    def test_spaces(self):
        assert normalize_phone_number("0905 000 3328").valid

    def test_dashes(self):
        assert normalize_phone_number("0905-000-3328").valid

    def test_mixed_spacing_and_parens(self):
        assert normalize_phone_number("(0905) 000-3328").valid

    def test_empty_input(self):
        result = normalize_phone_number("")
        assert not result.valid
        assert result.e164 == ""

    def test_letters(self):
        assert not normalize_phone_number("abcde12345f").valid

    def test_special_characters(self):
        assert not normalize_phone_number("0905$$$3328!!").valid

    def test_too_long(self):
        assert not normalize_phone_number("0" * 40).valid

    def test_too_short(self):
        assert not normalize_phone_number("0803000").valid

    def test_missing_leading_zero_on_local_number(self):
        # "905 000 3328" (10 digits, no leading 0 and no 234) is ambiguous
        # and intentionally rejected rather than guessed at.
        assert not normalize_phone_number("9050003328").valid


class TestDetectNetwork:
    def test_glo_prefix(self):
        result = detect_network("09050003328")
        assert result.prefix == "0905"
        assert result.provider is not None
        assert result.provider.slug == "glo"

    def test_mtn_prefix(self):
        result = detect_network("08030000000")
        assert result.provider is not None
        assert result.provider.slug == "mtn"

    def test_airtel_prefix(self):
        result = detect_network("08020000000")
        assert result.provider is not None
        assert result.provider.slug == "airtel"

    def test_9mobile_prefix(self):
        result = detect_network("08090000000")
        assert result.provider is not None
        assert result.provider.slug == "9mobile"

    def test_unsupported_prefix(self):
        result = detect_network("08990000000")
        assert result.normalized.valid
        assert result.provider is None

    def test_invalid_number_has_no_provider(self):
        result = detect_network("not-a-number")
        assert not result.normalized.valid
        assert result.provider is None
        assert result.prefix == ""

    def test_ported_number_caveat_is_structural_not_claimed(self):
        # detect_network only ever reports the *original* allocated
        # network — there's no current_network/ported field here at all,
        # which is the point: that claim belongs to a real MNP lookup,
        # not to prefix matching.
        result = detect_network("09050003328")
        assert not hasattr(result, "current_network")
        assert not hasattr(result, "ported")
