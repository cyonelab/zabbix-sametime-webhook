# Publishing Checklist

## Repository settings

Recommended repository name:

```text
zabbix-sametime-webhook
```

Recommended description:

```text
Zabbix 7 webhook for sending notifications to HCL Sametime 12.0.4 users, group chats, and channels.
```

Recommended topics:

```text
zabbix
sametime
hcl
webhook
monitoring
notifications
```

Enable:

- Issues
- Private vulnerability reporting
- Dependabot alerts
- Automatically delete head branches after pull requests are merged

## Initial push

Run these commands from the repository directory after reviewing every file:

```bash
git init
git add .
git commit -m "Initial release of Zabbix Sametime Webhook 1.0.0"
git branch -M main
git remote add origin git@github.com:cyonelab/zabbix-sametime-webhook.git
git push -u origin main
```

If the GitHub repository was initialized with files, clone it first and copy this project into the clone instead of forcing the first push.

## Validation

Confirm that the **Webhook validation** workflow passes on `main` before publishing the release.

## First release

Create an annotated tag:

```bash
git tag -a v1.0.0 -m "Zabbix Sametime Webhook 1.0.0"
git push origin v1.0.0
```

Create a GitHub release:

- Tag: `v1.0.0`
- Title: `Zabbix Sametime Webhook 1.0.0`
- Body: use [`release-notes-v1.0.0.md`](release-notes-v1.0.0.md)
- Asset: attach `zabbix-sametime-webhook.yaml`

## Final privacy review

Before pushing or attaching release assets, search for:

- Production hostnames and IP addresses
- Usernames and user IDs
- Passwords and password hashes
- Cookies, JWTs, CSRF tokens, LTPA tokens, and session IDs
- Channel IDs and group PlaceIds
- Customer names and alert contents

The repository examples use the `cyone.lv` domain consistently.
