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
