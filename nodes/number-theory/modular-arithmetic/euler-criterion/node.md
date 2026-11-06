---
tag: XEMGW8
kind: theorem
slug: euler-criterion
name: Euler's criterion
area: number-theory/modular-arithmetic
level: advanced
summary: (a/p) ≡ a^((p-1)/2) (mod p) for an odd prime p.
prereqs: [quadratic-residue, fermat-little-theorem]
see_also: [legendre-symbol, jacobi-symbol, quadratic-reciprocity, solovay-strassen, tonelli-shanks, cipolla-algorithm, modular-square-root, wilson-theorem]
sources:
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.8, Quadratic residues, Theorem 2.21 (Euler's criterion) and Theorems 2.31 and 2.32 (square roots of -1)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.5, Definition 2.145 and Fact 2.146(i) (the Legendre symbol and Euler's criterion), and Remark 2.151 (finding a quadratic non-residue)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Sections 6.5 to 6.7 (Wilson's theorem and quadratic residues)
  - url: https://en.wikipedia.org/wiki/Euler%27s_criterion
    title: Euler's criterion, Wikipedia
    locator: lead (the 1748 paper of Euler) and section Proof, Alternative proof (by pairing, with Wilson's theorem); note citing Gauss, Disquisitiones Arithmeticae, Article 106
---

**Euler's criterion** decides whether an integer is a square modulo an odd prime $p$ with one power: for $p \nmid a$, the residue $a^{(p-1)/2} \bmod p$ is $1$ if $a$ is a [quadratic residue](/quadratic-residue/) and $-1$ if it is not. In the notation of the [Legendre symbol](/legendre-symbol/), $\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod p$. So quadratic residuosity modulo a prime costs one [modular exponentiation](/modular-exponentiation/), $O(\log p)$ multiplications modulo $p$. The criterion gives the multiplicativity of the Legendre symbol, the rule for $-1$, the square root formula for $p \equiv 3 \pmod 4$, and the congruence that the [Solovay-Strassen](/solovay-strassen/) test checks with the [Jacobi symbol](/jacobi-symbol/). Root finding by [Tonelli-Shanks](/tonelli-shanks/) and [Cipolla's algorithm](/cipolla-algorithm/) uses it to find a nonresidue.

## Statement

Let $p$ be an odd prime and $a$ an integer. The **Legendre symbol** is
$$\left(\frac{a}{p}\right) = \begin{cases} 0 & \text{if } p \mid a, \\ 1 & \text{if } p \nmid a \text{ and } a \equiv x^2 \pmod p \text{ for some } x, \\ -1 & \text{otherwise.} \end{cases}$$

**Theorem (Euler's criterion).** For every odd prime $p$ and every integer $a$,
$$a^{(p-1)/2} \equiv \left(\frac{a}{p}\right) \pmod p.$$

Equivalently, for $p \nmid a$: $a^{(p-1)/2} \equiv \pm 1 \pmod p$, and $a^{(p-1)/2} \equiv 1$ if and only if $a$ is a quadratic residue modulo $p$ (Shoup, Theorem 2.21).

## In plain words

Fix an odd prime. Take a number that the prime does not divide, and raise it to the power "half of one less than the prime". Keep only the remainder. The result is always one of two values: one, or one less than the prime, which stands for minus one.

The result is one exactly when the number is a perfect square on the clock of that prime, and minus one exactly when it is not. So a single power, which a computer finds quickly even for huge primes, tells squares from non-squares. You do not need to search for a square root.

## Proof

Let $p$ be an odd prime. If $p \mid a$, both sides are $0$ modulo $p$, since $(p-1)/2 \ge 1$. Assume from now on that $p \nmid a$, and let $b = a^{(p-1)/2}$.

**Step 1: $b \equiv \pm 1$.** By [Fermat's little theorem](/fermat-little-theorem/), $b^2 = a^{p-1} \equiv 1 \pmod p$, so $p \mid (b - 1)(b + 1)$. Since $p$ is prime, $p \mid b - 1$ or $p \mid b + 1$.

**Step 2: residues give $1$.** If $a \equiv x^2$, then $p \nmid x$ and $b \equiv x^{p-1} \equiv 1$ by Fermat's little theorem.

**Step 3: there are exactly $(p-1)/2$ residues.** For $x, y \not\equiv 0$, $x^2 \equiv y^2$ means $p \mid (x - y)(x + y)$, so $y \equiv \pm x$. Since $p$ is odd, $x \not\equiv -x$. So the squaring map on the $p - 1$ nonzero residues is two-to-one, and its image, the set of quadratic residues, has $(p - 1)/2$ elements.

**Step 4: nonresidues give $-1$.** A nonzero polynomial of degree $d$ over the field $\mathbb{Z}/p\mathbb{Z}$ has at most $d$ roots: if $r$ is a root, then $f(X) = (X - r) g(X)$ with $\deg g = d - 1$, and any other root $s$ satisfies $(s - r) g(s) \equiv 0$ with $s - r \not\equiv 0$, so it is a root of $g$; induction on $d$ finishes the argument. The polynomial $X^{(p-1)/2} - 1$ has degree $(p - 1)/2$, and by Steps 2 and 3 its roots include all $(p - 1)/2$ quadratic residues. So it has no other root, and a nonresidue $a$ has $b \not\equiv 1$. By Step 1, $b \equiv -1$. $\blacksquare$

**A second proof, with Wilson's theorem.** Let $p \nmid a$. For each $x \in \{1, \ldots, p - 1\}$ there is a unique $y$ in the same set with $xy \equiv a$. If $a$ is a nonresidue, then $x \ne y$ always, so the $p - 1$ numbers split into $(p - 1)/2$ pairs with product $a$, and $(p - 1)! \equiv a^{(p-1)/2}$. If $a$ is a residue with square roots $\pm x_0$, these two are paired with themselves, the other $p - 3$ numbers form $(p - 3)/2$ pairs, and $(p - 1)! \equiv a^{(p-3)/2} \cdot x_0 \cdot (-x_0) \equiv -a^{(p-1)/2}$. By [Wilson's theorem](/wilson-theorem/), $(p - 1)! \equiv -1$, which gives $a^{(p-1)/2} \equiv -1$ and $a^{(p-1)/2} \equiv 1$ in the two cases. $\blacksquare$

## Consequences

- **Multiplicativity.** $\left(\frac{ab}{p}\right) = \left(\frac{a}{p}\right)\left(\frac{b}{p}\right)$, because $(ab)^{(p-1)/2} = a^{(p-1)/2} b^{(p-1)/2}$ and two values in $\{-1, 0, 1\}$ that agree modulo $p \ge 3$ are equal. So a residue times a nonresidue is a nonresidue, and two nonresidues multiply to a residue.
- **The rule for $-1$.** $\left(\frac{-1}{p}\right) = (-1)^{(p-1)/2}$, so $-1$ is a square modulo $p$ if and only if $p \equiv 1 \pmod 4$ (Shoup, Theorem 2.31). For $p \equiv 1 \pmod 4$ and any nonresidue $g$, $g^{(p-1)/4}$ is a square root of $-1$ (Shoup, Theorem 2.32).
- **Fast test.** Deciding whether $a$ is a square modulo $p$ takes one exponentiation with $O(\log p)$ multiplications modulo $p$, so $O(\log^3 p)$ bit operations with schoolbook arithmetic. The [Jacobi symbol](/jacobi-symbol/) algorithm, based on [quadratic reciprocity](/quadratic-reciprocity/), does the same test in $O(\log^2 p)$ bit operations.
- **Square roots for $p \equiv 3 \pmod 4$.** If $a$ is a residue, $x = a^{(p+1)/4}$ satisfies $x^2 = a^{(p+1)/2} = a \cdot a^{(p-1)/2} \equiv a$. This is the simple case of [modular square roots](/modular-square-root/).
- **Finding a nonresidue.** Half of the nonzero residues are nonresidues, so random choices find one after $2$ trials on average, each checked by the criterion (HAC, Remark 2.151). No deterministic polynomial time method is known without unproved hypotheses. Tonelli-Shanks and Cipolla's algorithm both need such a nonresidue.
- **Primality tests.** For an odd composite $n$, the congruence $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ with the Jacobi symbol fails for at least half of the units $a$. The [Solovay-Strassen](/solovay-strassen/) test checks it for random $a$. A [primitive root](/primitive-root/) modulo $p$ is always a nonresidue, since its power $(p-1)/2$ is not $1$.

## Tightness

- **The modulus must be prime.** Modulo $15$, $4 = 2^2$ is a square, but $4^{7} \equiv 4 \pmod{15}$, which is neither $1$ nor $-1$.
- **Composite numbers can pass.** $341 = 11 \cdot 31$ satisfies $2^{170} \equiv 1 \pmod{341}$, so the weak form "$a^{(n-1)/2} \equiv \pm 1$" holds for $a = 2$. The Jacobi form rejects $341$, because $\left(\frac{2}{341}\right) = -1$. The Carmichael number $561 = 3 \cdot 11 \cdot 17$ satisfies even the Jacobi form for $a = 2$: $2^{280} \equiv 1$ and $\left(\frac{2}{561}\right) = 1$. It is the smallest odd composite number that does.
- **The prime $2$.** The exponent $(p-1)/2$ is not an integer for $p = 2$, and every integer is a square modulo $2$, so the statement excludes $p = 2$.
- **Existence, not a root.** The criterion decides whether a square root exists, but it does not find one; for $p \equiv 1 \pmod 4$ a root needs Tonelli-Shanks or Cipolla's algorithm.

## History

Euler stated the criterion in a paper of 1748 (Wikipedia). Gauss proved it in the *Disquisitiones Arithmeticae* of 1801, Article 106. The notation $\left(\frac{a}{p}\right)$ is due to Legendre, who used it in his work on quadratic reciprocity; in this notation the criterion takes the short form above. Later, Solovay and Strassen turned its extension with the Jacobi symbol into a randomized primality test.

## References
