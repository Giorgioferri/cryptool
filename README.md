# cryptool

Un piccolo tool da riga di comando per **cifrare e decifrare file usando una password**.

La chiave non viene mai salvata da nessuna parte: viene ricalcolata ogni volta a partire dalla tua password tramite `PBKDF2HMAC`. Senza la password giusta (e senza il salt), il file resta illeggibile.

---

## Caratteristiche

- Cifratura simmetrica di qualsiasi file con una password scelta da te
- Chiave derivata dalla password al volo, mai scritta su disco
- Salt casuale generato a ogni cifratura
- Blocco temporaneo di 5 minuti dopo 5 password sbagliate consecutive
- Opzione `--delete` per cancellare il file originale subito dopo la cifratura

---

## Come funziona

| Componente | Dettaglio |
|------------|-----------|
| Cifratura | `Fernet` (AES a 128 bit in modalità CBC + HMAC, dalla libreria `cryptography`) |
| Derivazione chiave | `PBKDF2HMAC` con `SHA-256`, 100.000 iterazioni, chiave da 32 byte |
| Salt | 16 byte casuali, salvati in `salt.salt` |
| Input password | nascosto a schermo tramite `getpass` |

Il flusso è semplice: dalla password + salt si ricava una chiave, con quella chiave si cifra/decifra. Il salt viene salvato in chiaro (è normale: il salt non è un segreto, serve solo a rendere unica la derivazione della chiave ed evitare attacchi precalcolati).

---

## Requisiti

- Python 3.x
- Libreria `cryptography`

Installa la dipendenza:

```bash
pip install cryptography
```

---

## Utilizzo

### Cifrare un file

```bash
python cryptool.py encrypt input.txt output.enc
```

Ti viene chiesta una password, il contenuto di `input.txt` viene cifrato e salvato in `output.enc`. Viene creato anche il file `salt.salt`, **necessario per decifrare in seguito**.

Per cancellare automaticamente il file originale dopo la cifratura:

```bash
python cryptool.py encrypt input.txt output.enc --delete
```

### Decifrare un file

```bash
python cryptool.py decrypt placeholder output.enc
```

In fase di `decrypt` il tool legge il **secondo argomento** (il file cifrato), chiede la password e, se è corretta, stampa il contenuto decifrato direttamente a schermo.

> Il primo argomento è comunque richiesto dal parser ma in decifratura non viene usato: puoi passare un nome qualsiase. Conta solo il secondo file.

> ⚠️ Per decifrare serve il file `salt.salt` generato durante la cifratura. Se lo perdi, il file non è più recuperabile.

---

## Sicurezza

- La password non viene mai salvata né mostrata
- La chiave viene ricalcolata ogni volta partendo da password + salt, quindi non resta nessuna chiave su disco
- Dopo 5 tentativi falliti parte un countdown di 5 minuti prima di poter riprovare

---

## Note

- Progetto nato a scopo **didattico**, per mettere in pratica crittografia simmetrica e derivazione di chiavi in Python.
- Non pensato per proteggere dati ad alto rischio in ambienti reali: per quello esistono strumenti maturi e auditati (es. `age`, `gpg`, VeraCrypt).

---

## Licenza

MIT — sentiti libera di usarlo e modificarlo.
