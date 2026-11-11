---
tag: G2X3X9
kind: algorithm
slug: pbkdf2
name: PBKDF2
aliases:
- Password-Based Key Derivation Function 2
area: cryptography/hash-functions
level: core
summary: Iterates HMAC many times with a salt to slow password guessing.
solves: [password-hashing]
model: word-ram
complexity:
  vars: {c: the iteration count, l: the number of output blocks of the hash length}
  time: {worst: Θ(c l), average: Θ(c l), best: Θ(c l)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2000
  people: [Burt Kaliski]
  note: PBKDF2 is part of PKCS 5 version 2.0 of RSA Laboratories, published as RFC 2898 in 2000 and again as RFC 8018 in 2017.
prereqs: [hmac, password-hashing]
see_also: [bcrypt, scrypt, argon2, hkdf, memory-hard-function, pseudorandom-function, rainbow-table, sha-2]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8018"
    title: Kathleen Moriarty, Burt Kaliski and Andreas Rusch, RFC 8018, PKCS 5, Password-Based Cryptography Specification Version 2.1, January 2017
    locator: Section 4.1 (salt), Section 4.2 (iteration count), Section 5.2 (PBKDF2), Appendix B.1.1 (HMAC-SHA-1 as the default PRF)
  - url: "https://www.rfc-editor.org/rfc/rfc2898"
    title: Burt Kaliski, RFC 2898, PKCS 5, Password-Based Cryptography Specification Version 2.0, September 2000
    locator: Section 5.2 (PBKDF2)
  - url: "https://www.rfc-editor.org/rfc/rfc6070"
    title: Simon Josefsson, RFC 6070, PKCS 5 PBKDF2 Test Vectors, January 2011
    locator: Section 2 (PBKDF2 HMAC-SHA1 test vectors)
  - url: "https://www.rfc-editor.org/rfc/rfc7914"
    title: Colin Percival and Simon Josefsson, RFC 7914, The scrypt Password-Based Key Derivation Function, August 2016
    locator: Section 11 (test vectors for PBKDF2 with HMAC-SHA-256)
  - url: "https://doi.org/10.6028/NIST.SP.800-132"
    title: Meltem Sönmez Turan, Elaine Barker, William Burr and Lily Chen, NIST SP 800-132, Recommendation for Password-Based Key Derivation, Part 1, Storage Applications, December 2010
    locator: Section 5.1 (the salt), Section 5.2 (the iteration count), Section 5.3 (PBKDF2)
  - paper: "Mihir Bellare, Thomas Ristenpart and Stefano Tessaro, Multi-instance security and its application to password-based cryptography, CRYPTO 2012, LNCS 7417"
    locator: the analysis of salted iterated key derivation in the random oracle model
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    title: OWASP Cheat Sheet Series, Password Storage Cheat Sheet
    locator: section PBKDF2 (600,000 iterations for HMAC-SHA-256, 220,000 for HMAC-SHA-512, 1,400,000 for HMAC-SHA-1) and section PBKDF2 Pre-Hashing
---

PBKDF2 (Password-Based Key Derivation Function 2) turns a password and a salt into a key of any length by iterating a pseudorandom function, in practice [HMAC](/hmac/), $c$ times. The iteration count $c$ makes each guess of an attacker about $c$ times more expensive. It is standardized in PKCS 5 (RFC 2898 and RFC 8018) and in NIST SP 800-132, and it is the password hash that FIPS 140 validated modules provide. It needs almost no memory, so it is cheap to attack with GPUs and ASICs, and newer designs such as [scrypt](/scrypt/) and [Argon2](/argon2/) are better for new [password storage](/password-hashing/).

**Notation.** $P$ the password, $S$ the salt, $c$ the iteration count, $dkLen$ the output length in bytes. $\mathrm{PRF}(P, x)$ is HMAC-$H$ with key $P$ and message $x$, of $hLen$ bytes. $\mathrm{INT}(i)$ is the 4-byte big-endian form of $i$. $\oplus$ is XOR, $\|$ is concatenation, $l = \lceil dkLen / hLen \rceil$. The security analysis models the PRF as a random oracle (ROM).

## In plain words

Take a password and a random salt. Compute a keyed hash of the salt with the password as the key. Then take the keyed hash of that result, and of that result, and so on, many thousands of times. XOR all these results together. The XOR is one block of the key. If you need a longer key, do the same again with a counter 2, 3, and so on mixed into the salt, and put the blocks together.

The server does this once per login. An attacker who stole the stored key must do the same full chain for every password it guesses, so a chain of 600,000 steps makes each guess 600,000 times more expensive.

## The problem

Given a password $P$ with little entropy, a salt $S$ and a cost $c$, derive a key $DK$ of $dkLen$ bytes such that: $DK$ looks random to anyone who does not know $P$, testing a guess of $P$ costs about $c$ evaluations of the PRF, and distinct salts give unrelated keys. The key is stored as a password verifier or used as an encryption key.

## The algorithm

```pseudo id=main
PBKDF2(P, S, c, dkLen)                  ▷ RFC 8018, Section 5.2
L1  if dkLen > (2^32 − 1) · hLen then error "derived key too long"
L2  l ← ⌈dkLen / hLen⌉
L3  for i ← 1 to l do T_i ← F(P, S, c, i)
L6  return the first dkLen bytes of T_1 ‖ T_2 ‖ … ‖ T_l

F(P, S, c, i)
L4  U_1 ← PRF(P, S ‖ INT(i));  T ← U_1
L5  for j ← 2 to c do U_j ← PRF(P, U_{j−1});  T ← T ⊕ U_j
    return T

VERIFY(P', S, c, DK)
L7  return PBKDF2(P', S, c, |DK|) = DK      ▷ compare in constant time
```

The line numbers follow the order of the code, so lines L4 and L5 of the inner function come after line L3 that calls it.

**About the code.** The Python code is for study only, is not constant time, and must not protect real data. Use `hashlib.pbkdf2_hmac`, or Argon2id from libsodium or argon2-cffi for new systems. The HMAC inside is written out over a `hashlib` hash. The password is the HMAC key, so the code hashes the inner and outer padded key blocks once and copies those two states for each iteration. Each iteration then costs two compression function calls, and the output does not change. The tests compare with `hashlib.pbkdf2_hmac` only as a second check.

## Example

RFC 6070, second vector: PBKDF2-HMAC-SHA-1 with $P$ = `password`, $S$ = `salt`, $c = 2$, $dkLen = 20$. Since $hLen = 20$, there is one block, $l = 1$.

| step | value |
|---|---|
| L4: $U_1$ = HMAC-SHA-1(`password`, `salt` ‖ `00000001`) | `0c60c80f961f0e71f3a9b524af6012062fe037a6` |
| L5: $U_2$ = HMAC-SHA-1(`password`, $U_1$) | `e60cc942513261fd3eb76c0e617d53f6f73ebef1` |
| L5: $T_1 = U_1 \oplus U_2$ | `ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957` |

The value of $U_1$ is the first RFC 6070 vector, the one with $c = 1$, and $T_1$ is the second. The row for $U_2$ is their XOR; a direct HMAC computation gives the same value. The tests also check the RFC 6070 vectors with $c = 4096$ and the two PBKDF2-HMAC-SHA-256 vectors of RFC 7914, Section 11, one with $c = 80000$.

## Correctness

**The function is well defined.** Line L1 makes sure that the block index $i \le l$ fits in the 4-byte $\mathrm{INT}(i)$, so the inputs $S \| \mathrm{INT}(i)$ of different blocks are distinct. Each block $T_i$ depends only on $(P, S, c, i)$, so the first $k$ bytes of $DK$ do not depend on $dkLen$ as long as $dkLen \ge k$. The tests check this prefix property.

**Verification.** By determinism, $\mathrm{VERIFY}(P, S, c, \mathrm{PBKDF2}(P, S, c, n))$ is true. A wrong password is accepted only if two PBKDF2 outputs collide, which for an $n$-byte output and a random-looking function has probability about $2^{-8n}$ per guess.

**Security.** If HMAC-$H$ is a [PRF](/pseudorandom-function/) under the key $P$, the output is pseudorandom for anyone who does not know $P$; but $P$ has little entropy, so the real question is the cost of guessing. Bellare, Ristenpart and Tessaro (CRYPTO 2012) model the PRF as a random oracle and show, roughly, that with distinct salts an attacker who makes $q$ oracle queries does about as well as one who tests $q / c$ password guesses, against one user or against many. That is, $c$ iterations raise the cost of a guess by a factor of about $c$, and salts stop the attacker from sharing work between users. The bound counts oracle queries, so it does not consider memory or hardware cost.

## Complexity

PBKDF2 makes $c \cdot l$ PRF calls. With HMAC and the precomputed key states of the code, each PRF call is two compression function calls of $H$ when $hLen$ plus the padding fits in one block, as for SHA-1, SHA-256 and SHA-512. So PBKDF2-HMAC-SHA-256 with $c$ = 600,000 and a 32-byte output costs about 1.2 million SHA-256 compressions. Extra memory is a few hash states, independent of $c$. An attacker who checks a guess needs only one output block, so it pays $c$ PRF calls, not $c \cdot l$.

## Properties

- Deterministic, and the output length is chosen by the caller.
- Cost grows linearly in $c$, and $c$ can be raised over time.
- **Not memory hard.** Each chain needs only the HMAC state, a few hundred bytes. A GPU or ASIC runs thousands of chains in parallel at little cost per chain, so the attacker gains much more from special hardware than with [bcrypt](/bcrypt/), [scrypt](/scrypt/) or [Argon2](/argon2/).
- Approved by NIST (SP 800-132) and available in FIPS 140 validated modules.

## Variants and improvements

- **PBKDF1** (RFC 2898, Section 5.1) iterates a hash and is limited to the hash length, at most 20 bytes. RFC 8018 keeps it only for compatibility.
- **The PRF.** RFC 8018 lists HMAC-SHA-1 as the default and allows HMAC with SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256. OWASP gives different minimum counts for each: 1,400,000 for HMAC-SHA-1, 600,000 for HMAC-SHA-256 and 220,000 for HMAC-SHA-512.
- **Parallel PBKDF2.** Run several PBKDF2 chains with different indices and combine them, so the server uses several cores; the attacker gets the same parallelism.
- **Pre-hashing.** Hash a long password once with a salt before PBKDF2 to cap its cost; see the pitfalls.

## When to use it

Use PBKDF2 when a standard or FIPS 140 compliance requires it, for example in government systems, or for compatibility with formats that use it (WPA2 personal mode, encrypted PKCS 8 keys, many disk and archive formats). For new password storage without such a rule, prefer [Argon2id](/argon2/) or [scrypt](/scrypt/). To derive keys from a secret that already has high entropy, use [HKDF](/hkdf/): iteration adds nothing there.

## Pitfalls

- **Iteration counts that are too low.** RFC 2898 suggested 1000 iterations in 2000. SP 800-132 (2010), quoted in RFC 8018, Section 4.2, recommends at least 1,000 and says 10,000,000 may be right for critical keys. OWASP now asks for 600,000 with HMAC-SHA-256. As RFC 8018 puts it, $c$ iterations add only $\log_2 c$ bits of strength, so 600,000 iterations add about 19 bits. Old records with low counts need an upgrade path.
- **Asking for more than one block.** With $dkLen > hLen$ the defender computes $l$ chains, but the attacker can check a guess with the first block alone. Choose $dkLen \le hLen$ for verifiers, or use a hash with a longer output.
- **Long passwords and HMAC keys.** HMAC hashes a key that is longer than the block size. So a password of more than 64 bytes (for SHA-256) and its SHA-256 digest give the same output; the tests show this collision. A naive implementation that hashes the long key again in every iteration also gets slow, which caused a denial of service in Django in 2013.
- **Salts.** Use a fresh random salt per record; RFC 8018 asks for at least 64 bits and SP 800-132 for at least 128 random bits.
- **Comparing outputs.** Use a constant-time comparison, such as `hmac.compare_digest`.

## Implementations

The Python code gives `pbkdf2(password, salt, c, dk_len, hash_name)` (lines L1 to L6), `pbkdf2_block` (lines L4 and L5) and `verify` (line L7). The tests check all RFC 6070 vectors except the one with $c$ = 16,777,216, which takes minutes in pure Python, the two RFC 7914 Section 11 vectors for HMAC-SHA-256, and random inputs against `hashlib.pbkdf2_hmac` for SHA-1, SHA-256, SHA-512 and SHA3-256. They also check a wrong password, salt or count, the prefix property, the long-password collision and the avalanche of about 128 of 256 output bits.

## History

Morris and Thompson's Unix crypt (1979) already salted and iterated DES. PKCS 5 version 2.0, written by Burt Kaliski at RSA Laboratories, defined PBKDF2 to replace the length-limited PBKDF1; the IETF published it as RFC 2898 in September 2000. NIST approved it in SP 800-132 in 2010. RFC 6070 (2011) gave the first official test vectors. RFC 8018 (2017) republished the specification as PKCS 5 version 2.1 with more hash functions. The Password Hashing Competition (2013 to 2015) was started in part because PBKDF2 gives little protection against parallel hardware.

## References
