---
tag: 2MFHP1
kind: concept
slug: signature-forgery
name: Signature forgery
aliases:
- existential forgery
area: cryptography/signatures
level: intro
summary: "A valid signature that the key holder did not make. Kinds range from existential forgery to key recovery; real cases came from broken hashes, faulty verifiers and bad randomness."
prereqs: [existential-unforgeability]
see_also: [chosen-message-attack, key-only-attack, nonce-reuse-attack, chosen-prefix-collision, hash-and-sign-paradigm, signature-malleability, rsa-fault-attack, strong-unforgeability]
sources:
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: the classification of breaks into total break, universal, selective and existential forgery
  - url: "https://mailarchive.ietf.org/arch/msg/openpgp/5rnE9ZRN1AokBVj3VqblGlP63QE/"
    title: Hal Finney, Bleichenbacher's RSA signature forgery based on implementation error, IETF OpenPGP mailing list, 27 August 2006
    locator: the e = 3 forgery against PKCS #1 v1.5 verifiers that do not check that the hash ends the block, presented by Bleichenbacher at the CRYPTO 2006 rump session
  - paper: "Marc Stevens, Alexander Sotirov, Jacob Appelbaum, Arjen Lenstra, David Molnar, Dag Arne Osvik and Benne de Weger, Short chosen-prefix collisions for MD5 and the creation of a rogue CA certificate, CRYPTO 2009, LNCS 5677"
    locator: a certificate authority certificate forged from an MD5 chosen-prefix collision
  - url: "https://learn.microsoft.com/en-us/security-updates/securityadvisories/2012/2718704"
    title: Microsoft Security Advisory 2718704, Unauthorized digital certificates could allow spoofing, June 2012
    locator: the Flame malware signed with certificates derived from the Terminal Server Licensing Service, which used MD5
  - paper: "Marc Stevens, Counter-cryptanalysis, CRYPTO 2013, LNCS 8042"
    locator: detection of the MD5 chosen-prefix collision in the Flame certificate and evidence that it used a new collision variant
  - url: "https://media.ccc.de/v/27c3-4087-en-console_hacking_2010"
    title: fail0verflow, Console hacking 2010, PS3 epic fail, 27th Chaos Communication Congress, December 2010
    locator: the PlayStation 3 ECDSA signatures used the same nonce, so the private key followed from two signatures
  - url: "https://bitcoin.org/en/alert/2013-08-11-android"
    title: Bitcoin.org, Android security vulnerability, 11 August 2013
    locator: Bitcoin wallets on Android made ECDSA signatures with repeated nonces because of a flaw in the Java SecureRandom class on Android
  - url: "https://neilmadden.blog/2022/04/19/psychic-signatures-in-java/"
    title: Neil Madden, Psychic signatures in Java, April 2022 (CVE-2022-21449)
    locator: the ECDSA verifier in Java 15 to 18 accepted r = s = 0 for every message and key
  - paper: "Matus Nemec, Marek Sys, Petr Svenda, Dusan Klinec and Vashek Matyas, The return of Coppersmith's attack: practical factorization of widely used RSA moduli, ACM CCS 2017, DOI 10.1145/3133956.3133969"
    locator: RSA keys from the Infineon library had primes of a special form and could be factored (ROCA, CVE-2017-15361)
  - url: "https://www.debian.org/security/2008/dsa-1571"
    title: Debian Security Advisory DSA-1571-1, openssl, predictable random number generator, 13 May 2008 (CVE-2008-0166)
    locator: keys made on Debian systems from September 2006 had only a few thousand possible values, and DSA keys used on such systems were exposed through their nonces
  - paper: "Gaëtan Leurent and Thomas Peyrin, SHA-1 is a shambles: first chosen-prefix collision on SHA-1 and application to the PGP Web of Trust, USENIX Security 2020"
    locator: two PGP keys with different identities and colliding SHA-1 certification signatures
---

A signature forgery is a pair of message and signature that the verifier accepts although the holder of the private key never signed that message. The security notions for a [signature scheme](/signature-scheme/) are defined by the forgeries they rule out: [existential unforgeability](/existential-unforgeability/) forbids any valid signature on a new message, and [strong unforgeability](/strong-unforgeability/) also forbids new signatures on signed messages. In deployed systems, forgeries have almost never come from breaking the hard problem itself; they came from broken hash functions, faulty verifiers, weak randomness and bad key generation.

**Notation.** $sk$ and $pk$ are the private and public keys, $m$ a message and $\sigma$ a signature. $\mathrm{Verify}(pk, m, \sigma) = 1$ means that the verifier accepts. For ECDSA, $(r, s)$ is the signature and $k$ the per-signature nonce; for RSA, $N$ is the modulus and $e$ the public exponent.

## In plain words

A forged signature is one that a checker accepts as real, although the owner of the secret key never made it. It is the digital form of a fake handwritten signature, with one difference: a digital forgery is either perfect or impossible to make, because the checker uses exact mathematics.

Forgeries come in degrees. The worst case is that the attacker learns the secret key and can sign anything. A weaker attacker can sign any message without the key, or only one message it picked, or only some message it does not control.

Real forgeries mostly came from mistakes around the mathematics: an old hash function that became breakable, a checker that skipped a test, or a signer whose random numbers were not random.

## The idea

**Kinds of forgery.** Goldwasser, Micali and Rivest (1988) ordered the goals of a forger from strongest to weakest:

1. **Total break.** The forger learns $sk$ or an equivalent secret.
2. **Universal forgery.** The forger can sign every message.
3. **Selective forgery.** The forger signs a message that it chose before the attack.
4. **Existential forgery.** The forger signs at least one new message, possibly a meaningless one.

The attacks that lead there are the [key-only attack](/key-only-attack/), the known-message attack and the [chosen-message attack](/chosen-message-attack/). A scheme that resists existential forgery under adaptive chosen-message attack resists all the other pairs. An existential forgery on a meaningless message can still matter, because the message format of an application is often looser than its designers expect.

**Where forgeries come from.**

- **The scheme is broken without a hash.** Textbook RSA and unhashed ElGamal allow existential forgery from the public key alone. The [hash-and-sign paradigm](/hash-and-sign-paradigm/) removes these attacks.
- **The hash is broken.** A signature on $H(m)$ is also a signature on every $m'$ with $H(m') = H(m)$. Collisions for [MD5](/md5/) and [SHA-1](/sha-1/), in particular [chosen-prefix collisions](/chosen-prefix-collision/), turned a signature on a harmless certificate into one on a harmful certificate.
- **The verifier is faulty.** A verifier that does not parse the whole encoding, skips a range check or accepts zero values accepts signatures that the scheme does not allow.
- **The randomness is bad.** DSA and ECDSA reveal the private key when two signatures share a nonce, and lattice methods recover it from partly known nonces; see [nonce reuse attack](/nonce-reuse-attack/). Weak key generation gives keys that an attacker can compute.
- **Physical attacks.** Faults in the CRT computation of RSA signatures reveal a factor of $N$ ([RSA fault attack](/rsa-fault-attack/)), and timing or power leaks can reveal nonces or keys.
- **Key theft.** If $sk$ is stolen, every signature is a forgery that the scheme cannot detect. This is a problem of key storage and [revocation](/non-repudiation/), not of the scheme.

## Examples

The table lists real forgeries in order of date. None of them broke RSA, the discrete logarithm problem or the elliptic-curve discrete logarithm problem.

| year | case | cause | kind of forgery |
|---|---|---|---|
| 2006 | Bleichenbacher's e = 3 attack (CVE-2006-4339 in OpenSSL) | PKCS #1 v1.5 verifiers did not check that the hash was at the end of the block; with $e = 3$ an attacker builds a value with the correct start and garbage after the hash, and takes an integer cube root | universal forgery for keys with $e = 3$ |
| 2008 | Debian OpenSSL (CVE-2008-0166, DSA-1571-1) | a change in 2006 removed almost all entropy from the random generator; keys and DSA nonces made on Debian systems came from a small set | total break of the affected keys |
| 2008 | Rogue CA certificate (Stevens et al., CRYPTO 2009) | MD5 chosen-prefix collision between a normal certificate request and a CA certificate | a forged certificate authority |
| 2010 | PlayStation 3 (fail0verflow, 27C3) | the same ECDSA nonce $k$ in every signature | total break of the code-signing key |
| 2012 | Flame malware (Microsoft Advisory 2718704; Stevens, CRYPTO 2013) | Microsoft certificates still signed with MD5; a new chosen-prefix collision variant | code signed as Microsoft |
| 2013 | Android Bitcoin wallets (bitcoin.org alert, 11 August 2013) | Java SecureRandom on Android repeated ECDSA nonces | total break of affected wallet keys and theft of coins |
| 2017 | ROCA (Nemec et al., CCS 2017; CVE-2017-15361) | the Infineon library made RSA primes of a special form, so $N$ could be factored with Coppersmith's method | total break of keys in ID cards, TPMs and security tokens |
| 2020 | SHA-1 chosen-prefix collision (Leurent and Peyrin, USENIX Security 2020) | a PGP key certification signed with SHA-1 transferred to a second key | forged identity certification |
| 2022 | Java "psychic signatures" (CVE-2022-21449) | the ECDSA verifier in Java 15 to 18 did not check $1 \le r, s < n$ and accepted $r = s = 0$ | universal forgery for every key |

**Two cases in more detail.**

- **Nonce reuse.** With ECDSA, $s = k^{-1}(h + x r) \bmod n$ where $x$ is the private key. Two signatures with the same $k$ have the same $r$, and then $k = (h_1 - h_2)/(s_1 - s_2) \bmod n$ and $x = (s_1 k - h_1)/r \bmod n$. This is what happened in the PS3 and Android cases. See [nonce reuse attack](/nonce-reuse-attack/) and [deterministic nonce generation](/deterministic-nonce-generation/).
- **Zero values.** The ECDSA check computes a point from $s^{-1}$ and compares its $x$-coordinate with $r$. A verifier that does not reject $r = 0$ and $s = 0$ can end with a comparison of 0 with 0, which passes. FIPS 186-5 and SEC 1 require the range checks for this reason.

## Where it is used

- **Security analysis.** Each proof of security for a signature scheme is a proof that a certain kind of forgery is as hard as a stated problem. The weakest kind ruled out, and the attack model, are the first things to read in a security claim.
- **Testing verifiers.** Test suites such as Project Wycheproof collect signatures that a correct verifier must reject: values out of range, wrong encodings, and points not on the curve. The CVE-2022-21449 signature is now such a test case.
- **Retiring algorithms.** Practical forgeries are the reason why MD5 and SHA-1 were removed from certificates, and why standards fix exact rules for range checks, encodings and nonces.
- **Incident response.** After a total break, the only remedy is to revoke the key and replace it, and to treat every signature that has no trusted timestamp from before the break as suspect.

## References
