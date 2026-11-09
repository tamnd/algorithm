---
tag: S4Y6ZT
kind: theorem
slug: hockey-stick-identity
name: Hockey-stick identity
aliases:
- upper summation
- Christmas stocking identity
- column sum of Pascal's triangle
area: combinatorics/counting-algorithms
level: intro
summary: Binomial identity stating that the sum of C(i,k) for i from k to n equals C(n+1,k+1).
prereqs: [binomial-coefficient]
see_also: [pascal-triangle-dp, vandermondes-identity, stars-and-bars, double-counting, bijective-proof, prefix-sums, counting-lattice-paths, combinations-with-repetition]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 5.1, Basic identities (the identities called upper summation and parallel summation)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (summation formulas for binomial coefficients)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 5, The Binomial Coefficients (Section 5.1, Pascal's triangle, and the identities read off the triangle)
---

The hockey-stick identity says that a column of Pascal's triangle, summed from its top down to row $n$, equals the entry one row lower and one column to the right: $\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$ for all integers $n, k \ge 0$. In the triangle, the summed entries and the result form the shape of a hockey stick. The identity turns sums of polynomials into closed forms, counts the iterations of nested loops, and is the [prefix sum](/prefix-sums/) of a column of the triangle.

## Statement

Notation: $[n] = \{1, \ldots, n\}$, and $\binom{n}{k}$ or $C(n, k)$ is the number of $k$-subsets of $[n]$, which is $0$ when $k < 0$ or $k > n$.

**Theorem (hockey-stick identity).** For all integers $n \ge 0$ and $k \ge 0$,
$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}.$$
When $n < k$ the sum is empty and both sides are $0$.

**Theorem (parallel form).** For all integers $a \ge 0$ and $r \ge 0$,
$$\sum_{j=0}^{r} \binom{a + j}{j} = \binom{a + r + 1}{r}.$$

The parallel form is the first theorem with $k = a$, $n = a + r$ and the symmetry $\binom{a+j}{j} = \binom{a+j}{a}$; it sums a diagonal of the triangle instead of a column. Both sides of the parallel form are polynomials in $a$, so it holds for every real $a$ as well (Concrete Mathematics, Section 5.1).

**Shifted start.** For $0 \le s \le n + 1$, $\sum_{i=s}^{n} \binom{i}{k} = \binom{n+1}{k+1} - \binom{s}{k+1}$. This follows by subtracting the identity for $n = s - 1$.

## In plain words

Pick a column of Pascal's triangle and add up its numbers from the top down to some row. The total is the number one row further down and one column to the right. Drawn on the triangle, the numbers you added form a long straight handle and the answer forms the blade, like a hockey stick.

The reason is a count. To choose a group of several people from a numbered line, look at the person with the largest number in your group. If that person is fixed, you only have to choose the rest of the group from the people with smaller numbers. Adding up over all possible largest persons gives the total.

## Proof

*Combinatorial proof.* Count the $(k+1)$-subsets of $[n+1]$, which are $\binom{n+1}{k+1}$ in number. Each such subset $T$ has a largest element $\max T = i + 1$, with $k + 1 \le i + 1 \le n + 1$. The subsets with $\max T = i + 1$ are exactly the sets $\{i + 1\} \cup U$ with $U$ a $k$-subset of $[i]$, and $U \mapsto \{i+1\} \cup U$ is a bijection, so there are $\binom{i}{k}$ of them. The classes for different $i$ do not overlap and cover all $(k+1)$-subsets, so by the [rule of sum](/rule-of-sum/),
$$\binom{n+1}{k+1} = \sum_{i=k}^{n} \binom{i}{k}. \qquad \square$$

*Proof by induction on $n$.* For $n = 0$: if $k = 0$ the left side is $\binom{0}{0} = 1 = \binom{1}{1}$, and if $k \ge 1$ both sides are $0$. Assume the identity for $n - 1 \ge 0$. Then
$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n}{k+1} + \binom{n}{k} = \binom{n+1}{k+1},$$
by the induction hypothesis (which also covers $n - 1 < k$, where the sum is empty and $\binom{n}{k+1} = 0$) and Pascal's rule $\binom{n+1}{k+1} = \binom{n}{k} + \binom{n}{k+1}$, proved on the page [binomial coefficient](/binomial-coefficient/). $\blacksquare$

The induction proof is the triangle picture: Pascal's rule splits the blade $\binom{n+1}{k+1}$ into the entry above-left, $\binom{n}{k}$, which is the bottom of the handle, and the entry above, $\binom{n}{k+1}$, which is the blade of a shorter stick. Unrolling the rule $n - k + 1$ times walks up the column.

**Worked numbers.** For $k = 2$ and $n = 6$: $\binom{2}{2} + \binom{3}{2} + \binom{4}{2} + \binom{5}{2} + \binom{6}{2} = 1 + 3 + 6 + 10 + 15 = 35 = \binom{7}{3}$. For the parallel form with $a = 2$, $r = 3$: $\binom{2}{0} + \binom{3}{1} + \binom{4}{2} + \binom{5}{3} = 1 + 3 + 6 + 10 = 20 = \binom{6}{3}$.

## Consequences

- **Sums of integers.** With $k = 1$: $\sum_{i=1}^{n} i = \binom{n+1}{2} = n(n+1)/2$, for example $1 + 2 + \cdots + 100 = 5050 = \binom{101}{2}$. With $k = 2$: $\sum_{i=2}^{n} \binom{i}{2} = \binom{n+1}{3}$, the tetrahedral numbers.
- **Sums of powers.** Write a power in the basis of binomials and sum each column. Since $i^2 = 2\binom{i}{2} + \binom{i}{1}$, $\sum_{i=1}^{n} i^2 = 2\binom{n+1}{3} + \binom{n+1}{2} = n(n+1)(2n+1)/6$; for $n = 10$ both give $385$. Every polynomial sum $\sum_{i \le n} P(i)$ is found this way, which is the discrete analogue of integrating a polynomial (Concrete Mathematics, Chapter 5 and Section 2.6).
- **Nested loops.** The loops `for i1 in 1..n, for i2 in i1+1..n, ..., for ik in i(k-1)+1..n` run their body once for each $k$-subset of $[n]$, so $\binom{n}{k}$ times. Summing the innermost loop gives $n - i_{k-1}$, and the hockey-stick identity, applied once per level, collapses the sums to $\binom{n}{k}$. For $n = 10$ and three nested loops this is $120$ iterations. Loops with $\le$ instead of $<$ run $\binom{n+k-1}{k}$ times, the number of [combinations with repetition](/combinations-with-repetition/).
- **Multisets.** The parallel form is the recurrence of [stars and bars](/stars-and-bars/): the number $\binom{a+r+1}{r}$ of multisets of size $r$ from $a + 2$ kinds splits by how many copies of the last kind are used.
- **Prefix sums of a column.** In a table of [Pascal's triangle](/pascal-triangle-dp/), the prefix sums of column $k$ are column $k + 1$, so a query $\sum_{i=s}^{n} \binom{i}{k}$ costs $O(1)$ with the shifted form.
- **Lattice paths.** $\binom{n+1}{k+1}$ counts the monotone [lattice paths](/counting-lattice-paths/) with $k + 1$ up steps and $n - k$ right steps. Classifying them by the position of the last up step gives the identity, which is the combinatorial proof in the language of paths.

## Tightness

- **The range of $k$.** The identity needs $k \ge 0$. For $k = -1$ the left side is $0$, since all terms vanish, while $\binom{n+1}{0} = 1$.
- **The range of the sum.** The sum must start at the top of the column. Starting at $i = s > k$ removes $\binom{s}{k+1}$, by the shifted form; for $k = 2$, $s = 4$, $n = 6$ the sum is $6 + 10 + 15 = 31 = 35 - 4$.
- **Rows instead of columns.** Summing a row gives $2^n$, not a single entry, and summing a diagonal $\sum_j \binom{n-j}{j}$ gives the Fibonacci number $F_{n+1}$, not a binomial coefficient. Only columns and the parallel diagonals give one entry.

## History

The pattern of adding a column of the arithmetic triangle appears in the Chinese, Persian and Indian work on the triangle long before Pascal, and the name "hockey stick" comes from the modern picture of the triangle. Concrete Mathematics (Section 5.1) calls the column form "upper summation" and the diagonal form "parallel summation", and lists both among the basic identities. Some texts call it the Christmas stocking identity, after the shape drawn on the triangle with the blade at the bottom.

## References
