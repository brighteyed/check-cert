# SSL Certificate Expiration Checker
Check the expiration dates of SSL certificates for a list of domains. Supports command-line options and colored output for warnings

---

## Features

- Check SSL certificate expiration dates for multiple domains
- Customizable warning threshold (`--days`)
- Exit codes: `0` (no warnings) or `1` (warnings/errors)

---

## Installation

1. Install `pipx` (if not already installed):
   ```bash
   python -m pip install --user pipx
   python -m pipx ensurepath
   ```

2. Install the script:
   ```bash
   pipx install .
   ```

---

## Usage

1. Run the script:
   ```bash
   check_cert
   ```

2. Options:
   - Specify domains file: `--file domains.txt` (default: `domains.txt`)
   - Set warning threshold: `--days 30` (default: 45 days)

Example:
```bash
check_cert --file domains.txt --days 30
```
Output:
```
example.com: 2023-12-31 (in 123 days)
google.com: 2023-11-01 (in 45 days)
expired.badssl.com: 2023-10-01 (in 15 days)
```

---

## Domains File

Add domains to check (one per line):
```
example.com
google.com
expired.badssl.com
```

---

## Exit Codes
- `0`: No warnings found
- `1`: Warnings found (certificates expiring soon) or errors (e.g., file not found)