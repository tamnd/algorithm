---
tag: YWSZYG
kind: algorithm
slug: ecies
name: Elliptic Curve Integrated Encryption Scheme
aliases:
- ECIES
- DHIES
area: cryptography/public-key
level: advanced
summary: Hybrid public-key encryption from an ephemeral elliptic-curve Diffie-Hellman value, a key derivation function, a cipher and a MAC. IND-CCA2 under an oracle Diffie-Hellman assumption.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the field prime p, l: the message length in bytes}
  time: {worst: Θ(b^3 + l), average: Θ(b^3 + l), best: Θ(b^3 + l)}
  space: {extra: Θ(b + l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Michel Abdalla, Mihir Bellare, Phillip Rogaway]
  note: Proposed as DHAES to IEEE P1363a in 1998 and analysed as DHIES at CT-RSA 2001. The elliptic-curve form is in ANSI X9.63, IEEE 1363a, ISO/IEC 18033-2 and SEC 1.
prereqs: [ecdh, hybrid-encryption, ind-cca-security]
see_also: [elliptic-curve-cryptography, elgamal-encryption, key-encapsulation-mechanism, fujisaki-okamoto-transform, hmac, x25519, authenticated-encryption, small-subgroup-attack]
sources:
  - paper: "Michel Abdalla, Mihir Bellare and Phillip Rogaway, The oracle Diffie-Hellman assumptions and an analysis of DHIES, CT-RSA 2001, LNCS 2020, pages 143 to 158"
    locator: the definition of DHIES, the oracle Diffie-Hellman assumption, and the IND-CCA2 theorem
  - url: "https://www.secg.org/sec1-v2.pdf"
    title: Standards for Efficient Cryptography Group, SEC 1, Elliptic Curve Cryptography, version 2.0, 2009
    locator: Section 5.1 (ECIES) and Section 3.6.1 (the ANSI X9.63 key derivation function)
  - url: "https://www.secg.org/sec2-v2.pdf"
    title: Standards for Efficient Cryptography Group, SEC 2, Recommended Elliptic Curve Domain Parameters, version 2.0, 2010
    locator: the parameters of secp256k1
  - url: "https://eprint.iacr.org/2001/112"
    title: Victor Shoup, A proposal for an ISO standard for public key encryption, version 2.1, 2001
    locator: ECIES-KEM, the KEM and DEM split, and the benign malleability that comes from hashing only the shared x-coordinate
  - paper: "ISO/IEC 18033-2, Information technology, Security techniques, Encryption algorithms, Part 2, Asymmetric ciphers, 2006"
    locator: ECIES-KEM and its combination with a data encapsulation mechanism
  - book: isbn:9780387952734
    title: Darrel Hankerson, Alfred Menezes and Scott Vanstone, Guide to Elliptic Curve Cryptography, Springer, 2004
    locator: Chapter 4, the section on public-key encryption (ECIES)
  - paper: "Adrian Antipa, Daniel Brown, Alfred Menezes, Rene Struik and Scott Vanstone, Validation of elliptic curve public keys, PKC 2003, LNCS 2567, pages 211 to 223"
    locator: invalid curve attacks on ECIES and on one-pass ECDH without public key validation
  - paper: "David Cash, Eike Kiltz and Victor Shoup, The twin Diffie-Hellman problem and applications, Eurocrypt 2008, LNCS 4965"
    locator: hashed ElGamal that is IND-CCA2 under plain CDH in the random oracle model
  - url: "https://www.rfc-editor.org/rfc/rfc9180"
    title: Richard Barnes, Karthikeyan Bhargavan, Benjamin Lipp and Christopher Wood, RFC 9180, Hybrid Public Key Encryption, 2022
    locator: the DHKEM and the key schedule, a modern successor of ECIES
---

The Elliptic Curve Integrated Encryption Scheme (ECIES) is [hybrid encryption](/hybrid-encryption/) built on [elliptic-curve Diffie-Hellman](/ecdh/). The sender makes a fresh key pair $(k, R = kG)$, computes the Diffie-Hellman point $Z = kQ$ with the receiver's public key $Q$, hashes $Z$ into an encryption key and a MAC key, and sends $R$ with the encrypted message and its tag. Abdalla, Bellare and Rogaway proposed it over any group as DHAES (later DHIES) and proved it [IND-CCA2](/ind-cca-security/) secure under an oracle Diffie-Hellman assumption. It is standardized in SEC 1, ANSI X9.63, IEEE 1363a and ISO/IEC 18033-2, with different menus of options.

**Notation.** $E$ is an elliptic curve over the prime field $\mathbb{F}_p$, and $b$ is the number of binary digits of $p$. $G$ is the base point; it plays the role of the generator $g$ of the other pages, and its order $n$ is a prime. $h = \#E(\mathbb{F}_p)/n$ is the cofactor ($h = 1$ for secp256k1). $d$ is the private key, $Q = dG$ the public key, $k$ the ephemeral scalar and $R = kG$. $x(Z)$ is the x-coordinate of a point $Z$. $\mathrm{KDF}$ is a key derivation function, $\mathrm{MAC}$ a message authentication code, and $l$ the message length in bytes. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$ with $q_d$ decryption queries and $q_h$ hash queries, and $\mathrm{Adv}$ an advantage. See [elliptic-curve cryptography](/elliptic-curve-cryptography/) for the group law.

## In plain words

The receiver has a secret number and a public point made from it. To send a message, the sender makes a one-time secret number and a one-time public point. From the one-time secret and the receiver's public point, the sender computes a shared point; the receiver gets the same shared point from its own secret and the one-time public point. Both hash the shared point into two keys.

The sender uses the first key to encrypt the message with a fast symmetric cipher and the second key to compute a tag on the result. It sends the one-time public point, the encrypted message and the tag. The receiver checks the one-time point, recomputes the keys, checks the tag, and only then decrypts. Any change to the ciphertext makes the tag check fail.

## The problem

ECIES solves [public-key encryption](/public-key-encryption/) of messages of any length. The aim is IND-CCA2 security with a short ciphertext: one point plus the message length plus a tag. Plain [ElGamal](/elgamal-encryption/) on a curve needs the message encoded as a point and is malleable; ECIES avoids both by hashing the Diffie-Hellman value into symmetric keys.

## The algorithm

The domain parameters $(p, a, b, G, n, h)$ are public. The code uses the SEC 1 options: the ANSI X9.63 KDF with SHA-256, the XOR encryption scheme, and [HMAC](/hmac/)-SHA-256 with a 32-byte tag. With $\mathrm{bind} = $ true, the encoded point $\bar{R}$ also goes into the KDF, as in DHIES and ISO 18033-2.

```pseudo id=main
ECIES-KEYGEN(curve)
L1  d ← a uniform integer in {1, …, n − 1}
L2  Q ← d · G
L3  return the public key Q and the private key d

ECIES-ENCRYPT(Q, m)
L4  k ← a uniform integer in {1, …, n − 1}
L5  R ← k · G                         ▷ the ephemeral public key, sent as R̄
L6  Z ← (h · k) · Q                   ▷ the Diffie-Hellman point
L7  (k_E, k_M) ← KDF(x(Z) ‖ (R̄ if bind), |m| + 32)
L8  c ← m ⊕ k_E
L9  t ← MAC(k_M, c)
L10 return (R̄, c, t)

ECIES-DECRYPT(d, (R̄, c, t))
L11 R ← decode(R̄); if R is not on E then return ⊥
L12 Z ← (h · d) · R; if Z = O then return ⊥
L13 (k_E, k_M) ← KDF(x(Z) ‖ (R̄ if bind), |c| + 32)
L14 if MAC(k_M, c) ≠ t then return ⊥  ▷ compare in constant time
L15 return c ⊕ k_E
```

Lines L5 and L6 are an [ECDH](/ecdh/) exchange between the static key $Q$ and the ephemeral key $R$. Lines L7 to L9 are a one-time [authenticated encryption](/authenticated-encryption/) of $m$ in the encrypt-then-MAC form. Line L11 is public key validation, and line L12 multiplies by the cofactor so that a point of small order gives $Z = O$.

## Example

Take the toy curve $y^2 = x^3 + 2x + 2$ over $\mathbb{F}_{17}$. It has 19 points, so every point other than $O$ generates it, $n = 19$ is prime and $h = 1$. Take $G = (5, 1)$. The KDF and MAC are those of the code; the x-coordinate is one byte.

| step | computation | value |
|---|---|---|
| L1 | private key | $d = 7$ |
| L2 | $Q = 7G$ | $(0, 6)$ |
| L4 | ephemeral scalar | $k = 10$ |
| L5 | $R = 10G$, encoded as $\bar{R}$ | $(7, 11)$, bytes `04 07 0b` |
| L6 | $Z = 10Q$ | $(16, 4)$ |
| L7 | $\mathrm{KDF}(\texttt{10}, 34)$, first two bytes | $k_E =$ `65 98` |
| L8 | $m = $ "hi" $=$ `68 69`, XOR $k_E$ | $c =$ `0d f1` |
| L9 | HMAC-SHA-256 under the other 32 bytes | $t$ starts `50 b9 bb 64` |
| L12 | $Z = 7R$ | $(16, 4)$, the same point |
| L15 | $c \oplus k_E$ | "hi" |

The point $-R = (7, 6)$ gives $7 \cdot (-R) = (16, 13) = -Z$, which has the same x-coordinate 16. So without binding, $(\overline{-R}, c, t)$ is a different ciphertext that decrypts to "hi". The test file checks every number in this table and the same effect on secp256k1.

## Correctness

Both sides compute the same point: $(hk)Q = (hk)(dG) = (hd)(kG) = (hd)R$, because scalar multiplication satisfies $a(bP) = (ab)P$. This point is not $O$, because $n$ is prime and does not divide $h$, $k$ or $d$. So both sides feed the same input to the KDF, get the same $k_E$ and $k_M$, the tag check passes, and $c \oplus k_E = m$. The full proof is below.

## Complexity

With schoolbook arithmetic a field multiplication costs $\Theta(b^2)$ and an inversion $\Theta(b^2)$ by the extended Euclidean algorithm. A scalar multiplication by double-and-add takes $\Theta(b)$ point operations, so $\Theta(b^3)$.

- **Encryption**: two scalar multiplications (lines L5 and L6), plus $\Theta(l)$ hashing for the KDF, the XOR and the MAC: $\Theta(b^3 + l)$.
- **Decryption**: one curve equation check, one scalar multiplication and $\Theta(l)$ hashing: $\Theta(b^3 + l)$.
- **Ciphertext size**: $1 + 2b/8$ bytes for an uncompressed point (or $1 + b/8$ compressed), plus $l$, plus the tag. On a 256-bit curve the overhead is 97 bytes with the code's choices, against 256 bytes for RSA-2048 with OAEP.

$G$ is fixed, so line L5 can use precomputed multiples; Jacobian coordinates avoid most inversions. These change the constants, not the bound.

## Properties

### IND-CCA2 security

**Theorem (Abdalla, Bellare and Rogaway, 2001, informal).** Let DHIES hash $\bar{R} \| Z$ (the bound form). For every IND-CCA2 adversary $\mathcal{A}$ against DHIES there are adversaries $\mathcal{B}_1$, $\mathcal{B}_2$, $\mathcal{B}_3$ with about the same running time and

$$\mathrm{Adv}^{\mathrm{ind\text{-}cca2}}_{\mathrm{DHIES}}(\mathcal{A}) \le 2\,\mathrm{Adv}^{\mathrm{odh}}(\mathcal{B}_1) + 2\,\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_{\mathrm{SYM}}(\mathcal{B}_2) + 2\,q_d\,\mathrm{Adv}^{\mathrm{suf\text{-}cma}}_{\mathrm{MAC}}(\mathcal{B}_3),$$

where the symmetric scheme need only be secure for one message and the MAC need only be unforgeable after one tag. The paper states the exact constants.

The *oracle Diffie-Hellman* (ODH) assumption says that $\mathrm{KDF}(\bar{R} \| kQ)$ looks random given $Q$, $R$ and an oracle that returns $\mathrm{KDF}(\bar{X} \| dX)$ for every point $X \ne R$. It is a standard model assumption, but it is about the KDF and the group together. In the random oracle model for the KDF, ABR show that ODH follows from the *strong* Diffie-Hellman problem: [CDH](/computational-diffie-hellman/) is hard even with an oracle that decides whether $dX = Y$ for given $X, Y$. That reduction is tight, because the oracle lets it find the one hash query that matters. A reduction to plain CDH loses a factor $q_h$; Cash, Kiltz and Shoup (2008) avoid that loss with the twin Diffie-Hellman trick.

*Proof idea.* Replace the challenge keys by random strings; ODH says that $\mathcal{A}$ cannot notice, even with decryption answers, because every other ciphertext uses a different $\bar{R}$ or is handled by the oracle. Then the challenge message is hidden by a one-time cipher under a random key, and each decryption query that reuses the challenge $\bar{R}$ needs a forged tag under a random MAC key. $\square$

### Benign malleability

SEC 1 by default hashes only $x(Z)$. Then $\overline{-R}$, and on some menus the compressed and uncompressed encodings of $R$, give the same keys, so a ciphertext has a few public variants that decrypt to the same message. A strict IND-CCA2 adversary wins with one query. Shoup (2001) calls this *benign malleability*; the scheme still meets a relaxed notion in which the decryption oracle refuses such variants. ISO 18033-2 and DHIES put $\bar{R}$ into the KDF, which removes it (option bind of the code).

### Other properties

- **Randomized.** Each encryption uses a fresh $k$, as [probabilistic encryption](/probabilistic-encryption/) requires.
- **One static key operation per decryption.** Decryption needs only $d$ and one scalar multiplication.
- **No forward secrecy for the receiver.** Anyone who later learns $d$ can decrypt every past ciphertext.

## Variants and improvements

- **DHIES.** The same scheme in a subgroup of $\mathbb{Z}_p^*$; see [ElGamal](/elgamal-encryption/) for that setting.
- **ECIES-KEM plus a DEM.** ISO 18033-2 splits the scheme into a [KEM](/key-encapsulation-mechanism/) (lines L4 to L7, with $\bar{R}$ hashed) and a data encapsulation mechanism, usually an AEAD such as AES-GCM in place of lines L8 and L9.
- **Symmetric and MAC menus.** SEC 1 lists XOR, triple DES in CBC mode, AES in CBC and CTR modes, and HMAC or CMAC. XOR is fine for short messages; use AES-CTR or an AEAD for long ones.
- **Cofactor modes.** On curves with $h > 1$, such as Curve25519 with $h = 8$, line L12 multiplies by $h$ or the receiver checks that $nR = O$.
- **HPKE (RFC 9180).** A modern successor with a DH-based KEM over [X25519](/x25519/) or P-256, HKDF, an AEAD, and modes with sender authentication. libsodium's sealed boxes are a similar construction.
- **Twin ElGamal.** Two public keys and a two-point hash give IND-CCA2 under plain CDH in the random oracle model (Cash, Kiltz and Shoup 2008).
- **[Fujisaki-Okamoto](/fujisaki-okamoto-transform/) over ElGamal** gives another IND-CCA KEM from CDH in the random oracle model, at the cost of a re-encryption in decryption.

## When to use it

Use ECIES when a protocol or a standard requires it. Ethereum's RLPx transport, for example, uses an ECIES variant on secp256k1. For new designs prefer HPKE, which fixes one set of options and has published test vectors. Compared with [RSA-OAEP](/rsa-oaep/), ECIES has much shorter keys and ciphertexts and faster key generation. Compared with [Cramer-Shoup](/cramer-shoup-cryptosystem/), it is faster and shorter, but its proof needs an interactive assumption or the random oracle model. Neither ECIES nor RSA survives a large quantum computer; for that, use a post-quantum KEM such as [ML-KEM](/crystals-kyber/), alone or with ECIES in a hybrid.

## Pitfalls

- **No public key validation.** If line L11 is skipped, the attacker sends a point $R$ on another curve with the same $a$, where it has small order $r$. The doubling and addition formulas do not use $b$, so $dR$ is computed on that curve, and whether the tag check passes tells $d \bmod r$. With enough small $r$ and the Chinese remainder theorem the attacker gets $d$ (Antipa et al. 2003; Jager, Schwenk and Somorovsky showed it against TLS libraries in 2015). The test file shows the first step with a point of order 3 on $y^2 = x^3 + 1$.
- **Ignoring the cofactor.** On a curve with $h > 1$, a point of small order passes the curve check; without line L12's multiplication by $h$ this is a [small subgroup attack](/small-subgroup-attack/).
- **Hashing only $x(Z)$ when IND-CCA2 is needed.** The $-R$ variant decrypts to the same message (see the test). Bind $\bar{R}$ into the KDF, or check that $\bar{R}$ is in one canonical encoding and accept the relaxed notion knowingly.
- **A non-constant-time tag check or scalar multiplication.** A comparison that stops at the first wrong byte lets an attacker forge tags byte by byte, and a double-and-add loop that branches on $d$ leaks it through timing. The Python code is not constant time apart from the tag check.
- **Decrypt before verify.** Releasing $c \oplus k_E$ or any error before line L14 succeeds turns the scheme into a malleable one.
- **Incompatible option sets.** SEC 1, ANSI X9.63, IEEE 1363a and ISO 18033-2 differ in KDF input, key order, point encoding and tag length, so two "ECIES" libraries often fail to interoperate. Fix every option in the protocol.

## Implementations

The Python code is for study only. It is not constant time (double-and-add branches on the secret, and the field inversions leak timing), it uses affine coordinates, and it must not protect real data. Use HPKE or libsodium's sealed boxes from a maintained library. There are no official test vectors for ECIES, because the standards leave the options open. The tests check the secp256k1 constants ($G$ on the curve, $nG = O$, $p$ and $n$ prime), the worked example above, the KDF counter layout, the round trip with and without binding, rejection of changed ciphertexts, the $-R$ attack on the IND-CCA2 game, and the invalid curve leak without line L11.

## History

Abdalla, Bellare and Rogaway submitted DHAES to the IEEE P1363a working group in 1998; it was renamed DHIES, and their analysis with the oracle Diffie-Hellman assumptions appeared at CT-RSA 2001. The elliptic-curve version entered ANSI X9.63 (2001), SEC 1 (version 1.0 in 2000, version 2.0 in 2009), IEEE 1363a (2004) and ISO/IEC 18033-2 (2006). Shoup's 2001 proposal for the ISO standard introduced the KEM and DEM split and the analysis of benign malleability. Antipa, Brown, Menezes, Struik and Vanstone (2003) showed why public key validation is needed. HPKE (RFC 9180, 2022) is the current general-purpose successor.

## References
