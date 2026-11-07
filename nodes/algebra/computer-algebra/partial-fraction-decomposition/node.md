---
tag: P053GE
kind: algorithm
slug: partial-fraction-decomposition
name: Partial fraction decomposition
aliases:
- partial fractions
- partial fraction expansion
area: algebra/computer-algebra
level: core
summary: Writes a rational function as a sum of simpler rational terms over factors of its denominator.
model: blum-shub-smale-machine
complexity:
  vars: {d: the degree of the denominator b, m: the degree of the numerator a}
  time: {worst: O(d^2 + m d)}
  space: {extra: O(d + m)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  note: The decomposition is classical; in computer algebra it is computed with the extended Euclidean algorithm, as in von zur Gathen and Gerhard, Section 5.11, and it is the first step of rational integration.
prereqs: [polynomial-extended-euclidean-algorithm, chinese-remainder-theorem, polynomial-long-division]
see_also: [integration-of-rational-functions, hermite-reduction, horowitz-ostrogradsky, rothstein-trager, square-free-factorization, polynomial-gcd]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.11, Partial fraction decomposition (existence, uniqueness and the algorithm by the extended Euclidean algorithm); Chapter 22, Symbolic integration (its use for rational functions)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 1 (algebraic preliminaries, the extended Euclidean algorithm and partial fractions) and Chapter 2, Sections 2.1 and 2.2 (partial fractions in the Bernoulli algorithm and in Hermite reduction)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of rational functions (partial fractions with respect to a square-free factorization)
---

A partial fraction decomposition writes a rational function $a/b$ over a field $K$ as a polynomial plus a sum of fractions $a_{ij}/b_i^j$, where $b = b_1^{e_1} \cdots b_k^{e_k}$ is a factorization of the denominator into pairwise coprime factors and each numerator has $\deg a_{ij} < \deg b_i$. The decomposition exists and is unique for any such factorization, irreducible or not. The algorithm uses one [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) per factor to split the fraction, the same computation as the [Chinese remainder theorem](/chinese-remainder-theorem/), and then a $b_i$-adic expansion to split each power. It costs $O(d^2)$ field operations for a denominator of degree $d$, and it is the first step of the [integration of rational functions](/integration-of-rational-functions/).

## In plain words

A fraction with a complicated bottom part is hard to work with. If the bottom part is a product of pieces that share no common factor, you can split the fraction into a sum of fractions with one piece each at the bottom. Each new top part is smaller than its bottom piece. When a piece appears to a power, you split it further into one fraction for each power. The splitting uses the same trick as solving a system of remainders with the Chinese remainder theorem: for each piece, find a multiplier that is one modulo that piece and zero modulo the others. The result is unique, so it is a normal form for the fraction.

## The problem

**Input.** A field $K$, a polynomial $a \in K[x]$, and a list $(b_1, e_1), \ldots, (b_k, e_k)$ with $b_i \in K[x]$ of degree at least $1$, $e_i \ge 1$, and $\gcd(b_i, b_j) = 1$ for $i \ne j$. Let $b = \prod_i b_i^{e_i}$ and $d = \deg b$.

**Output.** A polynomial $q$ and polynomials $a_{ij}$ for $1 \le i \le k$ and $1 \le j \le e_i$, with $\deg a_{ij} < \deg b_i$, such that

$$\frac{a}{b} = q + \sum_{i=1}^{k} \sum_{j=1}^{e_i} \frac{a_{ij}}{b_i^{\,j}}.$$

**Uniqueness.** The output is unique. The proof is in the proof file below.

Common choices of factorization are the irreducible factorization (the *complete* decomposition), the [square-free factorization](/square-free-factorization/) $b = \prod_i b_i^i$, used in [Hermite reduction](/hermite-reduction/), and the factorization into linear factors over a splitting field, which gives the residues at the poles.

## The algorithm

```pseudo id=main
PARTIAL-FRACTIONS(a, (b_1, e_1), ..., (b_k, e_k))
L1  b ← b_1^{e_1} · · · b_k^{e_k}
L2  (q, a) ← (a quo b, a rem b)                 ▷ now deg a < deg b
L3  for i ← 1 to k do
L4      c_i ← b / b_i^{e_i}                     ▷ exact division
L5      find s_i with s_i c_i ≡ 1 (mod b_i^{e_i})  ▷ extended Euclid on c_i and b_i^{e_i}
L6      r_i ← (a · s_i) rem b_i^{e_i}            ▷ a / b = Σ_i r_i / b_i^{e_i}
L7      for j ← e_i down to 1 do
L8          (r_i, a_{ij}) ← (r_i quo b_i, r_i rem b_i)
L9  return q, (a_{ij})
```

Lines L4 to L6 split the proper fraction $a/b$ into one fraction $r_i / b_i^{e_i}$ for each coprime factor. The cofactor $c_i$ is coprime to $b_i^{e_i}$ because the $b_j$ are pairwise coprime, so line L5 succeeds. Lines L7 and L8 write $r_i$ in base $b_i$: $r_i = \sum_{m=0}^{e_i - 1} \rho_m b_i^m$ with $\deg \rho_m < \deg b_i$, and then $r_i / b_i^{e_i} = \sum_m \rho_m / b_i^{e_i - m}$. The first digit $\rho_0$ is the numerator of the highest power, so the loop runs $j$ downward.

## Example

Decompose $\dfrac{x^5 + 2}{(x - 1)^2 (x^2 + 1)}$ over $\mathbb{Q}$, with $b_1 = x - 1$, $e_1 = 2$, $b_2 = x^2 + 1$, $e_2 = 1$.

| line | computation | result |
|---|---|---|
| L1 | $b = (x - 1)^2 (x^2 + 1)$ | $x^4 - 2x^3 + 2x^2 - 2x + 1$ |
| L2 | divide $x^5 + 2$ by $b$ | $q = x + 2$, $a = 2x^3 - 2x^2 + 3x$ |
| L4, $i = 1$ | $c_1 = b / (x - 1)^2$ | $x^2 + 1$ |
| L5, $i = 1$ | inverse of $c_1$ modulo $(x - 1)^2$ | $s_1 = 1 - x/2$ |
| L6, $i = 1$ | $a s_1 \bmod (x - 1)^2$ | $r_1 = x + \tfrac{1}{2}$ |
| L8, $j = 2$ | $r_1 = 1 \cdot (x - 1) + \tfrac{3}{2}$ | $a_{12} = \tfrac{3}{2}$, $r_1 = 1$ |
| L8, $j = 1$ | $r_1 = 0 \cdot (x - 1) + 1$ | $a_{11} = 1$ |
| L4, $i = 2$ | $c_2 = b / (x^2 + 1)$ | $(x - 1)^2 = x^2 - 2x + 1$ |
| L5, $i = 2$ | inverse of $c_2$ modulo $x^2 + 1$ | $s_2 = x/2$ |
| L6, $i = 2$ | $a s_2 \bmod (x^2 + 1)$ | $r_2 = x - \tfrac{1}{2}$ |
| L8, $j = 1$ | $r_2 \bmod (x^2 + 1)$ | $a_{21} = x - \tfrac{1}{2}$ |

So

$$\frac{x^5 + 2}{(x - 1)^2 (x^2 + 1)} = x + 2 + \frac{1}{x - 1} + \frac{3/2}{(x - 1)^2} + \frac{x - 1/2}{x^2 + 1}.$$

At $x = 0$ both sides are $2$, and at $x = 2$ both sides are $34/5$. The inverse $s_1$ is right because $(1 - x/2)(x^2 + 1) - 1 = -\tfrac{1}{2} x (x - 1)^2$.

## Correctness

Lines L4 to L6 give $a = \sum_i r_i c_i$ exactly. Modulo $b_i^{e_i}$, each $c_j$ with $j \ne i$ is $0$ and $c_i s_i$ is $1$, so $\sum_j r_j c_j \equiv a s_i c_i \equiv a$. The moduli are pairwise coprime, so the sum is congruent to $a$ modulo $b$. Both sides have degree less than $d$, so they are equal, and dividing by $b$ gives $a/b = \sum_i r_i / b_i^{e_i}$. The $b_i$-adic expansion is exact by the division identity at each step of line L8. Uniqueness follows from the same congruences: the numerators of a decomposition are forced modulo each $b_i^{e_i}$. The full proof is in the proof file below.

## Complexity

The model counts field operations in $K$ with classical arithmetic. Let $D_i = e_i \deg b_i$, so $\sum_i D_i = d$.

- **L1.** Multiplying the factors one by one costs $O(d^2)$.
- **L2.** Long division of a degree $m$ polynomial by $b$ costs $O((m - d + 1) d)$ when $m \ge d$, and nothing otherwise.
- **L4.** Dividing $b$ by $b_i^{e_i}$ costs $O(d D_i)$.
- **L5.** The extended Euclidean algorithm on $c_i \bmod b_i^{e_i}$ and $b_i^{e_i}$, both of degree at most $D_i$, costs $O(D_i^2)$ after one reduction of cost $O(d D_i)$.
- **L6.** $a s_i$ has degree less than $d + D_i$, and its reduction modulo $b_i^{e_i}$ costs $O(d D_i)$.
- **L7, L8.** Each of the $e_i$ divisions by $b_i$ of a polynomial of degree less than $D_i$ costs $O(D_i \deg b_i)$, so $O(D_i^2)$ in all.

Summing over $i$ with $\sum D_i = d$ gives $O(d^2 + m d)$ field operations in the worst case. This bound is proved. With fast multiplication and the subproduct tree, von zur Gathen and Gerhard (Chapter 10) obtain $O(M(d) \log d)$. Over $\mathbb{Q}$, these counts ignore coefficient growth: the numerators can have much larger coefficients than $a$ and $b$, so the bit cost is larger, and multimodular methods are used for large inputs.

## Properties

- **Unique.** For a fixed factorization the output is unique, so it is a canonical form of $a/b$ relative to that factorization.
- **Linear in $a$.** For a fixed denominator the map $a \mapsto (q, a_{ij})$ is $K$-linear, because each line is linear in $a$.
- **No factorization needed for coprime splitting.** The factors need only be pairwise coprime, so a [square-free factorization](/square-free-factorization/), which costs only gcds, is enough. Irreducible factors give the finest decomposition over $K$.
- **Rational in the field of the input.** All results lie in $K$. No algebraic numbers appear unless the factorization introduces them.

## Variants and improvements

- **Square-free partial fractions.** With $b = \prod_i b_i^i$ square-free, this is the input of [Hermite reduction](/hermite-reduction/) and of the [Horowitz-Ostrogradsky method](/horowitz-ostrogradsky/).
- **Full decomposition over the algebraic closure.** For a square-free $b$ and $\deg a < \deg b$, $a/b = \sum_{b(\alpha) = 0} \frac{a(\alpha)/b'(\alpha)}{x - \alpha}$. Bronstein and Salvy give an algorithm that returns this sum indexed by the roots of factors of $b$, without computing the roots.
- **Fast version.** Replace the per-factor Euclidean algorithms by a subproduct tree and simultaneous reduction, as in fast Chinese remaindering, for $O(M(d) \log d)$ operations.
- **Linear algebra.** Solve for the coefficients of the $a_{ij}$ as a $d \times d$ linear system. This costs $O(d^3)$ and is the method of hand calculation.

## When to use it

Use it to integrate rational functions, to invert Laplace or $z$ transforms of rational functions, and to compute the terms of a rational generating function: $1/(1 - \alpha x)^j$ has known coefficients. For integration over $\mathbb{Q}$, prefer a square-free factorization to an irreducible one: the Rothstein-Trager and Lazard-Rioboo-Trager methods then find the logarithmic part with no factorization at all.

## Pitfalls

- **Factors that are not coprime.** With $b_1 = x - 1$ and $b_2 = x^2 + x - 2 = (x - 1)(x + 2)$, line L5 fails, because $c_i$ is not invertible modulo $b_i^{e_i}$. The implementation checks the gcd at line L5 and raises an error.
- **Skipping the polynomial part.** If $\deg a \ge \deg b$ and line L2 is left out, the numerators $r_i$ of line L6 are still reduced modulo $b_i^{e_i}$, so the result describes $(a \bmod b)/b$ and misses $q$.
- **The wrong direction of the expansion.** In line L7 the first remainder belongs to the highest power $b_i^{e_i}$. Running $j$ upward assigns the digits to the wrong powers.
- **Numerators of too high degree.** A decomposition with $\deg a_{ij} \ge \deg b_i$ is not unique, and comparing two such results for equality fails.

## Implementations

## History

The decomposition of a fraction into partial fractions over a coprime factorization is classical algebra. In computer algebra it is the base of rational integration: Hermite's reduction and the methods of Horowitz, Rothstein, Trager, Lazard and Rioboo all start from a partial fraction decomposition with respect to a square-free factorization (Bronstein, Chapter 2).

## References
