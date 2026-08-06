# Zabbix Sametime Webhook 1.0.0

## Highlights

- Sends Zabbix 7 notifications to HCL Sametime 12.0.4 users, standard group chats, and channels
- Supports channel lookup by exact name or channel ID
- Supports group lookup by name or PlaceId
- Uses the existing Sametime JWT session for Chatrooms API access
- Obtains CSRF tokens through the documented Auth API session check
- Automatically refreshes expired JWT access tokens
- Discovers a missing channel ID through the paginated channel list
- Includes English-only media type metadata and documentation
- Avoids logging passwords, tokens, raw cookies, response bodies, and alert message bodies

## Destination parameters

The first release uses these destination parameters:

- `ChannelId` or `Channel` for a modern channel
- `GroupPlaceId` or `Group` for a standard n-way group chat
- `To` for a direct message

Routing priority:

```text
ChannelId -> Channel -> GroupPlaceId -> Group -> To
```

After import, verify that the media type test log reports webhook version 1.0.0.

## Release assets

Attach `zabbix-sametime-webhook.yaml` to the GitHub release.
