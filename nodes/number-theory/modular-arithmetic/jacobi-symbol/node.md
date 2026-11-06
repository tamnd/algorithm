---
tag: QGNGA4
kind: concept
slug: jacobi-symbol
name: Jacobi symbol
aliases:
- Kronecker symbol
area: number-theory/modular-arithmetic
level: advanced
summary: Generalizes the Legendre symbol to odd composite moduli, computable without factoring.
prereqs: [legendre-symbol, quadratic-reciprocity]
see_also: [euler-criterion, quadratic-residue, solovay-strassen, baillie-psw, quadratic-residuosity-problem, goldwasser-micali-cryptosystem, euclidean-algorithm, half-gcd]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.5, Definition 2.147, Fact 2.148 (properties of the Jacobi symbol), Algorithm 2.149, Fact 2.150 (O((lg n)^2) bit operations), Example 2.152 ((158/235) = -1) and Example 2.153 (Z_21^*)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Chapter 12, Sections 12.2 (The Jacobi symbol), 12.3 (Computing the Jacobi symbol) and 12.6 (The quadratic residuosity assumption)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer, Graduate Texts in Mathematics 138
    locator: Section 1.4.2, The Legendre-Jacobi-Kronecker symbol (the definition for all integers n and the algorithm for the Kronecker symbol)
  - url: https://arxiv.org/abs/1004.2091
    title: Richard P. Brent and Paul Zimmermann, An O(M(n) log n) algorithm for the Jacobi symbol, ANTS-IX, Lecture Notes in Computer Science 6197, 2010, pages 83 to 95
    locator: abstract and introduction (subquadratic algorithms based on fast gcd)
  - url: https://en.wikipedia.org/wiki/Jacobi_symbol
    title: Jacobi symbol, Wikipedia
    locator: lead (introduced by Jacobi in 1837) and sections Calculating the Jacobi symbol and Primality testing
  - url: https://en.wikipedia.org/wiki/Kronecker_symbol
    title: Kronecker symbol, Wikipedia
    locator: sections Definition (the values for n = 2, n = -1 and n = 0) and Properties
---

The **Jacobi symbol** $\left(\frac{a}{n}\right)$ extends the [Legendre symbol](/legendre-symbol/) from an odd prime $p$ to any odd positive $n$: it is the product of the Legendre symbols for the prime factors of $n$, with multiplicity. It keeps the rules of [quadratic reciprocity](/quadratic-reciprocity/), and these rules compute it in $O(\log^2 n)$ bit operations by a loop like the [Euclidean algorithm](/euclidean-algorithm/), without the factorization of $n$. The price is meaning: modulo a prime, the symbol says whether $a$ is a square, but modulo a composite $n$, the value $1$ does not imply that $a$ is a square. Both sides of this trade-off are used: the [Solovay-Strassen](/solovay-strassen/) and [Baillie-PSW](/baillie-psw/) tests use the symbol, and the [quadratic residuosity problem](/quadratic-residuosity-problem/) rests on the gap. The **Kronecker symbol** extends the definition further to every integer $n$.

## In plain words

For a prime clock size, the Legendre symbol is plus one for the squares and minus one for the non-squares. The Jacobi symbol takes a clock size that is any odd number, splits it into its prime factors, and multiplies the Legendre answers for these primes.

The surprise is that you do not need to find the prime factors. The symbol obeys a few flip rules, much like the steps of the Euclidean algorithm for the greatest common divisor. These rules swap the two numbers and shrink them, and they track a sign. The result comes out in a few steps even for numbers with hundreds of digits.

The answer minus one proves that a number is not a square. The answer plus one does not prove that it is one.

## The idea

**Definition.** Let $n \ge 1$ be odd with prime factorization $n = p_1^{e_1} \cdots p_k^{e_k}$. For an integer $a$,
$$\left(\frac{a}{n}\right) = \left(\frac{a}{p_1}\right)^{e_1} \cdots \left(\frac{a}{p_k}\right)^{e_k},$$
with the Legendre symbols on the right, and $\left(\frac{a}{1}\right) = 1$. For prime $n$ it is the Legendre symbol (HAC, Definition 2.147). Jacobi introduced the symbol in 1837.

**Properties.** For odd $m, n \ge 1$ and integers $a, b$ (HAC, Fact 2.148):

1. $\left(\frac{a}{n}\right) \in \{-1, 0, 1\}$, and it is $0$ exactly when $\gcd(a, n) > 1$.
2. It is multiplicative in each argument: $\left(\frac{ab}{n}\right) = \left(\frac{a}{n}\right)\left(\frac{b}{n}\right)$ and $\left(\frac{a}{mn}\right) = \left(\frac{a}{m}\right)\left(\frac{a}{n}\right)$.
3. It depends only on $a \bmod n$.
4. $\left(\frac{-1}{n}\right) = (-1)^{(n-1)/2}$ and $\left(\frac{2}{n}\right) = (-1)^{(n^2-1)/8}$, which is $1$ for $n \equiv \pm 1 \pmod 8$ and $-1$ for $n \equiv \pm 3 \pmod 8$.
5. *Reciprocity.* $\left(\frac{m}{n}\right) = \left(\frac{n}{m}\right)$, unless $m \equiv n \equiv 3 \pmod 4$, when $\left(\frac{m}{n}\right) = -\left(\frac{n}{m}\right)$.

Rules 4 and 5 hold for composite $m$ and $n$ because they hold for primes and both sides are multiplicative.

**Computation.** Rules 2 to 5 give a loop on a pair $(a, n)$ with $n$ odd and a sign $t$, starting with $a \bmod n$ and $t = 1$:

1. While $a$ is even, divide $a$ by $2$, and flip $t$ if $n \equiv 3$ or $5 \pmod 8$ (rule 4).
2. Swap $a$ and $n$; flip $t$ if both are $\equiv 3 \pmod 4$ (rule 5). Replace $a$ by $a \bmod n$ (rule 3).
3. Repeat until $a = 0$. The result is $t$ if $n = 1$ at the end, and $0$ otherwise (then $\gcd(a, n) = n > 1$).

The pairs follow the remainders of the Euclidean algorithm on $(a, n)$, with the factors $2$ removed, so the loop has $O(\log n)$ rounds and takes $O(\log^2 n)$ bit operations with schoolbook division (HAC, Fact 2.150), the cost of a gcd. Algorithms based on fast gcd, such as the [half-gcd](/half-gcd/) and binary recursive gcd, compute it in $O(M(d) \log d)$ bit operations for numbers of $d$ binary digits, where $M(d)$ is the cost of a $d$-digit multiplication (Brent and Zimmermann). Unlike Euler's power $a^{(n-1)/2}$, which takes $O(\log^3 n)$ with schoolbook arithmetic, the loop needs no exponentiation.

**What the value means.** If $a \equiv x^2 \pmod n$ with $\gcd(a, n) = 1$, then $a$ is a square modulo every $p_i$, so $\left(\frac{a}{n}\right) = 1$. The converse fails: $\left(\frac{a}{n}\right) = 1$ can come from an even number of factors $-1$. For $n = pq$ with distinct odd primes, half of the units have symbol $1$, and only half of those, a quarter of all units, are squares. Deciding which of them are squares without the factors of $n$ is the quadratic residuosity problem.

**The Kronecker symbol.** Kronecker (1885) extended the symbol to every integer $n$, by complete multiplicativity in $n$ and three extra values (Cohen, Section 1.4.2): $\left(\frac{a}{2}\right)$ is $0$ for even $a$, $1$ for $a \equiv \pm 1 \pmod 8$ and $-1$ for $a \equiv \pm 3 \pmod 8$; $\left(\frac{a}{-1}\right)$ is $-1$ for $a < 0$ and $1$ for $a \ge 0$; and $\left(\frac{a}{0}\right)$ is $1$ for $a = \pm 1$ and $0$ otherwise. For a fixed discriminant $D$, the map $n \mapsto \left(\frac{D}{n}\right)$ is a character, used for quadratic fields and binary quadratic forms.

## Examples

- **Symbol $1$ without a square.** $\left(\frac{2}{15}\right) = \left(\frac{2}{3}\right)\left(\frac{2}{5}\right) = (-1)(-1) = 1$, but the squares of the units modulo $15$ are only $1$ and $4$.
- **The group $\mathbb{Z}_{21}^*$.** Of the $12$ units modulo $21$, the six with symbol $1$ are $1, 4, 5, 16, 17, 20$, and the three squares are $1, 4, 16$ (HAC, Example 2.153).
- **Against Euler's power.** For $n = 21$ and $a = 8$, $\left(\frac{8}{21}\right) = -1$ but $8^{10} \equiv 1 \pmod{21}$, so $a = 8$ shows that $21$ is composite.
- **Kronecker symbol.** $\left(\frac{-4}{n}\right)$ is $1$ for $n \equiv 1 \pmod 4$, $-1$ for $n \equiv 3 \pmod 4$ and $0$ for even $n$. Also $\left(\frac{5}{2}\right) = -1$ and $\left(\frac{3}{-5}\right) = \left(\frac{3}{-1}\right)\left(\frac{3}{5}\right) = -1$.

**A computation.** $\left(\frac{158}{235}\right)$ with $235 = 5 \cdot 47$ (HAC, Example 2.152):

| step | pair $(a, n)$ | rule | sign $t$ |
|---|---|---|---|
| start | $(158, 235)$ | | $1$ |
| remove one factor $2$ | $(79, 235)$ | $235 \equiv 3 \pmod 8$: flip | $-1$ |
| swap and reduce | $(235 \bmod 79, 79) = (77, 79)$ | $79 \equiv 235 \equiv 3 \pmod 4$: flip | $1$ |
| swap and reduce | $(79 \bmod 77, 77) = (2, 77)$ | $77 \equiv 1 \pmod 4$: no flip | $1$ |
| remove one factor $2$ | $(1, 77)$ | $77 \equiv 5 \pmod 8$: flip | $-1$ |
| swap and reduce | $(0, 1)$ | $77 \equiv 1 \pmod 4$: no flip | $-1$ |

So $\left(\frac{158}{235}\right) = -1$, and $158$ is not a square modulo $235$.

## Where it is used

- **Primality testing.** The [Solovay-Strassen](/solovay-strassen/) test checks [Euler's criterion](/euler-criterion/) $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ for random $a$. The [Baillie-PSW](/baillie-psw/) test and the [Lucas tests](/lucas-primality-test/) choose a parameter $D$ with $\left(\frac{D}{n}\right) = -1$.
- **Finding nonresidues.** Before [Tonelli-Shanks](/tonelli-shanks/) or [Cipolla's algorithm](/cipolla-algorithm/), a nonresidue modulo $p$ is found by random trials; the Jacobi loop checks each trial faster than Euler's power.
- **Cryptography.** The [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) encrypts a bit as a unit of symbol $1$ modulo $n = pq$ that is a square or not. Anyone can compute the symbol, but only the owner of $p$ and $q$ can tell the two cases apart. The [Blum Blum Shub](/blum-blum-shub/) generator works in the same group.
- **Algebraic number theory.** The Kronecker symbol $\left(\frac{D}{p}\right)$ tells how a prime $p$ splits in the quadratic field of discriminant $D$, and it enters the class number formula.

## References
