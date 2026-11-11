---
tag: 9PHA6E
kind: problem
slug: computational-diffie-hellman
name: Computational Diffie-Hellman problem
aliases:
- CDH
- CDH problem
- computational Diffie-Hellman
area: cryptography/public-key
level: core
summary: Given g, g^x and g^y in a cyclic group, compute g^(xy). No harder than discrete logarithm and believed as hard in the groups used for Diffie-Hellman key exchange.
prereqs: [discrete-logarithm-problem, cyclic-group]
see_also: [decisional-diffie-hellman, diffie-hellman, elgamal-encryption, shoup-generic-lower-bound, generic-group-model, bilinear-diffie-hellman, baby-step-giant-step, pollard-rho-discrete-logarithm]
sources:
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), 1976
    locator: Section III, the key exchange whose key is g^(xy)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.7, The Diffie-Hellman problem; Chapter 8, Note 8.23 (i)
  - paper: doi:10.1007/3-540-69053-0_18
    title: Victor Shoup, Lower bounds for discrete logarithms and related problems, EUROCRYPT 1997, Lecture Notes in Computer Science 1233
    locator: pages 256 to 266, the generic lower bound for the Diffie-Hellman problem
  - paper: "Bert den Boer, Diffie-Hellman is as strong as discrete log for certain primes, CRYPTO 1988, LNCS 403, pages 530 to 539"
    locator: the reduction from discrete logarithm to Diffie-Hellman when the totient of p - 1 is smooth
  - paper: "Ueli M. Maurer and Stefan Wolf, The relationship between breaking the Diffie-Hellman protocol and computing discrete logarithms, SIAM Journal on Computing 28(5), pages 1689 to 1721, 1999"
    locator: the reduction with an auxiliary elliptic curve of smooth order
  - paper: "Dan Boneh, The decision Diffie-Hellman problem, ANTS-III, LNCS 1423, pages 48 to 63, 1998"
    locator: the survey of CDH, DDH and the relations between them
  - paper: "Tatsuaki Okamoto and David Pointcheval, The gap-problems, a new class of problems for the security of cryptographic schemes, PKC 2001, LNCS 1992, pages 104 to 118"
    locator: the definition of the gap Diffie-Hellman problem
  - paper: "Dan Boneh and Ramarathnam Venkatesan, Hardness of computing the most significant bits of secret keys in Diffie-Hellman and related schemes, CRYPTO 1996, LNCS 1109, pages 129 to 142"
    locator: the hard-core bits of g^(xy) modulo p
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 9, the section on cryptographic assumptions in cyclic groups (the DL, CDH and DDH experiments)
---

The computational Diffie-Hellman problem (CDH) asks, given a generator $g$ of a [cyclic group](/cyclic-group/) and two elements $g^x$ and $g^y$, for the element $g^{xy}$. It is the problem an eavesdropper must solve to compute the key of [Diffie-Hellman key exchange](/diffie-hellman/), and it is equivalent to recovering the message of [ElGamal encryption](/elgamal-encryption/). An algorithm for the [discrete logarithm problem](/discrete-logarithm-problem/) solves CDH, and in the groups used in practice no faster way is known. Its decisional form, [DDH](/decisional-diffie-hellman/), is a stronger assumption.

**Notation.** $G = \langle g \rangle$ is a cyclic group of order $q$; on this page $q$ is a prime unless stated otherwise. $x, y \in \mathbb{Z}_q$ are the secret exponents, $X = g^x$ and $Y = g^y$. $\lambda$ is the security parameter, so $q$ has about $2\lambda$ binary digits. $\mathcal{A}$ is an adversary that runs in time $t$, and $\mathrm{Adv}$ is its success probability.

## In plain words

Two people agree on a public starting element. Each picks a secret number, raises the starting element to it, and sends the result to the other. Each then raises the received element to its own secret number. Both arrive at the same element, the shared key.

The problem asks an eavesdropper to find that shared key from the two values sent in public. One way is to find a secret number from its public value, which is the discrete logarithm problem. Nobody knows a fundamentally faster way in the groups used in practice. The problem is to compute the key, not just to recognize it: recognizing the key is the separate, decisional problem.

## Definition

**Input.** A description of a cyclic group $G$ of order $q$ with a generator $g$, and two elements $X = g^x$ and $Y = g^y$, where $x$ and $y$ are not given.

**Output.** The element $g^{xy}$.

The element $g^{xy}$ is well defined: it does not depend on which exponents represent $X$ and $Y$, because $x$ and $y$ are unique modulo $q$.

**The CDH assumption.** For a family of groups indexed by $\lambda$, the success probability

$$\mathrm{Adv}^{\mathrm{cdh}}_G(\mathcal{A}) = \Pr\bigl[\mathcal{A}(G, g, g^x, g^y) = g^{xy}\bigr], \quad x, y \text{ uniform in } \mathbb{Z}_q,$$

is negligible in $\lambda$ for every adversary $\mathcal{A}$ that runs in time polynomial in $\lambda$. A group is a CDH group if the assumption is believed to hold for it.

## Variants

- **Square Diffie-Hellman.** Given $g^x$, compute $g^{x^2}$. For odd $q$ it is equivalent to CDH: $g^{xy} = \bigl(g^{(x+y)^2} / (g^{x^2} g^{y^2})\bigr)^{1/2}$, where the exponent $1/2$ is taken modulo $q$.
- **Inverse Diffie-Hellman.** Given $g^x$, compute $g^{1/x}$. For prime $q$ it is also equivalent to CDH, with a polynomial loss.
- **Gap Diffie-Hellman.** CDH stays hard even with an oracle for DDH (Okamoto and Pointcheval, 2001). This is the assumption behind several random oracle proofs, among them DHIES and [ECIES](/ecies/), and it holds in pairing groups, where DDH is easy.
- **Static Diffie-Hellman.** The exponent $x$ is fixed and the adversary may ask for $Z^x$ on elements of its choice before it must answer a fresh $Y^x$. It models a long-term key used many times. Brown and Gallant (2004) showed that such queries help the attacker when $q - 1$ has suitable factors.
- **Bilinear Diffie-Hellman.** In a group with a pairing $e$, compute $e(g, g)^{xyz}$ from $g^x$, $g^y$ and $g^z$; see [bilinear Diffie-Hellman](/bilinear-diffie-hellman/).
- **Composite order.** In $\mathbb{Z}_n^*$ for an RSA modulus $n$, CDH is at least as hard as factoring $n$ (Shmuely 1985, McCurley 1988).

## Examples

Take $p = 23$ and $g = 2$, which has order $q = 11$ in $\mathbb{Z}_{23}^*$, because $2^{11} = 2048 = 89 \cdot 23 + 1$. The group is $G = \{1, 2, 4, 8, 16, 9, 18, 13, 3, 6, 12\}$, listed as $2^0, \ldots, 2^{10}$.

| party | secret | public value | key |
|---|---|---|---|
| Alice | $x = 3$ | $X = 2^3 = 8$ | $Y^x = 13^3 \bmod 23 = 12$ |
| Bob | $y = 7$ | $Y = 2^7 \bmod 23 = 13$ | $X^y = 8^7 \bmod 23 = 12$ |

The CDH instance is $(g, X, Y) = (2, 8, 13)$ and its answer is $g^{21} = g^{10} = 12$. An attacker who lists the eleven powers of 2 finds $x = 3$ from $X = 8$ and then computes $13^3 \bmod 23 = 12$. In a group of order $q \approx 2^{256}$ that list cannot be made.

## Known algorithms

No algorithm is known that solves CDH in a standard group faster than by computing a discrete logarithm. So the known attacks are the discrete logarithm algorithms.

| group | best known attack | cost |
|---|---|---|
| any group of prime order $q$ | [Pollard rho](/pollard-rho-discrete-logarithm/), [baby-step giant-step](/baby-step-giant-step/) | $\Theta(q^{1/2})$ group operations |
| group of composite order $n$ | [Pohlig-Hellman](/pohlig-hellman/) then one of the above | about $\sum_i e_i (\log n + p_i^{1/2})$ for $n = \prod p_i^{e_i}$ |
| subgroup of $\mathbb{F}_p^*$ | [index calculus](/index-calculus/), number field sieve | subexponential in $\log p$, so $p$ must have about 3072 binary digits for $\lambda = 128$ |
| prime order elliptic curve group | Pollard rho | $\Theta(q^{1/2})$, so $q$ has about $2\lambda$ binary digits |
| any group, quantum computer | [Shor's algorithm](/shor-algorithm/) | polynomial in $\log q$ |

Pohlig-Hellman is why $q$ must be prime or have a large prime factor, and the number field sieve is why finite field groups need much larger parameters than [elliptic curve](/elliptic-curve-cryptography/) groups.

## Bounds

**Generic lower bound.** In the [generic group model](/generic-group-model/), an algorithm sees group elements only through random labels and an oracle for the group operation. Shoup (1997) proved that a generic algorithm that makes $m$ oracle calls in a group of prime order $q$ computes $g^{xy}$ with probability $O(m^2 / q)$. So constant success needs $\Omega(q^{1/2})$ operations, which Pollard rho matches. See [Shoup's generic lower bound](/shoup-generic-lower-bound/). The bound says nothing about algorithms that use the representation of the group, such as index calculus in $\mathbb{F}_p^*$.

**Hard-core bits.** In $\mathbb{Z}_p^*$, computing about $(\log p)^{1/2}$ of the most significant bits of $g^{xy}$ is as hard as computing all of $g^{xy}$ (Boneh and Venkatesan, 1996). This is a bound on partial information that is weaker than DDH.

## Reductions

Write $P \le Q$ if an algorithm for $Q$ gives an algorithm for $P$ with polynomial overhead.

- **CDH $\le$ DL.** Find $x$ from $X$, then return $Y^x$. One discrete logarithm and one exponentiation.
- **DDH $\le$ CDH.** Given $(X, Y, Z)$, compute $g^{xy}$ and compare it with $Z$. So DDH is the stronger assumption: DDH hard implies CDH hard implies DL hard.
- **DL $\le$ CDH, in special cases.** den Boer (1988) showed this for $\mathbb{Z}_p^*$ when the [Euler totient](/euler-totient/) $\varphi(p - 1)$ has only small prime factors. Maurer (1994) and Maurer and Wolf (1999) showed it for a group of prime order $q$ whenever an elliptic curve over $\mathbb{F}_q$ with smooth order is known; for most $q$ such a curve is believed to exist. The reduction is not tight: it makes a polynomial number of calls to the CDH algorithm. No reduction is known in general.
- **CDH $\le$ DDH fails in some groups.** In groups with an efficient pairing, DDH is easy and CDH is believed hard. These are the gap groups of Joux and Nguyen (2003).
- **Random self-reducibility.** Given $(X, Y)$, choose $a, b$ uniform in $\mathbb{Z}_q$ and set $X' = X g^a$, $Y' = Y g^b$. The pair $(X', Y')$ is uniform and independent of $(X, Y)$. If $Z' = g^{(x+a)(y+b)}$, then $g^{xy} = Z' X^{-b} Y^{-a} g^{-ab}$. So an algorithm that succeeds on a fraction $\varepsilon$ of the instances gives, with about $1/\varepsilon$ independent tries, a list of candidates that contains the answer with constant probability. Since a CDH answer cannot be checked without a DDH oracle, picking the right candidate needs the self-corrector of Shoup (1997). This is why the CDH assumption is stated for uniform $x$ and $y$ without loss.
- **One-wayness of ElGamal.** Recovering the message of an ElGamal ciphertext with the public key is equivalent to CDH in the same group (Handbook of Applied Cryptography Note 8.23 (i)).

## Applications

- **[Diffie-Hellman key exchange](/diffie-hellman/).** A passive eavesdropper cannot compute the key unless it solves CDH. For the key to look random, which a key derivation step needs, the protocols assume DDH or hash $g^{xy}$ in the [random oracle model](/random-oracle-model/).
- **[ElGamal encryption](/elgamal-encryption/).** One-way under CDH, IND-CPA under DDH. Hashed ElGamal, which encrypts $m \oplus H(g^{xy})$, is IND-CPA under CDH in the random oracle model.
- **[ECIES](/ecies/) and DHIES.** IND-CCA in the random oracle model under gap Diffie-Hellman.
- **Fujisaki-Okamoto on ElGamal.** CDH gives the one-wayness that the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) needs.
- **Pairing-based signatures.** BLS signatures are secure under CDH in a pairing group, where DDH is easy; see [bilinear pairing](/bilinear-pairing/).

## References
