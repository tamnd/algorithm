---
tag: F5F4ZX
kind: concept
slug: quadratic-residue
name: Quadratic residue
aliases:
- quadratic nonresidue
area: number-theory/modular-arithmetic
level: core
summary: A unit a modulo n that is congruent to a perfect square modulo n; modulo an odd prime exactly half of the units are quadratic residues.
prereqs: [multiplicative-group-modulo-n, congruence]
see_also: [legendre-symbol, euler-criterion, quadratic-reciprocity, jacobi-symbol, modular-square-root, tonelli-shanks, quadratic-residuosity-problem, goldwasser-micali-cryptosystem]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Definition 2.134, Fact 2.135, Example 2.136 (Q_13), Fact 2.137 and Example 2.138 (Q_21), Fact 2.140 (number of square roots)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Section 6.5, Quadratic residues, and Section 6.7, Elementary properties of quadratic residues and non-residues
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 3.1, Quadratic residues
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 5, Quadratic Reciprocity, Section 5.1, Quadratic Residues and Nonresidues
---

An integer $a$ coprime to $n$ is a quadratic residue modulo $n$ if $x^2 \equiv a \pmod n$ has a solution, and a quadratic nonresidue otherwise. Modulo an odd prime $p$, exactly half of the $p - 1$ nonzero residues are quadratic residues, and they form a subgroup of index 2 in the [multiplicative group](/multiplicative-group-modulo-n/). [Euler's criterion](/euler-criterion/) decides membership with one [modular exponentiation](/modular-exponentiation/), the [Legendre symbol](/legendre-symbol/) records the answer as $\pm 1$, and [quadratic reciprocity](/quadratic-reciprocity/) relates the answers for two primes. Modulo a composite $n$ with unknown factors, deciding whether $a$ is a square is believed hard, which is the basis of several cryptosystems.

## In plain words

Take every number on a clock that shares no factor with the clock size, square it, and see where it lands. The positions you can reach in this way are the squares of the clock, and the other positions are the non-squares. On a clock with a prime number of positions, exactly half of the nonzero positions are squares. A square times a square is a square, a square times a non-square is a non-square, and two non-squares multiply to a square, just as signs multiply. There is a fast test to tell squares from non-squares when the clock size is a prime. When the clock size is a product of two large secret primes, no fast test is known.

## The idea

**Definition.** Let $n \ge 2$ and $\gcd(a, n) = 1$. Then $a$ is a *quadratic residue* modulo $n$ if there is an $x$ with $x^2 \equiv a \pmod n$, and a *quadratic nonresidue* otherwise. Residues that share a factor with $n$, such as 0, are neither; this is the convention of HAC and of most number theory texts. The set of quadratic residues modulo $n$ is written $Q_n$, and the solutions $x$ are the square roots of $a$.

**Odd prime modulus.** Let $p$ be an odd prime.

- *Half are squares.* If $x^2 \equiv y^2$, then $p \mid (x - y)(x + y)$, so $y \equiv \pm x$. Since $x \not\equiv -x$, each quadratic residue has exactly two square roots, and the squaring map on $\mathbb{Z}_p^*$ is two-to-one. So $|Q_p| = (p - 1)/2$, and $Q_p$ is the set of squares of $1, 2, \ldots, (p - 1)/2$.
- *A subgroup of index 2.* $Q_p$ is the image of the homomorphism $x \mapsto x^2$, so it is a subgroup, and its cosets are $Q_p$ and the nonresidues. This gives the sign rules: residue times residue is a residue, residue times nonresidue is a nonresidue, and nonresidue times nonresidue is a residue.
- *With a primitive root.* If $g$ is a [primitive root](/primitive-root/) modulo $p$, then $a = g^i$ is a quadratic residue if and only if $i$ is even (HAC, Fact 2.135).
- *Euler's criterion.* $a^{(p-1)/2} \equiv 1 \pmod p$ for a residue, and $\equiv -1$ for a nonresidue. So one modular exponentiation decides the question; see [Euler's criterion](/euler-criterion/).
- *The symbol.* The [Legendre symbol](/legendre-symbol/) $(a/p)$ is $1$ for a residue, $-1$ for a nonresidue and 0 for $p \mid a$. It is multiplicative in $a$, and quadratic reciprocity lets it be computed by a gcd-like method.

**Special values.** For an odd prime $p$, $-1$ is a quadratic residue if and only if $p \equiv 1 \pmod 4$, and $2$ is a quadratic residue if and only if $p \equiv \pm 1 \pmod 8$. These are the supplements to [quadratic reciprocity](/quadratic-reciprocity/).

**Composite modulus.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), $a$ is a quadratic residue modulo $n$ if and only if it is one modulo each prime power $p^e$ that exactly divides $n$.

- For an odd prime $p$ and $e \ge 1$, $a$ is a quadratic residue modulo $p^e$ if and only if it is one modulo $p$; square roots lift by [Hensel lifting](/hensel-lifting/).
- Modulo $2$ and $4$, the residues are 1; modulo $2^e$ with $e \ge 3$, an odd $a$ is a quadratic residue if and only if $a \equiv 1 \pmod 8$.
- For $n = pq$ with distinct odd primes, $|Q_n| = (p - 1)(q - 1)/4$, a quarter of $\mathbb{Z}_n^*$, and each residue has 4 square roots (HAC, Facts 2.137 and 2.140).

The [Jacobi symbol](/jacobi-symbol/) $(a/n)$ is the product of the Legendre symbols for the prime factors of $n$. It is $-1$ only for nonresidues, but $+1$ does not mean that $a$ is a residue: modulo 15, $(2/15) = (2/3)(2/5) = (-1)(-1) = 1$, but 2 is not a square.

**Computational questions.**

- *Deciding*, modulo a prime: Euler's criterion in $O(\log p)$ multiplications, or the Jacobi symbol algorithm in $O((\log p)^2)$ bit operations.
- *Deciding*, modulo $n = pq$ with unknown factors: this is the [quadratic residuosity problem](/quadratic-residuosity-problem/), for which no method faster than factoring $n$ is known.
- *Finding square roots*, modulo a prime: the [modular square root](/modular-square-root/) problem, solved by [Tonelli-Shanks](/tonelli-shanks/) or [Cipolla's algorithm](/cipolla-algorithm/). Modulo $n = pq$ it is as hard as factoring $n$.
- *Finding a nonresidue*, modulo a prime: half of all residues work, so random trials take 2 tries on average. No deterministic polynomial-time method is known without unproven hypotheses; under the generalized Riemann hypothesis, the least nonresidue is below $2 (\ln p)^2$ (Bach, 1990).

## Examples

**Modulo 7.** The squares of $1, 2, 3$ are $1, 4, 2$, so $Q_7 = \{1, 2, 4\}$ and the nonresidues are $3, 5, 6$. Since $7 \equiv 3 \pmod 4$, $-1 \equiv 6$ is a nonresidue; since $7 \equiv -1 \pmod 8$, 2 is a residue: $3^2 = 9 \equiv 2$.

**Modulo 11, with Euler's criterion.** $Q_{11} = \{1, 3, 4, 5, 9\}$. The values $a^5 \bmod 11$ for $a = 1, \ldots, 10$ are $1, 10, 1, 1, 1, 10, 10, 10, 1, 10$: 1 exactly on $Q_{11}$, and $10 \equiv -1$ on the nonresidues.

**Modulo 13.** $Q_{13} = \{1, 3, 4, 9, 10, 12\}$, and the nonresidues are $2, 5, 6, 7, 8, 11$. Since $13 \equiv 1 \pmod 4$, $-1 \equiv 12 = 5^2 - 13$ is a residue. With the primitive root 6, the residues are the even powers $6^0, 6^2, \ldots$, which are $1, 10, 9, 12, 3, 4$.

**Modulo 23.** $Q_{23} = \{1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18\}$, eleven elements.

**Composite moduli.** $Q_{15} = \{1, 4\}$, a quarter of the 8 units: 4 has the square roots $2, 7, 8, 13$. $Q_{21} = \{1, 4, 16\}$ (HAC, Example 2.138). $Q_8 = \{1\}$ and $Q_{16} = \{1, 9\}$, which agrees with the rule $a \equiv 1 \pmod 8$.

## Where it is used

- **Cryptography.** The [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) encrypts a bit as a random residue or a random nonresidue with Jacobi symbol 1 modulo $n = pq$. The [Rabin cryptosystem](/rabin-cryptosystem/) encrypts by squaring modulo $n$, and [Blum Blum Shub](/blum-blum-shub/) outputs bits of repeated squares.
- **Primality testing.** The [Solovay-Strassen test](/solovay-strassen/) checks Euler's criterion against the Jacobi symbol, which must agree for prime $n$.
- **Factoring.** The quadratic sieve and the number field sieve keep only the primes $p$ for which $n$ is a quadratic residue modulo $p$, since only those can divide values of $x^2 - n$.
- **Square roots modulo primes.** Tonelli-Shanks needs one nonresidue; elliptic curve point decompression needs a square root modulo the field prime.
- **Representations by sums of squares.** An odd prime is a sum of two squares if and only if $-1$ is a quadratic residue, that is, $p \equiv 1 \pmod 4$.
- **Combinatorial designs.** For a prime $p \equiv 3 \pmod 4$ the quadratic residues form a difference set, which gives Paley's construction of Hadamard matrices of order $p + 1$. For $p \equiv 1 \pmod 4$ they define the Paley graph. Quadratic residue codes are built from the same sets.

## References
