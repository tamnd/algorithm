---
tag: PEKVQA
kind: algorithm
slug: rsa-signature
name: RSA signature
aliases:
- RSA signing
- "PKCS #1 v1.5 signature"
- RSASSA-PKCS1-v1_5
area: cryptography/signatures
level: intro
summary: "Sign by computing s = EM^d mod N, where EM is a padded hash of the message, and verify by s^e mod N = EM. Textbook RSA without padding is forgeable. RFC 8017 Section 8.2, FIPS 186-5."
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1978
  people: [Ronald L. Rivest, Adi Shamir, Leonard Adleman]
  note: The RSA paper of 1978 proposed signing with the private exponent. RSA Laboratories published PKCS #1 v1.5 in 1993; it is now RFC 8017 (2016).
prereqs: [rsa-cryptosystem, signature-scheme, hash-and-sign-paradigm]
see_also: [rsa-pss, rsa-fdh, rsa-fault-attack, chosen-message-attack, key-only-attack, rsa-pkcs1-v1-5-encryption, chinese-remainder-theorem, rsa-problem]
sources:
  - paper: "Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978"
    locator: the RSA permutation and signing with the private exponent
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, November 2016
    locator: Section 3.2 (private key in CRT form), Section 5.2.1 (RSASP1), Section 8 (the recommendation of RSASSA-PSS for new applications), Section 8.2 (RSASSA-PKCS1-v1_5), Section 9.2 (EMSA-PKCS1-v1_5 and the DigestInfo prefixes in Note 1)
  - url: "https://csrc.nist.gov/pubs/fips/186-5/final"
    title: NIST FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: Section 5, the RSA digital signature algorithm, with RSASSA-PKCS1-v1_5 and RSASSA-PSS
  - paper: "Dan Boneh, Richard A. DeMillo and Richard J. Lipton, On the importance of checking cryptographic protocols for faults, EUROCRYPT 1997, LNCS 1233, pages 37 to 51"
    locator: the fault attack on RSA with the CRT
  - url: "https://github.com/pyca/cryptography/tree/main/vectors/cryptography_vectors/asymmetric/RSA"
    title: RSA Laboratories, pkcs1v15sign-vectors.txt, and NIST CAVP SigGen15_186-3.rsp, as mirrored by the pyca/cryptography project
    locator: pkcs1v15sign-vectors.txt Example 1 key and Examples 1.17 and 1.18 (SHA-1); SigGen15_186-3.rsp, section mod = 1024, first SHA256 entry
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, Section 11.3.1 (RSA signature scheme), Section 11.3.2 (attacks), Section 11.3.6 (PKCS #1)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, plain RSA signatures and their insecurity, and RSA-FDH
---

An RSA signature is $s = \mathrm{EM}^d \bmod N$, where $(N, d)$ is an [RSA](/rsa-cryptosystem/) private key and $\mathrm{EM}$ is an encoding of a hash of the message; anyone checks it with the public key $(N, e)$ by testing $s^e \bmod N = \mathrm{EM}$. The encoding is essential: textbook RSA, which signs the message itself, lets anyone forge from the public key alone. The standard encoding is EMSA-PKCS1-v1_5 of RFC 8017, Section 9.2, which puts a fixed DER prefix that names the hash in front of the hash and fills the rest with `ff` bytes. Signing costs one exponentiation modulo $N$, about four times faster with the [Chinese remainder theorem](/chinese-remainder-theorem/), and verification with $e = 65537$ costs 17 modular multiplications.

**Notation.** $N = pq$ is the modulus with distinct primes $p$ and $q$, $k$ its length in bytes and $b$ its length in binary digits. $e$ is the public exponent and $d$ the private exponent, with $ed \equiv 1 \pmod{\mathrm{lcm}(p - 1, q - 1)}$. $d_P = d \bmod (p - 1)$, $d_Q = d \bmod (q - 1)$ and $q_{\mathrm{inv}} = q^{-1} \bmod p$ form the CRT key. $H$ is the hash and $T$ the DER encoding of the DigestInfo value for $H(M)$. $A$ is an adversary with running time $t$, $q_s$ signing queries and, in the [random oracle model](/random-oracle-model/), $q_h$ hash queries. OS2IP and I2OSP convert between byte strings and integers, big-endian.

## In plain words

The RSA key has a public number and a secret number. Raising a value to the secret power and then to the public power, with the same modulus, gives back the value. So the signer raises the value to the secret power, and anyone can undo it with the public power and see the value again.

Raising the message itself to the secret power is not safe. Signatures multiply: from the signatures of two values, anyone gets the signature of their product. Also anyone can pick a random "signature", raise it to the public power, and call the result a signed message. The fix is to sign a fixed-format block: a fixed start, filler bytes, a label for the hash function, and the hash. A forger would need a signature whose public-power result is exactly that block, and the algebra tricks do not produce one.

## The problem

Sign arbitrary byte strings so that the scheme is [existentially unforgeable](/existential-unforgeability/) under chosen-message attack, using the RSA trapdoor permutation $x \mapsto x^e \bmod N$. The security target is EUF-CMA, and the hardness assumption is the [RSA problem](/rsa-problem/): given $N$, $e$ and a random $y$, find $x$ with $x^e \equiv y \pmod N$.

## The algorithm

```pseudo id=main
RSASSA-PKCS1-V1_5-SIGN(K, M)          ▷ RFC 8017 Section 8.2.1, K = (N, p, q, dP, dQ, qInv)
L1  k ← length of N in bytes
L2  h ← H(M)
L3  T ← DigestInfo prefix of H ‖ h       ▷ RFC 8017 Section 9.2, Note 1
L4  if k < |T| + 11 then error "intended encoded message length too short"
L5  EM ← 00 ‖ 01 ‖ ff^(k − |T| − 3) ‖ 00 ‖ T
L6  m ← OS2IP(EM)
L7  s1 ← m^dP mod p;  s2 ← m^dQ mod q     ▷ RSASP1 with the CRT, Section 5.2.1
L8  h' ← qInv · (s1 − s2) mod p
L9  s ← s2 + q · h'
L10 return I2OSP(s, k)

RSASSA-PKCS1-V1_5-VERIFY((N, e), M, S)   ▷ RFC 8017 Section 8.2.2
L11 if |S| ≠ k then return invalid
L12 s ← OS2IP(S); if s ≥ N then return invalid
L13 m ← s^e mod N                      ▷ RSAVP1
L14 EM ← I2OSP(m, k)
L15 EM' ← the encoding of M by lines L2 to L5
L16 return valid if EM = EM', else invalid
```

The DigestInfo prefixes of RFC 8017, Section 9.2, Note 1, in hexadecimal:

| hash | prefix | $\lvert T \rvert$ |
|---|---|---|
| SHA-1 | `3021300906052b0e03021a05000414` | 35 |
| SHA-224 | `302d300d06096086480165030402040500041c` | 47 |
| SHA-256 | `3031300d060960864801650304020105000420` | 51 |
| SHA-384 | `3041300d060960864801650304020205000430` | 67 |
| SHA-512 | `3051300d060960864801650304020305000440` | 83 |

Lines L7 to L9 are Garner's form of the CRT. Without the CRT, lines L7 to L9 are the single step $s \leftarrow m^d \bmod N$. Line L16 compares the whole encoded block. RFC 8017 allows this form of verification, and it is the safe one: a verifier that parses $\mathrm{EM}$ and reads the hash out of it must also check that no bytes follow the hash and that the padding has the right length.

**Textbook RSA.** The insecure scheme signs an integer $m \in \mathbb{Z}_N$ directly: $s = m^d \bmod N$, accepted when $s^e \equiv m \pmod N$. It has two forgeries. From the public key alone: pick any $s$ and output $(s^e \bmod N, s)$ ([key-only attack](/key-only-attack/)). From two signatures: $s_1 s_2 \bmod N$ is a signature on $m_1 m_2 \bmod N$ ([chosen-message attack](/chosen-message-attack/)).

**About the code.** The Python code is for study only. It is not constant time, its key generator uses a seeded non-cryptographic random source, and it must not protect real data. Use the pyca/cryptography library or a FIPS 140 validated module. The page is about the RSA signature, not about the hash, so the code takes SHA-1 and SHA-2 from `hashlib`.

## Example

**A toy CRT signature.** Take $p = 61$, $q = 53$, $N = 3233$, $e = 17$ and $d = 2753$. Then $d_P = 53$, $d_Q = 49$ and $q_{\mathrm{inv}} = 38$. To sign the value $m = 65$:

| step | value |
|---|---|
| L7: $s_1 = 65^{53} \bmod 61$ | 39 |
| L7: $s_2 = 65^{49} \bmod 53$ | 5 |
| L8: $h' = 38 \cdot (39 - 5) \bmod 61$ | 11 |
| L9: $s = 5 + 53 \cdot 11$ | 588 |
| L13: $588^{17} \bmod 3233$ | 65 |

The result equals $65^{2753} \bmod 3233 = 588$, computed without the CRT.

**A real encoding.** In Example 1.17 of the RSA Laboratories PKCS #1 v1.5 vectors, $N$ has 1024 binary digits, so $k = 128$, and the hash is SHA-1. The message is the 4 bytes `eb1e5935`, with SHA-1 hash `823c99f2d9aa8e8fdf2fca152ef8379cfeb1d304`. $T$ has $15 + 20 = 35$ bytes, so $\mathrm{EM}$ is `0001`, then $128 - 35 - 3 = 90$ bytes `ff`, then `00`, then $T$. The signature starts with `370cb9839ae6074f`, and the code reproduces all 128 bytes.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that RSA is a permutation on $\mathbb{Z}_N$ (Lemma 1), that lines L7 to L9 compute $m^d \bmod N$ (Lemma 2), that an honest signature always verifies (Theorem 1), and that the verifier accepts exactly one value of $s^e \bmod N$ for each message (Lemma 3).

**Security.** RFC 8017, Section 8, says that no attacks are known against RSASSA-PKCS1-v1_5, but requires RSASSA-PSS in new applications for robustness. The reason is the proof: [RSA-PSS](/rsa-pss/) has a tight proof in the random oracle model, while the deterministic, partly fixed PKCS #1 v1.5 encoding long had none. Jager, Kakvi and May (ACM CCS 2018) later gave a proof in the random oracle model under RSA-type assumptions, with conditions that the paper states. For textbook RSA there is no security at all.

## Complexity

With schoolbook arithmetic on $b$-bit numbers, one modular multiplication costs $\Theta(b^2)$, and an exponentiation by [square and multiply](/modular-exponentiation/) with a $b$-bit exponent costs about $1.5 b$ multiplications, so $\Theta(b^3)$ in all. With the CRT, line L7 does two exponentiations with $b/2$-bit moduli and exponents, each about $1/8$ of the full cost, so signing is about four times faster. Verification with $e = 65537 = 2^{16} + 1$ costs 16 squarings and 1 multiplication, $\Theta(b^2)$. The hash costs time linear in the message length. The signature has $k$ bytes, as long as the modulus. Extra space is $\Theta(b)$.

| operation | cost in modular exponentiations |
|---|---|
| sign, no CRT | 1 with a $b$-bit exponent mod $N$ |
| sign, CRT | 2 with $b/2$-bit exponents mod $p$ and $q$ |
| verify, $e = 65537$ | 1 with a 17-bit exponent mod $N$ |

## Properties

- **Deterministic.** The same key and message always give the same signature, so signing needs no random numbers. This avoids the nonce failures of [DSA](/dsa/) and [ECDSA](/ecdsa/).
- **Unique signature per message.** For a fixed key, each message has exactly one valid signature, so the scheme is also [strongly unforgeable](/strong-unforgeability/) as soon as it is existentially unforgeable.
- **Fast verification, slow signing.** With a small $e$, verification is tens of times faster than signing; DSA and ECDSA are the other way round.
- **Large signatures.** 256 bytes for a 2048-bit modulus, against 64 bytes for [Ed25519](/ed25519/).
- **No message recovery.** The message must be sent with the signature (a scheme with appendix).

## Variants and improvements

- **[RSA-PSS](/rsa-pss/).** Randomized encoding with a salt and a mask, tight security in the ROM; required for new applications by RFC 8017.
- **[RSA-FDH](/rsa-fdh/).** Hash onto all of $\mathbb{Z}_N$; the cleanest scheme to analyse.
- **ISO/IEC 9796-2 and PSS-R.** Encodings with message recovery.
- **[Rabin signatures](/rabin-signature/).** Use $e = 2$, so forgery is as hard as factoring for suitable encodings.
- **[Blinding](/rsa-blinding/).** Multiply by $r^e$ before signing and divide by $r$ after, to hide the timing of the private exponentiation; the same algebra gives [Chaum blind signatures](/chaum-blind-signature/).
- **Multi-prime RSA.** RFC 8017 allows more than two primes; the CRT then has more, smaller parts.

## When to use it

Use RSASSA-PKCS1-v1_5 when a protocol or a verifier needs it: X.509 certificates, TLS 1.2, older code-signing formats and many hardware tokens still use it. For new designs, prefer RSA-PSS if RSA is required, or [Ed25519](/ed25519/) or [ECDSA](/ecdsa/) for smaller keys and signatures. Use a modulus of at least 2048 binary digits, $e = 65537$, and SHA-256 or a stronger hash.

## Pitfalls

- **Lenient parsing.** A verifier that finds the hash by parsing $\mathrm{EM}$ and ignores bytes after it accepts forged signatures when $e = 3$ (Bleichenbacher, 2006). Compare the whole block as in line L16. See [chosen-message attack](/chosen-message-attack/).
- **Faults in CRT signing.** One wrong half in line L7 gives a signature $s'$ with $\gcd(s'^e - m, N)$ equal to a prime factor (Boneh, DeMillo and Lipton, 1997). Verify each signature before release. See [RSA fault attack](/rsa-fault-attack/).
- **Weak hashes.** The signature is only as strong as the [collision resistance](/collision-resistance/) of $H$. MD5 and SHA-1 collisions gave rogue certificates; see [hash-and-sign](/hash-and-sign-paradigm/).
- **One key, two schemes.** RFC 8017 recommends that a key pair be used in only one scheme. A decryption oracle for textbook-style RSA is a signing oracle.
- **Unpadded or short padding.** Signing a short hash with few fixed bytes gives the algebra room to work; the full-length padding of line L5 is part of the security.
- **Timing.** The private exponentiation leaks through its running time unless it is constant time or blinded ([timing attack](/timing-attack/)).
- **Weak keys.** Bad random numbers at key generation give shared or guessable primes; see [signature forgery](/signature-forgery/) for ROCA and the Debian OpenSSL bug.

## Implementations

The Python code gives `emsa_pkcs1_v15_encode` (lines L2 to L5), `rsasp1_crt` (lines L7 to L9), `sign`, `verify` (lines L11 to L16), `sign_checked` with the verify-before-release check, textbook RSA, and a seeded toy key generator. The tests check the SHA-1 signatures of Examples 1.17 and 1.18 of the RSA Laboratories vectors, both by signing and by verifying, and the first SHA-256 entry of the 1024-bit section of the NIST CAVP file SigGen15_186-3.rsp, by verifying. They also run round trips with SHA-256, SHA-384 and SHA-512, reject changed messages, flipped bits, wrong lengths and out-of-range values, show the textbook multiplicative forgery and its failure against the padded scheme, and recover a prime factor from a faulty CRT signature.

## History

Diffie and Hellman described digital signatures in 1976, and Rivest, Shamir and Adleman gave the first scheme in 1978: sign with the private exponent. The weaknesses of signing the message directly were soon clear, and RSA Laboratories published the PKCS #1 v1.5 encoding in 1993, later republished as RFC 2313 (1998). PKCS #1 v2.1 (RFC 3447, 2003) added RSASSA-PSS, and v2.2 (RFC 8017, 2016) is the current version. In 2006 Bleichenbacher showed forgeries against many verifiers that parsed the encoding loosely, and NIST FIPS 186-5 (2023) still approves both RSASSA-PKCS1-v1_5 and RSASSA-PSS.

## References
