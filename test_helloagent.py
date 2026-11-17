from mcp_server import list_approved_applications_by_vendor


def test_approved_microsoft_application():
    result = list_approved_applications_by_vendor("Microsoft")
    assert result["count"] == 1
    assert result["applications"] == ["HR Portal"]
    print("PASS: Approved Microsoft application returned")


def test_unknown_vendor():
    result = list_approved_applications_by_vendor("Oracle")
    assert result["count"] == 0
    assert result["applications"] == []
    print("PASS: Unknown vendor returns empty list")


def test_case_insensitive_vendor():
    result = list_approved_applications_by_vendor("microsoft")
    assert result["applications"] == ["HR Portal"]
    print("PASS: Case-insensitive vendor matching")

def test_unapproved_application_excluded():
    from mcp_server import applications

    applications["Test Unapproved App"] = {
        "vendor": "Microsoft",
        "approval_status": "Not Approved"
    }

    try:
        result = list_approved_applications_by_vendor("Microsoft")
        assert "Test Unapproved App" not in result["applications"]
        assert result["applications"] == ["HR Portal"]
        print("PASS: Unapproved application excluded")
    finally:
        del applications["Test Unapproved App"]

def test_missing_approval_status_excluded():
    from mcp_server import applications

    applications["Unknown Approval App"] = {
        "vendor": "Microsoft"
    }

    try:
        result = list_approved_applications_by_vendor("Microsoft")
        assert "Unknown Approval App" not in result["applications"]
        assert result["applications"] == ["HR Portal"]
        print("PASS: Missing approval status excluded")
    finally:
        del applications["Unknown Approval App"]

if __name__ == "__main__":
    test_approved_microsoft_application()
    test_unknown_vendor()
    test_case_insensitive_vendor()
    test_unapproved_application_excluded()
    test_missing_approval_status_excluded()
    print("All 5 automated tests passed.")