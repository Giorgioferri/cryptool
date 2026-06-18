# cryptool

A small command-line tool to **encrypt and decrypt files using a password**.

The key is never stored anywhere: it's re-derived from your password every time using `PBKDF2HMAC`. Without the right password (and the salt), the file stays unreadable.

---

## Features

- Symmetric encryption of any file with a password of your choice
- Key derived from the password on the fly, never written to disk
- Random salt generated on every encryption
- Temporary 5-minute lockout after 5 consecutive wrong passwords
- `--delete` flag to remove the original file right after encryption

---

## How it works

| Component | Detail |
|-----------|--------|
| Encryption | `Fernet` (AES-128 in CBC mode + HMAC, from the `cryptography` library) |
| Key derivation | `PBKDF2HMAC` with `SHA-256`, 100,000 iterations, 32-byte key |
| Salt | 16 random bytes, stored in `salt.salt` |
| Password input | hidden from the screen via `getpass` |

The flow is simple: from password + salt a key is derived, and that key is used to encrypt/decrypt. The salt is stored in plaintext (that's fine: a salt isn't a secret, it just makes the key derivation unique and prevents precomputed attacks).

---

## Requirements

- Python 3.x
- The `cryptography` library

Install the dependency:

```bash
pip install cryptography
```

---

## Usage

### Encrypt a file

```bash
python cryptool.py encrypt input.txt output.enc
```

You'll be prompted for a password, the contents of `input.txt` get encrypted and saved to `output.enc`. A `salt.salt` file is also created, which is **required to decrypt later**.

To automatically delete the original file after encryption:

```bash
python cryptool.py encrypt input.txt output.enc --delete
```

### Decrypt a file

```bash
python cryptool.py decrypt placeholder output.enc
```

When decrypting, the tool reads the **second argument** (the encrypted file), asks for the password, and if it's correct, prints the decrypted contents straight to the screen.

> The first argument is still required by the parser but isn't used during decryption: you can pass any name. Only the second file matters.

> ⚠️ Decryption needs the `salt.salt` file generated during encryption. If you lose it, the file can't be recovered.

---

## Security

- The password is never stored or displayed
- The key is recomputed every time from password + salt, so no key is ever left on disk
- After 5 failed attempts, a 5-minute countdown starts before you can try again

---

## Notes

- This is an **educational** project, built to practice symmetric cryptography and key derivation in Python.
- Not meant to protect high-risk data in real-world environments: for that, use mature and audited tools (e.g. `age`, `gpg`, VeraCrypt).

---

## License

MIT — feel free to use and modify it.
