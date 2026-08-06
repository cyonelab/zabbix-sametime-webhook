# Troubleshooting

## Confirm the active webhook version

Every test begins with a line similar to:

```text
[Sametime Webhook v1.0.0] Script: HCL Sametime Zabbix Webhook v1.0.0
```

If the log reports an older version after import, update the existing media type or replace its JavaScript and save it before testing again.

## Login fails

Typical messages:

```text
Login failed (HTTP 401)
Login failed (HTTP 403)
```

Check:

- `{$ST_URL}` points to the Sametime base URL
- The technical account username and password are correct
- The account is permitted to use Chat REST APIs
- Zabbix can reach the Sametime server and trust its TLS certificate
- A configured proxy is reachable

Do not paste the password or response cookies into an issue.

## Chatrooms session validation fails

Typical messages:

```text
Chatrooms session validation failed (HTTP 401)
Chatrooms session validation failed (HTTP 403)
Chatrooms session validation failed: no x-csrf-token response header
```

Webhook 1.0.0 uses the JWT cookies returned by the Chat REST login and obtains a CSRF token from `/sametime-auth/api/v1/check`. It uses `/refresh` only when `/check` returns HTTP 401.

Confirm that all Sametime 12.0.4 Auth and Chatrooms services are reachable through the same base URL and that reverse-proxy routing preserves response cookies and headers.

## Channel is not found by name

Typical message:

```text
FindChannelByName failed for channel "<name>" (HTTP 404)
```

Check:

- The name matches exactly
- The technical account can see the channel
- The account has accepted membership or has been added by a moderator
- `{$ST_CHANNELID}` is empty while testing name lookup

## ChannelId is not returned by `/byName`

Some Sametime 12.0.4 deployments omit the documented `id` field from the `/chatrooms/byName` response. The webhook automatically searches the paginated `/chatrooms` list by exact name.

Expected log sequence:

```text
FindChannelIdInList GET page 0
FindChannelIdInList HTTP code: 200
Resolved channel "<name>", ChannelId: <id>, PlaceId: chatroom:<value>
```

If the ID lookup fails, delivery continues using the already resolved `placeId`.

## Group is not found

Typical message:

```text
PlaceId not found for Topic "<name>"
```

Despite the legacy API wording in the message, the external parameter is named `Group` in webhook 1.0.0.

Check:

- The technical account is a member of the group chat
- The group is visible in the account's recent conversations
- The group name is unique
- The conversation is a standard `NWAY_TEXT` chat, not a modern channel

The conversation lookup reads at most 200 visible conversations.

## EnterNWay succeeds but no message appears

Check the subsequent `SendNWay HTTP code`. A successful sequence contains:

```text
EnterNWay HTTP code: 200
SendNWay HTTP code: 200
```

For a channel, confirm that the technical account is a Contributor (`MEMBER`) or Moderator (`MODERATOR`). A Viewer (`READER`) can view the channel but cannot publish.

## Request times out

Channel delivery performs authentication, session validation, lookup, conversation entry, and message delivery. Check DNS, TLS negotiation, proxy latency, and Sametime service health. The default webhook timeout is 20 seconds.

## Preparing logs for an issue

Remove or replace:

- Sametime hostname
- Username and user IDs
- Passwords
- Cookie and token values
- Session IDs
- Channel IDs and PlaceIds
- Alert subjects and message bodies
- Customer names and internal system names

Use placeholders such as `<HOST>`, `<USER>`, `<SESSION_ID>`, `<CHANNEL_ID>`, and `<PLACE_ID>`.
