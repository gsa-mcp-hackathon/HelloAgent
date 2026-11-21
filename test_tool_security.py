"""Automated security checks for HelloAgent's LLM-to-MCP tool boundary.

Run from the HelloAgent project root:
    python -m pytest -q test_tool_security.py
"""

import pytest

from tool_security import validate_tool_arguments, validate_tool_name


@pytest.mark.parametrize(
    "tool_name",
    ["list_applications", "list_approved_applications_by_vendor"],
)
def test_allowed_tool_names(tool_name):
    assert validate_tool_name(tool_name) == tool_name


@pytest.mark.parametrize("tool_name", ["delete_application", "say_hello", None, ""])
def test_unauthorized_tool_names_are_rejected(tool_name):
    with pytest.raises(ValueError, match="Unsupported MCP tool selection"):
        validate_tool_name(tool_name)


def test_list_applications_accepts_empty_arguments():
    assert validate_tool_arguments("list_applications", {}) == {}


@pytest.mark.parametrize("arguments", [{"delete": True}, {"vendor": "Microsoft"}, None, []])
def test_list_applications_rejects_unexpected_arguments(arguments):
    with pytest.raises(ValueError, match="Unexpected arguments for list_applications|Invalid tool arguments"):
        validate_tool_arguments("list_applications", arguments)


def test_vendor_lookup_accepts_valid_vendor():
    assert validate_tool_arguments(
        "list_approved_applications_by_vendor", {"vendor": "Microsoft"}
    ) == {"vendor": "Microsoft"}


@pytest.mark.parametrize("vendor", [12345, "", "   ", None, False])
def test_vendor_lookup_rejects_invalid_vendor(vendor):
    with pytest.raises(ValueError, match="Invalid vendor"):
        validate_tool_arguments(
            "list_approved_applications_by_vendor", {"vendor": vendor}
        )


@pytest.mark.parametrize(
    "arguments",
    [{}, {"vendor": "Microsoft", "delete": True}, {"wrong_key": "Microsoft"}],
)
def test_vendor_lookup_requires_exact_argument_keys(arguments):
    with pytest.raises(ValueError, match="Unexpected vendor lookup arguments"):
        validate_tool_arguments("list_approved_applications_by_vendor", arguments)


def test_vendor_lookup_rejects_non_dict_arguments():
    with pytest.raises(ValueError, match="Invalid tool arguments"):
        validate_tool_arguments("list_approved_applications_by_vendor", "Microsoft")


def test_argument_validation_rejects_unauthorized_tool_before_execution():
    with pytest.raises(ValueError, match="Unsupported MCP tool selection"):
        validate_tool_arguments("delete_application", {"application_name": "HR Portal"})
