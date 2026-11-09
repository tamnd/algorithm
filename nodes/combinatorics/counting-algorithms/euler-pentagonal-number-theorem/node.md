---
tag: TY17BP
kind: theorem
slug: euler-pentagonal-number-theorem
name: Euler's pentagonal number theorem
aliases:
- Pentagonal number theorem
- pentagonal number theorem
- Euler's pentagonal theorem
- Franklin's involution
area: combinatorics/counting-algorithms
level: advanced
summary: Expands the product of (1-x^k) as a sum over generalized pentagonal numbers.
prereqs: [generating-functions, ferrers-diagram]
see_also: [euler-pentagonal-recurrence, integer-partition-counting, integer-partition-function, euler-partition-theorem, ferrers-diagram, power-series-inversion, hardy-ramanujan-asymptotics]
sources:
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 1, The elementary theory of partitions (Euler's pentagonal number theorem and Franklin's proof), and Chapter 2, Infinite series generating functions (Jacobi's triple product identity)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 14, Partitions (Euler's pentagonal-number theorem with Franklin's combinatorial proof, and the recurrences for p(n) and the sum of divisors)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Identities versus bijections (Franklin's involution for the pentagonal number theorem)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Euler's pentagonal formula and the recurrence for p(n))
---

Euler's pentagonal number theorem says that the infinite product $(1 - x)(1 - x^2)(1 - x^3) \cdots$ collapses to a sparse series: almost all coefficients are 0, and the others are $\pm 1$ at the generalized pentagonal numbers. Since the product is the reciprocal of the [generating function](/generating-functions/) of the partition numbers $p(n)$, the theorem gives [Euler's pentagonal recurrence](/euler-pentagonal-recurrence/), the standard way to compute $p(0), \ldots, p(n)$ in $O(n^{3/2})$ additions. Franklin's sign-reversing involution on partitions into distinct parts proves it with no algebra.

## Statement

**Notation.** $x$ is a formal variable, $j$ runs over all integers, and $g_j = j(3j - 1)/2$. The numbers $g_j$ for $j = 0, 1, -1, 2, -2, \ldots$ are the generalized pentagonal numbers $0, 1, 2, 5, 7, 12, 15, 22, 26, 35, 40, 51, 57, 70$ (OEIS A001318). $p(n)$ is the number of partitions of $n$.

**Theorem (Euler).** As formal power series,

$$\prod_{k \ge 1} (1 - x^k) = \sum_{j = -\infty}^{\infty} (-1)^j x^{j(3j-1)/2} = 1 - x - x^2 + x^5 + x^7 - x^{12} - x^{15} + x^{22} + x^{26} - \cdots.$$

The coefficient sequence starts $1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1$ (OEIS A010815). The values $g_j$ are distinct for distinct $j$, so each coefficient is $0$, $1$ or $-1$.

**Combinatorial form.** For $n \ge 0$, let $D_e(n)$ and $D_o(n)$ be the numbers of partitions of $n$ into an even and an odd number of distinct parts. Then $D_e(n) - D_o(n) = (-1)^j$ if $n = g_j$, and $0$ if $n$ is not a generalized pentagonal number.

The two forms are equivalent, because expanding $\prod_k (1 - x^k)$ picks a finite set of distinct parts $k$ and gives each one a factor $-1$, so the coefficient of $x^n$ is $D_e(n) - D_o(n)$.

## In plain words

Look at all the ways to write a number as a sum of different positive whole numbers. Sort them into two groups: those with an even number of terms and those with an odd number. For almost every number the two groups have the same size. The only exceptions are the pentagonal numbers 1, 2, 5, 7, 12, 15, 22 and so on, where one group has exactly one extra member. This balance lets a program find the number of all splits of a number by a short signed sum of earlier values.

## Proof

We prove the combinatorial form with Franklin's involution. Draw a partition $\lambda_1 > \lambda_2 > \cdots > \lambda_\ell \ge 1$ into distinct parts as a [Ferrers diagram](/ferrers-diagram/), row $i$ having $\lambda_i$ cells. For $\ell \ge 1$, define:

- the *base* $s = \lambda_\ell$, the length of the smallest row;
- the *slope* $\sigma$, the largest $i$ with $\lambda_1, \lambda_2, \ldots, \lambda_i$ consecutive integers, that is, $\lambda_i = \lambda_1 - (i - 1)$. Then $1 \le \sigma \le \ell$, and the slope is the run of last cells of the first $\sigma$ rows.

Call $\lambda$ *exceptional* if $\sigma = \ell$ and $s \in \{\sigma, \sigma + 1\}$. Define a map $\phi$ on the partitions into distinct parts of $n \ge 1$ that are not exceptional.

- **Move A, when $s \le \sigma$.** Remove the smallest part, and add 1 to each of the $s$ largest parts. In the diagram, the base becomes a new slope.
- **Move B, when $s > \sigma$.** Subtract 1 from each of the $\sigma$ largest parts, and add a new smallest part $\sigma$. In the diagram, the slope becomes a new base.

*Move A is well defined.* After removing $\lambda_\ell$ there are $\ell - 1$ parts, and $s \le \ell - 1$: if $\sigma < \ell$ then $s \le \sigma \le \ell - 1$, and if $\sigma = \ell$ then $s < \sigma$ because $\lambda$ is not exceptional. Adding 1 to the first $s$ parts keeps them distinct and decreasing. The result $\mu$ has $\ell - 1$ parts, its first $s$ parts are consecutive, and $\mu_s = \lambda_s + 1 \ge \lambda_{s+1} + 2$, so the slope of $\mu$ is exactly $s$. The base of $\mu$ is at least $\lambda_{\ell-1} > s$. So $\mu$ is in the case of move B, and move B on $\mu$ subtracts 1 from its first $s$ parts and adds the part $s$, which gives back $\lambda$. $\mu$ is not exceptional: if it had slope equal to its length, $\ell - 1 = s$, its base would be $\lambda_{\ell-1} + 1$ (here the slope covers all parts), and $\lambda_{\ell-1} + 1 \ge s + 2$.

*Move B is well defined.* If $\sigma < \ell$, the part $\lambda_{\sigma+1}$ is at most $\lambda_\sigma - 2$, so subtracting 1 from the first $\sigma$ parts keeps all parts distinct, and the smallest part $s > \sigma$ is untouched, so the new part $\sigma$ is the unique smallest. If $\sigma = \ell$, every part drops by 1, and the smallest becomes $s - 1 > \sigma$ because $s \ge \sigma + 2$ when $\lambda$ is not exceptional. The result $\mu$ has $\ell + 1$ parts, base $\sigma$ and slope at least $\sigma$, so it is in the case of move A. Move A on $\mu$ removes the part $\sigma$ and adds 1 to the first $\sigma$ parts, which gives back $\lambda$. $\mu$ is not exceptional: if its slope were its full length $\ell + 1$, its base would be $\sigma$ with slope $\ell + 1 > \sigma$, which is not one of the two exceptional cases.

So $\phi$ is an involution on the non-exceptional partitions, and it changes the number of parts by exactly 1. It pairs each non-exceptional partition with an even number of parts with one that has an odd number of parts, so the non-exceptional partitions add $0$ to $D_e(n) - D_o(n)$.

*The exceptional partitions.* If $\sigma = \ell = s$, then $\lambda = (2\ell - 1, 2\ell - 2, \ldots, \ell)$ with sum $\ell(3\ell - 1)/2 = g_\ell$. If $\sigma = \ell$ and $s = \ell + 1$, then $\lambda = (2\ell, 2\ell - 1, \ldots, \ell + 1)$ with sum $\ell(3\ell + 1)/2 = g_{-\ell}$. Both have $\ell$ parts and sign $(-1)^\ell$. Since the $g_j$ are distinct, each $n \ge 1$ has at most one exceptional partition, with sign $(-1)^j$ when $n = g_j$. For $n = 0$ the empty partition gives $1 = (-1)^0$. $\square$

## Consequences

**The recurrence for $p(n)$.** Multiply the theorem by $\sum_n p(n) x^n = \prod_k (1 - x^k)^{-1}$. The product is $1$, so for $n \ge 1$, $\sum_j (-1)^j p(n - g_j) = 0$, that is,

$$p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + p(n-12) + p(n-15) - \cdots,$$

with $p(m) = 0$ for $m < 0$. It has about $2\sqrt{2n/3}$ terms, which gives the $O(n^{3/2})$ [pentagonal recurrence](/euler-pentagonal-recurrence/) for the whole prefix.

**The recurrence for the sum of divisors.** Let $\sigma(n)$ be the sum of the divisors of $n$. Taking the logarithmic derivative of the theorem gives $-\sum_k \frac{k x^k}{1 - x^k} = \frac{\sum_j (-1)^j g_j x^{g_j}}{\sum_j (-1)^j x^{g_j}}$, and the left side is $-\sum_m \sigma(m) x^m$. Clearing the denominator gives, for $n \ge 1$,

$$\sigma(n) = \sigma(n-1) + \sigma(n-2) - \sigma(n-5) - \sigma(n-7) + \cdots,$$

where a term $\sigma(n - g_j)$ with $g_j = n$ is replaced by $n$. For example, $\sigma(5) = \sigma(4) + \sigma(3) - 5 = 7 + 4 - 5 = 6$. Euler found this curious rule, which links an additive and a multiplicative function.

**Fast power series algorithms.** The reciprocal of $\sum_n p(n) x^n$ has only $O(\sqrt n)$ nonzero terms up to $x^n$. So [power series inversion](/power-series-inversion/) of this sparse series is a fast way to get $p(0), \ldots, p(n)$ modulo a prime, and multiplying a series by $\prod_k (1 - x^k)$ costs $O(n^{3/2})$ operations instead of $O(n^2)$.

**Partitions into distinct parts.** Partitions of $n$ into distinct parts are almost evenly split by the parity of the number of parts. The imbalance is at most 1, so the parity of the number of parts of a random partition into distinct parts carries almost no bias.

## Tightness

- **The exceptions occur.** For each generalized pentagonal number the difference $D_e(n) - D_o(n)$ is $\pm 1$, not $0$. For $n = 5$, the distinct partitions are $5$, $4 + 1$ and $3 + 2$, so $D_e = 2$ and $D_o = 1$, and indeed $5 = g_2$ with sign $+1$.
- **Sparsity is special to the first power.** The cube of the product is still sparse, by Jacobi's identity $\prod_k (1 - x^k)^3 = \sum_{m \ge 0} (-1)^m (2m + 1)\, x^{m(m+1)/2}$, a consequence of the Jacobi triple product (Andrews, Chapter 2), but its coefficients $1, -3, 5, -7, 9, \ldots$ are unbounded. The square $\prod_k (1 - x^k)^2$ starts $1 - 2x - x^2 + 2x^3 + x^4 + 2x^5 - 2x^6 - 2x^8 - 2x^9 + x^{10}$, so its coefficients are not limited to $0$ and $\pm 1$.
- **Signs matter.** The related product $\prod_k (1 + x^k)$, the generating function of partitions into distinct parts, has all coefficients positive and growing. The cancellation comes from the sign $(-1)^\ell$ alone.

## History

Euler found the identity by expanding the product by hand in the 1740s and later published a proof by algebraic manipulation of the series. Fabian Franklin gave the combinatorial involution proof in 1881. Jacobi's triple product identity, from 1829, contains the theorem as a special case, and the pentagonal theorem is the first example of the modular form identities that later led to Ramanujan's partition congruences and to the [Rademacher formula](/rademacher-formula/).

## References
