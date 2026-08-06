# Security Policy

## Supported versions

Only the latest released version is currently supported.

## Credentials

Use a dedicated least-privilege Sametime technical account. Store its password as a Zabbix secret macro and restrict access to media type configuration.

Do not commit or publish:

- Passwords or password hashes
- JWT, CSRF, LTPA, or session tokens
- Cookie values
- Private keys or certificates
- Production hostnames or IP addresses
- User IDs, channel IDs, or group PlaceIds from private environments
- Customer data or alert contents

## Reporting a vulnerability

Do not report security vulnerabilities through public GitHub issues.

Use GitHub private vulnerability reporting if it is enabled for this repository, or contact the organization through its published security contact.

Include:

- A description of the vulnerability
- Reproduction steps
- The affected webhook, Zabbix, and Sametime versions
- The possible impact
- Suggested remediation, if available

Sanitize every log before sharing it. Replace private values with clear placeholders such as `<HOST>`, `<USER>`, `<CHANNEL_ID>`, and `<TOKEN>`.
