<<<<<<< HEAD
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from nigeria_network_detector.detector import (
	clean_phone_number,
	detect_nigerian_network,
	validate_nigerian_number,
)


@pytest.mark.parametrize(
	("phone_number", "expected"),
	[
		("0803 123 4567", "08031234567"),
		("+234 803 123 4567", "08031234567"),
		(2348031234567, "08031234567"),
		("(0803)-123-4567", "08031234567"),
	],
)
def test_clean_phone_number_normalizes_common_formats(phone_number, expected):
	assert clean_phone_number(phone_number) == expected


@pytest.mark.parametrize(
	("number", "expected"),
	[
		("08031234567", (True, "Valid")),
		("8031234567", (False, "Number must be 11 digits")),
		("18031234567", (False, "Number must start with 0")),
		("0803123456a", (False, "Number must contain only digits")),
	],
)
def test_validate_nigerian_number(number, expected):
	assert validate_nigerian_number(number) == expected


@pytest.mark.parametrize(
	("phone_number", "expected_network"),
	[
		("08031234567", "MTN"),
		("07025123456", "MTN"),
		("08051234567", "Glo"),
		("08021234567", "Airtel"),
		("08091234567", "9mobile"),
		("08041234567", "Ntel"),
		("07021234567", "Smile"),
	],
)
def test_detect_nigerian_network_returns_matching_provider(
	phone_number, expected_network
):
	assert detect_nigerian_network(phone_number) == expected_network


def test_detect_nigerian_network_accepts_international_format():
	assert detect_nigerian_network("+234 803 123 4567") == "MTN"


def test_detect_nigerian_network_reports_unknown_prefix():
	assert detect_nigerian_network("08991234567") == "Unknown network"


def test_detect_nigerian_network_reports_invalid_number():
	assert (
		detect_nigerian_network("12345")
		== "Invalid Nigerian number format: Number must be 11 digits"
	)
=======
"""Unit tests for the pure detection logic in `detector.py`."""

from __future__ import annotations

import pytest

from nigeria_network_detector.detector import (
    NETWORK_PREFIXES,
    clean_phone_number,
    detect_nigerian_network,
    get_network_prefixes,
    validate_nigerian_number,
)


class TestCleanPhoneNumber:
    def test_local_format_unchanged(self):
        assert clean_phone_number("08031234567") == "08031234567"

    def test_strips_spaces(self):
        assert clean_phone_number("0803 123 4567") == "08031234567"

    def test_strips_dashes_and_parens(self):
        assert clean_phone_number("(0803)-123-4567") == "08031234567"

    def test_international_plus_format(self):
        assert clean_phone_number("+2348031234567") == "08031234567"

    def test_international_no_plus_format(self):
        assert clean_phone_number("2348031234567") == "08031234567"

    def test_bare_ten_digit_format(self):
        # No leading 0, no country code - what the UI hint calls
        # "8031234567".
        assert clean_phone_number("8031234567") == "08031234567"

    def test_non_string_input_is_coerced(self):
        assert clean_phone_number(8031234567) == "08031234567"

    def test_empty_string(self):
        assert clean_phone_number("") == ""

    def test_letters_are_stripped(self):
        assert clean_phone_number("0803-ABC-4567") == "08034567"


class TestValidateNigerianNumber:
    def test_valid_number(self):
        assert validate_nigerian_number("08031234567") == (True, "Valid")

    def test_too_short(self):
        ok, message = validate_nigerian_number("0803123")
        assert ok is False
        assert "11 digits" in message

    def test_too_long(self):
        ok, message = validate_nigerian_number("080312345678")
        assert ok is False
        assert "11 digits" in message

    def test_missing_leading_zero(self):
        ok, message = validate_nigerian_number("18031234567")
        assert ok is False
        assert "start with 0" in message

    def test_non_digit_characters(self):
        ok, message = validate_nigerian_number("0803abc4567")
        assert ok is False
        assert "only digits" in message


class TestGetNetworkPrefixes:
    def test_returns_all_expected_networks(self):
        networks = get_network_prefixes()
        assert set(networks) == {
            "MTN", "Glo", "Airtel", "9mobile", "Ntel", "Smile",
        }

    def test_returns_shared_reference(self):
        # Documents current behaviour: callers get the module-level dict,
        # not a defensive copy.
        assert get_network_prefixes() is NETWORK_PREFIXES

    @pytest.mark.parametrize("network", list(NETWORK_PREFIXES))
    def test_each_network_has_required_fields(self, network):
        info = get_network_prefixes()[network]
        assert isinstance(info["prefixes"], list) and info["prefixes"]
        assert isinstance(info["color"], str) and info["color"].startswith("#")
        assert isinstance(info["description"], str) and info["description"]

    def test_no_duplicate_prefixes_across_networks(self):
        seen: dict[str, str] = {}
        for network, info in NETWORK_PREFIXES.items():
            for prefix in info["prefixes"]:
                assert prefix not in seen, (
                    f"{prefix} claimed by both {seen.get(prefix)} and {network}"
                )
                seen[prefix] = network


class TestDetectNigerianNetwork:
    @pytest.mark.parametrize(
        ("number", "expected_network"),
        [
            ("08031234567", "MTN"),
            ("08061234567", "MTN"),
            ("07025123456", "MTN"),  # 5-digit prefix must win over 4-digit
            ("08051234567", "Glo"),
            ("08021234567", "Airtel"),
            ("08091234567", "9mobile"),
            ("08041234567", "Ntel"),
            ("07021234567", "Smile"),
        ],
    )
    def test_known_prefixes(self, number, expected_network):
        assert detect_nigerian_network(number) == expected_network

    def test_international_format_is_detected(self):
        assert detect_nigerian_network("+2348031234567") == "MTN"

    def test_bare_ten_digit_is_detected(self):
        assert detect_nigerian_network("8031234567") == "MTN"

    def test_unknown_but_well_formed_prefix(self):
        # 0700 is not currently assigned to any network in NETWORK_PREFIXES.
        assert detect_nigerian_network("07001234567") == "Unknown network"

    def test_invalid_format_wrong_length(self):
        result = detect_nigerian_network("123")
        assert result.startswith("Invalid Nigerian number format")

    def test_invalid_format_empty_string(self):
        result = detect_nigerian_network("")
        assert result.startswith("Invalid Nigerian number format")

    def test_invalid_format_letters_only(self):
        result = detect_nigerian_network("not-a-number")
        assert result.startswith("Invalid Nigerian number format")
>>>>>>> a4caf25f5d7ce7f90ef5fbe4bbb9a8501ce2669b
