# Tests

The repository validator checks the static structure of the Zabbix export and compiles the embedded JavaScript with Node.js.

Install the development requirement and run:

```bash
python3 -m pip install -r requirements-dev.txt
python3 tests/validate_export.py
```

The validator does not contact a Sametime server or send a notification. Functional testing requires a non-production Zabbix and Sametime environment.
