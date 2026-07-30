# 🔐 Secure Password Manager

A command-line password manager written in Python that securely stores website credentials using modern cryptographic techniques.

---

## Features

- AES-256-GCM authenticated encryption
- PBKDF2-HMAC-SHA256 key derivation
- 600,000 PBKDF2 iterations
- Random salt generation
- Random nonce generation
- Secure master password authentication
- Encrypted password storage
- Modular Python architecture

---

## Tech Stack

- Python 3
- cryptography
- JSON
- AES-256-GCM
- PBKDF2
- SHA-256

---

## Project Structure

```
Password-Manager/
│
├── main.py
├── crypto_utils.py
├── storage.py
├── requirements.txt
├── README.md
├── LICENSE
└── sample_vault.json
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Password-Manager.git
```

Move into the project

```bash
cd Password-Manager
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

## Security

This project uses

- AES-256-GCM encryption
- PBKDF2-HMAC-SHA256
- 600000 PBKDF2 iterations
- Random 128-bit salt
- Random nonce per encryption
- Authentication tag verification

Passwords are never stored in plaintext.

---

## Future Improvements

- Password generator
- Password strength checker
- Clipboard support
- GUI using Tkinter
- Two-factor authentication
- Secure cloud synchronization

---

## Author

G Vinayaka Bharadwaj

LinkedIn:
https://linkedin.com/in/vinayaka-bharadwaj-a577831a8
