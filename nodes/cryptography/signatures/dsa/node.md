---
tag: J4WE85
kind: algorithm
slug: dsa
name: Digital Signature Algorithm
aliases:
- DSA
- DSS
- Digital Signature Standard
area: cryptography/signatures
level: intro
summary: "NIST discrete-log signature in a subgroup of prime order q of Z_p*, with (L, N) up to (3072, 256) and a secret nonce per signature. FIPS 186-5 (2023) keeps it only to verify old signatures."
model: word-ram
complexity:
  vars: {b: the number of binary digits of the prime p, N: the number of binary digits of the subgroup order q}
  time: {worst: Θ(N b^2), average: Θ(N b^2), best: Θ(N b^2)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1991
  people: [David W. Kravitz, NIST]
  note: Proposed by NIST in August 1991 and published as FIPS 186 in May 1994. FIPS 186-3 (2009) added the larger (L, N) pairs. FIPS 186-5 (2023) withdrew approval for signing.
prereqs: [elgamal-signature, discrete-logarithm-problem]
see_also: [ecdsa, schnorr-signature, deterministic-nonce-generation, nonce-reuse-attack, lll-algorithm, ed25519, sha-2, signature-forgery]
sources:
  - url: "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf"
    title: NIST, FIPS 186-4, Digital Signature Standard (DSS), July 2013
    locator: Section 4.2 (the (L, N) pairs), Section 4.6 (signature generation), Section 4.7 (verification), Appendix A.1.1.2 and A.1.1.3 (generation and validation of p and q), Appendix A.2.1 (the generator g), Appendix B.1 (key pairs), Appendix B.2 (the per-message secret k)
  - url: "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf"
    title: NIST, FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: DSA is no longer approved for digital signature generation; it may be used to verify signatures generated before the implementation date of the standard
  - paper: "NIST, FIPS 186, Digital Signature Standard (DSS), May 1994"
    locator: the first version, with N = 160, SHA-1 and L from 512 to 1024 in steps of 64
  - url: "https://www.rfc-editor.org/rfc/rfc6979"
    title: Thomas Pornin, RFC 6979, Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA), August 2013
    locator: Appendix A.2.2, DSA with 2048 binary digits and N = 256, keys and signatures with k for SHA-1 to SHA-512 on the messages "sample" and "test"
  - paper: "Nick A. Howgrave-Graham and Nigel P. Smart, Lattice attacks on digital signature schemes, Designs, Codes and Cryptography 23(3), pages 283 to 290, 2001"
    locator: recovery of the DSA private key from a few known binary digits of each nonce, with lattice reduction
  - paper: "Phong Q. Nguyen and Igor E. Shparlinski, The insecurity of the Digital Signature Algorithm with partially known nonces, Journal of Cryptology 15(3), pages 151 to 176, 2002"
    locator: a provable polynomial-time attack through the hidden number problem when a few binary digits of each nonce are known
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.5.1, the DSA, and Note 11.62 on r = 0 and s = 0
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, DSA and ECDSA
---

The Digital Signature Algorithm (DSA) is the signature scheme of the US Digital Signature Standard (DSS), FIPS 186. It is a variant of [ElGamal signatures](/elgamal-signature/) that works in a subgroup of prime order $q$ of the integers modulo a large prime $p$: a signature is $r = (g^k \bmod p) \bmod q$ and $s = k^{-1}(z + x r) \bmod q$, so it has $2N$ binary digits instead of $2L$. NIST proposed it in 1991 and published it in 1994; FIPS 186-3 (2009) added parameters with $q$ of 224 and 256 binary digits. FIPS 186-5 (February 2023) no longer approves DSA for signature generation and keeps it only to verify signatures made before; its elliptic-curve form, [ECDSA](/ecdsa/), and EdDSA remain.

**Notation.** $p$ is a prime of $L$ binary digits ($b = L$ in the complexity), $q$ a prime of $N$ binary digits that divides $p - 1$, and $g$ an element of order $q$ in $\mathbb{Z}_p^*$; $(p, q, g)$ are the domain parameters. The private key is $x$ with $1 \le x \le q - 1$ and the public key is $y = g^x \bmod p$. $k$ is the per-message secret number, the nonce. $\mathrm{Hash}$ has output length $\mathit{outlen}$, and $z$ is the integer given by the leftmost $\min(N, \mathit{outlen})$ binary digits of $\mathrm{Hash}(M)$. The signature is $(r, s)$.

## In plain words

DSA is a way to sign with a secret number whose public version is a power of a fixed base. The signer picks a fresh secret random number for each message, raises the base to it, and keeps only a short remainder of the result as the first half of the signature. It then solves a small equation that mixes this value, the hash of the message and the secret key to get the second half.

The checker reverses the equation using only public values and checks that it arrives at the same short remainder. All the work happens in a small group of prime size, which keeps signatures short.

The fresh random number is critical. If it is ever repeated, or even if a few of its digits leak over many signatures, an attacker can compute the secret key.

## The problem

Sign messages with a key whose security rests on the [discrete logarithm problem](/discrete-logarithm-problem/) in $\mathbb{Z}_p^*$, with signatures and exponents of only $N$ binary digits, about twice the security level, while $p$ is large enough to resist index calculus. The design moves ElGamal into a subgroup of prime order $q$, as Schnorr did, and keeps an ElGamal-style signing equation.

## The algorithm

**Parameters.** FIPS 186-4, Section 4.2 allows these pairs $(L, N)$:

| $L$ | $N$ | use |
|---|---|---|
| 1024 | 160 | only to verify old signatures since SP 800-131A; first allowed in FIPS 186 |
| 2048 | 224 | added in FIPS 186-3 |
| 2048 | 256 | added in FIPS 186-3 |
| 3072 | 256 | added in FIPS 186-3 |

The hash must have a security strength at least that of the pair; if $\mathit{outlen} > N$, only the leftmost $N$ binary digits of the hash are used.

**Domain parameters (FIPS 186-4, Appendix A).** Appendix A.1.1.2 makes $p$ and $q$ verifiably from a random seed: it hashes the seed to get a candidate $q = 2^{N-1} + U + 1 - (U \bmod 2)$ and tests it for primality; then, for a counter from 0 to $4L - 1$, it hashes the seed plus an offset into a number $X$ of $L$ binary digits, sets $p = X - ((X \bmod 2q) - 1)$, so that $p \equiv 1 \pmod{2q}$, and tests $p$. The seed and the counter are published, so that anyone can check by Appendix A.1.1.3 that the parameters were not chosen with a hidden structure. Appendix A.2.1 sets $g = h^{(p-1)/q} \bmod p$ for some $h$, usually $h = 2$, with $g \ne 1$.

```pseudo id=main
SIGN((p, q, g), x, M)
L1  z ← the leftmost min(N, outlen) binary digits of Hash(M), as an integer
L2  k ← uniform in {1, ..., q − 1}, secret and new for this message
L3  r ← (g^k mod p) mod q
L4  s ← k^(−1) · (z + x·r) mod q
L5  if r = 0 or s = 0 then go to L2
L6  return (r, s)

VERIFY((p, q, g), y, M, (r, s))
L7  if not (0 < r < q and 0 < s < q) then return invalid
L8  w ← s^(−1) mod q
L9  z ← the leftmost min(N, outlen) binary digits of Hash(M), as an integer
L10 u1 ← z·w mod q;  u2 ← r·w mod q
L11 v ← (g^u1 · y^u2 mod p) mod q
L12 return valid if v = r, else invalid
```

**The nonce $k$.** FIPS 186-4, Appendix B.2 gives two ways to draw $k$ from an approved random bit generator: take $N + 64$ random binary digits $c$ and set $k = (c \bmod (q - 1)) + 1$, which makes the bias negligible, or draw $N$ binary digits and retry until the value is in range. $k$ must be secret, uniform, and used once; $k^{-1} \bmod q$ must be kept as secret as $k$. [Deterministic nonce generation](/deterministic-nonce-generation/) (RFC 6979) derives $k$ from $x$ and the hash with HMAC instead.

**About the code.** The Python code is for study only. It is not constant time, its parameter generator uses a seeded non-cryptographic random source in the tests, and it must not protect real data. DSA is no longer approved for signing; use ECDSA or Ed25519 from the pyca/cryptography library or from a FIPS 140 validated module. The hash comes from `hashlib`, because the page is about the signature.

## Example

Toy parameters: $p = 23$, $q = 11$ (which divides $22$) and $g = 4$, which has order 11 because $4^{11} = 2^{22} \equiv 1 \pmod{23}$. The private key is $x = 7$, so $y = 4^7 \bmod 23 = 8$. Take $z = 5$ as the hash value and $k = 3$.

| line | computation | value |
|---|---|---|
| L3 | $g^k \bmod p = 4^3 \bmod 23$ | 18 |
| L3 | $r = 18 \bmod 11$ | 7 |
| L4 | $k^{-1} \bmod 11$ | 4 |
| L4 | $s = 4 \cdot (5 + 7 \cdot 7) \bmod 11 = 4 \cdot 54 \bmod 11$ | 7 |
| L8 | $w = 7^{-1} \bmod 11$ | 8 |
| L10 | $u_1 = 5 \cdot 8 \bmod 11$, $u_2 = 7 \cdot 8 \bmod 11$ | 7, 1 |
| L11 | $g^{u_1} y^{u_2} \bmod 23 = 8 \cdot 8 \bmod 23$ | 18 |
| L11 | $v = 18 \bmod 11$ | 7 |

$v = r$, so the signature is valid. Line L11 rebuilds exactly $g^k \bmod p = 18$, because $u_1 + x u_2 = 7 + 7 \cdot 1 = 14 \equiv 3 = k \pmod{11}$.

**Official vectors.** RFC 6979, Appendix A.2.2 gives a key with $L = 2048$ and $N = 256$ and, for the message "sample" with SHA-256, the nonce $k$ = `8926A27C...9D597C52` and the signature $r$ = `EACE8BDB...932CC809`, $s$ = `7081E175...93A38D53`. RFC 6979 derives $k$ deterministically, but this page uses the vectors only because they print $k$: the tests pass that $k$ to the FIPS 186-4 signing routine and get the printed $r$ and $s$. The tests use the vectors for SHA-256 on "sample" and "test", for SHA-1 (shorter than $N$) and for SHA-512 (truncated to 256 binary digits).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Line L4 gives $k \equiv w (z + x r) \pmod q$, so $u_1 + x u_2 \equiv k$, and since $g$ has order $q$, line L11 computes $g^k \bmod p$ again and reduces it to $r$.

**Security.** Forging is at least as hard as computing discrete logarithms in the subgroup, since $x$ gives every signature, but there is no proof that DSA is [EUF-CMA](/existential-unforgeability/) under the discrete logarithm assumption alone. The reduction modulo $q$ in line L3 is not an algebraic map, which blocks the usual proofs; the known proofs for DSA-type schemes use idealized models of the group or of this conversion. The best known attacks compute discrete logarithms, either in $\mathbb{Z}_p^*$ with the number field sieve, which sets $L$, or in the subgroup with [Pollard's rho](/pollard-rho-discrete-logarithm/) in about $\sqrt{q}$ steps, which sets $N$.

**Attacks on the nonce.** The private key falls if $k$ is weak:

- **Reuse.** Two signatures with the same $k$ have the same $r$, and then $k = (z_1 - z_2)(s_1 - s_2)^{-1}$ and $x = (k s_1 - z_1) r^{-1} \bmod q$; see [nonce reuse attack](/nonce-reuse-attack/).
- **Partial knowledge.** Howgrave-Graham and Smart (2001) recovered $x$ from a few known binary digits of each nonce over many signatures, with [lattice reduction](/lll-algorithm/). Nguyen and Shparlinski (2002) turned this into a provable attack through the hidden number problem. Each signature gives a linear relation $k_i \equiv s_i^{-1} z_i + s_i^{-1} r_i x \pmod q$ with a $k_i$ that is partly known, and enough such relations pin down $x$ as a short vector in a lattice.
- **Bias.** Even a small statistical bias of $k$ leaks $x$ over enough signatures, which is why Appendix B.2 adds 64 extra random binary digits before the reduction modulo $q - 1$.

## Complexity

With schoolbook arithmetic on numbers of $b = L$ binary digits, an exponentiation with an exponent of $N$ binary digits costs $\Theta(N b^2)$.

| operation | cost |
|---|---|
| sign | 1 exponentiation $g^k \bmod p$ with an $N$-digit exponent, 1 inverse modulo $q$, 2 multiplications modulo $q$; $g^k$ can be computed before the message is known |
| verify | 2 exponentiations with $N$-digit exponents ($g^{u_1}$, $y^{u_2}$), or one simultaneous double exponentiation, 1 inverse modulo $q$ |
| signature size | $2N$ binary digits, for example 512 for $N = 256$ |
| public key | $L$ binary digits for $y$, plus the domain parameters |

For $(L, N) = (3072, 256)$ the exponents have 256 binary digits instead of 3072 in ElGamal, which is the main gain of the subgroup.

## Properties

- **Randomized.** Each signature uses a new $k$.
- **Not strongly unforgeable as such.** No proof covers [strong unforgeability](/strong-unforgeability/); unlike in ECDSA, the obvious change $s \to q - s$ does not work, because $r$ depends on $g^k$ and not only on a coordinate that is the same for $\pm$.
- **Precomputation.** $k$, $r$ and $k^{-1}$ do not depend on the message, so a signer can compute them in advance; they must then be stored as secrets.
- **Withdrawn for signing.** FIPS 186-5 allows DSA only to verify signatures made before the standard took effect.

## Variants and improvements

- **[ECDSA](/ecdsa/).** The same equations in an elliptic-curve group, with $r$ the $x$-coordinate of $kG$ modulo $n$. Keys and signatures are much shorter at the same security level.
- **Deterministic DSA (RFC 6979).** Derives $k$ from $x$ and $z$ with HMAC-DRBG, which removes the need for a good random source at signing time; see [deterministic nonce generation](/deterministic-nonce-generation/).
- **[Schnorr signatures](/schnorr-signature/).** The same subgroup with a linear signing equation and a hash of the commitment, with a proof in the random oracle model through the forking lemma. EdDSA follows this pattern.
- **GOST R 34.10-94 and KCDSA.** National standards with closely related equations.

## When to use it

Do not use DSA for new signatures: FIPS 186-5 no longer approves it for signing. Implement DSA verification only to check existing signatures, for example in old OpenPGP keys or archived documents. For new systems use [Ed25519](/ed25519/) or ECDSA, or a post-quantum scheme such as ML-DSA (FIPS 204).

## Pitfalls

- **Nonce reuse, leakage or bias.** The main cause of real breaks of DSA and ECDSA. Use an approved random bit generator with the extra 64 binary digits of Appendix B.2, or RFC 6979.
- **Missing range checks.** A verifier must reject $r$ or $s$ outside $(0, q)$; accepting $r = 0$ or $s = 0$ can let trivial signatures through, as happened in Java's ECDSA in 2022 (see [signature forgery](/signature-forgery/)).
- **Unchecked domain parameters.** A $g$ that is not of order $q$, or a $p$ and $q$ chosen with a hidden structure, can weaken or break the scheme. Validate parameters with Appendix A.1.1.3 and A.2.2, or use known parameters.
- **Hash truncation.** Use the leftmost $N$ binary digits of a longer hash, not the rightmost, and do not reduce a longer hash modulo $q$ first; implementations that do otherwise fail the RFC 6979 vectors with SHA-384 and SHA-512.
- **Old parameter sizes.** $L = 1024$ and $N = 160$ with SHA-1 are below current security levels.

## Implementations

The Python code gives `generate_pq` and `validate_pq` (FIPS 186-4 Appendix A.1.1.2 and A.1.1.3), `generate_g` (A.2.1), `keygen` (B.1), `sign` (lines L1 to L6) and `verify` (lines L7 to L12). The tests use the key and the signatures of RFC 6979, Appendix A.2.2, copied by hand, with the printed $k$; they check rejections of changed messages, values, hashes and keys, randomized round trips, the truncation rule, and the generation and validation of a $(1024, 160)$ parameter set from a fixed seed. No official vector for the parameter generation is used, so that part is tested by round trip and validation only.

## History

NIST proposed DSA in August 1991, and FIPS 186 was published in May 1994 with $N = 160$, SHA-1 and $L$ from 512 to 1024. The algorithm is credited to David Kravitz of the NSA and was covered by US patent 5,231,668, which the government made available royalty-free. FIPS 186-1 (1998) and 186-2 (2000) added RSA and ECDSA; a change notice to 186-2 fixed $L = 1024$. FIPS 186-3 (2009) added the pairs $(2048, 224)$, $(2048, 256)$ and $(3072, 256)$ with SHA-2, and FIPS 186-4 (2013) kept them. FIPS 186-5 (February 2023) no longer approves DSA for signature generation and keeps it only to verify signatures made before.

## References
