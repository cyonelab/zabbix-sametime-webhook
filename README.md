# Zabbix Sametime Webhook

[![Webhook validation](https://github.com/cyonelab/zabbix-sametime-webhook/actions/workflows/validate.yml/badge.svg)](https://github.com/cyonelab/zabbix-sametime-webhook/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Zabbix 7 webhook for sending monitoring notifications to HCL Sametime 12.0.4 users, group chats, and channels.

## Features

- Direct messages to a Sametime user
- Messages to standard n-way group chats
- Messages to Sametime 12.0.4 channels
- Channel lookup by exact name or channel ID
- Group chat lookup by name or PlaceId
- Automatic Sametime session, JWT, CSRF, and cookie handling
- Optional HTTP proxy support
- Zabbix trigger, discovery, and autoregistration message templates
- Sanitized debug logging that does not print passwords, tokens, or message bodies
- Backward-compatible handling of the legacy `PlaceId` and `Topic` parameter names

## Compatibility

| Component | Supported version |
|---|---|
| Zabbix | 7.x |
| HCL Sametime | 12.0.4 |
| Webhook | 1.0.0 |

Other versions may work but have not been validated by this project.

## Routing

The first configured destination in this order is used:

```text
ChannelId -> Channel -> GroupPlaceId -> Group -> To
```

| Destination | ID parameter | Name parameter | Sametime API object |
|---|---|---|---|
| Channel | `ChannelId` | `Channel` | Chatroom/channel |
| Group chat | `GroupPlaceId` | `Group` | `NWAY_TEXT` conversation |
| User | `To` | Not applicable | Direct chat user |

`ChannelId` and `GroupPlaceId` are different identifiers. A channel also has an internal `placeId`, but the webhook resolves that value automatically.

## Requirements

- Zabbix 7.x with webhook media types enabled
- HCL Sametime 12.0.4
- A dedicated Sametime technical account
- Network access from the Zabbix server to the Sametime server
- Membership in every target group chat or channel
- Contributor (`MEMBER`) or Moderator (`MODERATOR`) channel role for publishing

## Installation

1. Download [`zabbix-sametime-webhook.yaml`](zabbix-sametime-webhook.yaml).
2. In Zabbix, open **Alerts → Media types**.
3. Select **Import**.
4. Upload the YAML file.
5. Enable updating existing media types if replacing an earlier version.
6. Configure the required Zabbix macros.
7. Test the media type before assigning it to production actions.

Menu names can vary slightly between Zabbix minor releases.

## Required macros

| Macro | Description | Example |
|---|---|---|
| `{$ST_URL}` | Sametime base URL | `https://meet.cyone.lv` |
| `{$ST_USERNAME}` | Technical account login | `monitoring-bot@cyone.lv` |
| `{$ST_PASSWORD}` | Technical account password | Store as a secret macro |

## Destination macros

Configure only the destination needed for a given media type or alert context.

| Macro | Description |
|---|---|
| `{$ST_CHANNELID}` | Exact Sametime channel ID |
| `{$ST_CHANNEL}` | Exact Sametime channel name |
| `{$ST_GROUP_PLACEID}` | Existing n-way group chat PlaceId |
| `{$ST_GROUP}` | Group chat display name |
| `{$ST_PROXY}` | Optional proxy URL |

Undefined optional macros are treated as empty values.

### Channel by name

```text
{$ST_CHANNEL}=Monitoring Notifications
{$ST_CHANNELID}=
{$ST_GROUP_PLACEID}=
{$ST_GROUP}=
```

### Channel by ID

```text
{$ST_CHANNELID}=<channel-id>
{$ST_CHANNEL}=
{$ST_GROUP_PLACEID}=
{$ST_GROUP}=
```

### Group chat by name

```text
{$ST_CHANNELID}=
{$ST_CHANNEL}=
{$ST_GROUP_PLACEID}=
{$ST_GROUP}=Operations Team
```

### Direct message

Leave all channel and group macros empty. Zabbix passes the media recipient through `{ALERT.SENDTO}` as the `To` parameter.

## Finding a ChannelId

Configure `{$ST_CHANNEL}` with the exact channel name and run a media type test. Debug logging for webhook 1.0.0 includes a sanitized line similar to:

```text
Resolved channel "Monitoring Notifications", ChannelId: <channel-id>, PlaceId: chatroom:<value>
```

Copy the reported channel ID to `{$ST_CHANNELID}` and clear `{$ST_CHANNEL}`. ID-based routing avoids a name lookup and is the preferred long-term configuration.

## Validation

Install the development dependency and run the repository validation:

```bash
python3 -m pip install -r requirements-dev.txt
python3 tests/validate_export.py
```

The validation checks the Zabbix export structure, required parameters, English-only content, version consistency, and JavaScript compilation.

## Documentation

- [Configuration reference](docs/configuration.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Release notes for 1.0.0](docs/release-notes-v1.0.0.md)
- [Publishing checklist](docs/publishing.md)

## Security

Use a dedicated least-privilege account. Store its password as a Zabbix secret macro. Never publish production cookies, JWTs, CSRF tokens, passwords, private hostnames, user identifiers, channel identifiers, or alert contents.

See [SECURITY.md](SECURITY.md) before reporting a vulnerability or attaching webhook logs to an issue.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Distributed under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

This project is an independent integration and is not affiliated with, endorsed by, or maintained by HCL Technologies or Zabbix LLC. HCL Sametime, Zabbix, and related product names may be trademarks of their respective owners.
