---
tag: EJCXJ0
kind: definition
slug: euler-jacobi-pseudoprime
name: Euler-Jacobi pseudoprime
aliases:
- Euler pseudoprime
- Euler-Jacobi probable prime
area: number-theory/primality
level: core
summary: Odd composite n with a^((n-1)/2) ≡ (a/n) (mod n) for a base a coprime to n, with the Jacobi symbol (a/n); it passes the Solovay-Strassen test with the base a.
prereqs: [jacobi-symbol, euler-criterion, fermat-pseudoprime]
see_also: [solovay-strassen, fermat-pseudoprime, strong-pseudoprime, carmichael-number, compositeness-witness, jacobi-symbol, euler-criterion, pseudoprime]
sources:
  - paper: doi:10.1137/0206006
    title: Robert Solovay and Volker Strassen, A fast Monte-Carlo test for primality, SIAM Journal on Computing 6 (1977)
    locator: pages 84 to 85 (at most half of the bases are liars)
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026 (Euler and strong pseudoprimes, and the implication strong implies Euler-Jacobi)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5, Probable primes and witnesses (Euler pseudoprimes and their relation to strong pseudoprimes)
---

An Euler-Jacobi pseudoprime to the base $a$ is an odd composite number $n$ that satisfies the congruence $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, with the [Jacobi symbol](/jacobi-symbol/) on the right. Every odd [prime](/prime-number/) satisfies it by [Euler's criterion](/euler-criterion/), so such an $n$ fools the [Solovay-Strassen test](/solovay-strassen/) with the base $a$. The condition is stronger than the [Fermat](/fermat-pseudoprime/) one, and unlike for Fermat's test no composite fools it for all bases: at most half of the bases coprime to $n$ are liars. The smallest Euler-Jacobi pseudoprime to the base 2 is $561$.

## Definition

Let $n \ge 3$ be odd and composite, and let $a$ be an integer with $\gcd(a, n) = 1$. Then $n$ is an **Euler-Jacobi pseudoprime to the base $a$** if

$$a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n,$$

where $\left(\frac{a}{n}\right) \in \{1, -1\}$ is the Jacobi symbol. The base $a$ is then an **Euler liar** for $n$; a base coprime to $n$ that breaks the congruence is an **Euler witness**. An odd number, prime or composite, that satisfies the congruence is an *Euler-Jacobi probable prime* to the base $a$.

**Why primes pass.** For an odd prime $p$ and $p \nmid a$, Euler's criterion says $a^{(p-1)/2} \equiv \left(\frac{a}{p}\right) \pmod p$, and the Jacobi symbol modulo a prime is the [Legendre symbol](/legendre-symbol/).

**A weaker notion with the same name.** Some authors call a composite $n$ an *Euler pseudoprime* to the base $a$ when only $a^{(n-1)/2} \equiv \pm 1 \pmod n$, without matching the sign to the Jacobi symbol. This is weaker: $341 = 11 \cdot 31$ has $2^{170} \equiv 1 \pmod{341}$, but $\left(\frac{2}{341}\right) = -1$ since $341 \equiv 5 \pmod 8$. So 341 is an Euler pseudoprime to the base 2 in the weak sense, but not an Euler-Jacobi pseudoprime. On this page "Euler pseudoprime" means the Jacobi form.

**The liars form a subgroup of at most half the units.** Let $E(n)$ be the set of Euler liars in $(\mathbb{Z}/n\mathbb{Z})^*$. Since both sides of the congruence are multiplicative in $a$, $E(n)$ is closed under products and is a subgroup. It is a proper subgroup, so by [Lagrange's theorem](/lagranges-theorem-group-theory/) $|E(n)| \le \varphi(n)/2$.

*Proof that $E(n)$ is proper.* If $p^2 \mid n$ for a prime $p$, then each Euler liar is a Fermat liar (square both sides), and the number of Fermat liars is $\prod_i \gcd(n - 1, p_i - 1)$, which divides $\prod_i (p_i - 1)$ and so is at most $\varphi(n)/p < \varphi(n)$ (see the [Fermat test](/fermat-primality-test/)). Otherwise $n = pm$ with $p$ prime, $p \nmid m$ and $m \ge 3$. Take a quadratic non-residue $b$ modulo $p$, and by the [Chinese remainder theorem](/chinese-remainder-theorem/) an $a$ with $a \equiv b \pmod p$ and $a \equiv 1 \pmod m$. Then $\left(\frac{a}{n}\right) = \left(\frac{b}{p}\right)\left(\frac{1}{m}\right) = -1$, while $a^{(n-1)/2} \equiv 1 \pmod m$. If $a$ were a liar, $a^{(n-1)/2} \equiv -1 \pmod n$, and so $1 \equiv -1 \pmod m$, which fails for $m \ge 3$. $\square$

**Place among the other pseudoprimes.** For a base $a$ coprime to an odd composite $n$:

- Each Euler-Jacobi pseudoprime to the base $a$ is a Fermat pseudoprime to the base $a$, by squaring the congruence.
- Each [strong pseudoprime](/strong-pseudoprime/) to the base $a$ is an Euler-Jacobi pseudoprime to the base $a$ (Pomerance, Selfridge and Wagstaff 1980).
- If $n \equiv 3 \pmod 4$, the two notions agree: $n$ is an Euler-Jacobi pseudoprime to the base $a$ if and only if it is a strong pseudoprime to the base $a$.

## Examples and non-examples

**Examples.**

- $561 = 3 \cdot 11 \cdot 17$ is the smallest Euler-Jacobi pseudoprime to the base 2: $2^{280} \equiv 1 \pmod{561}$, and $\left(\frac{2}{561}\right) = 1$ since $561 \equiv 1 \pmod 8$.
- The smallest ones to the bases 2, 3, 5, 7 are $561$, $121$, $781$ and $25$.
- $1729 = 7 \cdot 13 \cdot 19$ is an Euler-Jacobi pseudoprime to the bases 2, 3 and 5. It has exactly $648 = \varphi(1729)/2$ Euler liars, so the bound $\varphi(n)/2$ is attained. The Carmichael number $15841$ attains it too.
- $2047 = 23 \cdot 89$ is a strong pseudoprime to the base 2, and so an Euler-Jacobi pseudoprime to the base 2.

**Non-examples.**

- $341$, as above: a Fermat pseudoprime to the base 2, but the sign is wrong.
- Carmichael numbers in general: $561$ has $80$ Euler liars among its $320$ units, so most bases expose it, although every unit is a Fermat liar.
- No odd composite is an Euler-Jacobi pseudoprime to every base coprime to it; there is no analogue of a [Carmichael number](/carmichael-number/) for this test.

**How many there are.** Below $10^3, 10^4, 10^5, 10^6$ there are $1, 12, 36, 114$ Euler-Jacobi pseudoprimes to the base 2. For comparison, there are $245$ Fermat pseudoprimes and $46$ strong pseudoprimes to the base 2 below $10^6$.

## Related definitions

- [Solovay-Strassen test](/solovay-strassen/): the randomized test that checks the congruence for random bases; its error is at most $1/2$ per base by the subgroup bound above.
- [Fermat pseudoprime](/fermat-pseudoprime/): the weaker condition $a^{n-1} \equiv 1 \pmod n$.
- [Strong pseudoprime](/strong-pseudoprime/): the stronger condition behind [Miller-Rabin](/miller-rabin/), with at most $\varphi(n)/4$ liars for $n > 9$.
- [Euler's criterion](/euler-criterion/) and the [Jacobi symbol](/jacobi-symbol/): the facts the definition rests on. The Jacobi symbol is computed in $O((\log n)^2)$ bit operations with quadratic reciprocity and no factoring.
- [Compositeness witness](/compositeness-witness/): an Euler witness is one kind.
- [Pseudoprime](/pseudoprime/): the general term.

## References
