---
tag: MAND5E
kind: technique
slug: congruence-of-squares
name: Congruence of squares
aliases:
- Kraitchik's method
- x^2 ≡ y^2 mod n
area: number-theory/factorization
level: core
summary: Find x and y with x^2 ≡ y^2 (mod N) but x ≢ ±y (mod N). Then gcd(x - y, N) is a proper factor of N. Most fast factoring methods build such a pair.
prereqs: [congruence, gcd-of-two-integers, chinese-remainder-theorem, quadratic-residue]
see_also: [fermat-factorization, dixon-random-squares, quadratic-sieve, continued-fraction-factorization, general-number-field-sieve, relation-collection, smooth-number, nontrivial-square-root-of-one]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.1.1, Basic QS, pages 261 to 266 (the reduction to x^2 ≡ y^2 with x ≢ ±y, and the example n = 1649)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (Fermat's method, Kraitchik's improvement and the combination of congruences by linear algebra)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 15.3, An algorithm for factoring integers (a congruence of squares from smooth relations, with a proof that it splits N with probability at least 1/2)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.4, Factoring into primes (factoring via continued fractions, which combines congruences x^2 ≡ (-1)^e p_1^(e_1) ... (mod N))
---

A congruence of squares is a pair of integers $x, y$ with $x^2 \equiv y^2 \pmod N$ and $x \not\equiv \pm y \pmod N$. From such a pair, one [gcd](/gcd-of-two-integers/) computation gives a proper factor $\gcd(x - y, N)$ of $N$. The technique is to build the pair as a product of many small congruences $x_i^2 \equiv a_i \pmod N$ whose right sides $a_i$ are [smooth](/smooth-number/), and to pick the product by linear algebra over the field with two elements. [Dixon's method](/dixon-random-squares/), [CFRAC](/continued-fraction-factorization/), the [quadratic sieve](/quadratic-sieve/) and the [number field sieve](/general-number-field-sieve/) are all instances, so this one idea is behind every subexponential factoring method in use.

## In plain words

If two numbers have the same square, modulo the number you want to factor, they need not be equal or opposite. When they are not, their difference shares a factor with the number, but not all of it. A gcd computation then pulls this factor out.

Such pairs are hard to find directly. So you collect many easy facts of the form "this square leaves this small remainder", where each remainder has only small prime factors. Each remainder is a short list of exponents. When the exponents of a group of remainders add up to even numbers, the product of the remainders is a perfect square. Finding such a group is a problem of solving equations with only zeros and ones, which a computer does fast.

## When it applies

- $N$ is odd, composite and not a prime power. For a prime power $N = p^k$ with $p$ odd, each $x$ coprime to $N$ has only the two square roots $\pm x$, so no useful pair exists; test for prime powers first.
- You can produce many congruences $x_i^2 \equiv a_i \pmod N$ with $|a_i|$ much smaller than $N$, so that a fair fraction of the $a_i$ factor over a small set of primes. The smaller the $a_i$, the faster the method.
- The factors of $N$ have no special structure to exploit. For small factors, [trial division](/trial-division/), [Pollard's rho](/pollard-rho/) and the [elliptic curve method](/elliptic-curve-factorization/) are faster, because the cost of a congruence of squares depends on $N$, not on its smallest factor.

## The template

**Lemma 1 (the split).** Let $x^2 \equiv y^2 \pmod N$ and $x \not\equiv \pm y \pmod N$. Then $d = \gcd(x - y, N)$ satisfies $1 < d < N$.

*Proof.* $N$ divides $x^2 - y^2 = (x - y)(x + y)$. If $d = N$, then $N \mid x - y$, so $x \equiv y$, a contradiction. If $d = 1$, then $N$ and $x - y$ are coprime, so by [Euclid's lemma](/euclids-lemma/) $N \mid x + y$, so $x \equiv -y$, again a contradiction. $\square$

**Lemma 2 (most pairs split).** Let $N$ be odd with $r \ge 2$ distinct prime factors, and let $x$ be coprime to $N$. Then $x^2$ has exactly $2^r$ square roots modulo $N$, and only two of them are $\pm x$. So if $y$ is a root of $x^2$ that does not depend on which of the $2^r$ roots $x$ is, the pair splits $N$ with probability $1 - 2^{1-r} \ge 1/2$.

*Proof.* Write $N = \prod_{i=1}^{r} q_i^{e_i}$. For an odd prime power $q^e$ and $x$ coprime to $q$, the group of units modulo $q^e$ is [cyclic](/cyclic-group/) of even order, so $z^2 \equiv x^2$ has exactly the two solutions $z \equiv \pm x \pmod{q^e}$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), a root modulo $N$ is a free choice of sign for each $i$, which gives $2^r$ roots. Exactly two choices, all signs equal, give $\pm x$. If $x$ is uniform among the $2^r$ roots and independent of $y$, the probability that $x \equiv \pm y$ is $2 / 2^r$. $\square$

The template builds $y$ from data that does not reveal which root $x$ is.

```pseudo id=main
CONGRUENCE-OF-SQUARES(N)                   ▷ N odd, composite, not a prime power
L1  B ← a smoothness bound; P ← the primes p ≤ B, plus −1   ▷ hole: the factor base
L2  R ← empty list
L3  while |R| ≤ |P| do
L4      produce x with a ≡ x² (mod N) and |a| small        ▷ hole: the source of relations
L5      if a factors over P then append (x, a, the exponent vector of a) to R
L6  for each nonempty S ⊆ R whose exponent vectors add to 0 modulo 2 do   ▷ hole: GF(2) solver
L7      X ← ∏_{i ∈ S} x_i mod N
L8      Y ← ∏_{p ∈ P} p^{(Σ_{i ∈ S} e_{i,p}) / 2} mod N
L9      d ← gcd(X − Y, N)
L10     if 1 < d < N then return d
L11 go to L2 with more or other relations
```

**Walk-through.** Lines L1 to L5 are [relation collection](/relation-collection/): each relation $x_i^2 \equiv a_i$ with $a_i = \prod_{p \in P} p^{e_{i,p}}$ (the prime $-1$ records the sign) is stored with its exponent vector modulo 2. Once there are more relations than primes in $P$, the vectors are linearly dependent over $\mathrm{GF}(2)$, so line L6 finds at least one nonempty set $S$ whose vectors add to zero; [Gaussian elimination over GF(2)](/xor-gaussian-elimination/) gives a basis of all such sets. For each $S$, every exponent $\sum_{i \in S} e_{i,p}$ is even, so $\prod_{i \in S} a_i = Y^2$ with the $Y$ of line L8, and $X^2 = \prod x_i^2 \equiv \prod a_i = Y^2 \pmod N$. Lemma 1 turns a pair with $X \not\equiv \pm Y$ into a factor at line L10. With $k$ independent dependencies, the chance that all of them fail is about $2^{-k}$ under the heuristic of Lemma 2.

**The holes.** The factor base $P$ and the bound $B$; the way to produce small squares modulo $N$ (line L4); the test for smoothness (trial division or a sieve); and the linear algebra (dense elimination, or [block Lanczos](/block-lanczos-algorithm/) and [block Wiedemann](/block-wiedemann-algorithm/) for large sparse systems).

**Example.** $N = 1649 = 17 \cdot 97$. Near $\sqrt{N} \approx 40.6$:

| $x$ | $x^2 \bmod 1649$ | factorization |
|---|---|---|
| 41 | 32 | $2^5$ |
| 42 | 115 | $5 \cdot 23$ |
| 43 | 200 | $2^3 \cdot 5^2$ |

Neither 32 nor 200 is a square, but $32 \cdot 200 = 6400 = 80^2$: the exponent vectors $(5, 0)$ and $(3, 2)$ over the primes $(2, 5)$ add to $(8, 2)$, which is even. So $(41 \cdot 43)^2 \equiv 80^2 \pmod{1649}$. Here $41 \cdot 43 = 1763 \equiv 114$, and $114 \not\equiv \pm 80$. Then $\gcd(114 - 80, 1649) = \gcd(34, 1649) = 17$, and $1649 = 17 \cdot 97$.

## Classic examples

- **[Fermat's method](/fermat-factorization/).** Look for $x$ with $x^2 - N$ a perfect square $y^2$. Then $N = (x - y)(x + y)$ exactly. This is the case $|S| = 1$, with $a = x^2 - N$ itself a square; it is fast only when the factors are close.
- **[Dixon's random squares](/dixon-random-squares/).** Take $x$ at random and $a = x^2 \bmod N$. The randomness makes Lemma 2 a theorem, and the expected time is proved to be subexponential.
- **[Continued fraction factorization](/continued-fraction-factorization/).** The convergents $P_k / Q_k$ of $\sqrt{N}$ give $P_k^2 \equiv \pm r$ with $r < 2\sqrt{N}$, so the residues are much smaller than in Dixon's method.
- **[Quadratic sieve](/quadratic-sieve/) and [MPQS](/multiple-polynomial-quadratic-sieve/).** Take $a = (\lceil \sqrt{N} \rceil + t)^2 - N$ for small $t$, and find the smooth values with a sieve instead of trial division.
- **[Number field sieve](/general-number-field-sieve/).** The squares live in two rings, $\mathbb{Z}$ and $\mathbb{Z}[\alpha]$, joined by a ring map to $\mathbb{Z}/N\mathbb{Z}$. The relations are pairs $(a, b)$ with $a - bm$ and $a - b\alpha$ both smooth.
- **[SQUFOF](/shanks-squfof/).** A square form in the cycle of reduced binary quadratic forms of discriminant $4N$ gives a congruence of squares directly.
- **Factoring from square roots of one.** A [nontrivial square root of one](/nontrivial-square-root-of-one/) $b$ is the pair $x = b$, $y = 1$. [Miller-Rabin](/miller-rabin/) finds one when $N$ is a Carmichael number, and [Shor's algorithm](/shor-algorithm/) gets one from the order of a random element.

## Variations

- **Allow a sign.** Put $-1$ in the factor base, so that negative residues $a_i$ can be used. CFRAC and the quadratic sieve both need this.
- **Large primes.** Keep relations with one or two primes larger than $B$. Two such relations with the same large prime multiply to a relation over $P$ times a square. This raises the yield of each sieve run.
- **A multiplier.** Factor $kN$ instead of $N$ for a small $k$ chosen so that many small primes are [quadratic residues](/quadratic-residue/) modulo $kN$; this is the [Knuth-Schroeppel multiplier](/knuth-schroeppel-multiplier/). A factor of $kN$ gives a factor of $N$ after removing the factors of $k$.
- **Rings other than $\mathbb{Z}$.** The number field sieve, and the [index calculus](/index-calculus/) for discrete logarithms, use the same collect-and-combine plan with a [factor base](/factor-base/) in another ring.

## Pitfalls

- **Prime powers and even numbers.** For $N = p^k$ the only roots of $x^2$ are $\pm x$, so every pair is trivial and the method loops forever. Remove the factors $2$, test for a perfect power (by an integer $k$-th root for each $k \le \lg N$) and test for primality before line L1.
- **A factor base prime divides $N$.** Methods that choose $P$ by the condition that $N$ is a quadratic residue modulo $p$ skip each $p$ that divides $N$, because the [Legendre symbol](/legendre-symbol/) is then $0$, and so they never see this factor. Check $\gcd(p, N)$ for each small prime in line L1; a hit is already a factor and ends the work.
- **Computing $Y$ wrongly.** Line L8 must take the square root of the product as an exact integer, by halving the summed exponents. Taking a modular square root of $\prod a_i \bmod N$ instead would need the factorization of $N$.
- **Only one dependency.** A single dependency fails with probability about $1/2$. Keep a few more relations than primes, so that the solver returns ten or more independent dependencies, and try each one.
- **Forgetting the condition $x \not\equiv \pm y$.** A pair with $x \equiv \pm y$ gives $\gcd = N$ or $1$. This is not an error in the program, only a dependency that failed; move on to the next one.

## Exercises

1. For $N = 1649$, the relation $42^2 \equiv 115 = 5 \cdot 23$ cannot be used with the two others above. Explain why from the exponent vectors.
2. Let $N = 15$. List all $x \in [0, 14]$ coprime to $15$ with $x^2 \equiv 1$, and check Lemma 2 for $r = 2$.
3. Show that for $N = p^k$ with $p$ an odd prime and $\gcd(x, N) = 1$, the congruence $z^2 \equiv x^2 \pmod N$ has exactly the two solutions $\pm x$.
4. Show that for $N = 2^k$ with $k \ge 3$ an odd $x^2$ has four square roots, and explain why the template still does not help to factor powers of two.
5. Find a congruence of squares for $N = 2041$ from the residues of $x^2 - N$ for $x = 46, \dots, 51$, and use it to factor $N$.

## References
