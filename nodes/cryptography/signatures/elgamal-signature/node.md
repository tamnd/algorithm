---
tag: D1G2DP
kind: algorithm
slug: elgamal-signature
name: ElGamal signature
aliases:
- ElGamal digital signature
- ElGamal signature scheme
area: cryptography/signatures
level: advanced
summary: "The first discrete-logarithm signature (ElGamal 1985): r = g^k mod p and s = k^-1 (h - x r) mod (p - 1). DSA and Schnorr replaced it; it has no standard and no proof as given."
model: word-ram
complexity:
  vars: {b: the number of binary digits of the prime p}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1985
  people: [Taher ElGamal]
  note: Published with ElGamal encryption at CRYPTO 1984 and in IEEE Transactions on Information Theory in 1985. Schnorr (1989) and DSA (1991) moved it to a prime-order subgroup.
prereqs: [discrete-logarithm-problem, signature-scheme, modular-inverse]
see_also: [dsa, schnorr-signature, elgamal-encryption, key-only-attack, nonce-reuse-attack, deterministic-nonce-generation, forking-lemma, ecdsa]
sources:
  - paper: "Taher ElGamal, A public key cryptosystem and a signature scheme based on discrete logarithms, IEEE Transactions on Information Theory 31(4), pages 469 to 472, 1985"
    locator: the signature scheme with the verification equation g^m = y^r r^s mod p
  - paper: "Daniel Bleichenbacher, Generating ElGamal signatures without knowing the secret key, EUROCRYPT 1996, LNCS 1070"
    locator: forgeries for weak generators, for example g = 2 with p = 1 mod 4, and the need for a prime-order subgroup
  - paper: "David Pointcheval and Jacques Stern, Security proofs for signature schemes, EUROCRYPT 1996, LNCS 1070"
    locator: the forking lemma and a proof in the random oracle model for a modified ElGamal scheme that hashes the message together with r
  - paper: "Claus-Peter Schnorr, Efficient signature generation by smart cards, Journal of Cryptology 4(3), pages 161 to 174, 1991"
    locator: signatures in a subgroup of prime order q, with short exponents and short signatures
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.5.2, Algorithms 11.63 and 11.64, Example 11.65 (p = 2357), Note 11.66 (security, k reuse, unhashed forgery, range check of r), Note 11.67 (weak generators)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, signatures from the discrete logarithm problem, Schnorr and DSA
---

The ElGamal signature scheme signs with a fresh secret exponent $k$: it publishes $r = g^k \bmod p$ and $s = k^{-1}(h - x r) \bmod (p - 1)$, where $h$ is the hash of the message and $x$ the private key, and anyone can check $g^h \equiv y^r r^s \pmod p$. Taher ElGamal published it in 1985 as the first signature scheme based on the [discrete logarithm problem](/discrete-logarithm-problem/). It is the ancestor of [Schnorr signatures](/schnorr-signature/), [DSA](/dsa/) and [ECDSA](/ecdsa/), which replaced it, because it works in the full group modulo $p$, has long signatures, has known weak cases and has no proof of security in its original form.

**Notation.** $p$ is a prime, $g$ a generator of $\mathbb{Z}_p^*$, and $b$ the length of $p$ in binary digits. The private key is $x$ with $1 \le x \le p - 2$, and the public key is $y = g^x \bmod p$. $h = H(m) \bmod (p - 1)$ is the hash of the message $m$. The nonce $k$ is a secret exponent with $\gcd(k, p - 1) = 1$, new for each signature. The signature is $(r, s)$.

## In plain words

The signer has a secret number $x$ and publishes $g$ raised to the power $x$. To sign, the signer picks a new secret random number, publishes $g$ to that power as the first half of the signature, and solves a simple equation that mixes the message hash, the secret key and the random number to get the second half.

The checker cannot see the secrets, but it can check the same equation "in the exponent", using only public numbers. Solving that equation without the secret key would mean solving a discrete logarithm.

The random number must be new and secret every time. If the signer uses it twice, two signatures give two equations with two unknowns, and anyone can solve them for the secret key.

## The problem

Build a [signature scheme](/signature-scheme/) whose private key is a discrete logarithm $x$ of a public value $y = g^x \bmod p$, such that a signature can be checked with $y$ alone and making one without $x$ seems as hard as computing discrete logarithms modulo $p$. ElGamal (1985) gave no reduction; the scheme was designed against the known attacks of the time.

## The algorithm

```pseudo id=main
KEYGEN(p, g)
L1  x ← uniform in {1, ..., p − 2}
L2  y ← g^x mod p;  return (sk = x, pk = y)

SIGN(x, m)
L3  h ← H(m) mod (p − 1)
L4  k ← uniform in {1, ..., p − 2}, again until gcd(k, p − 1) = 1
L5  r ← g^k mod p
L6  s ← k^(−1) · (h − x·r) mod (p − 1)
L7  if s = 0 then go to L4
L8  return (r, s)

VERIFY(y, m, (r, s))
L9  if not (1 ≤ r ≤ p − 1 and 1 ≤ s ≤ p − 2) then return invalid
L10 h ← H(m) mod (p − 1)
L11 return valid if g^h ≡ y^r · r^s (mod p), else invalid
```

Line L4 needs $\gcd(k, p - 1) = 1$ so that the [modular inverse](/modular-inverse/) of line L6 exists. Line L7 rejects $s = 0$, which would let a reader solve $h \equiv x r \pmod{p-1}$ for $x$. The range check of line L9 on $r$ is required: HAC Note 11.66(iv) shows that without it, one valid signature lets an attacker sign messages of its choice. The original paper signs the message $m$ itself as an integer; without a hash, the scheme has an existential forgery under a [key-only attack](/key-only-attack/) (HAC Note 11.66(iii)), so this page and the code use a hash.

**About the code.** The Python code is for study only. It is not constant time, its toy group comes from a seeded non-cryptographic random source, and it must not protect real data. ElGamal signatures have no standard and no validated implementation; use Ed25519 or ECDSA from the pyca/cryptography library or from a FIPS 140 validated module. The code takes SHA-256 from `hashlib` and reduces it modulo $p - 1$.

## Example

The worked example of HAC (Example 11.65) uses $p = 2357$, $g = 2$, $x = 1751$ and $y = 2^{1751} \bmod 2357 = 1185$, and signs the integer $h = 1463$ directly, with the hash replaced by the identity for the example only.

| step | computation | value |
|---|---|---|
| L4 | $k$ | 1529 |
| L5 | $r = 2^{1529} \bmod 2357$ | 1490 |
| L6 | $k^{-1} \bmod 2356$ | 245 |
| L6 | $s = 245 \cdot (1463 - 1751 \cdot 1490) \bmod 2356$ | 1777 |
| L11 | $y^r r^s = 1185^{1490} \cdot 1490^{1777} \bmod 2357$ | 1072 |
| L11 | $g^h = 2^{1463} \bmod 2357$ | 1072 |

**Nonce reuse.** Sign $h_2 = 1000$ with the same $k = 1529$. The result is $(1490, 1430)$, with the same $r$. Subtracting the two signing equations gives $(1777 - 1430)\,k = 347\,k \equiv 1463 - 1000 = 463 \pmod{2356}$. Since $\gcd(347, 2356) = 1$, this has one solution, $k = 1529$. Then $1490\,x \equiv 1463 - 1529 \cdot 1777 \pmod{2356}$ has two solutions, 573 and 1751, because $\gcd(1490, 2356) = 2$, and only $2^{1751} \bmod 2357$ equals $y$. So $x = 1751$. The proof is Theorem 2 of [proofs/correctness.md](proofs/correctness.md), and the tests run the same recovery on a toy group of 128 binary digits.

**A weak generator.** The parameters of this example are exactly the weak case found by Bleichenbacher (1996), given as HAC Note 11.67(iii): $p \equiv 1 \pmod 4$ and $g = 2$ divides $p - 1$. With $q = (p - 1)/2 = 1178$ and $t = (p - 3)/2 = 1177$, the attacker sets $r = q$ and finds $z$ with $g^{qz} \equiv y^q$; here $g^q \equiv y^q \equiv -1$, so $z = 1$. For $h = 1463$ it sets $s = t\,(h - qz) \bmod 2356 = 893$. Then $1178^{893} \cdot 1185^{1178} \equiv 1072 \equiv 2^{1463} \pmod{2357}$, so $(1178, 893)$ is a valid signature made without $x$. It passes the range check of line L9. The defence is to work in a subgroup of prime order, as DSA and Schnorr do.

## Correctness

The proof that each signature verifies, and the proof that a repeated $k$ gives the key, are in [proofs/correctness.md](proofs/correctness.md). The key step is that line L6 gives $h \equiv x r + k s \pmod{p - 1}$, and exponents of $g$ can be taken modulo $p - 1$ by [Fermat's little theorem](/fermat-little-theorem/).

**Security.** There is no proof that the scheme as given in 1985 is [EUF-CMA](/existential-unforgeability/). The known facts:

- A forger who picks $r$ must solve $y^r r^s \equiv g^h$ for $s$, a discrete logarithm problem in $r$; a forger who picks $s$ faces an equation of unknown hardness in $r$ (HAC Note 11.66(i)).
- Without a hash, anyone can forge existentially from the public key (HAC Note 11.66(iii)).
- With weak generators, anyone can forge selectively (Bleichenbacher 1996).
- Pointcheval and Stern (1996) proved a modified scheme, which hashes $m$ together with $r$, EUF-CMA in the [random oracle model](/random-oracle-model/) under the discrete logarithm assumption, using the [forking lemma](/forking-lemma/).

## Complexity

With schoolbook arithmetic on numbers of $b$ binary digits:

| operation | cost |
|---|---|
| key generation | 1 exponentiation, $\Theta(b^3)$ |
| sign | 1 exponentiation with a full-size exponent, 1 inverse modulo $p - 1$ ($\Theta(b^2)$ with the extended Euclidean algorithm), 2 multiplications |
| verify | 3 exponentiations with full-size exponents ($g^h$, $y^r$, $r^s$) |
| signature size | $2b$ binary digits |

Line L4 accepts a random $k$ with probability $\varphi(p - 1)/(p - 1)$; for a safe prime $p = 2q + 1$ this is $(q - 1)/(2q)$, just under $1/2$, so the loop runs about twice on average. The exponents have $b$ binary digits; in Schnorr and DSA they have only as many as the subgroup order $q$, for example 256 instead of 3072.

## Properties

- **Randomized.** Each signature uses a new $k$, so two signatures on the same message differ.
- **No proof of unforgeability.** Neither [EUF-CMA](/existential-unforgeability/) nor [strong unforgeability](/strong-unforgeability/) is proved for the scheme as given.
- **Fragile nonce.** Reuse of $k$ reveals $x$, and so do partly known nonces, through lattice methods on DSA-style schemes; see [nonce reuse attack](/nonce-reuse-attack/).
- **No standard.** No NIST or IETF standard specifies ElGamal signatures; DSA, ECDSA and EdDSA are the standardized descendants.

## Variants and improvements

- **Schnorr signatures (1989, 1991).** Work in a subgroup of prime order $q$, hash the commitment together with the message, and have a proof in the random oracle model through the forking lemma.
- **DSA (1991, FIPS 186 of 1994).** Keeps the ElGamal signing equation but works modulo a prime $q$ that divides $p - 1$, and reduces $r$ modulo $q$, so a signature has $2 \cdot 160$ binary digits instead of $2 \cdot 1024$ in the first version.
- **Generalized ElGamal.** HAC Section 11.5.2 lists other signing equations that rearrange the roles of $h$, $r$ and $s$, with the same security comments as Note 11.66.
- **Nyberg and Rueppel.** A variant with message recovery.
- **ECDSA and EdDSA.** The same ideas in elliptic-curve groups, with much shorter keys.

## When to use it

Do not use ElGamal signatures in new systems. They are larger and slower than Schnorr, DSA and ECDSA in the same group, have weak parameter cases, have no standard and have no proof in their original form. Study them as the common ancestor of the discrete-logarithm signatures, and use [Ed25519](/ed25519/) or [ECDSA](/ecdsa/) in practice.

## Pitfalls

- **Reused or predictable $k$.** Two signatures with the same $k$ reveal $x$, as in the example. Draw $k$ from a [cryptographically secure generator](/cryptographically-secure-prng/) or derive it as in [deterministic nonce generation](/deterministic-nonce-generation/).
- **No hash.** Signing $m$ directly allows existential forgery from the public key alone.
- **No range check on $r$.** Omitting $1 \le r \le p - 1$ lets an attacker turn one signature into signatures on chosen messages (HAC Note 11.66(iv)).
- **Weak generator.** $g = 2$ with $p \equiv 1 \pmod 4$, or any $g$ that divides $p - 1$ with an easy subgroup, allows Bleichenbacher's forgery. Use a prime-order subgroup.
- **Small factors of $p - 1$.** If $p - 1$ has only small prime factors, the Pohlig-Hellman method computes $x$ (HAC Note 11.67(ii)).

## Implementations

The Python code gives `keygen` (lines L1 and L2), `sign` (lines L3 to L8), `verify` (lines L9 to L11), wrappers that hash with SHA-256, `toy_group`, which makes a safe prime $p = 2q + 1$ of 128 binary digits from a fixed seed and a generator of $\mathbb{Z}_p^*$, and `recover_key_from_reused_k`, the attack of Theorem 2. There is no standard and therefore no official test vector. The tests use the published worked example of HAC Example 11.65, round trips and rejections on the toy group, and the key recovery from a reused $k$ on both groups.

## History

Taher ElGamal presented the encryption and signature schemes at CRYPTO 1984 and published them in IEEE Transactions on Information Theory in 1985. Schnorr (CRYPTO 1989, Journal of Cryptology 1991) moved the idea into a subgroup of prime order and made signatures short. NIST proposed DSA in 1991 as a variant of ElGamal in such a subgroup, and published it as FIPS 186 in 1994. In 1996, Bleichenbacher showed forgeries for weak generators, and Pointcheval and Stern gave the first proof for a modified ElGamal scheme in the random oracle model.

## References
