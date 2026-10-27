from backend import _extract_fields, _validate

def test_extract_invoice_fields():
    text = """Invoice No: INV-2026-001
Invoice Date: 26 October 2026
South India Bottling Company Pvt Ltd
Email: accounts@example.com
Phone: +91 98765 43210
Grand Total: INR 28,500.00"""
    fields = _extract_fields(text)
    assert fields["invoice_number"] == "INV-2026-001"
    assert fields["invoice_date"]
    assert fields["email"] == "accounts@example.com"
    assert fields["total_amount"] == "28500.00"
    assert fields["currency"] == "INR"
    assert _validate(fields)["is_valid"]
