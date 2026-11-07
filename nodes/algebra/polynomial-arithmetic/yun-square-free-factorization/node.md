---
tag: 8QF8S3
kind: algorithm
slug: yun-square-free-factorization
name: Yun's square-free factorization
aliases:
- Yun's algorithm
- Yun's square-free decomposition
area: algebra/polynomial-arithmetic
level: advanced
summary: Splits a polynomial into square-free parts using gcds with its derivative, at the cost of a constant number of gcds.
solves: [square-free-factorization]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the input polynomial f, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
  fast_gcd_time: {worst: O(M(n) log n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [square-free-factorization, polynomial-euclidean-algorithm]
see_also: [square-free-factorization, square-free-polynomial, polynomial-gcd, polynomial-euclidean-algorithm, multiplicity-of-roots, discriminant, polynomial-factorization-over-finite-fields, distinct-degree-factorization]
sources:
  - paper: doi:10.1145/800205.806320
    title: David Y. Y. Yun, On square-free decomposition algorithms, SYMSAC 1976
    locator: pp. 26 to 35
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.6, Squarefree factorization (p. 393; Yun's algorithm and its cost)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (squarefree factorization by gcds with the derivative)
  - paper: doi:10.1145/321879.321890
    title: David R. Musser, Multivariate polynomial factorization, Journal of the ACM 22(2), 1975
    locator: pp. 291 to 308 (the earlier repeated-gcd method)
  - paper: doi:10.1007/BF01613611
    title: Patrizia Gianni and Barry Trager, Square-free algorithms in positive characteristic, Applicable Algebra in Engineering, Communication and Computing 7(1), 1996
    locator: pp. 1 to 14
---

Yun's algorithm computes the [square-free factorization](/square-free-factorization/) $f = c\, a_1 a_2^2 \cdots a_k^k$ of a polynomial over a field of characteristic $0$, or of characteristic larger than $\deg f$. After one gcd of $f$ and $f'$, it finds each $a_i$ as the gcd of two polynomials built from derivatives, and these polynomials shrink so fast that their degrees add up to $n = \deg f$. So the whole algorithm costs at most a constant times one gcd of degree $n$: $O(n^2)$ field operations with the [Euclidean algorithm](/polynomial-euclidean-algorithm/), and $O(M(n) \log n)$ with a fast gcd. David Yun published it in 1976.

## In plain words

A factor that occurs three times in a polynomial occurs two times in its derivative. So the common part of the polynomial and its derivative contains every repeated factor, one time fewer. Dividing the polynomial by this common part leaves each different factor exactly once.

Yun's method then peels off the factors by count. At each step it keeps the product of the factors not yet found, and a second polynomial made from derivatives that is divisible by all of them except the ones of the current count. The common part of these two is the product of the factors of the current count. It removes them and repeats. Each step works on smaller polynomials, so the total work is close to that of one common part of the original polynomial and its derivative.

## The problem

Given a nonzero $f \in F[x]$ of degree $n$ over a field $F$, find $c = \operatorname{lc}(f)$ and monic $a_1, \ldots, a_k$ with $f = c \prod_i a_i^{\,i}$, each $a_i$ square-free, the $a_i$ pairwise coprime, and $a_k \ne 1$. Yun's algorithm needs $F$ of characteristic $0$ or of characteristic $p > n$.

**Cost model.** We count field operations at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $F$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. The $O(n^2)$ bound is for the Euclidean algorithm and schoolbook division, as in the implementation; the $O(M(n) \log n)$ bound is for a fast Euclidean algorithm and fast division.

## The algorithm

The input is first made monic: $c = \operatorname{lc}(f)$ and $f \leftarrow f / c$. A constant input returns $(c, [\,])$.

```pseudo id=main
YUN(f)                                         ▷ f monic, deg f = n ≥ 1; char F = 0 or > n
L1  A ← [ ]
L2  b ← gcd(f, f′)                              ▷ monic gcd
L3  c ← f / b;  d ← f′ / b − c′
L4  while c ≠ 1 do
L5      a ← gcd(c, d)
L6      append a to A
L7      c ← c / a
L8      d ← d / a − c′
L9  return A                                   ▷ A = [a_1, …, a_k]
```

All divisions are exact. Write $b_i = \prod_{j \ge i} a_j$. Line L3 sets $c = b_1$, the square-free part of $f$. Before the $i$th pass of the loop, $c = b_i$ and

$$d = \sum_{j > i} (j - i)\, a_j'\, \frac{b_i}{a_j}.$$

Every term contains $a_i$, and no term except the $j$th contains $a_j$ for $j > i$, so $\gcd(c, d) = a_i$. The loop runs exactly $k$ times. When the algorithm reaches the last factor, $d = 0$ and $\gcd(c, 0) = c = a_k$.

## Example

Over $\mathbb{Q}$, let $f = x^5 - x^4 - 2x^3 + 2x^2 + x - 1 = (x - 1)^3 (x + 1)^2$. Then $f' = 5x^4 - 4x^3 - 6x^2 + 4x + 1$.

| Step | $a$ | $c$ after the step | $d$ after the step |
|---|---|---|---|
| L2, L3 | | $f / b = x^2 - 1$ | $f'/b - c' = 3x + 1$ |
| $i = 1$ | $\gcd(x^2 - 1, 3x + 1) = 1$ | $x^2 - 1$ | $(3x + 1) - 2x = x + 1$ |
| $i = 2$ | $\gcd(x^2 - 1, x + 1) = x + 1$ | $x - 1$ | $1 - 1 = 0$ |
| $i = 3$ | $\gcd(x - 1, 0) = x - 1$ | $1$ | $0$ |

Line L2 gives $b = \gcd(f, f') = x^3 - x^2 - x + 1 = (x - 1)^2 (x + 1)$. The output is $a_1 = 1$, $a_2 = x + 1$, $a_3 = x - 1$, and indeed $f = (x + 1)^2 (x - 1)^3$. The formula for $d$ checks: for $i = 1$ it gives $1 \cdot 1 \cdot (x - 1) + 2 \cdot 1 \cdot (x + 1) = 3x + 1$. The tests run this example and the others on the [square-free factorization](/square-free-factorization/) page.

## Correctness

Over a field of characteristic $0$ or $p > n$, each square-free $a_j$ is coprime to $j\, a_j'$, because an irreducible factor $q$ has $q' \ne 0$ of lower degree. From this, $\gcd(f, f') = \prod_j a_j^{\,j-1}$, so line L3 gives $c = b_1$ and the value of $d$ stated above for $i = 1$. In the loop, $\gcd(b_i, d_i) = a_i$ because each term of $d_i$ contains $a_i$ and each $a_j$ with $j > i$ divides all terms but one, which is coprime to it. Lines L7 and L8 turn $b_i$ and $d_i$ into $b_{i+1}$ and $d_{i+1}$ by the product rule. The loop stops when $b_i = 1$, that is after $i = k$. The full proof is below.

## Complexity

Let $n_i = \deg b_i = \sum_{j \ge i} \deg a_j$. Then

$$\sum_{i=1}^{k} n_i = \sum_{j=1}^{k} j \deg a_j = n,$$

because $a_j$ is counted in $n_1, \ldots, n_j$. Pass $i$ makes one gcd of polynomials of degree at most $n_i$, two exact divisions and one derivative.

- **With the Euclidean algorithm and schoolbook division.** Pass $i$ costs $O(n_i^2)$, and $\sum n_i^2 \le n^2$, so the loop costs $O(n^2)$. Lines L2 and L3 also cost $O(n^2)$. Total $O(n^2)$ field operations. This is proved.
- **With fast arithmetic.** If a gcd of degree $d$ costs $G(d)$ with $G(d)/d$ nondecreasing, the loop costs $\sum_i G(n_i) \le G(n)$, and line L2 costs $G(n)$. With the fast Euclidean algorithm, $G(n) = O(M(n) \log n)$, so the total is $O(M(n) \log n)$. This is proved, given the bound for the fast gcd in von zur Gathen and Gerhard, Chapter 11.
- **Space.** $O(n)$ field elements besides the output.

## Properties

- **Output.** The factors $a_i$ are monic, square-free and pairwise coprime; $a_i = 1$ is possible for $i < k$, and $a_k \ne 1$.
- **Field operations only.** No factoring and no roots are needed, so the algorithm is exact over $\mathbb{Q}$ and over finite fields of large characteristic.
- **Over $\mathbb{Z}$.** For a monic $f \in \mathbb{Z}[x]$, every $a_i$ is in $\mathbb{Z}[x]$, by Gauss's lemma, though the intermediate gcds over $\mathbb{Q}$ may have fractions. In practice the gcds are computed with a modular or subresultant method.
- **Number of passes.** Exactly $k$, the largest multiplicity.
- Deterministic and not recursive.

## Variants and improvements

- **Finite fields of small characteristic.** If $p \le n$, a factor whose multiplicity is divisible by $p$ is invisible to the derivative. The fix is to run the loop, then take the $p$-th root of the remaining part $f / \prod_i a_i^{\,i}$, which is a polynomial in $x^p$, and repeat with multiplicities multiplied by $p$. Knuth, Section 4.6.2, and von zur Gathen and Gerhard, Section 14.6, describe this.
- **Imperfect fields.** Over fields such as $\mathbb{F}_p(t)$, $p$-th roots may not exist; Gianni and Trager (1996) give square-free algorithms for this case.
- **Over $\mathbb{Z}$.** Remove the content first, then run Yun's algorithm with integer gcds such as the [subresultant gcd](/subresultant-gcd/) or [Brown's modular gcd](/brown-modular-gcd/).
- **Multivariate polynomials.** Take the derivative with respect to one variable and use multivariate gcds; the algorithm then gives the square-free factorization in that variable, and the content in that variable is treated separately.
- **Square-free part only.** If only $a_1 a_2 \cdots a_k$ is needed, stop after line L3: it is $c = f / \gcd(f, f')$.

## When to use it

Use Yun's algorithm as the first step of factoring or root isolation whenever the input may have repeated factors and the characteristic is $0$ or larger than the degree. Over $\mathbb{F}_p$ with $p \le n$, use the finite-field variant with $p$-th roots. If the input is known to be square-free, test it with one gcd, $\gcd(f, f') = 1$, and skip the rest.

## Pitfalls

- **Small characteristic.** Over $\mathbb{F}_3$, $f = (x + 1)^3 (x + 2)$ has $f' = (x + 1)^3$, and the algorithm returns only $a_1 = x + 2$: the cube is lost without any error. The tests include this case. Check the precondition $p > n$, or use the finite-field variant.
- **Monic gcds.** The proof uses monic gcds; a gcd normalized in another way changes $b$ by a constant and makes $d$ wrong by that constant unless the divisions use the same normalization.
- **The zero polynomial.** It has no square-free factorization; the implementation raises an error.
- **Coefficient growth over $\mathbb{Q}$.** Naive Euclidean gcds over $\mathbb{Q}$ produce large fractions, as on the [polynomial GCD](/polynomial-gcd/) page. Use integer gcd algorithms for large inputs.
- **Leading coefficient.** Factor it out first; otherwise $f / \gcd(f, f')$ is not monic and the output is off by constants.

## Implementations

## History

Yun (1976) introduced the algorithm and showed that square-free decomposition costs at most a constant times a gcd. Before it, repeated gcds with the derivative were used, as in Musser's factoring work (1975). Von zur Gathen and Gerhard, Section 14.6, present Yun's algorithm with its cost and the finite-field version, and Gianni and Trager (1996) treated fields of positive characteristic that are not perfect.

## References
