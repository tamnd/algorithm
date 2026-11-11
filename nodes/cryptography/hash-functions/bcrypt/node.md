---
tag: PKNJPH
kind: algorithm
slug: bcrypt
name: bcrypt
aliases:
- Blowfish-based password hash
area: cryptography/hash-functions
level: core
summary: Password hash using the expensive Eksblowfish key setup with a salt and cost factor.
solves: [password-hashing]
model: word-ram
complexity:
  vars: {k: the cost parameter}
  time: {worst: Θ(2^k), average: Θ(2^k), best: Θ(2^k)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1999
  people: [Niels Provos, David Mazières]
  note: Provos and Mazières presented bcrypt at USENIX 1999 as the password hash of OpenBSD. It is still the default in OpenBSD and in many web frameworks.
prereqs: [blowfish, password-hashing]
see_also: [pbkdf2, scrypt, argon2, memory-hard-function, key-schedule, feistel-network]
sources:
  - paper: "Niels Provos and David Mazières, A future-adaptable password scheme, Proceedings of the 1999 USENIX Annual Technical Conference, FREENIX Track, pages 81 to 91"
    locator: the section on Eksblowfish (the algorithms EksBlowfishSetup and ExpandKey) and the section on bcrypt (the value OrpheanBeholderScryDoubt and the 64 encryptions)
  - paper: "Bruce Schneier, Description of a new variable-length key, 64-bit block cipher (Blowfish), Fast Software Encryption 1993, LNCS 809"
    locator: the subkey generation, which fills the P-array and the S-boxes with the hexadecimal digits of pi
  - url: "https://www.schneier.com/wp-content/uploads/2015/12/vectors-2.txt"
    title: Eric Young, Blowfish test vectors
    locator: ecb test data, key bytes, clear bytes and cipher bytes
  - url: "https://github.com/pyca/bcrypt/blob/main/tests/test_bcrypt.py"
    title: Python Cryptographic Authority, bcrypt package, tests/test_bcrypt.py
    locator: the lists _test_vectors and _2y_test_vectors, and test_checkpw_wrong_password
  - url: "https://www.openwall.com/crypt/"
    title: Solar Designer, crypt_blowfish, Openwall
    locator: the notes on versions 1.1 to 1.3 (the 8-bit character bug CVE-2011-2483, the $2y$ prefix, and the $2b$ prefix of OpenBSD 5.5)
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    title: OWASP Cheat Sheet Series, Password Storage Cheat Sheet
    locator: section bcrypt (work factor 10 or more, the 72-byte input limit, and pre-hashing)
  - paper: "Katja Malvoni, Solar Designer and Josip Knezović, Are your passwords safe: energy-efficient bcrypt cracking with low-cost parallel hardware, USENIX WOOT 2014"
    locator: bcrypt cracking on FPGAs compared with CPUs and GPUs
---

bcrypt is a password hashing function designed by Niels Provos and David Mazières (USENIX 1999). It takes a password, a 128-bit salt and a cost $k$, and runs a deliberately expensive version of the [Blowfish](/blowfish/) key schedule, called EksBlowfish, with $2^k$ rounds of key mixing. It then encrypts a fixed 24-byte text 64 times with the resulting cipher. Raising $k$ by one doubles the work, so the cost can follow faster hardware. bcrypt needs 4 KB of S-boxes that change all the time, which slowed GPU attacks for many years. It is not memory hard in the modern sense, and new systems should prefer [Argon2id](/argon2/) or [scrypt](/scrypt/).

**Notation.** $k$ the cost, $s$ the 16-byte salt, $p$ the password. The Blowfish state is the P-array $P_1, \ldots, P_{18}$ of 32-bit words and four S-boxes of 256 words, 4168 bytes in all. $\mathrm{Enc}$ is Blowfish encryption of a 64-bit block under the current state. bcrypt is a dedicated design: its security is a conjecture about Blowfish, and no reduction proves it.

## In plain words

Blowfish is a block cipher whose setup is slow: to prepare a key, it encrypts 521 times to fill its tables. bcrypt makes this setup much slower on purpose. It mixes the password and the salt into the tables, and then mixes the password, then the salt, again and again, $2^k$ times. Each mixing step changes the whole 4 KB table. The final tables depend on every step, so there is no shortcut.

When the tables are ready, bcrypt uses them to encrypt the text `OrpheanBeholderScryDoubt` 64 times. The result, with the cost and the salt, is the stored hash, for example `$2b$12$` followed by 53 characters.

## The problem

Store a [password verifier](/password-hashing/) whose computation costs a tunable amount, so that each guess of an attacker costs as much as one login, with a salt so that each user must be attacked alone. bcrypt fixes the output at 23 bytes and the salt at 16 bytes, and encodes all of it in one printable string.

## The algorithm

```pseudo id=main
BCRYPT(k, s, p)                          ▷ Provos and Mazières 1999; version $2b$
L1  key ← the first 72 bytes of p, then one zero byte
L2  state ← EKSBLOWFISHSETUP(k, s, key)
L3  ctext ← "OrpheanBeholderScryDoubt";  repeat 64 times: ctext ← Enc_state(ctext) in ECB mode
L4  return "$2b$" ‖ k ‖ "$" ‖ base64(s) ‖ base64(first 23 bytes of ctext)

EKSBLOWFISHSETUP(k, s, key)              ▷ the expensive key schedule
L5  state ← INITSTATE()                  ▷ P and S from the hex digits of π
L6  state ← EXPANDKEY(state, s, key)
L7  repeat 2^k times: state ← EXPANDKEY(state, 0, key);  state ← EXPANDKEY(state, 0, s)

EXPANDKEY(state, salt, key)
    P_i ← P_i ⊕ (word i of key, repeated cyclically) for i = 1 .. 18
    (L, R) ← (0, 0)
    for each pair of slots (P_1, P_2), (P_3, P_4), …, (S_4[254], S_4[255]) do
        (L, R) ← Enc_state((L, R) ⊕ next 64 bits of salt, repeated cyclically)
        store L and R in the pair of slots
```

The plain Blowfish key schedule is EXPANDKEY(INITSTATE(), 0, key). Each call to EXPANDKEY makes $9 + 512 = 521$ encryptions, and each encryption uses the table entries that the previous ones wrote. The base64 of bcrypt uses the alphabet `./A-Za-z0-9` with no padding, so the salt takes 22 characters and the hash 31.

**About the code.** The Python code is for study only, is not constant time, and must not protect real data. Use the `bcrypt` package of pyca or crypt_blowfish of Openwall, or better Argon2id from libsodium. The code includes its own Blowfish. It computes the 1042 table words as hexadecimal digits of π with exact integers, by Machin's formula $\pi = 16 \arctan(1/5) - 4 \arctan(1/239)$, instead of copying them. It is not a digit-by-digit spigot. Like C implementations, it stops reading the password at 72 bytes; unlike them, it does not stop at a zero byte inside the password.

## Example

The Openwall test vector `$2a$05$CCCCCCCCCCCCCCCCCCCCC.E5YPO9kmyuRGyh0XouQYb4YMJKvyOeW` for the password `U*U`, as listed in the tests of pyca/bcrypt.

| part | text | meaning |
|---|---|---|
| prefix | `$2a$` | version 2a |
| cost | `05` | $k = 5$, so $2^5 = 32$ loops in line L7 |
| salt | `CCCCCCCCCCCCCCCCCCCCC.` | 16 bytes `10410410410410410410410410410410` |
| hash | `E5YPO9kmyuRGyh0XouQYb4YMJKvyOeW` | 23 bytes `1bb69143f9a8d304c8d23d99ab049a77a68e2ccc744206` |

The key is `U*U` and a zero byte, 4 bytes, so line L6 XORs the P-array with the words `552a5500` repeated. The setup makes $521 \cdot (1 + 2 \cdot 32) = 33{,}865$ Blowfish encryptions, and line L3 adds $64 \cdot 3 = 192$ more, for 34,057 in all. The 24 bytes after line L3 lose their last byte, and the remaining 23 bytes give the 31 characters of the hash. The salt bytes and the hash bytes in the table are the base64 decoding of the published string.

## Correctness

**Verification.** bcrypt is deterministic, and the stored string contains the version, the cost and the salt. So CHECKPW, which recomputes BCRYPT with the stored setting and compares, accepts the right password. A wrong password is accepted only on a collision of the 184-bit output.

**Why every loop is needed.** Each EXPANDKEY overwrites all 1042 words of the state, and each new word is an encryption under the state that the previous writes produced. So the state after step $i$ is a function of the state after step $i - 1$ that, as far as is known, cannot be computed faster than by running it. The output therefore needs all $2 \cdot 2^k + 1$ calls. This is a heuristic argument about Blowfish, not a proof; no shortcut is known.

**Security.** The paper argues that the cost to test one guess is the cost of EksBlowfishSetup, and that the 128-bit salt stops precomputation. The 4 KB state must be read at random positions in every round, which makes bcrypt slow on GPUs, where fast memory per thread is small. FPGAs with many small memory blocks run it more efficiently (Malvoni, Solar Designer and Knezović, WOOT 2014). There is no reduction to a standard assumption.

## Complexity

The work is $(2^{k+1} + 1) \cdot 521 + 192$ Blowfish encryptions, so $\Theta(2^k)$. Each encryption makes 16 rounds of four S-box lookups. Extra memory is the 4168-byte state, a constant. Common costs are 10 to 12; at cost 12 a hash makes about 4.3 million encryptions.

## Properties

- Deterministic, with the cost and salt in the output string.
- Cost doubles with each step of $k$, from 4 to 31.
- Uses 4 KB of fast memory, but this does not grow with the cost: bcrypt is not memory hard.
- Only the first 72 bytes of the password count.
- Output of 184 bits.

## Variants and improvements

- **Version prefixes.** `$2$` was the first version. `$2a$` fixed the handling of the terminating zero byte and of non-ASCII text. `$2x$` and `$2y$` come from crypt_blowfish of Openwall after CVE-2011-2483 (2011): a sign extension bug for bytes of 128 or more weakened some hashes, and `$2x$` marks hashes made with the bug, `$2y$` hashes made with the fix. `$2b$` (OpenBSD, 2014) fixed a bug in the OpenBSD code where the password length wrapped at 256 bytes. For passwords under 72 bytes, correct implementations of `$2a$`, `$2b$` and `$2y$` give the same output, as the tests show.
- **bcrypt_pbkdf.** OpenSSH uses bcrypt as the PRF of a PBKDF2-like construction to protect private keys.
- **Pre-hashing.** To accept long passwords, hash them first with a keyed hash and encode the result in base64; see the pitfalls.

## When to use it

bcrypt is acceptable for existing systems, with a cost of 10 or more as OWASP asks. For new systems, prefer Argon2id, which can use much more memory, or scrypt. bcrypt is not a key derivation function: its output is short and fixed, so use bcrypt_pbkdf, PBKDF2 or Argon2 to derive keys.

## Pitfalls

- **The 72-byte limit.** Bytes after the 72nd are ignored, so two long passwords with the same start collide. Some libraries now raise an error instead.
- **Zero bytes.** C implementations stop at the first zero byte. Pre-hashing to raw binary can thus cut the input short: bcrypt of a raw digest that starts with a zero byte is bcrypt of the empty password. Encode the digest in base64 first.
- **Password shucking.** bcrypt of an unsalted fast hash, such as SHA-1 of the password, lets an attacker test leaked SHA-1 values from other breaches against bcrypt directly. Use a keyed hash with a secret pepper when pre-hashing.
- **Version mix-ups.** Old `$2a$` hashes from buggy implementations may need the `$2x$` rule to verify.
- **Low cost.** A cost set in 1999 is far too low today; raise it and rehash at the next login.

## Implementations

The Python code gives `pi_hex_words`, the `Blowfish` class with `encrypt` and `expand_key`, `blowfish_key_schedule`, `eks_blowfish_setup` (lines L5 to L7), `bcrypt_raw` (lines L1 to L3), `hashpw` (line L4), `checkpw` and the bcrypt base64 functions. The tests check the first words of π, six Blowfish vectors of Eric Young, eight bcrypt vectors at cost 4 and 5 from the tests of pyca/bcrypt (with `$2a$`, `$2b$` and `$2y$` prefixes, the Openwall vectors, a non-ASCII password and a 72-byte binary password), a wrong password, the 72-byte limit, the base64 round trip, the effect of the salt and the cost, and an avalanche of about half the output bits. Python has no bcrypt in its standard library, so there is no second check against it.

## History

Morris and Thompson's Unix crypt (1979) used 25 DES encryptions and could not grow its cost. Provos and Mazières designed bcrypt for OpenBSD and published it in 1999, with the aim that the cost could follow Moore's law. It became the default password hash of OpenBSD and was adopted by Ruby on Rails, PHP (`password_hash`, since 5.5), Spring Security and many others. The Openwall bug of 2011 and the OpenBSD bug of 2014 led to the `$2y$` and `$2b$` prefixes. The Password Hashing Competition (2013 to 2015) produced Argon2, which can use much more memory than bcrypt.

## References
