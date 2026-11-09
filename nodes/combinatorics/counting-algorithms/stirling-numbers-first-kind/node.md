---
tag: W0GNH4
kind: definition
slug: stirling-numbers-first-kind
name: Stirling numbers of the first kind
aliases:
- unsigned Stirling numbers
- s(n,k)
- Stirling cycle numbers
- c(n,k)
area: combinatorics/counting-algorithms
level: core
summary: Counts permutations of n elements with k cycles.
prereqs: [permutation-cycle-decomposition, binomial-coefficient]
see_also: [stirling-numbers-second-kind, permutation-cycle-decomposition, bell-numbers, eulerian-numbers, exponential-generating-functions, harmonic-series, factorial, derangement]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.1, Stirling Numbers (Table 259, the recurrence 6.8, and the conversions 6.11 to 6.14)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3, Cycles and inversions (the numbers c(n,k) and s(n,k))
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.6 (Stirling numbers) and Section 1.2.10, Analysis of an Algorithm (the number of changes of the maximum)
---

The unsigned Stirling number of the first kind $c(n, k)$, also written ${n \brack k}$, is the number of permutations of $n$ elements that have exactly $k$ cycles. For example, $c(4, 2) = 11$. The numbers are the coefficients of the rising factorial $x(x+1)\cdots(x+n-1)$, and with signs they convert falling factorials back to powers, so they are the inverse of the [Stirling numbers of the second kind](/stirling-numbers-second-kind/). In the analysis of algorithms they give the distribution of the number of cycles of a random permutation and of the number of times a running maximum changes.

## Definition

**Notation.** $n \ge 0$ is the number of elements and $k \ge 0$ the number of cycles. $S_n$ is the set of the $n!$ permutations of $[n] = \{1, \ldots, n\}$. Each permutation splits $[n]$ into disjoint cycles, by its [cycle decomposition](/permutation-cycle-decomposition/), and a fixed point is a cycle of length 1.

For integers $n, k \ge 0$,

$$c(n, k) = \bigl|\{\sigma \in S_n : \sigma \text{ has exactly } k \text{ cycles}\}\bigr|.$$

The empty permutation has no cycles, so $c(0, 0) = 1$. For $n \ge 1$, $c(n, 0) = 0$, and $c(n, k) = 0$ for $k > n$. The *signed* Stirling numbers are $s(n, k) = (-1)^{n-k} c(n, k)$. Books differ here: Stanley writes $c(n, k)$ for the unsigned and $s(n, k)$ for the signed numbers, as this page does, and Concrete Mathematics writes ${n \brack k}$ for the unsigned ones.

**Recurrence.** For $n \ge 1$ and $k \ge 1$,

$$c(n, k) = (n - 1)\, c(n-1, k) + c(n-1, k-1).$$

*Proof.* Split the permutations of $[n]$ with $k$ cycles by the element $n$. If $n$ is a fixed point, removing the cycle $(n)$ leaves a permutation of $[n-1]$ with $k - 1$ cycles, and each one arises once. Otherwise, $n$ sits in a cycle $(\ldots\, a\; n\; b \ldots)$, and removing $n$, so that $a$ maps to $b$, leaves a permutation of $[n-1]$ with $k$ cycles. Conversely, from such a permutation, $n$ can be put right after any of the $n - 1$ elements $a$, and these $n - 1$ choices give different permutations of $[n]$. So this case has $(n-1)\, c(n-1, k)$ members. $\square$

**Rising factorials.** For $n \ge 0$,

$$x^{\overline n} = x(x+1)\cdots(x+n-1) = \sum_{k=0}^{n} c(n, k)\, x^k, \qquad x^{\underline n} = x(x-1)\cdots(x-n+1) = \sum_{k=0}^{n} s(n, k)\, x^k.$$

*Proof.* Let $r(n, k)$ be the coefficient of $x^k$ in $x^{\overline n}$. Then $r(0, 0) = 1$ and $r(0, k) = 0$ for $k \ne 0$. From $x^{\overline n} = x^{\overline{n-1}} \cdot (x + n - 1)$ we get $r(n, k) = (n-1)\, r(n-1, k) + r(n-1, k-1)$, the same recurrence with the same initial values as $c(n, k)$, so $r = c$ by induction on $n$. For the second identity, $x^{\underline n} = (-1)^n (-x)^{\overline n} = \sum_k (-1)^{n-k} c(n, k)\, x^k$. $\square$

**Inverse of the second kind.** For all $n, m \ge 0$, $\sum_{k} S(n, k)\, s(k, m) = [n = m]$. *Proof.* Put the second identity into $x^n = \sum_k S(n, k)\, x^{\underline k}$ from the page on the second kind: $x^n = \sum_m \bigl(\sum_k S(n, k)\, s(k, m)\bigr) x^m$, and compare the coefficients. $\square$

**Generating functions.** The [exponential generating function](/exponential-generating-functions/) of one cycle is $\log \frac{1}{1 - z}$, so by the exponential formula,

$$\sum_{n \ge 0} c(n, k) \frac{z^n}{n!} = \frac{1}{k!} \Bigl(\log \frac{1}{1 - z}\Bigr)^k, \qquad \sum_{n, k} c(n, k)\, u^k \frac{z^n}{n!} = (1 - z)^{-u}.$$

**Mean number of cycles.** A uniformly random permutation of $[n]$ has $H_n = 1 + \frac12 + \cdots + \frac1n$ cycles on average. *Proof.* The mean is $\frac{1}{n!} \sum_k k\, c(n, k)$, which is $\frac{1}{n!} \frac{d}{dx} x^{\overline n}$ at $x = 1$. Since $1^{\overline n} = n!$ and $\frac{d}{dx} \log x^{\overline n} = \sum_{i=0}^{n-1} \frac{1}{x + i}$, the value is $\sum_{i=0}^{n-1} \frac{1}{1 + i} = H_n$. $\square$ So the number of cycles is about $\ln n$, see the [harmonic series](/harmonic-series/).

### Computing the numbers

- **The table.** The recurrence fills $c(m, j)$ for $m \le n$ and $j \le k$ in $O(nk)$ operations. The numbers are at most $n!$, so they have $O(n \log n)$ bits.
- **One row.** Row $n$ is the coefficient list of $x^{\overline n}$. Multiplying the factors one at a time costs $O(n^2)$ operations. Modulo a suitable prime, a balanced product tree with [FFT multiplication](/fft-polynomial-multiplication/) costs $O(n \log^2 n)$.
- **The signs.** A program that uses $s(n, k)$ where $c(n, k)$ is meant gets negative counts for odd $n - k$. Keep the two names apart.

## Examples and non-examples

**Example 1.** $c(4, 2) = 11$. The permutations of $[4]$ with two cycles are the 8 permutations of type "a fixed point and a 3-cycle", $(1)(2\,3\,4)$, $(1)(2\,4\,3)$, $(2)(1\,3\,4)$, $(2)(1\,4\,3)$, $(3)(1\,2\,4)$, $(3)(1\,4\,2)$, $(4)(1\,2\,3)$, $(4)(1\,3\,2)$, and the 3 of type "two 2-cycles", $(1\,2)(3\,4)$, $(1\,3)(2\,4)$, $(1\,4)(2\,3)$. The recurrence gives $3\, c(3, 2) + c(3, 1) = 3 \cdot 3 + 2 = 11$.

**Example 2.** The triangle of $c(n, k)$ for $n = 0$ to $7$ (OEIS A132393; the signed form is A008275).

| n \ k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | sum |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| 3 | 0 | 2 | 3 | 1 | 0 | 0 | 0 | 0 | 6 |
| 4 | 0 | 6 | 11 | 6 | 1 | 0 | 0 | 0 | 24 |
| 5 | 0 | 24 | 50 | 35 | 10 | 1 | 0 | 0 | 120 |
| 6 | 0 | 120 | 274 | 225 | 85 | 15 | 1 | 0 | 720 |
| 7 | 0 | 720 | 1764 | 1624 | 735 | 175 | 21 | 1 | 5040 |

Each row sums to $n!$, because each permutation has some number of cycles.

**Example 3: special values.** $c(n, 1) = (n-1)!$, the number of cyclic orders of $[n]$. $c(n, n-1) = \binom{n}{2}$, since one cycle is a transposition and the rest are fixed points. $c(n+1, 2) = n!\, H_n$, for example $c(5, 2) = 24 \cdot \frac{25}{12} = 50$.

**Example 4: a falling factorial.** $x^{\underline 3} = x^3 - 3x^2 + 2x$, so $s(3, 3) = 1$, $s(3, 2) = -3$, $s(3, 1) = 2$.

**Example 5: the running maximum.** A loop that scans $n$ distinct keys in random order and updates the maximum when a key is larger than all before it makes $k$ updates, the first one included, with probability $c(n, k)/n!$. The positions of these left-to-right maxima split the permutation into $k$ runs, and the map that reads each run as a cycle is a bijection onto the permutations with $k$ cycles. So the mean number of updates is $H_n$.

**Non-example 1: cycle type.** $c(n, k)$ does not depend on the lengths of the cycles. The number of permutations with a given cycle type $1^{m_1} 2^{m_2} \cdots$ is $n!/\prod_j j^{m_j} m_j!$, a single term of the sum that makes $c(n, k)$.

**Non-example 2: set partitions.** Two permutations with the same cycles as sets but a different order inside a cycle, such as $(1\,2\,3)$ and $(1\,3\,2)$, are different, so $c(n, k) \ge S(n, k)$. A block of $j$ elements carries $(j-1)!$ cycles, so for $n \ge 1$ the two numbers are equal exactly when $k \ge n - 1$, where no block has more than 2 elements. For example $c(3, 2) = S(3, 2) = 3$, but $c(3, 1) = 2 > S(3, 1) = 1$.

**Non-example 3: descents.** The number of permutations of $[n]$ with $k$ descents is an [Eulerian number](/eulerian-numbers/), not $c(n, k + 1)$. For $n = 3$ the Eulerian row is $1, 4, 1$, and the cycle row is $2, 3, 1$.

## Related definitions

- [Stirling numbers of the second kind](/stirling-numbers-second-kind/) count set partitions, and the signed first kind is their inverse matrix.
- The [cycle decomposition](/permutation-cycle-decomposition/) of a permutation is the structure that $c(n, k)$ counts.
- [Derangements](/derangement/) are the permutations with no cycle of length 1.
- [Eulerian numbers](/eulerian-numbers/) count permutations by descents, a different statistic with the same row sums $n!$.
- The [harmonic series](/harmonic-series/) gives the mean number of cycles, $H_n$.
- [Exponential generating functions](/exponential-generating-functions/) give the series $(1 - z)^{-u}$ through the exponential formula.

## References
