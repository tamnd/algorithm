---
tag: SMWJN1
kind: algorithm
slug: rabin-signature
name: Rabin signature
aliases:
- Rabin-Williams signature
- Rabin-Williams
- modified-Rabin signature
- RW signature
area: cryptography/signatures
level: advanced
summary: A signature is a square root modulo N = pq of the hash of the message. Verifying costs one squaring, and forging in the random oracle model is as hard as factoring N.
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1979
  people: [Michael O. Rabin, Hugh C. Williams, Daniel J. Bernstein]
  note: Rabin (1979) signed with square roots and proved that taking them is as hard as factoring. Williams (1980) added the tweaks for primes 3 and 7 modulo 8. Bernstein (2008) proved tight security.
prereqs: [rabin-cryptosystem, signature-scheme, modular-square-root]
see_also: [rsa-signature, rsa-fdh, chinese-remainder-theorem, random-oracle-model, signature-malleability, chosen-message-attack, rsa-fault-attack, integer-factorization]
sources:
  - paper: "Michael O. Rabin, Digitalized signatures and public-key functions as intractable as factorization, MIT Laboratory for Computer Science, Technical Report MIT/LCS/TR-212, January 1979"
    locator: the signature as a square root of a hash of the message and a random string, and the proof that extracting square roots modulo N is as hard as factoring N
  - paper: "Hugh C. Williams, A modification of the RSA public-key encryption procedure, IEEE Transactions on Information Theory 26(6), pages 726 to 729, 1980"
    locator: moduli N = pq with p = 3 and q = 7 modulo 8, where multiplication by -1 and 2 makes every value invertible by the square-root map
  - paper: "Daniel J. Bernstein, Proving tight security for Rabin-Williams signatures, EUROCRYPT 2008, LNCS 4965, pages 70 to 87"
    locator: the tweaks e and f, the choices of square root (principal, unstructured, fixed unstructured), and tight security proofs relative to factoring in the random oracle model
  - paper: "Mihir Bellare and Phillip Rogaway, The exact security of digital signatures, how to sign with RSA and Rabin, EUROCRYPT 1996, LNCS 1070, pages 399 to 416"
    locator: the hashed Rabin signature and its security relative to factoring in the random oracle model
  - paper: "IEEE Std 1363-2000, IEEE Standard Specifications for Public-Key Cryptography"
    locator: the RW signature and verification primitives for integer factorization keys (IFSP-RW and IFVP-RW)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.3.4, the Rabin signature scheme, Note 11.27 (redundancy and existential forgery), and the modified-Rabin scheme with p = 3 and q = 7 modulo 8 (Algorithms 11.29 and 11.30)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, signatures from trapdoor permutations and the Rabin trapdoor
---

A Rabin signature on a message is a square root modulo a composite $N = pq$ of a hash of the message. Only the owner of the factors can take square roots, and Rabin (1979) proved that an algorithm that takes them for random values factors $N$. Verification is one squaring modulo $N$, faster than RSA verification even with $e = 3$. The Rabin-Williams form on this page uses primes $p \equiv 3$ and $q \equiv 7 \pmod 8$ and two small tweaks $e$ and $f$, so that every hash value can be signed at the first attempt.

**Notation.** $N = pq$ with primes $p \equiv 3 \pmod 8$ and $q \equiv 7 \pmod 8$, and $b$ is the number of binary digits of $N$. $H$ maps messages to $\mathbb{Z}_N$, and $h = H(M)$. A signature is $(e, f, s)$ with $e \in \{1, -1\}$, $f \in \{1, 2\}$ and $0 \le s < N$. $\left(\frac{a}{r}\right)$ is the Legendre symbol of $a$ modulo a prime $r$, computed by Euler's criterion $a^{(r-1)/2} \bmod r$.

## In plain words

The public key is a large number that is the product of two secret primes. To sign, the signer hashes the message to a number and finds a number whose square is the hash, working with remainders modulo the public number. Anyone can check a signature by squaring it, which is very fast. Finding such a root without the two primes is as hard as splitting the public number into its primes.

Only a quarter of the numbers have such a root. The Williams form fixes this by multiplying the hash by one of four small factors so that a root always exists, and it sends that factor along with the signature.

Each value has four roots. The signer must always give the same root for the same hash, because two different roots of one value reveal the primes.

## The problem

Sign messages so that a forger must factor $N$: not only in a heuristic sense, as for RSA, where inverting the RSA function is not known to be as hard as factoring, but with a proof in the [random oracle model](/random-oracle-model/). Verification should be as cheap as possible.

## The algorithm

**Key generation.** Pick random primes $p \equiv 3 \pmod 8$ and $q \equiv 7 \pmod 8$ of about $b/2$ binary digits each, and set $N = pq$. The public key is $N$; the private key is $(p, q)$ and a secret value that selects among the square roots. By Lemma 1 of the proof, $-1$ is a non-square modulo both primes, and $2$ is a non-square modulo $p$ but a square modulo $q$, so the four products $e f$ cover all four combinations of squares and non-squares.

```pseudo id=main
SIGN((p, q, secret), M)
L1  h ← H(M) in Z_N
L2  e ← (h / q);  f ← 1 if (h / p)·e = 1, else 2
L3  h' ← h · (e·f)^(−1) mod N
L4  s_p ← h'^((p+1)/4) mod p;  s_q ← h'^((q+1)/4) mod q
L5  replace s_p by p − s_p and s_q by q − s_q, each by a secret bit that is a fixed function of h
L6  s ← the CRT combination of s_p mod p and s_q mod q
L7  return (e, f, s)

VERIFY(N, M, (e, f, s))
L8  if e ∉ {1, −1} or f ∉ {1, 2} or not 0 ≤ s < N then return invalid
L9  h ← H(M) in Z_N
L10 return valid if e·f·s^2 ≡ h (mod N), else invalid
```

Line L2 is the content of the tweaks: $e$ makes $h'$ a square modulo $q$, and then $f$ fixes the symbol modulo $p$ without changing it modulo $q$. Line L4 takes square roots with one exponentiation each, which works because $p \equiv q \equiv 3 \pmod 4$ (see [modular square root](/modular-square-root/)). Line L6 uses the [Chinese remainder theorem](/chinese-remainder-theorem/).

**About the code.** The Python code is for study only. It is not constant time, its keys come from a seeded non-cryptographic random source, and it must not protect real data; use RSA-PSS or Ed25519 from the pyca/cryptography library or from a FIPS 140 validated module. The hash is SHA-256 in counter mode cut to $b - 1$ binary digits, a full-domain hash in the style of [RSA-FDH](/rsa-fdh/), and the secret root choice of line L5 is two bits of HMAC-SHA-256 of $h$ under a secret key.

## Example

Toy key: $p = 11$ ($\equiv 3 \pmod 8$), $q = 7$ ($\equiv 7 \pmod 8$), $N = 77$. Take $h = 10$ in place of a hash value.

| line | computation | value |
|---|---|---|
| L2 | $10 \bmod 7 = 3$, a non-square modulo 7 (the squares are 1, 2, 4) | $e = -1$ |
| L2 | $10$ is a non-square modulo 11 (the squares are 1, 3, 4, 5, 9), so $\left(\frac{10}{11}\right) e = (-1)(-1) = 1$ | $f = 1$ |
| L3 | $h' = 10 \cdot (-1)^{-1} \bmod 77$ | 67 |
| L4 | $67 \bmod 11 = 1$, $s_p = 1^{3} \bmod 11$ | 1 |
| L4 | $67 \bmod 7 = 4$, $s_q = 4^{2} \bmod 7$ | 2 |
| L6 | $s \equiv 1 \pmod{11}$, $s \equiv 2 \pmod 7$ | 23 |
| L10 | $e f s^2 = -529 \bmod 77$ | 10 |

The four square roots of 67 modulo 77 are 12, 23, 54 and 65, the CRT combinations of $\pm 1 \bmod 11$ and $\pm 2 \bmod 7$. Line L5 picks one of them. If a signer ever gave both 23 and 12 for the same $h$, anyone could compute $\gcd(23 - 12, 77) = 11$ and factor $N$. The pair 23 and $54 = 77 - 23$ reveals nothing.

**No official vector.** This page found no published test vector for Rabin-Williams signatures that it could copy, so the tests check this example, check the tweak lemma for every $h$ coprime to three small moduli, and run round trips on a key of 512 binary digits from a fixed seed.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 computes the Legendre symbols of $-1$ and $2$. Lemma 2 shows that exactly one pair $(e, f)$ makes $h'$ a square modulo both primes. Lemma 3 shows that line L4 gives square roots. By the Chinese remainder theorem $s^2 \equiv h'$, so $e f s^2 \equiv h \pmod N$. The proof also shows why two roots that are not negatives of each other give a factor of $N$.

**Security.** Rabin (1979) proved that an algorithm that takes square roots of a noticeable fraction of the squares modulo $N$ can be used to factor $N$: pick $x$ at random, ask for a root of $x^2$, and with probability $1/2$ the answer is not $\pm x$. With a hash modelled as a random oracle, Bellare and Rogaway (1996) related forging hashed Rabin signatures to factoring, and Bernstein (2008) gave tight proofs relative to factoring for Rabin-Williams variants, including one with no random prefix in which the root of each hash value is fixed by a secret function, as in line L5.

## Complexity

| operation | cost with schoolbook arithmetic |
|---|---|
| sign | 2 Legendre symbols and 2 square roots, each one exponentiation modulo a prime of $b/2$ binary digits, then 1 CRT step: $\Theta(b^3)$ |
| verify | 1 squaring, 1 multiplication by $e f$ and 1 reduction modulo $N$: $\Theta(b^2)$ |
| signature size | $b$ binary digits for $s$, plus 2 binary digits for $e$ and $f$ |
| space | $\Theta(b)$ |

The Legendre symbols can also be computed with the Jacobi symbol algorithm in $O(b^2)$. RSA verification with $e = 3$ needs two multiplications and two reductions, so Rabin-Williams verification costs about half; with $e = 65537$ RSA needs 17.

## Properties

- **Deterministic.** The root choice is a fixed function of $h$, so a message always gets the same signature. This is required: a signer that picks the root at random and signs the same hash twice gives two roots that factor $N$ with probability $1/2$.
- **Not strongly unforgeable as written.** $(e, f, N - s)$ also verifies, so anyone can make a second signature on a signed message. A verifier that accepts only one root of each pair, for example $s < N/2$, removes this; see [signature malleability](/signature-malleability/).
- **Security tied to factoring.** Unlike RSA, whose security is tied to the RSA problem, a forger against hashed Rabin-Williams in the random oracle model gives a factoring algorithm.
- **Fast verification.** One squaring modulo $N$.

## Variants and improvements

- **Rabin's original scheme (1979).** Append a random string $U$ to $M$ and retry until $H(M \Vert U)$ is a square modulo $N$, which takes four tries on average; the signature is $(U, s)$. With $p \equiv q \equiv 3 \pmod 4$ only, the tweak $e = \pm 1$ alone is not enough, which is why Williams moved to $p \equiv 3$ and $q \equiv 7 \pmod 8$.
- **Modified-Rabin (HAC Section 11.3.4).** The Williams form with redundancy in place of a hash; it is a message-recovery scheme.
- **Choice of root.** Bernstein compares the principal root (the one that is itself a square), a random root, and a fixed root selected by a secret function. A random root is the dangerous choice: two signatures on one hash value can factor $N$.
- **Compressed signatures.** Because the verifier needs only $s^2 \bmod N$, a Rabin signature can be replaced by shorter data from which a valid root follows. Bleichenbacher (CT-RSA 2004) showed such a compression to about half the length of $N$.
- **[RSA signatures](/rsa-signature/).** The same hash-and-sign shape with an odd exponent $e$, where the map $x \mapsto x^e$ is a permutation.

## When to use it

Rabin-Williams signatures fit settings where verification must be very cheap and a factoring-based assumption is wanted, such as many verifiers on small devices. They are not in FIPS 186 and are rarely in common libraries, so most systems use [RSA-PSS](/rsa-pss/), ECDSA or Ed25519. Use a hash with the full width of $N$, a fixed root choice, and a verifier that rejects out-of-range values.

## Pitfalls

- **Signing raw values.** A signer that returns a square root of any value an attacker sends gives the attacker the factors after about two queries: send $x^2$ and wait for a root that is not $\pm x$. The tests run this attack on the toy key. Always sign a hash of the message.
- **Random root choice.** Signing the same hash value twice with roots from different pairs factors $N$, as in the example: $\gcd(23 - 12, 77) = 11$.
- **No hash, key-only forgery.** Without a hash, anyone can pick $s$ and output $(s^2 \bmod N, s)$, a valid signature on a message that the forger does not control; see [key-only attack](/key-only-attack/).
- **Faults in the CRT step.** As for RSA with the CRT, one wrong value of $s_p$ or $s_q$ gives a signature $s$ with $\gcd(s^2 - h', N)$ equal to a prime factor; see [RSA fault attack](/rsa-fault-attack/). Verify each signature before it is released.
- **Wrong primes.** With $p \equiv q \pmod 8$ the tweaks do not cover all four cases, and some hash values cannot be signed.
- **Missing range checks.** The verifier must check $e$, $f$ and $0 \le s < N$; otherwise $s + N$ is a second signature.

## Implementations

The Python code gives `keygen` (toy keys from a seed), `hash_to_int`, `tweaks` (line L2), `sign_hash` and `sign` (lines L1 to L7), `verify_hash` and `verify` (lines L8 to L10), and `factor_from_two_roots`. The tests check the toy example, the tweak lemma for every $h$ coprime to $77$, $437$ and $1333$, determinism, rejections of changed messages, tweaks and roots, the second signature $N - s$, factoring from two roots of one hash value, and the factoring of $N$ through a signer that signs raw values. No official vector is used.

## History

Rabin's technical report of January 1979 proposed signatures and encryption based on squaring modulo $N = pq$ and proved that inverting squaring is as hard as factoring, the first public-key scheme with such a proof. Williams (1980) chose $p \equiv 3$ and $q \equiv 7 \pmod 8$ so that one of $\pm h$ and $\pm 2h$ always has a square root. Bellare and Rogaway (1996) gave exact security bounds for hashed Rabin signatures in the random oracle model. IEEE 1363-2000 standardized the RW signature primitive. Bernstein (EUROCRYPT 2008) named the tweaks $e$ and $f$, compared the choices of root, and proved tight security relative to factoring.

## References
