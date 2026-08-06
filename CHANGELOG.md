# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [1.0.0] - 2026-08-06

### Added

- Initial public release
- Direct-message delivery to Sametime users
- Delivery to standard n-way group chats by name or PlaceId
- Delivery to Sametime 12.0.4 channels by name or channel ID
- Channel ID discovery through the paginated Chatrooms API
- JWT session validation and CSRF token handling for the Chatrooms API
- Access-token refresh through `/sametime-auth/api/v1/refresh`
- Session handshake and conversation entry before group or channel delivery
- Optional HTTP proxy support
- Zabbix trigger, discovery, and autoregistration templates
- Sanitized debug logging
- English documentation, validation, and GitHub project files
