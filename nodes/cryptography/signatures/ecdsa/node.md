---
tag: QNKB84
kind: algorithm
slug: ecdsa
name: Elliptic Curve Digital Signature Algorithm
aliases:
- ECDSA
area: cryptography/signatures
level: intro
summary: "DSA over an elliptic curve group: r is the x coordinate of kG mod n and s = (z + r d)/k mod n. Used widely in TLS and blockchains; FIPS 186-5, SEC 1, X9.62."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1992
  people: [Scott Vanstone]
  note: Proposed by Vanstone in 1992 in answer to the NIST proposal of DSA. Standardized in ANSI X9.62 (1999), FIPS 186-2 (2000) and SEC 1. FIPS 186-5 (2023) is the current NIST standard.
prereqs: [dsa, elliptic-curve-cryptography, digital-signature]
see_also: [schnorr-signature, ed25519, deterministic-nonce-generation, nonce-reuse-attack, signature-malleability, signature-forgery, threshold-signature, elliptic-curve-discrete-logarithm-problem]
sources:
  - url: "https://doi.org/10.6028/NIST.FIPS.186-5"
    title: NIST, FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: Section 6 (the Elliptic Curve Digital Signature Algorithm), signature generation and signature verification
  - url: "https://www.secg.org/sec1-v2.pdf"
    title: Certicom Research, SEC 1, Elliptic Curve Cryptography, version 2.0, 2009
    locator: Section 4.1 (ECDSA), with 4.1.3 signing, 4.1.4 verification and 4.1.6 public key recovery
  - paper: "ANSI X9.62-2005, Public Key Cryptography for the Financial Services Industry, The Elliptic Curve Digital Signature Algorithm (ECDSA), American National Standards Institute, 2005"
    locator: the first standard of ECDSA (first edition 1999), with the signing and verification steps
  - url: "https://doi.org/10.6028/NIST.SP.800-186"
    title: NIST, SP 800-186, Recommendations for Discrete Logarithm-based Cryptography, Elliptic Curve Domain Parameters, February 2023
    locator: Section 3.2.1, the parameters of the curve P-256
  - url: "https://www.rfc-editor.org/rfc/rfc6979"
    title: Thomas Pornin, RFC 6979, Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA), 2013
    locator: Appendix A.2.5 (ECDSA, 256 bits, P-256), the key and the SHA-256 signatures of "sample" and "test", copied in the tests
  - paper: doi:10.1007/s102070100002
    title: Don Johnson, Alfred Menezes and Scott Vanstone, The Elliptic Curve Digital Signature Algorithm (ECDSA), International Journal of Information Security 1(1), 2001, pages 36 to 63
    locator: the history of the scheme, the steps, and the survey of attacks and security arguments
  - paper: doi:10.1007/s10623-003-6154-z
    title: Daniel R. L. Brown, Generic groups, collision resistance, and ECDSA, Designs, Codes and Cryptography 35, 2005, pages 119 to 152
    locator: the proof of security of ECDSA in the generic group model, from properties of the hash function
  - paper: doi:10.1145/2976749.2978413
    title: Manuel Fersch, Eike Kiltz and Bertram Poettering, On the provable security of (EC)DSA signatures, ACM CCS 2016, pages 1651 to 1662
    locator: the proof of unforgeability with the conversion function modeled as an idealized bijective random oracle
  - url: "https://nvd.nist.gov/vuln/detail/CVE-2022-21449"
    title: NIST National Vulnerability Database, CVE-2022-21449
    locator: the Java ECDSA verifier that accepted the signature r = s = 0
---

ECDSA is the [DSA](/dsa/) signature moved from a subgroup of $\mathbb{Z}_p^*$ to the group of points of an [elliptic curve](/elliptic-curve-cryptography/). The signer picks a fresh secret nonce $k$, takes $r$ as the $x$ coordinate of the point $kG$ reduced mod the group order $n$, and computes $s = k^{-1}(z + r d) \bmod n$ from the hash $z$ of the message and the secret key $d$. The verifier rebuilds $kG$ as $u_1 G + u_2 Q$ without knowing $k$. ECDSA is in ANSI X9.62, SEC 1 and FIPS 186-5. It signs most TLS certificates on P-256, and it is the signature of Bitcoin and Ethereum on secp256k1.

**Notation.** $E$ is a curve over $\mathbb{F}_p$ with a base point $G$ of prime order $n$. $d \in [1, n-1]$ is the secret key and $Q = dG$ the public key. $H$ is a hash function and $z$ is the integer made of the leftmost $\lceil \log_2 n \rceil$ binary digits of $H(m)$. $x(P)$ is the $x$ coordinate of a point $P$, seen as an integer in $[0, p-1]$. $O$ is the point at infinity.

## In plain words

The signer has a secret number and a public point made from it. To sign, the signer picks a new secret random number, turns it into a point, and keeps only one coordinate of that point as the first half of the signature. The second half mixes the random number, the secret key, the first half and the hash of the message, so that only someone who knows the secret key could make it fit.

The verifier cannot see the random number, but it can rebuild its point from the two halves, the hash and the public point, and then compare the coordinate with the first half.

The random number is the weak spot. If it repeats, leaks or is slightly biased, anyone can compute the secret key from a few signatures.

## The problem

ECDSA solves the [digital signature](/digital-signature/) problem: key generation, signing and verification, such that honest signatures verify and an adversary that sees signatures on messages of its choice cannot make a valid signature on a new message (EUF-CMA, see [existential unforgeability](/existential-unforgeability/)). It does so with keys and signatures much shorter than [RSA signatures](/rsa-signature/) or DSA at the same security, because the best known attack on the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/) on a good curve is generic and takes about $\sqrt{n}$ steps.

## The algorithm

Key generation picks $d$ uniform in $[1, n-1]$ and sets $Q = dG$.

```pseudo id=main
SIGN(d, m)
L1  z ← the leftmost ⌈log2 n⌉ binary digits of H(m), as an integer
L2  k ← uniform in [1, n − 1]                 ▷ fresh, secret, unbiased
L3  (x1, y1) ← k·G
L4  r ← x1 mod n
L5  s ← k⁻¹ · (z + r·d) mod n
L6  if r = 0 or s = 0 then go to L2
L7  return (r, s)

VERIFY(Q, m, (r, s))
L8  if r ∉ [1, n − 1] or s ∉ [1, n − 1] then return false
L9  z ← the leftmost ⌈log2 n⌉ binary digits of H(m), as an integer
L10 w ← s⁻¹ mod n;  u1 ← z·w mod n;  u2 ← r·w mod n
L11 X ← u1·G + u2·Q
L12 if X = O then return false
L13 return x(X) mod n = r
```

The verifier must also check that $Q$ is a point of the curve, not $O$, and in the group of order $n$. On a curve of prime order such as P-256 the last check is automatic.

**The function $x(\cdot) \bmod n$.** This conversion function is the only link between the point $kG$ and the integer $r$. It is not a hash: the points $P$ and $-P$ give the same $r$, and it has no clean algebraic structure either. This is why the security proofs of ECDSA need unusual assumptions (see Properties).

**P-256.** FIPS 186-5 with SP 800-186 fixes curves; the most used is P-256, $y^2 = x^3 - 3x + b$ over $\mathbb{F}_p$ with $p = 2^{256} - 2^{224} + 2^{192} + 2^{96} - 1$ and a prime group order $n$ of 256 binary digits. Its cofactor is 1. Bitcoin and Ethereum use secp256k1 from SEC 2 instead.

### The low-s rule

If $(r, s)$ is valid, so is $(r, n - s)$: it is the signature with the nonce $-k$, whose point $-kG$ has the same $x$ coordinate. So ECDSA is not [strongly unforgeable](/strong-unforgeability/): anyone can change a signature into a second valid one for the same message (see [signature malleability](/signature-malleability/)). Bitcoin relied on a signature to fix a transaction id, so this changed ids. The fix is the low-s rule: the signer outputs $\min(s, n - s)$, and the verifier rejects $s > n/2$. Bitcoin Core made it a relay rule in 2015, and Ethereum made it a consensus rule for transactions in EIP-2 (Homestead).

### Public key recovery

From $(r, s)$ and $m$ anyone can compute the public key, given a small hint $v$ that tells which point $R$ had the $x$ coordinate $r$. Rewrite the signing equation as $sk = z + rd$, multiply by $G$, and solve:

$$Q = r^{-1}(sR - zG).$$

The candidates for $R$ are the points with $x(R) = r + jn$ (for $j = 0$, and $j = 1$ when $r + n < p$, which is rare) and either parity of $y$. The recovery id $v \in \{0, 1, 2, 3\}$ stores the parity in its low digit and $j$ in its high digit. Ethereum sends $(r, s, v)$ and no public key: the address is a hash of the recovered key. SEC 1 Section 4.1.6 gives the steps. When the signer applies the low-s rule, it also flips the parity digit of $v$, because $n - s$ belongs to the point $-R$.

## Example

RFC 6979 Appendix A.2.5 gives a P-256 key and signatures with SHA-256. The secret key is

$d$ = `C9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721`,

and $Q = dG$ has $x(Q)$ = `60FED4BA...60F29FB6` and $y(Q)$ = `7903FE10...D4462299`. For the message "sample":

| step | value |
|---|---|
| $z$ | SHA-256("sample") = `AF2BDBE1...62ADD1BF`, all 256 binary digits |
| $k$ (from RFC 6979) | `A6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60` |
| $r = x(kG) \bmod n$ | `EFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716` |
| $s = k^{-1}(z + rd) \bmod n$ | `F7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8` |

The verifier computes $u_1 G + u_2 Q$ and finds a point whose $x$ coordinate mod $n$ is $r$. This $s$ starts with `F7`, so it is above $n/2$: a signer that applies the low-s rule outputs $n - s$ instead, and both values verify under the plain rules. The code on this page reproduces this vector and the one for "test" with the given $k$.

## Correctness

Let $(r, s)$ come from lines L1 to L7, so $s k \equiv z + r d \pmod n$ and $s \ne 0$. Then

$$u_1 G + u_2 Q = s^{-1} z G + s^{-1} r d G = s^{-1}(z + r d) G = k G,$$

because $G$ has order $n$. So $X = kG \ne O$, and $x(X) \bmod n = r$. The proof below also covers the low-s rule and public key recovery.

## Complexity

Let $n$ also denote, by abuse, the number of binary digits of the group order ($n = 256$ for P-256).

- **Signing**: one fixed-base scalar multiplication $kG$ (fast with tables, because $G$ is fixed), one inverse mod $n$ and two multiplications mod $n$.
- **Verification**: one inverse mod $n$ and one double scalar multiplication $u_1 G + u_2 Q$, which Shamir's trick does in about the cost of one.
- **Sizes**: a public key is one point (33 bytes compressed for P-256), a signature is two integers mod $n$ (64 bytes raw, about 70 to 72 bytes in the DER encoding of X9.62).
- **Time**: with schoolbook field arithmetic a group operation costs $\Theta(n^2)$ word operations and a scalar multiplication $\Theta(n)$ group operations, so $\Theta(n^3)$. Space is $\Theta(n)$.

## Properties

- **Security proofs need strong idealizations.** No proof of ECDSA from the plain discrete log assumption in the random oracle model is known. Brown (2005) proved it EUF-CMA in the [generic group model](/generic-group-model/), if the hash is collision resistant and has two one-wayness properties. Fersch, Kiltz and Poettering (2016) proved it unforgeable with the conversion function $x(\cdot) \bmod n$ modeled as an idealized bijective random oracle, from the hardness of the discrete logarithm and properties of the hash.
- **Not strongly unforgeable.** $(r, n - s)$ is a second valid signature; the low-s rule removes it.
- **Randomized, and fragile in the nonce.** If $k$ repeats for two messages, $k = (z_1 - z_2)/(s_1 - s_2)$ and then $d = (s_1 k - z_1)/r$ mod $n$. If a few top binary digits of many nonces are known or biased, a lattice attack on the hidden number problem finds $d$. See the [nonce reuse attack](/nonce-reuse-attack/) page. [Deterministic nonce generation](/deterministic-nonce-generation/) (RFC 6979) removes the need for a random source at signing time; FIPS 186-5 allows it.
- **The signature does not bind the key.** The hash does not include the public key, so one signature on one message verifies under several keys: public key recovery returns up to four of them, one per $v$.

## Variants and improvements

- **Deterministic ECDSA** (RFC 6979, and allowed in FIPS 186-5): $k$ is an HMAC-DRBG output keyed by $d$ and $H(m)$. The verifier and the signature format do not change.
- **Hedged ECDSA**: mix fresh randomness into the deterministic nonce, which helps against fault attacks. See [deterministic nonce generation](/deterministic-nonce-generation/).
- **Low-s and recoverable signatures**, described above. Ethereum writes $v$ as 27 or 28, and from EIP-155 on also mixes in the chain id.
- **Threshold ECDSA**: the inverse $k^{-1}$ makes multi-party ECDSA much harder than for Schnorr; see [threshold signatures](/threshold-signature/).
- **Schnorr-type signatures** such as [Ed25519](/ed25519/) and [BIP 340](/schnorr-signature/) on the same kind of group have a proof in the random oracle model, no malleability, and linear multi-party signing.

## When to use it

Use ECDSA when a standard or a peer requires it: X.509 certificates in TLS on P-256, FIDO and WebAuthn, smart cards, and Bitcoin and Ethereum transactions on secp256k1. Use a library (OpenSSL, BoringSSL, libsecp256k1, or a FIPS 140 validated module) with deterministic or hedged nonces and the low-s rule where malleability matters. For new designs without that constraint, [Ed25519](/ed25519/) is simpler to implement safely.

## Pitfalls

- **A reused, leaked or biased nonce.** Sony reused one $k$ in the PlayStation 3, and a weak random generator in Android in 2013 repeated nonces in Bitcoin wallets. Timing leaks of a few binary digits of $k$ (Minerva, TPM-Fail) were enough for lattice attacks. See the [nonce reuse attack](/nonce-reuse-attack/).
- **A missing range check.** Line L8 must reject $r = 0$ and $s = 0$. Java 15 to 18 skipped it, so the signature $r = s = 0$ verified for every message and key (CVE-2022-21449, a [signature forgery](/signature-forgery/)).
- **Malleability.** A protocol that uses the signature bytes as an id must apply the low-s rule and a strict encoding (Bitcoin did both, in BIP 66 for strict DER and in its low-s relay rule).
- **The wrong hash truncation.** When $H$ outputs more binary digits than $n$ has, keep the leftmost ones, not the rightmost ones, or the signatures will not interoperate.
- **Invalid public keys.** A verifier must check that $Q$ is on the curve and in the right group, and must not trust a key recovered from a signature unless it compares it with a known key or address.
- **Side channels.** The scalar multiplication $kG$ and the inverse $k^{-1}$ must take time that does not depend on $k$.

## Implementations

The Python code on this page implements P-256 in affine coordinates, signing with a given or random $k$, verification with the range checks, the low-s rule and public key recovery. The tests reproduce the two SHA-256 vectors of RFC 6979 Appendix A.2.5, copied by hand, and check malleability, the $r = s = 0$ rejection and recovery. The code is for study only. It is not constant time, it branches on secret values, and it must not be used to protect real data.

## History

Scott Vanstone proposed ECDSA in 1992, in comments on the NIST proposal of the [Digital Signature Algorithm](/dsa/). It was accepted in ISO/IEC 14888-3 in 1998, in ANSI X9.62 in 1999, in IEEE 1363 in 2000 and in FIPS 186-2 in 2000, and the SECG published it in SEC 1. Johnson, Menezes and Vanstone wrote the standard survey of the scheme in 2001.

Bitcoin chose ECDSA on secp256k1 in 2009, and Ethereum followed in 2015 with public key recovery. Brown gave the generic group proof in 2005 and Fersch, Kiltz and Poettering the idealized conversion function proof in 2016. Pornin's RFC 6979 (2013) gave a deterministic nonce after nonce failures such as the PlayStation 3 key recovery of 2010. FIPS 186-5 (2023) is the current NIST version, and it allows deterministic ECDSA.

## References
