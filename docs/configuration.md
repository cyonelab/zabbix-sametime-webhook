# Configuration Reference

## Media type parameters

| Parameter | Default value | Purpose |
|---|---|---|
| `Channel` | `{$ST_CHANNEL}` | Exact channel name |
| `ChannelId` | `{$ST_CHANNELID}` | Exact channel ID |
| `Group` | `{$ST_GROUP}` | Standard n-way group chat name |
| `GroupPlaceId` | `{$ST_GROUP_PLACEID}` | Standard n-way group chat PlaceId |
| `Host` | `{$ST_URL}` | Sametime base URL |
| `Message` | `{ALERT.MESSAGE}` | Zabbix alert body |
| `Password` | `{$ST_PASSWORD}` | Sametime technical account password |
| `proxy` | `{$ST_PROXY}` | Optional HTTP proxy |
| `Subject` | `{ALERT.SUBJECT}` | Zabbix alert subject |
| `To` | `{ALERT.SENDTO}` | Direct-message Sametime user ID |
| `Username` | `{$ST_USERNAME}` | Sametime technical account username |

## Routing priority

The webhook selects exactly one destination:

```text
ChannelId -> Channel -> GroupPlaceId -> Group -> To
```

If both `ChannelId` and `To` are populated, the channel is used. Keep unrelated destination macros empty to make the configuration explicit.

## Required connection macros

### `{$ST_URL}`

The Sametime base URL without an API path:

```text
https://meet.cyone.lv
```

Trailing slashes are accepted and removed by the webhook.

### `{$ST_USERNAME}`

The login name for a dedicated Sametime technical account:

```text
monitoring-bot@cyone.lv
```

The account must be able to sign in through the Chat REST API.

### `{$ST_PASSWORD}`

The technical account password. Configure it as a Zabbix secret macro. Do not place a literal password in the exported YAML.

## Channel configuration

### Lookup by name

Set `{$ST_CHANNEL}` to the exact channel name. The lookup is performed through:

```text
POST /sametime-chatrooms/api/v1/chatrooms/byName
```

The webhook resolves the returned channel to the `placeId` required by the Chat REST API. If the response omits the documented channel ID, the webhook searches the paginated channel list and logs the matching ID.

### Lookup by ID

Set `{$ST_CHANNELID}` to the exact Chatrooms API channel ID. This is the recommended stable configuration after discovering the ID.

The technical account must be an active member with permission to publish. The channel UI calls these roles Contributor and Moderator; the Chatrooms API represents them as `MEMBER` and `MODERATOR`. Viewer (`READER`) is not sufficient.

## Group chat configuration

### Lookup by name

Set `{$ST_GROUP}` to the group chat display name. The technical account must already be a member or have a visible invitation.

The webhook first searches up to 200 visible `NWAY_TEXT` conversations. It tries an exact case-insensitive match, followed by a partial match. Exact and unique names are strongly recommended.

### Lookup by PlaceId

Set `{$ST_GROUP_PLACEID}` when the n-way group PlaceId is already known. This skips conversation lookup.

## Direct-message configuration

Leave channel and group macros empty. Configure the user's Zabbix media recipient with the Sametime user ID expected by the Chat REST API. Zabbix passes that value as `{ALERT.SENDTO}`.

## Proxy configuration

Set `{$ST_PROXY}` to a proxy URL supported by the Zabbix `HttpRequest` object, for example:

```text
http://proxy.cyone.lv:8080
```

Leave the macro empty when direct connectivity is available.

## Authentication flow

For channels, the webhook performs the following sequence:

1. Sign in through `/stwebapi/user/connect`.
2. Collect the RTC nonce, session ID, and cookies.
3. Join the RTC stream when a session ID is available.
4. Validate the JWT through `/sametime-auth/api/v1/check` and collect the Chatrooms CSRF token.
5. Refresh an expired access token through `/sametime-auth/api/v1/refresh` when required.
6. Resolve the channel to a `placeId`.
7. Enter the n-way conversation.
8. Send the message through `/stwebapi/chat/nway`.

## Timeout

The media type timeout is 20 seconds. Channel delivery uses more API calls than direct delivery. Increase the timeout only after confirming that network latency or proxy behavior requires it.
