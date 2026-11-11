---
tag: 95YWP2
kind: algorithm
slug: shamir-secret-sharing
name: Shamir's secret sharing
aliases:
- Shamir threshold scheme
area: cryptography/protocols
level: core
summary: Hide a secret as the constant term of a random polynomial and give each party a point on it.
model: word-ram
complexity:
  vars: {n: the number of parties, t: the threshold; each field operation counts as one step}
  time: {worst: Θ(n t), average: Θ(n t), best: Θ(n t)}
  space: {extra: Θ(n + t)}
properties: {deterministic: false, randomized: true}
history:
  year: 1979
  people: [Adi Shamir]
  note: Shamir published the scheme in the Communications of the ACM in November 1979. Blakley published a geometric threshold scheme in the same year, independently.
prereqs: [secret-sharing, lagrange-interpolation, polynomial-interpolation]
see_also: [verifiable-secret-sharing, threshold-cryptography, threshold-signature, bgw-protocol, secure-multiparty-computation, reed-solomon-code, horner-rule, blom-scheme]
sources:
  - paper: doi:10.1145/359168.359176
    title: Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979, 612-613
    locator: the (k, n) threshold scheme with a random polynomial of degree k - 1, the secrecy argument, and the remarks on adding shares and changing the polynomial
  - paper: "G. R. Blakley, Safeguarding cryptographic keys, Proceedings of the AFIPS National Computer Conference, vol. 48, 1979, 313-317"
    title: G. R. Blakley, Safeguarding cryptographic keys
    locator: the independent geometric threshold scheme of the same year
  - paper: "Amir Herzberg, Stanislaw Jarecki, Hugo Krawczyk and Moti Yung, Proactive secret sharing or how to cope with perpetual leakage, CRYPTO 1995, LNCS 963, 339-352"
    title: Amir Herzberg, Stanislaw Jarecki, Hugo Krawczyk and Moti Yung, Proactive secret sharing or how to cope with perpetual leakage
    locator: the share renewal protocol that adds random sharings of zero, with verification
  - paper: "Robert J. McEliece and Dilip V. Sarwate, On sharing secrets and Reed-Solomon codes, Communications of the ACM 24(9), 1981, 583-584"
    title: Robert J. McEliece and Dilip V. Sarwate, On sharing secrets and Reed-Solomon codes
    locator: Shamir shares as a Reed-Solomon codeword, and the correction of wrong shares by decoding
  - url: https://csrc.nist.gov/pubs/fips/197/final
    title: NIST, FIPS 197, Advanced Encryption Standard (AES)
    locator: Section 4.2, multiplication in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1, with the examples {57}{83} = {c1} and {53}{ca} = {01}
  - paper: "Amos Beimel, Secret-sharing schemes, a survey, IWCC 2011, LNCS 6639, 11-46"
    title: Amos Beimel, Secret-sharing schemes, a survey
    locator: the presentation of Shamir's scheme as a linear scheme and its optimal share size
---

Shamir's secret sharing splits a secret $s$ among $n$ parties so that any $t$ of them can recover it and any $t - 1$ learn nothing at all. The dealer picks a random polynomial $f$ of degree $t - 1$ with $f(0) = s$ and gives party $i$ the value $f(i)$. Since $t$ points fix a polynomial of degree $t - 1$, any $t$ parties find $f$, and so $s$, by [Lagrange interpolation](/lagrange-interpolation/). Since $t - 1$ points fit a polynomial through any value at 0, they say nothing about $s$. Each share is one field element, as large as the secret, which is the smallest possible. The scheme is the basis of [threshold cryptography](/threshold-cryptography/), [verifiable secret sharing](/verifiable-secret-sharing/) and the [BGW protocol](/bgw-protocol/).

**Notation.** $\mathbb{F}$ is a finite field with more than $n$ elements: $\mathbb{F}_p$ for a prime $p > n$, or $\mathrm{GF}(2^8)$ for bytes. $s \in \mathbb{F}$ is the secret, $t$ the threshold ($1 \le t \le n$), and $f(X) = s + a_1 X + \cdots + a_{t-1} X^{t-1}$ the dealer's polynomial. Party $i$ has the point $x_i = i$ and the share $y_i = f(i)$. For a set of points $x_1, \ldots, x_t$, the Lagrange coefficients at 0 are $\lambda_j = \prod_{m \ne j} x_m / (x_m - x_j)$.

## In plain words

Two points fix a line, three points fix a parabola, and in general $t$ points fix a polynomial of degree $t - 1$. Put the secret where the curve crosses the vertical axis, pick the other coefficients at random, and give each party one point of the curve. Any $t$ parties draw the curve and read off the secret.

With one point fewer, every crossing is still possible: for each candidate secret there is exactly one curve through the $t - 1$ points and that crossing. So the points give no hint. Over the real numbers this would fail, because the size of the numbers leaks information, so all the arithmetic is done in a finite field, where every value is as likely as every other.

## The problem

This is the threshold case of [secret sharing](/secret-sharing/): the authorized sets are the sets of at least $t$ parties. The goals are correctness for every set of $t$ parties and perfect secrecy against every set of $t - 1$, with shares as small as the secret.

## The algorithm

```pseudo id=main
SHARE(s, t, n)
L1  choose a_1, ..., a_{t-1} uniformly in F;  f(X) = s + a_1 X + ... + a_{t-1} X^{t-1}
L2  for i = 1 to n:
L3      give party i the share (i, f(i))          // Horner's rule, t - 1 steps

RECONSTRUCT((x_1, y_1), ..., (x_t, y_t))          // distinct, nonzero x_j
L4  for j = 1 to t:  λ_j = Π_{m ≠ j} x_m / (x_m - x_j)
L5  return Σ_j λ_j y_j
```

The share point 0 is never used, because $f(0)$ is the secret. Over $\mathrm{GF}(2^8)$ a byte string is shared byte by byte, with a fresh polynomial for each byte and the same $x_i$ for all bytes; subtraction is XOR.

## Example

Take $p = 11$, $s = 7$, $t = 3$, $n = 5$ and the random coefficients $a_1 = 3$, $a_2 = 5$, so $f(X) = 7 + 3X + 5X^2$. The shares are
$$f(1) = 4, \quad f(2) = 0, \quad f(3) = 6, \quad f(4) = 0, \quad f(5) = 4.$$
Parties 1, 2 and 3 compute $\lambda_1 = \frac{2 \cdot 3}{(2-1)(3-1)} = 3$, $\lambda_2 = \frac{1 \cdot 3}{(1-2)(3-2)} = -3 \equiv 8$, $\lambda_3 = \frac{1 \cdot 2}{(1-3)(2-3)} = 1$, and
$$s = 3 \cdot 4 + 8 \cdot 0 + 1 \cdot 6 = 18 \equiv 7.$$
Parties 1 and 2 alone hold $(1, 4)$ and $(2, 0)$. For the candidate secret 0, the polynomial $8X + 7X^2$ passes through both points ($8 + 7 = 15 \equiv 4$ and $16 + 28 = 44 \equiv 0$), and every other candidate also has exactly one polynomial; each comes from exactly one choice of $(a_1, a_2)$, so all 11 secrets are equally likely.

If party 3 gives the wrong share 7 instead of 6, the result is $7 + \lambda_3 \cdot 1 = 8$, with no sign of an error.

Over $\mathrm{GF}(2^8)$ with the AES polynomial $\mathtt{0x11b}$, the byte $s = \mathtt{0x53}$ with $t = 2$ and $a_1 = \mathtt{0xca}$ gives the shares $f(1) = \mathtt{0x99}$, $f(2) = \mathtt{0xdc}$ and $f(3) = \mathtt{0x16}$.

## Correctness

A nonzero polynomial of degree less than $t$ has fewer than $t$ roots, so there is only one polynomial of degree less than $t$ through $t$ points with distinct $x_j$, and it is $\sum_j y_j \ell_j(X)$ with the Lagrange basis $\ell_j$. At $X = 0$, $\ell_j(0) = \lambda_j$, so line L5 returns $f(0) = s$. For secrecy, fix $t - 1$ distinct nonzero points. For each secret, the map from $(a_1, \ldots, a_{t-1})$ to the $t - 1$ shares is affine with a Vandermonde-type matrix that is invertible, so the shares are uniform in $\mathbb{F}^{t-1}$ for every secret. The full proofs are below.

## Complexity

- **Sharing**: $n$ evaluations of a polynomial of degree $t - 1$ by [Horner's rule](/horner-rule/), $\Theta(n t)$ field operations, plus $t - 1$ random field elements.
- **Reconstruction**: $\Theta(t^2)$ field operations for the $\lambda_j$, and $t$ inversions, or one inversion with batching. When the set of parties is fixed, the $\lambda_j$ can be computed once.
- **Size**: each share is one field element, the same size as the secret, which is optimal for a perfect scheme.
- **Large $n$**: with fast multipoint evaluation and interpolation both steps take $O(n \log^2 n)$ field operations.

## Properties

- **Perfect secrecy.** Any $t - 1$ shares are uniform and independent of the secret. The scheme needs no computational assumption.
- **Ideal.** Shares are as large as the secret, which meets the lower bound of Karnin, Greene and Hellman.
- **Linear.** If parties hold shares of $s$ and of $s'$ on the same points, the sums of their shares are shares of $s + s'$, and $c$ times a share is a share of $c s$. This is what makes Shamir shares useful in [secure multiparty computation](/secure-multiparty-computation/) and threshold signatures. Products of shares are shares of $s s'$ on a polynomial of degree $2(t - 1)$, which needs a degree reduction step.
- **Extensible.** The dealer can add new parties later by giving out more points of the same $f$, without changing old shares.
- **Not robust.** Nothing in a share shows that it is correct. A wrong share gives a wrong secret silently. With more than $t$ shares one can detect errors, and with enough extra shares correct them by Reed-Solomon decoding.

## Variants and improvements

- **Verifiable secret sharing.** Feldman and Pedersen publish commitments to the coefficients so that each party can check its share; see [verifiable secret sharing](/verifiable-secret-sharing/).
- **Proactive refresh.** Herzberg, Jarecki, Krawczyk and Yung (1995) let the parties renew their shares in periods. Each party deals a random sharing of 0, and every party adds all the shares of 0 it receives to its share. The secret does not change, because $f + g$ with $g(0) = 0$ still has the constant term $s$, but the new shares are independent of the old ones. So an attacker who learns $t - 1$ shares in one period and $t - 1$ in the next learns nothing, and old shares become useless. Their protocol uses verifiable sharing to stop dishonest parties from dealing bad sharings of 0.
- **Packed and ramp sharing.** Put $k$ secrets at $k$ points of one polynomial (Franklin and Yung), at the cost of a gap of $k$ between the privacy and reconstruction thresholds.
- **Short shares for long secrets.** Krawczyk's computational scheme encrypts the secret with a key, shares the key with Shamir's scheme, and spreads the ciphertext with an erasure code.
- **Weighted and hierarchical schemes.** Give important parties several points, or use derivatives of $f$ (Tassa) for levels of parties.

## When to use it

Use it to split a key or a seed among people or machines, for example for backup with a quorum, and as the sharing layer of threshold signatures, threshold decryption and MPC. The secret must be an element of the field, or a byte string shared byte by byte over $\mathrm{GF}(2^8)$. Use [verifiable secret sharing](/verifiable-secret-sharing/) if the dealer or the parties may cheat, and threshold protocols that never reconstruct the key if one machine must never hold it.

## Pitfalls

- **The point 0.** Never give out $f(0)$, and never use a share point that is 0 in the field, for example $x = p$ over $\mathbb{F}_p$, or $x = 256$ truncated to a byte over $\mathrm{GF}(2^8)$.
- **Integers instead of a field.** Over the integers, or modulo a number that is not prime, shares leak information about the secret, for example its parity or its size.
- **Weak randomness.** The coefficients must be uniform and secret. Coefficients from a bad generator, or derived from the secret, can make $t - 1$ shares enough.
- **Reusing a polynomial.** Sharing two secrets with related polynomials lets parties combine shares across them.
- **Silent wrong results.** A cheating party can shift the result by a chosen amount: with $\lambda_j$ known, adding $\delta$ to its share shifts the secret by $\lambda_j \delta$. Check consistency with extra shares, or use verifiable sharing, or authenticate shares with a MAC.
- **Mixing old and new shares** after a refresh gives a wrong secret.
- **Side channels.** Reconstruction handles the secret in memory; field arithmetic with table lookups in $\mathrm{GF}(2^8)$ is not constant time.

## Implementations

The Python code on this page implements the scheme over $\mathbb{F}_p$ and over $\mathrm{GF}(2^8)$ with the reduction polynomial $\mathtt{0x11b}$, with a consistency check for more than $t$ shares, addition of shares and proactive refresh. The tests check the example; that every $t$-subset reconstructs; perfect secrecy by enumeration, with $p = 11$ and $t = 3$ (each pair of shares comes from exactly one pair of coefficients, for every secret) and over $\mathrm{GF}(256)$ with $t = 2$; that a bad share gives a wrong secret without an error, shifted by exactly $\lambda_j$; that the check with $t + 1$ shares finds a bad share; linearity; and that refresh keeps the secret while old and new shares do not mix. The field multiplication is checked against the two products in FIPS 197; there are no official test vectors for Shamir's scheme itself, because its shares are random. The code is for study only, is not constant time, and must not be used to protect real data. Use a reviewed implementation, such as the one in HashiCorp Vault or a SLIP-0039 library, with randomness from libsodium or a FIPS 140 validated module.

## History

Adi Shamir's two-page paper "How to share a secret" appeared in the Communications of the ACM in November 1979. It defined $(k, n)$ threshold schemes, gave the polynomial construction, and noted that shares can be added and that the polynomial can be changed from time to time. George Blakley published a scheme with hyperplanes in the same year, independently. In 1981 McEliece and Sarwate observed that Shamir's shares form a Reed-Solomon codeword, which gives error correction. Karnin, Greene and Hellman (1983) proved that shares cannot be smaller than the secret. The scheme became the base of verifiable secret sharing (Feldman 1987, Pedersen 1991), of the BGW protocol for multiparty computation (1988), of proactive secret sharing (1995), and of threshold signature schemes used today.

## References
