# Contributing

Thank you for considering a contribution.

## Reporting bugs

Before opening an issue:

1. Confirm that the problem occurs with the latest release.
2. Check existing issues.
3. Run the export validation.
4. Remove credentials, cookies, tokens, private hostnames, user IDs, channel IDs, PlaceIds, customer data, and alert contents.

Include:

- Zabbix version
- HCL Sametime version
- Webhook version
- Destination type: direct user, group chat, or channel
- Expected behavior
- Actual behavior
- Reproduction steps
- Sanitized Zabbix webhook log

## Development workflow

Create a focused branch:

```bash
git checkout -b fix/short-description
```

Install development requirements and validate changes:

```bash
python3 -m pip install -r requirements-dev.txt
python3 tests/validate_export.py
```

Keep the media type description, script metadata, changelog, and release notes aligned when changing the webhook version.

## Pull requests

Keep each pull request focused on one change. Explain what changed, why it changed, and how it was tested. Do not test pull requests against production destinations.
