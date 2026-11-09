---
tag: 9YQ387
kind: definition
slug: binomial-coefficient
name: Binomial coefficient
aliases: [n choose k, choose function]
area: combinatorics/counting-algorithms
level: intro
summary: The number of k-element subsets of an n-element set.
prereqs: [rule-of-product]
see_also: [factorial, binomial-theorem, pascal-triangle-dp, multinomial-coefficient, binomial-coefficient-computation, binomial-coefficient-bounds, stars-and-bars, lucas-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C.1, Counting
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.6, Binomial Coefficients
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Chapter 5, Binomial Coefficients (Section 5.1, Basic identities)
---

The binomial coefficient $\binom{n}{k}$, read "$n$ choose $k$", is the number of $k$-element subsets of an $n$-element set. It counts the ways to pick $k$ items from $n$ items when the order of the picks does not matter, and it equals $n!/(k!\,(n-k)!)$ for $0 \le k \le n$. It is the coefficient of $x^k y^{n-k}$ in $(x + y)^n$, which is the [binomial theorem](/binomial-theorem/) and the source of the name. Its values form Pascal's triangle (OEIS A007318) and grow fast, so a program that computes them must take care with overflow and wasted work; see [computing binomial coefficients](/binomial-coefficient-computation/).

## Definition

Let $X$ be a finite set with $n = |X|$ elements, where $n \ge 0$ is an integer. For each integer $k$, the binomial coefficient is

$$\binom{n}{k} = \bigl|\{\, S \subseteq X : |S| = k \,\}\bigr|.$$

The value depends only on $n$, not on the set $X$: a bijection from one $n$-element set onto another carries the $k$-element subsets of the first set one to one onto those of the second. When $k < 0$ or $k > n$, no subset has exactly $k$ elements, so $\binom{n}{k} = 0$. We use $[n] = \{1, \ldots, n\}$ as the standard $n$-element set, and also write $C(n, k)$ in plain text.

**The factorial formula.** For $0 \le k \le n$,

$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!} = \frac{n(n-1)\cdots(n-k+1)}{k!}, \qquad \text{where } 0! = 1.$$

*Proof.* Count the sequences $(a_1, \ldots, a_k)$ of distinct elements of $X$ in two ways. By the [rule of product](/rule-of-product/), $a_i$ has $n - i + 1$ choices, so there are $n(n-1)\cdots(n-k+1) = n!/(n-k)!$ sequences. Each $k$-element subset $S$ gives exactly $k!$ sequences, one for each order of its elements, and different subsets give different sequences. So $k!\binom{n}{k} = n!/(n-k)!$. $\square$

**Symmetry.** For $0 \le k \le n$, $\binom{n}{k} = \binom{n}{n-k}$. *Proof.* The map $S \mapsto X \setminus S$ sends $k$-subsets to $(n-k)$-subsets and is its own inverse, so it is a bijection. $\square$

**Pascal's rule.** For $n \ge 1$ and every integer $k$, $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$. *Proof.* Fix $x \in X$. The $k$-subsets that contain $x$ are the sets $\{x\} \cup T$ with $T$ a $(k-1)$-subset of $X \setminus \{x\}$, and the map $T \mapsto \{x\} \cup T$ is a bijection, so there are $\binom{n-1}{k-1}$ of them. The $k$-subsets that do not contain $x$ are the $k$-subsets of $X \setminus \{x\}$, so there are $\binom{n-1}{k}$ of them. The two groups do not overlap and together hold all $k$-subsets, so the [rule of sum](/rule-of-sum/) gives the rule. For $k \le 0$ or $k \ge n$ the same argument holds with the empty families counted as 0. $\square$ With $\binom{0}{0} = 1$, this rule determines every value, which is the method of [Pascal's triangle](/pascal-triangle-dp/).

**Row sum.** $\sum_{k=0}^{n} \binom{n}{k} = 2^n$. *Proof.* Each subset of $X$ has exactly one size, so the sizes split the $2^n$ subsets into groups of $\binom{n}{k}$. $\square$

**Shape of a row.** For $0 \le k < n$, $\binom{n}{k+1} / \binom{n}{k} = (n - k)/(k + 1)$, and this ratio is greater than 1 exactly when $k < (n-1)/2$. So a row increases up to the middle and then decreases, and its largest entry is the central coefficient $\binom{n}{\lfloor n/2 \rfloor}$. By [Stirling's approximation](/stirling-approximation/), $\binom{2m}{m} \sim 4^m / \sqrt{\pi m}$, so $\binom{n}{\lfloor n/2 \rfloor}$ has about $n - \tfrac12 \lg n$ bits. Exact bounds are on the page [binomial coefficient bounds](/binomial-coefficient-bounds/).

## Examples and non-examples

**Example 1.** $\binom{5}{2} = 10$. The two-element subsets of $[5]$ are $\{1,2\}$, $\{1,3\}$, $\{1,4\}$, $\{1,5\}$, $\{2,3\}$, $\{2,4\}$, $\{2,5\}$, $\{3,4\}$, $\{3,5\}$, $\{4,5\}$, and the formula gives $5!/(2!\,3!) = 120/12 = 10$.

**Example 2.** The edge cases $\binom{n}{0} = \binom{n}{n} = 1$ count the empty set and the whole set, and $\binom{n}{1} = n$ counts the single elements. In particular $\binom{0}{0} = 1$: the empty set has one subset, itself.

**Example 3.** Row 10 of the triangle is $1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1$. It is symmetric, its largest entry is $\binom{10}{5} = 252$, and its sum is $1024 = 2^{10}$.

**Example 4.** The table shows $\binom{n}{k}$ for $0 \le n \le 5$ and $0 \le k \le 5$. Each entry is the sum of the entry above it and the entry above and to the left, as Pascal's rule says: for example $6 = 3 + 3$ in row 4.

| n \ k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 2 | 1 | 0 | 0 | 0 |
| 3 | 1 | 3 | 3 | 1 | 0 | 0 |
| 4 | 1 | 4 | 6 | 4 | 1 | 0 |
| 5 | 1 | 5 | 10 | 10 | 5 | 1 |

**Example 5.** A poker hand is a 5-card subset of a 52-card deck, so there are $\binom{52}{5} = 2{,}598{,}960$ hands. The value $\binom{100}{50}$ has 97 bits, so it does not fit in a 64-bit word, although $n = 100$ is small.

**Example 6 (parity).** By [Lucas's theorem](/lucas-theorem/) with $p = 2$, $\binom{n}{k}$ is odd exactly when each binary 1 of $k$ is also a 1 of $n$. For $n = 13 = 1101_2$ the odd entries are at $k = 0, 1, 4, 5, 8, 9, 12, 13$.

**Non-example 1.** $n^k / k!$ is not $\binom{n}{k}$. For $n = 4$, $k = 2$ it is $8$, while $\binom{4}{2} = 6$. The correct numerator is the falling product $n(n-1)\cdots(n-k+1)$.

**Non-example 2.** $4!/2! = 12$ counts the ordered pairs of distinct elements of a 4-element set. $\binom{4}{2} = 6$ counts the unordered pairs: each one comes from two ordered pairs.

**Non-example 3.** The number of ways to choose $k$ items from $n$ kinds *with repetition* is not $\binom{n}{k}$ but $\binom{n+k-1}{k}$; see [stars and bars](/stars-and-bars/). For $n = 3$ kinds and $k = 2$ items it is 6, not 3.

**Edge case.** $\binom{3}{5} = 0$. Under this definition, it is not undefined and not an error: a 3-element set has no 5-element subset. The formula $n!/(k!(n-k)!)$ does not apply here, because $(n-k)!$ is not defined for $n - k < 0$.

## Related definitions

- **Generalized binomial coefficient.** For any number $r$ (real, complex, or an element of a ring that contains the rationals) and integer $k \ge 0$, $\binom{r}{k} = r(r-1)\cdots(r-k+1)/k!$, and $\binom{r}{k} = 0$ for $k < 0$. It agrees with the set definition when $r$ is a nonnegative integer. It gives $\binom{-1}{k} = (-1)^k$ and Newton's series $(1 + z)^r = \sum_k \binom{r}{k} z^k$; Concrete Mathematics, Chapter 5, uses this definition throughout.
- The [factorial](/factorial/) $n!$ is the number of [permutations](/permutation/) of $n$ items, and it appears in the formula.
- The [multinomial coefficient](/multinomial-coefficient/) $\binom{n}{k_1, \ldots, k_m}$ counts the ways to split $n$ items into labeled groups of sizes $k_1, \ldots, k_m$. With two groups, it is $\binom{n}{k_1}$.
- [Pascal's triangle dynamic programming](/pascal-triangle-dp/) fills the table above row by row, and [computing binomial coefficients](/binomial-coefficient-computation/) is the problem of getting one value, exactly or modulo a number.
- Identities: the [binomial theorem](/binomial-theorem/), the [hockey-stick identity](/hockey-stick-identity/) and [Vandermonde's identity](/vandermondes-identity/).
- [Combinations with repetition](/combinations-with-repetition/) are counted by $\binom{n+k-1}{k}$, and the [Catalan numbers](/catalan-numbers/) are $\binom{2n}{n}/(n+1)$.
- The [k-subsets](/k-subset-enumeration/) themselves are listed by the algorithms of the area generating combinations, and ranked by the [combinatorial number system](/combinatorial-number-system/).

## References
