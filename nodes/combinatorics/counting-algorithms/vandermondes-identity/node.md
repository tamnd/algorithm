---
tag: C741VV
kind: theorem
slug: vandermondes-identity
name: Vandermonde's identity
aliases:
- Vandermonde's convolution
- Chu-Vandermonde identity
area: combinatorics/counting-algorithms
level: core
summary: Binomial identity stating that the sum over k of C(m,k) times C(n,r-k) equals C(m+n,r).
prereqs: [binomial-coefficient, binomial-theorem]
see_also: [hockey-stick-identity, generating-functions, double-counting, counting-lattice-paths, multinomial-coefficient, pascal-triangle-dp, catalan-numbers]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 5.1, Basic identities (Vandermonde's convolution, its combinatorial proof and its history)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (sums of products, the convolution formula)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1 (the exercises on binomial coefficient identities, including the Vandermonde convolution)
---

Vandermonde's identity says that $\sum_{k} \binom{m}{k}\binom{n}{r-k} = \binom{m+n}{r}$: choosing $r$ items from a pool of $m + n$ items is the same as choosing $k$ of them from the first $m$ and $r - k$ from the other $n$, for each possible $k$. In the language of [generating functions](/generating-functions/), it says that $(1+z)^m (1+z)^n = (1+z)^{m+n}$, so the rows of Pascal's triangle convolve into rows. It holds for all real $m$ and $n$ as a polynomial identity, and it is the source of $\sum_k \binom{n}{k}^2 = \binom{2n}{n}$ and of the total probability of the hypergeometric distribution.

## Statement

Notation: $[n] = \{1, \ldots, n\}$; $\binom{n}{k}$ or $C(n, k)$ is the number of $k$-subsets of $[n]$, which is $0$ when $k < 0$ or $k > n$; and for real $x$ and integer $k \ge 0$, $\binom{x}{k} = x(x-1)\cdots(x-k+1)/k!$, with $\binom{x}{k} = 0$ for $k < 0$. The sums run over all integers $k$; only finitely many terms are nonzero.

**Theorem (Vandermonde's identity).** For all integers $m, n \ge 0$ and every integer $r$,
$$\sum_{k} \binom{m}{k}\binom{n}{r - k} = \binom{m + n}{r}.$$

**Theorem (general form).** For all real numbers $x$ and $y$ and every integer $r \ge 0$,
$$\sum_{k=0}^{r} \binom{x}{k}\binom{y}{r - k} = \binom{x + y}{r}.$$

For integers $x = m \ge 0$ and $y = n \ge 0$ the general form is the first theorem, since the generalized coefficient agrees with the set count. For $r < 0$ both sides of the first theorem are $0$.

## In plain words

A club has some men and some women, and you want a committee of a fixed size. You can count the committees directly. Or you can split them by how many men they contain: for each possible number of men, choose the men from the men and the rest from the women, and multiply. Adding these products over all possible numbers of men gives the same total, because each committee has exactly one number of men.

The same idea works for paths on a grid, for drawing colored balls from a bag, and for multiplying two polynomials whose coefficients are rows of Pascal's triangle.

## Proof

*Combinatorial proof of the first theorem.* Let $X = A \cup B$ with $A = \{a_1, \ldots, a_m\}$ and $B = \{b_1, \ldots, b_n\}$ disjoint, so $|X| = m + n$ and $X$ has $\binom{m+n}{r}$ subsets of size $r$. Classify each $r$-subset $S$ of $X$ by $k = |S \cap A|$. The map $S \mapsto (S \cap A, S \cap B)$ is a bijection from the $r$-subsets with $|S \cap A| = k$ onto the pairs (a $k$-subset of $A$, an $(r-k)$-subset of $B$), with inverse $(U, V) \mapsto U \cup V$. By the [rule of product](/rule-of-product/) there are $\binom{m}{k}\binom{n}{r-k}$ such pairs, and by the [rule of sum](/rule-of-sum/) over $k$ the identity follows. For $r < 0$ or $r > m + n$ both sides count no sets. $\square$

*Proof by generating functions.* By the [binomial theorem](/binomial-theorem/), $(1+z)^m = \sum_k \binom{m}{k} z^k$ and $(1+z)^n = \sum_j \binom{n}{j} z^j$. The coefficient of $z^r$ in the product is $\sum_k \binom{m}{k}\binom{n}{r-k}$, and in $(1+z)^{m+n}$ it is $\binom{m+n}{r}$. Two equal polynomials have equal coefficients. $\square$

*Proof of the general form.* Fix $r \ge 0$. Both sides are polynomials in the two variables $x$ and $y$, of total degree at most $r$. By the first theorem they agree at every point $(x, y) = (m, n)$ with integers $m, n \ge 0$. For fixed $n \in \{0, 1, 2, \ldots\}$, the difference of the two sides is a polynomial in $x$ with infinitely many roots, so it is zero for every real $x$. Now fix any real $x$: the difference is a polynomial in $y$ that vanishes at every integer $n \ge 0$, so it is zero for every real $y$. $\blacksquare$

**Worked numbers.** For $m = 3$, $n = 4$, $r = 3$ the terms are $\binom{3}{0}\binom{4}{3} = 4$, $\binom{3}{1}\binom{4}{2} = 18$, $\binom{3}{2}\binom{4}{1} = 12$ and $\binom{3}{3}\binom{4}{0} = 1$, and their sum is $35 = \binom{7}{3}$. For $x = y = \tfrac12$ and $r = 2$, with $\binom{1/2}{0} = 1$, $\binom{1/2}{1} = \tfrac12$, $\binom{1/2}{2} = -\tfrac18$: the sum is $-\tfrac18 + \tfrac14 - \tfrac18 = 0 = \binom{1}{2}$.

## Consequences

- **Sum of squares of a row.** With $m = n$ and $r = n$, and the symmetry $\binom{n}{n-k} = \binom{n}{k}$: $\sum_{k} \binom{n}{k}^2 = \binom{2n}{n}$. For $n = 5$: $1 + 25 + 100 + 100 + 25 + 1 = 252 = \binom{10}{5}$. In the language of paths, a monotone [lattice path](/counting-lattice-paths/) from $(0, 0)$ to $(n, n)$ crosses the anti-diagonal $x + y = n$ at exactly one point $(k, n-k)$, with $\binom{n}{k}$ ways before and $\binom{n}{k}$ ways after it.
- **The hypergeometric distribution.** Draw $r$ balls without replacement from an urn with $m$ red and $n$ blue balls. The probability of exactly $k$ red balls is $\binom{m}{k}\binom{n}{r-k}/\binom{m+n}{r}$, and Vandermonde's identity says that these probabilities sum to 1. For $m = n = 5$ and $r = 4$ they are $\tfrac{1}{42}, \tfrac{5}{21}, \tfrac{10}{21}, \tfrac{5}{21}, \tfrac{1}{42}$ for $k = 0, \ldots, 4$, over $\binom{10}{4} = 210$ draws.
- **Other forms.** With symmetry, $\sum_k \binom{m}{k}\binom{n}{k} = \binom{m+n}{m}$, and, more generally, $\sum_k \binom{m}{s + k}\binom{n}{t - k} = \binom{m+n}{s + t}$ by a shift of $k$ (Concrete Mathematics, Section 5.1).
- **Negative upper index.** With $\binom{-1}{k} = (-1)^k$, the general form for $x = y = -1$ gives $\sum_{k=0}^{r} (-1)^k(-1)^{r-k} = (r+1)(-1)^r = \binom{-2}{r}$. With upper negation, $\binom{-a}{k} = (-1)^k\binom{a + k - 1}{k}$, the general form becomes a convolution of multiset counts: $\sum_k \binom{a + k - 1}{k}\binom{b + r - k - 1}{r - k} = \binom{a + b + r - 1}{r}$, which is the [stars and bars](/stars-and-bars/) count split by the first $a$ kinds.
- **Combining two parts in a count.** If a part $A$ has $a_k$ ways to take $k$ items and a disjoint part $B$ has $b_j$ ways to take $j$ items, the whole has $\sum_k a_k b_{r-k}$ ways to take $r$ items, a convolution that a counting DP computes, or a [polynomial multiplication](/fft-polynomial-multiplication/) for long rows. Vandermonde's identity is the case where every item is free, $a_k = \binom{m}{k}$ and $b_j = \binom{n}{j}$. Pascal's rule is the case $n = 1$: $\binom{m+1}{r} = \binom{m}{r} + \binom{m}{r-1}$.
- **Multinomial form.** By induction on the number of parts, $\sum \binom{n_1}{k_1}\cdots\binom{n_j}{k_j} = \binom{n_1 + \cdots + n_j}{r}$, the sum over all $k_1 + \cdots + k_j = r$.

## Tightness

- **The upper indices add, the lower indices must add too.** Each term must have lower indices $k$ and $r - k$ with the fixed sum $r$. Replacing $\binom{n}{r-k}$ by $\binom{n}{r}$ gives $2^m\binom{n}{r}$, not $\binom{m+n}{r}$; for $m = 1$, $n = 2$, $r = 1$ that is $4$ against $\binom{3}{1} = 3$.
- **The second index must be $r - k$.** The sum $\sum_k \binom{m}{k}\binom{n}{k}$ is $\binom{m+n}{m}$, not $\binom{m+n}{k}$; for $m = n = 2$ it is $1 + 4 + 1 = 6 = \binom{4}{2}$.
- **Lower indices do not convolve the same way.** $\sum_k \binom{k}{a}\binom{n-k}{b}$ is a sum over the upper indices, and it equals $\binom{n+1}{a+b+1}$ for integers $a, b, n \ge 0$, not $\binom{n}{a+b}$; it comes from the position of the $(a+1)$-st element of an $(a+b+1)$-subset, as in the [hockey-stick identity](/hockey-stick-identity/).

## History

The identity is named after Alexandre-Théophile Vandermonde, who published it in 1772. It was known much earlier: Concrete Mathematics (Section 5.1) notes that it appears in the work of the Chinese mathematician Zhu Shijie (Chu Shih-Chieh) of 1303, which is why it is also called the Chu-Vandermonde identity. The general form for real $x$ and $y$, by the polynomial argument, is the form used throughout Concrete Mathematics.

## References
