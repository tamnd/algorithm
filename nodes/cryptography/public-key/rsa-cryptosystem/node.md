---
tag: D5K7RQ
kind: algorithm
slug: rsa-cryptosystem
name: RSA cryptosystem
aliases:
- RSA
area: cryptography/public-key
level: intro
summary: Public-key encryption from modular exponentiation with a hard to factor modulus. Textbook RSA is deterministic and malleable, so a real scheme needs OAEP padding.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1978
  people: [Ron Rivest, Adi Shamir, Leonard Adleman]
  note: Found at MIT in 1977 and published in Communications of the ACM in February 1978. Clifford Cocks had described the same function at GCHQ in 1973, in work that stayed secret until 1997.
prereqs: [public-key-encryption, modular-exponentiation, chinese-remainder-theorem]
see_also: [rsa-oaep, rsa-pkcs1-v1-5-encryption, rsa-problem, rsa-signature, rabin-cryptosystem, wiener-attack]
sources:
  - url: "https://doi.org/10.1145/359340.359342"
    title: Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978
    locator: Sections 1 to 3 (the scheme, the encryption and decryption steps, and the key generation)
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, 2016
    locator: Section 3 (key formats), Section 5.1.1 (RSAEP) and Section 5.1.2 (RSADP with the CRT quintuple)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.2, Algorithm 8.1 and Example 8.4 (the small worked example used on this page)
  - url: "https://doi.org/10.6028/NIST.SP.800-57pt1r5"
    title: Elaine Barker, NIST Special Publication 800-57 Part 1 Revision 5, Recommendation for Key Management, Part 1, General, 2020
    locator: Section 5.6.1, Table 2 (2048 bit RSA for 112 bit security, 3072 bit RSA for 128 bit security)
  - url: "https://www.ams.org/notices/199902/boneh.pdf"
    title: Dan Boneh, Twenty years of attacks on the RSA cryptosystem, Notices of the AMS 46(2), pages 203 to 213, 1999
    locator: Sections 2 and 4 (elementary attacks, low public exponent attacks and the broadcast attack)
---

RSA is the public-key encryption and signature scheme of Rivest, Shamir and Adleman. The public key is a modulus $N = pq$ of two large primes and an exponent $e$; the private key is $d$ with $ed \equiv 1 \pmod{\lambda(N)}$. Encryption raises the message to the power $e$ modulo $N$, and decryption raises the ciphertext to the power $d$. Textbook RSA, which is the bare primitive on this page, is deterministic and malleable, so a real scheme adds padding: [RSA-OAEP](/rsa-oaep/) for new applications, and [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) only for compatibility.

**Notation.** $p$ and $q$ are the primes, $N = pq$ the modulus, $b$ the number of binary digits of $N$, $\varphi(N) = (p-1)(q-1)$, $\lambda(N) = \mathrm{lcm}(p-1, q-1)$, $e$ the public exponent, $d$ the private exponent, $m$ a message representative with $0 \le m < N$ and $c$ a ciphertext representative. RFC 8017 writes $n$ for the modulus and $k$ for its length in octets.

## In plain words

Pick two big prime numbers and multiply them. The product is public, the two primes are secret. Anybody can scramble a number by raising it to a fixed public power and keeping the remainder after division by the product. Only the holder of the secret can unscramble it, because the secret power that undoes the public power comes from the two primes.

To unscramble a number, you need the two primes, or at least the secret power. Finding the primes from their product is the hard part. For a product of 2048 binary digits, no known machine can do it.

The bare operation leaks information. The same message always gives the same scrambled value, and a product of two scrambled values is the scrambled value of the product. So every real use first mixes the message with random padding.

## The problem

RSA solves [public-key encryption](/public-key-encryption/). Its one-way function is the map $m \mapsto m^e \bmod N$, and the trapdoor is the factorization of $N$. Inverting the map without the trapdoor is the [RSA problem](/rsa-problem/).

## The algorithm

```pseudo id=main
RSA-KEYGEN(b, e)                         ▷ b binary digits of modulus, e the public exponent
L1  repeat
L2      p ← a random prime of ⌈b/2⌉ digits, q ← a random prime of ⌊b/2⌋ digits
L3  until p ≠ q, gcd(e, (p−1)(q−1)) = 1 and p·q has b binary digits
L4  N ← p·q,  λ ← lcm(p−1, q−1)
L5  d ← e^(−1) mod λ
L6  dP ← d mod (p−1),  dQ ← d mod (q−1),  qInv ← q^(−1) mod p
L7  return the public key (N, e) and the private key (p, q, dP, dQ, qInv)

RSA-ENCRYPT((N, e), m)                   ▷ 0 ≤ m < N
L8  return m^e mod N

RSA-DECRYPT((p, q, dP, dQ, qInv), c)     ▷ 0 ≤ c < N
L9  m1 ← c^dP mod p
L10 m2 ← c^dQ mod q
L11 h ← (m1 − m2)·qInv mod p
L12 return m2 + q·h
```

Line L2 draws each prime with a random odd candidate and a [Miller-Rabin test](/miller-rabin/). Line L3 keeps only the pairs for which $e$ has an inverse, and for which the product has the wanted length. Line L5 uses the [extended Euclidean algorithm](/extended-euclidean-algorithm/). RFC 8017 Section 3.2 defines $d$ modulo $\lambda(N)$, which is the [Carmichael function](/carmichael-function/) of $N$; the original paper of 1978 uses $\varphi(N)$. Both work, and the value modulo $\lambda(N)$ is never longer, so it is never slower.

**About the code.** The Python code of this page is for study only. It is not constant time, it has no blinding, and it must not be used to protect real data. Use a FIPS 140 validated module, or the RSA code of your platform's standard library. The attack helpers run only on toy keys that the test file makes.

Lines L8 to L12 are RSAEP and RSADP of RFC 8017 Section 5.1. Lines L9 to L12 are the [Chinese remainder theorem](/chinese-remainder-theorem/) in Garner form: two exponentiations modulo a prime of $b/2$ digits, then one multiplication and one addition. The private values $dP$, $dQ$ and $qInv$ hold no more information than $p$ and $q$ do.

## Example

The small example is Example 8.4 of the Handbook of Applied Cryptography: $p = 2357$, $q = 2551$, so $N = 6012707$ and $\varphi(N) = 6007800$. With $e = 3674911$ the inverse is $d = 422191$. The message $m = 5234673$ encrypts to

$$c = 5234673^{3674911} \bmod 6012707 = 3650502 .$$

Decryption with the single exponent gives $3650502^{422191} \bmod 6012707 = 5234673$. The CRT form uses $\lambda(N) = 3003900$, which gives the same $d = 422191$ here, and then

| value | formula | result |
|---|---|---|
| $dP$ | $d \bmod (p-1)$ | 467 |
| $dQ$ | $d \bmod (q-1)$ | 1441 |
| $qInv$ | $q^{-1} \bmod p$ | 1300 |
| $m_1$ | $c^{dP} \bmod p$ | 2133 |
| $m_2$ | $c^{dQ} \bmod q$ | 21 |
| $h$ | $(m_1 - m_2) qInv \bmod p$ | 2052 |
| $m$ | $m_2 + qh$ | 5234673 |

A message that is not coprime to $N$ decrypts as well. With the same key, $m = p = 2357$ gives $c = 1129003$, and decryption returns 2357.

## Correctness

Write $ed = 1 + k\lambda(N)$. For each prime factor $r$ of $N$, the exponent $r - 1$ divides $\lambda(N)$, so $m^{ed} \equiv m \pmod r$: this is clear when $r \mid m$, because both sides are 0, and it follows from Fermat's little theorem when $r \nmid m$. The two congruences give $m^{ed} \equiv m \pmod N$ for every integer $m$, with no condition on $\gcd(m, N)$. The CRT form returns the same value, because $dP \equiv d \pmod{p-1}$ and both exponents are at least 1. The full proof, with the bounds $0 \le m < N$ for the CRT output, is below.

## Complexity

Let $b$ be the number of binary digits of $N$, with schoolbook arithmetic, so one modular multiplication costs $\Theta(b^2)$.

- **Encryption**: $\lfloor \log_2 e \rfloor$ squarings and one multiplication for each 1 digit of $e$, by [modular exponentiation](/modular-exponentiation/). With $e = 65537 = 2^{16}+1$ this is 16 squarings and 1 multiplication, so $\Theta(b^2)$ in total.
- **Decryption with one exponent**: $\Theta(b)$ modular multiplications, so $\Theta(b^3)$.
- **Decryption with the CRT**: two exponentiations with exponents and moduli of $b/2$ digits. Each costs $\Theta((b/2)^3)$, so the total is $\Theta(b^3)/4$: a speed up near 4 in practice.
- **Key generation**: the search for one prime of $b/2$ digits tests $O(b)$ candidates on average, each with a Miller-Rabin test of $\Theta(b^3)$, so $\Theta(b^4)$ on average.
- **Space**: $\Theta(b)$ for the key and the intermediate values.

This is why RSA is thousands of times slower than a block cipher, and why protocols use [hybrid encryption](/hybrid-encryption/): RSA transports a symmetric key, and the symmetric cipher carries the data.

## Properties

- **Deterministic.** Textbook RSA sends equal messages to equal ciphertexts, so it is not [IND-CPA](/ind-cpa-security/) secure: an adversary that sees the two candidate messages can encrypt both and compare. Padding adds the randomness.
- **Multiplicative.** $(m_1 m_2)^e \equiv m_1^e \cdot m_2^e \pmod N$. So textbook RSA is malleable and is not [non-malleable](/non-malleability/) in any sense. The same property gives [RSA blinding](/rsa-blinding/) and the chosen-ciphertext attack of the [padding oracle](/padding-oracle-attack/) pages.
- **A permutation.** For $\gcd(e, \lambda(N)) = 1$ the map is a bijection of $\{0, 1, \ldots, N-1\}$, which makes RSA a [trapdoor one-way permutation](/trapdoor-one-way-function/) candidate.
- **Key sizes.** SP 800-57 Part 1 Rev. 5, Table 2, gives 2048 binary digits for 112 bit security and 3072 for 128 bit security. RSA-250, a modulus of 250 decimal digits (829 binary digits), was factored in February 2020 with about 2700 core years of computation.

## Variants and improvements

- **Padding.** [RSA-OAEP](/rsa-oaep/) (RFC 8017 Section 7.1) is required for new applications. [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) is kept only for old systems.
- **Signatures.** The same key signs with [RSA-PSS](/rsa-pss/) or, in old systems, with [PKCS #1 v1.5 signatures](/rsa-signature/). Never share a key between encryption and signature.
- **Faster arithmetic.** [Montgomery multiplication](/montgomery-multiplication/) or Barrett reduction removes the division from each modular step. [Sliding window exponentiation](/sliding-window-exponentiation/) cuts the number of multiplications.
- **More primes.** Multi-prime RSA ($N = pqr$) makes CRT decryption faster, and RFC 8017 Section 3.2 allows it. The factors get smaller, so the margin against the elliptic curve method drops.
- **Small private exponent.** Never do this: $d < N^{1/4}/3$ falls to [Wiener's attack](/wiener-attack/), and $d < N^{0.292}$ falls to Boneh and Durfee.
- **Rebalanced RSA.** Choose $dP$ and $dQ$ small and let $e$ be large, to make decryption fast. The security margin is thinner than for the standard choice.

## When to use it

Use RSA with OAEP when you must interoperate with an old system or a standard that names it, for example a TLS certificate chain or a key transport format. For new designs prefer [ECIES](/ecies/) or a post-quantum [KEM](/key-encapsulation-mechanism/) such as ML-KEM: the keys and the signatures are much shorter at the same security level, and key generation is fast. RSA stays attractive when verification must be cheap and the public exponent can be small, as in a certificate that many parties check. [Shor's algorithm](/shor-algorithm/) breaks RSA on a large quantum computer, so data that must stay secret for decades needs a post-quantum scheme now.

## Pitfalls

- **No padding.** Encrypting a raw message with line L8 is not secure. A short message with $e = 3$ and $m^3 < N$ gives $m$ by an exact cube root. The test file shows this on a toy key.
- **The same message to many keys.** The same unpadded $m$ sent to $e$ keys with the same small $e$ falls to Håstad's broadcast attack (1988): the CRT of the ciphertexts is $m^e$ modulo the product, which is above $m^e$, so an exact $e$-th root gives $m$. The [Coppersmith method](/coppersmith-method/) extends this to padded messages with a known part and to related messages.
- **A shared modulus.** Two users with the same $N$ and different exponents can each read the other's traffic, and $\gcd$ of the exponents breaks the common modulus setup.
- **A small private exponent.** See the variants above. Pick $e$ first, never $d$.
- **No CRT check.** A fault during line L9 or L10 leaks $p$ by one $\gcd$, which is the [RSA fault attack](/rsa-fault-attack/). Verify the result before you output it.
- **Secret dependent timing.** Line L9 and line L10 with a square and multiply loop leak $d$ through the running time. Use blinding and a constant time ladder, as the [timing attack](/timing-attack/) page shows.
- **Weak primes from a weak generator.** If the random source repeats, two moduli share a factor, and a batch $\gcd$ over a collection of public keys finds it. Use the system random source.

## Implementations

## History

Diffie and Hellman asked for a public-key cipher in 1976. Rivest, Shamir and Adleman found this one at MIT in 1977 and published it in Communications of the ACM in February 1978. The patent (US 4,405,829, filed 1977, granted 1983) expired in September 2000. Clifford Cocks described the same function at GCHQ in a 1973 note, which became public in December 1997; see [public-key cryptography](/public-key-cryptography/) for that history. The first standard, PKCS #1 v1.5, is from 1993; RFC 8017 (2016) is the current version, with OAEP since v2.0 (1998).

## References
