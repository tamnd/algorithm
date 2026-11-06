---
tag: ACKYPK
kind: concept
slug: legendre-symbol
name: Legendre symbol
aliases:
- quadratic character mod p
area: number-theory/modular-arithmetic
level: advanced
summary: (a/p) is 1, -1 or 0 according to whether a is a residue, nonresidue or divisible by the odd prime p.
prereqs: [quadratic-residue]
see_also: [euler-criterion, quadratic-reciprocity, jacobi-symbol, gauss-lemma, solovay-strassen, modular-square-root, goldwasser-micali-cryptosystem, quadratic-residuosity-problem]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.5, Legendre and Jacobi symbols (Definition 2.145, Fact 2.146, Algorithm 2.149, Fact 2.150 and Remark 2.151)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Sections 6.5 and 6.7 (quadratic residues and Legendre's symbol), Section 6.11 (Gauss's lemma and the quadratic character of 2)
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 5, Sections 5.1 and 5.2 (the Legendre symbol, Euler's criterion, the law of quadratic reciprocity)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer GTM 138
    locator: Section 1.4.2, The Legendre-Jacobi-Kronecker symbol
---

The Legendre symbol $\left(\frac{a}{p}\right)$, for an odd prime $p$ and an integer $a$, is $0$ if $p \mid a$, $1$ if $a$ is a [quadratic residue](/quadratic-residue/) modulo $p$, and $-1$ if $a$ is a nonresidue. It turns the question "is $a$ a square modulo $p$?" into a value that is multiplicative in $a$: $\left(\frac{ab}{p}\right) = \left(\frac{a}{p}\right)\left(\frac{b}{p}\right)$. [Euler's criterion](/euler-criterion/) gives $\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod p$, and the law of [quadratic reciprocity](/quadratic-reciprocity/) with its two supplements lets the symbol be computed by a method like the Euclidean algorithm. Legendre introduced the notation in 1798.

## In plain words

On a clock with an odd prime number of positions, every position is a square, a non-square, or zero. The Legendre symbol is a short label for this: plus one for a square, minus one for a non-square, and zero for zero. These labels multiply like signs. A square times a non-square is a non-square, and two non-squares give a square. There are two fast ways to find the label. One raises the number to half the clock size, rounded down. The other swaps the number and the clock size again and again, as in Euclid's method, and tracks a sign at each swap.

## The idea

**Definition.** For an odd prime $p$ and an integer $a$,

$$\left(\frac{a}{p}\right) = \begin{cases} 0 & \text{if } p \mid a, \\ 1 & \text{if } p \nmid a \text{ and } x^2 \equiv a \pmod p \text{ has a solution}, \\ -1 & \text{otherwise.} \end{cases}$$

It is also written $(a/p)$ or $(a \mid p)$. Then $x^2 \equiv a \pmod p$ has exactly $1 + (a/p)$ solutions modulo $p$.

**Basic properties** (HAC, Fact 2.146).

- *Periodicity.* If $a \equiv b \pmod p$, then $(a/p) = (b/p)$.
- *Euler's criterion.* $(a/p) \equiv a^{(p-1)/2} \pmod p$. For $p \nmid a$, $a^{(p-1)/2}$ is a square root of $a^{p-1} \equiv 1$, so it is $\pm 1$, and it is $1$ exactly on the squares; see [Euler's criterion](/euler-criterion/).
- *Complete multiplicativity.* $(ab/p) = (a/p)(b/p)$, from Euler's criterion. In particular $(a^2/p) = 1$ for $p \nmid a$, and $(a/p)$ is determined by the values at $-1$, $2$ and the odd primes dividing $a$.
- *Balance.* $\sum_{a=0}^{p-1} (a/p) = 0$, since half of the nonzero residues are squares.
- *The first supplement.* $(-1/p) = (-1)^{(p-1)/2}$: $-1$ is a square exactly when $p \equiv 1 \pmod 4$.
- *The second supplement.* $(2/p) = (-1)^{(p^2-1)/8}$: $2$ is a square exactly when $p \equiv \pm 1 \pmod 8$.
- *Quadratic reciprocity.* For distinct odd primes $p$ and $q$, $(p/q)(q/p) = (-1)^{\frac{p-1}{2} \cdot \frac{q-1}{2}}$. So $(p/q) = (q/p)$ unless $p \equiv q \equiv 3 \pmod 4$, when $(p/q) = -(q/p)$.

**Gauss's lemma.** For $p \nmid a$, let $\mu$ be the number of $k \in \{1, \ldots, (p-1)/2\}$ for which the least positive residue of $ka$ modulo $p$ is greater than $p/2$. Then $(a/p) = (-1)^\mu$. It gives the second supplement and is the basis of several proofs of reciprocity; see [Gauss's lemma](/gauss-lemma/).

**As a character.** The map $a \mapsto (a/p)$ on $\mathbb{Z}_p^*$ is a group homomorphism onto $\{\pm 1\}$, with kernel the squares. It is the unique character of order 2 modulo $p$, the *quadratic character*, and so a Dirichlet character. Its Gauss sum $g = \sum_a (a/p) \zeta^a$, with $\zeta = e^{2\pi i/p}$, satisfies $g^2 = (-1/p)\, p$, which gives another proof of reciprocity.

**Generalizations.** The [Jacobi symbol](/jacobi-symbol/) $(a/n)$ extends the definition to odd $n = p_1 \cdots p_r$ as the product $\prod (a/p_i)$; it keeps multiplicativity and reciprocity, but $(a/n) = 1$ no longer implies that $a$ is a square modulo $n$. The Kronecker symbol extends it further to even $n$.

**Computing it.**

- *By Euler's criterion*: one [modular exponentiation](/modular-exponentiation/), $O(\log p)$ multiplications modulo $p$, or $O(k^3)$ bit operations for $k$-digit $p$ with schoolbook arithmetic.
- *By reciprocity*: treat the symbol as a Jacobi symbol, so that no factoring is needed. Reduce $a$ modulo $n$, remove factors 2 with the second supplement, swap $a$ and $n$ with reciprocity, and repeat. The sequence of remainders is that of a Euclidean algorithm, so it takes $O(k^2)$ bit operations (HAC, Algorithm 2.149 and Fact 2.150). Subquadratic versions based on half-gcd methods exist.
- Both methods give the symbol only; finding the square root itself is the [modular square root](/modular-square-root/) problem.

## Examples

**Modulo 7.** The squares are $1, 2, 4$, so $(a/7)$ for $a = 1, \ldots, 6$ is $1, 1, -1, 1, -1, -1$. Euler's criterion: $3^3 = 27 \equiv -1 \pmod 7$, so $(3/7) = -1$. Gauss's lemma for $a = 3$: the least residues of $3, 6, 9$ are $3, 6, 2$, and one of them, 6, exceeds $3.5$, so $(3/7) = (-1)^1 = -1$. For $a = 2$: $2, 4, 6$, two exceed $3.5$, so $(2/7) = 1$, and $7 \equiv -1 \pmod 8$ agrees.

**The supplements.** $(-1/13) = 1$, since $13 \equiv 1 \pmod 4$ and $5^2 = 25 \equiv -1$. $(2/11) = -1$, since $11 \equiv 3 \pmod 8$.

**By reciprocity.** Compute $(219/383)$, where 383 is prime and $219 = 3 \cdot 73$. Then $(219/383) = (3/383)(73/383)$.

- $3 \equiv 383 \equiv 3 \pmod 4$, so $(3/383) = -(383/3) = -(2/3) = -(-1) = 1$.
- $73 \equiv 1 \pmod 4$, so $(73/383) = (383/73) = (18/73) = (2/73)(9/73) = (2/73) = 1$, since $73 \equiv 1 \pmod 8$ and 9 is a square.

So $(219/383) = 1$, and Euler's criterion agrees: $219^{191} \equiv 1 \pmod{383}$.

**Balance.** Modulo 11 the values for $a = 1, \ldots, 10$ are five $+1$ and five $-1$, and their sum is 0.

## Where it is used

- **Deciding quadratic residuosity** modulo a prime, as the first step of [Tonelli-Shanks](/tonelli-shanks/) and to find a quadratic nonresidue by random trials, two on average (HAC, Remark 2.151).
- **Primality testing.** The [Solovay-Strassen test](/solovay-strassen/) checks $a^{(n-1)/2} \equiv (a/n)$ with the Jacobi symbol; for prime $n$ it always holds.
- **Cryptography.** The [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) hides a bit in whether a number with Jacobi symbol 1 is a square modulo $n = pq$; the secret key computes Legendre symbols modulo $p$ and $q$. The Legendre pseudorandom function, $k \mapsto ((k + x)/p)$ for a secret $x$, is studied as a primitive for multiparty computation.
- **Elliptic curves.** The curve $y^2 = x^3 + ax + b$ over $\mathbb{F}_p$ has $p + 1 + \sum_x ((x^3 + ax + b)/p)$ points, because each $x$ gives $1 + ((x^3 + ax + b)/p)$ values of $y$.
- **Factoring.** The quadratic sieve keeps the primes $p$ with $(n/p) = 1$ in its factor base.
- **Analytic number theory and combinatorics.** Character sums of $(a/p)$, such as the Pólya-Vinogradov inequality, bound the least nonresidue; the sequence $(a/p)$ gives Paley's Hadamard matrices and Legendre sequences with good correlation.

## References
