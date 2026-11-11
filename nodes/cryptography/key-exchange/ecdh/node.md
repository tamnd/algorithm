---
tag: 79PZ04
kind: algorithm
slug: ecdh
name: Elliptic-curve Diffie-Hellman
aliases:
- ECDH
- elliptic-curve key agreement
area: cryptography/key-exchange
level: core
summary: Diffie-Hellman in the group of points of an elliptic curve. Each side sends dG, checks the point it gets, and both use the x-coordinate of d_A d_B G as the shared secret.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the field prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1985
  people: [Victor S. Miller, Neal Koblitz]
  note: Miller (CRYPTO 1985) and Koblitz (1987) proposed elliptic curve groups for cryptography, with Diffie-Hellman as the first example. ECDH was standardized in IEEE 1363, ANSI X9.63, SEC 1 and NIST SP 800-56A.
prereqs: [diffie-hellman, elliptic-curve-cryptography]
see_also: [diffie-hellman, x25519, x448, elliptic-curve-cryptography, elliptic-curve-discrete-logarithm-problem, small-subgroup-attack, ecies, ecdsa]
sources:
  - paper: doi:10.6028/NIST.SP.800-56Ar3
    title: Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev and Richard Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018
    locator: Section 5.6.1.2 (ECC key pair generation), Section 5.6.2.3.3 (ECC full public-key validation), Section 5.6.2.3.4 (ECC partial public-key validation) and Section 5.7.1.2 (the ECC CDH primitive)
  - url: "https://www.rfc-editor.org/rfc/rfc5903"
    title: David Fu and Jerome Solinas, RFC 5903, Elliptic Curve Groups modulo a Prime (ECP Groups) for IKE and IKEv2, June 2010
    locator: Section 3 (the P-256, P-384 and P-521 groups) and Section 8 (test vectors, 8.1 for P-256 and 8.2 for P-384)
  - paper: doi:10.1007/3-540-39799-X_31
    title: Victor S. Miller, Use of elliptic curves in cryptography, CRYPTO 1985, LNCS 218, pages 417 to 426
    locator: the proposal of elliptic curve groups and the analogue of Diffie-Hellman key exchange
  - paper: doi:10.1090/S0025-5718-1987-0866109-5
    title: Neal Koblitz, Elliptic curve cryptosystems, Mathematics of Computation 48(177), pages 203 to 209, 1987
    locator: the elliptic curve analogues of Diffie-Hellman and of ElGamal
  - paper: doi:10.1007/3-540-36288-6_16
    title: Adrian Antipa, Daniel Brown, Alfred Menezes, René Struik and Scott Vanstone, Validation of elliptic curve public keys, PKC 2003, LNCS 2567, pages 211 to 223
    locator: the invalid-curve attack on ECDH without public key validation
  - paper: doi:10.1007/978-3-319-24174-6_21
    title: Tibor Jager, Jörg Schwenk and Juraj Somorovsky, Practical invalid curve attacks on TLS-ECDH, ESORICS 2015, LNCS 9326, pages 407 to 425
    locator: invalid curve attacks on TLS libraries that skipped the on-curve check
  - book: isbn:9780387952734
    title: Darrel Hankerson, Alfred Menezes and Scott Vanstone, Guide to Elliptic Curve Cryptography, Springer, 2004
    locator: Chapter 3 (elliptic curve arithmetic, Jacobian coordinates and scalar multiplication) and Chapter 4 (cryptographic protocols, public key validation and ECDH)
---

Elliptic-curve Diffie-Hellman (ECDH) is [Diffie-Hellman key exchange](/diffie-hellman/) in the group of points of an [elliptic curve](/elliptic-curve-cryptography/) over a finite field. Each party picks a secret scalar $d$, sends the point $dG$, checks the point it receives, and multiplies it by its own scalar; both get $d_A d_B G$, and its $x$-coordinate is the shared secret. The best known attacks on the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/) take about $\sqrt{n}$ steps, so a 256-bit curve gives about the security of 3072-bit finite-field Diffie-Hellman with keys of 32 bytes. The check of the received point is essential: without it, the invalid-curve attack recovers the private key.

**Notation.** $E$ is the curve $y^2 = x^3 + ax + b$ over $\mathbb{F}_p$, with $p$ a prime of $m$ binary digits. $O$ is the point at infinity, the identity of the group $E(\mathbb{F}_p)$. $G$ is a base point of prime order $n$, and $h = \#E(\mathbb{F}_p)/n$ is the cofactor ($h = 1$ for P-256 and P-384). $d_A$ and $d_B$ are private scalars in $[1, n-1]$, and $Q_A = d_A G$ and $Q_B = d_B G$ the public points. $kP$ is $P$ added to itself $k$ times. $Z$ is the shared secret.

## In plain words

On an elliptic curve, two points can be "added" to give a third point of the curve, by a fixed rule with lines through the points. Adding a point to itself many times is fast, but given the result, finding how many times was used seems very hard.

So the curve plays the role that powers of a number play in ordinary Diffie-Hellman. Alice picks a secret count and sends the base point added to itself that many times; Bob does the same. Each one then adds the point received to itself their own secret number of times. Both end at the same point.

The keys are much shorter than in ordinary Diffie-Hellman for the same strength. Each side must check that the point received is really on the right curve, or a cheater can learn the secret.

## The problem

Two parties exchange messages over a public channel and must end with the same secret that a passive adversary cannot compute: the [key agreement problem](/key-agreement-problem/). The domain parameters $(p, a, b, G, n, h)$ are public and fixed, for example the curve P-256.

## The algorithm

Each party runs ECDH-KEYGEN and sends $Q$. On the peer's point, it runs VALIDATE and then ECC-CDH. This follows SP 800-56A Rev. 3.

```pseudo id=main
ECDH-KEYGEN(E, G, n)
L1  d ← a uniform integer in [1, n − 1]
L2  Q ← dG                                     ▷ scalar multiplication
L3  return (d, Q)                              ▷ keep d secret, send Q

VALIDATE(Q, full)                              ▷ Sections 5.6.2.3.3 and 5.6.2.3.4
L4  if Q = O then fail
L5  if x_Q or y_Q is not in [0, p − 1] then fail
L6  if y_Q² ≢ x_Q³ + a·x_Q + b (mod p) then fail  ▷ Q is on E
L7  if full and nQ ≠ O then fail               ▷ Q is in the subgroup of order n

ECC-CDH(d, Q)                                  ▷ Section 5.7.1.2
L8  P ← (h·d)Q
L9  if P = O then fail
L10 return x_P as a big-endian string of ⌈m/8⌉ bytes
```

**About the code.** Line L2 and line L8 are scalar multiplications. The Python code uses double-and-add in Jacobian coordinates $(X : Y : Z)$ with $x = X/Z^2$ and $y = Y/Z^3$, so that it needs only one field inversion at the end. The addition and doubling formulas use $a$ but never $b$; this is why line L6 matters. Lines L4 to L6 are partial validation, and line L7 adds the order check of full validation. When $h = 1$, every point of $E$ other than $O$ has order $n$, so partial validation is enough. The multiplication by $h$ in line L8 sends any component of small order to $O$. The code checks the RFC 5903 vectors for P-256 and P-384. It is for study only and is not constant time: the loop branches on the bits of $d$.

## Example

**A toy curve.** Take $E: y^2 = x^3 + 2x + 2$ over $\mathbb{F}_{17}$ with $G = (5, 1)$. The curve has 19 points, so $n = 19$ and $h = 1$. The multiples of $G$ are $G = (5,1)$, $2G = (6,3)$, $3G = (10,6)$, $7G = (0,6)$, and so on, up to $19G = O$.

| step | Alice | Bob |
|---|---|---|
| L1 | $d_A = 3$ | $d_B = 7$ |
| L2 | $Q_A = 3G = (10, 6)$ | $Q_B = 7G = (0, 6)$ |
| L6 | $6^2 = 36 \equiv 2$ and $0 + 0 + 2 = 2$ | $6^2 \equiv 2$ and $1000 + 20 + 2 = 1022 \equiv 2$ |
| L8 | $3 Q_B = 21G = 2G = (6, 3)$ | $7 Q_A = 21G = (6, 3)$ |
| L10 | $Z = 6$ | $Z = 6$ |

A peer that sends $(1, 1)$ fails at line L6: $1^2 = 1$, but $1 + 2 + 2 = 5$.

**P-256, RFC 5903 Section 8.1.** With the private keys of that section, both parties get the point whose $x$-coordinate is

$$Z = \texttt{D6840F6B42F6EDAFD13116E0E12565202FEF8E9ECE7DCE03812464D04B9442DE},$$

which is the 32-byte shared secret. The Python tests check this value and the P-384 vector of Section 8.2.

## Correctness

The points of $E$ form a commutative group, so scalar multiplication satisfies $a(bP) = (ab)P = b(aP)$. Hence $d_A Q_B = d_A d_B G = d_B Q_A$, and with $h = 1$ both parties compute the same point and the same $x$-coordinate. An honest $Q = dG$ with $1 \le d \le n-1$ is not $O$, has reduced coordinates, lies on $E$ and satisfies $nQ = O$, so it passes VALIDATE. The point $h d_A d_B G$ is not $O$, since $n$ is prime, $n \nmid d_A d_B$ and $\gcd(h, n) = 1$. The full proof, with the cofactor, is below.

Security rests on the [ECDLP](/elliptic-curve-discrete-logarithm-problem/) and on the elliptic-curve forms of the [CDH](/computational-diffie-hellman/) and [DDH](/decisional-diffie-hellman/) problems, assumed hard on the standard curves.

## Complexity

A scalar multiplication by an $m$-digit scalar does about $m$ doublings and $m/2$ additions with double-and-add. In Jacobian coordinates, a doubling costs about 8 field multiplications and an addition about 16, plus one inversion at the end (the exact counts depend on the formulas). Each field multiplication of $m$-digit numbers costs $\Theta(m^2)$ with schoolbook arithmetic, so each party does $\Theta(m^3)$ work for lines L2 and L8, and the same for the order check of line L7. Each party sends one point, $2m$ binary digits uncompressed or $m + 1$ compressed. The extra space is $\Theta(m)$.

For the same security, $m$ is much smaller than for finite-field Diffie-Hellman: index calculus and the number field sieve do not apply to well-chosen curves, so the best attack is [Pollard's rho](/pollard-rho-discrete-logarithm/) with about $\sqrt{\pi n / 4}$ group operations. P-256 gives about 128 bits of security, against 3072 digits for a finite field.

## Properties

- **Contributory** and **one round**, as Diffie-Hellman.
- **Forward secrecy** when both key pairs are ephemeral and erased.
- **Unauthenticated.** It needs signatures, static keys or a password protocol against a [man in the middle](/man-in-the-middle-attack/).
- **Only $x$ is used.** $dQ$ and $-dQ$ have the same $x$-coordinate, so the sign of $y$ does not matter.

## Variants and improvements

- **Montgomery curves and the ladder.** [X25519](/x25519/) and [X448](/x448/) use $x$-only arithmetic, need no point validation beyond clamping, and run in constant time with simple code.
- **Cofactor ECDH.** SP 800-56A multiplies by $h$ (line L8) for curves with $h > 1$; Curve25519 handles its cofactor 8 by clamping instead.
- **Static and ephemeral keys.** One-pass and two-pass schemes with static keys (ECMQV, the unified model) give implicit authentication; [ECIES](/ecies/) is ECDH with a static receiver key and a KDF.
- **Point compression.** Send $x$ and one bit of $y$; the receiver recovers $y$ with a square root mod $p$.
- **Faster scalar multiplication.** Windowed and NAF methods, precomputed tables for the fixed point $G$ in line L2, and complete addition formulas that have no special cases.

## When to use it

Use ECDH on P-256 or P-384 when a standard or a FIPS 140 module requires NIST curves, as in many government and enterprise systems. Otherwise prefer [X25519](/x25519/), which is easier to implement safely. Always add authentication, pass $Z$ through a KDF such as [HKDF](/hkdf/), and use a maintained library with constant-time code.

## Pitfalls

- **No on-curve check.** The formulas never use $b$, so they work just as well on any curve $y^2 = x^3 + ax + b'$. An attacker sends a point of small order $\ell$ on such a curve; the victim computes $d Q'$, which reveals $d \bmod \ell$ (up to sign, since only $x$ is used). With several primes $\ell$ and the Chinese remainder theorem, the attacker recovers $d$ (Antipa et al., PKC 2003). Jager, Schwenk and Somorovsky (ESORICS 2015) found TLS libraries that skipped this check. The tests of this page run the attack on a toy curve with $p = 65519$ and $n = 65447$; it recovers the key without validation and fails at line L6 with it.
- **Ignoring the cofactor** on curves with $h > 1$: an element of small order then fixes part of the secret ([small subgroup attack](/small-subgroup-attack/)).
- **Raw Z as a key.** $Z$ is a field element, not a uniform string; hash it.
- **Bad randomness.** A repeated or biased $d$ leaks the key in some protocols; draw it from a cryptographic generator.
- **Timing and faults.** Double-and-add branches on secret bits. Fault attacks that move the computation to a weaker curve (Biehl, Meyer and Müller, CRYPTO 2000) are another reason to check points.

## Implementations

## History

Victor Miller (CRYPTO 1985) and Neal Koblitz (*Mathematics of Computation*, 1987) independently proposed the groups of elliptic curves over finite fields for cryptography, and both described the Diffie-Hellman analogue. Standards followed around 2000: IEEE 1363, ANSI X9.63 and SEC 1 defined ECDH and its cofactor variant, and NIST published the P-curves in FIPS 186-2. NIST SP 800-56A (2006, revised 2007, 2013 and 2018) fixed the validation rules used above. Validation attacks drove much of the later history: invalid-curve and fault attacks around 2000 to 2003, the TLS attacks of 2015, and the move to Montgomery curves such as Curve25519, whose $x$-only ladder avoids the problem.

## References
