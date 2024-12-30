def validate_report_request(data):
    """Validates the report request payload."""
    required_keys = ["type", "kind", "format"]
    allowed_formats = ["nonfiscalprintout", "standard", "to_pc"]
    allowed_kinds = [
        "receipt", "invoice", "dailyreport", "nonfiscal", "all", "receipt_by_trad_sys_num"
    ]

    errors = []
    report = data.get("report", {})
    
    for key in required_keys:
        if key not in report:
            errors.append(f"Missing required field: {key}")

    if report.get("type") != "protectedmemory":
        errors.append(f"Invalid type: {report.get('type')}")

    if report.get("format") not in allowed_formats:
        errors.append(f"Invalid format: {report.get('format')}")

    if report.get("kind") not in allowed_kinds:
        errors.append(f"Invalid kind: {report.get('kind')}")

    return len(errors) == 0, errors
