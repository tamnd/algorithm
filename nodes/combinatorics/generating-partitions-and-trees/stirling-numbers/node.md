---
tag: N8R660
kind: concept
slug: stirling-numbers
name: Stirling numbers of the second kind
aliases:
- Stirling numbers S(n,k)
- Stirling set numbers
area: combinatorics/generating-partitions-and-trees
level: core
summary: S(n,k) counts the partitions of an n-element set into exactly k nonempty blocks; they satisfy S(n,k) = k S(n-1,k) + S(n-1,k-1) and sum to the Bell number B_n.
prereqs: [set-partitions]
see_also: [stirling-numbers-second-kind, stirling-numbers-first-kind, bell-numbers, restricted-growth-string, set-partition-generation, inclusion-exclusion-principle, exponential-generating-functions, binomial-coefficient]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 6.1, Stirling numbers (the recurrence, the triangle, and the conversion between ordinary powers and falling powers)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.9, The twelvefold way (Stirling numbers of the second kind, surjections and the explicit formula)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (the Stirling numbers as counts of restricted growth strings with a given number of blocks)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (set partitions with k blocks and the generating function (e^z - 1)^k / k!)
---

The Stirling number of the second kind $S(n, k)$ is the number of ways to partition a set of $n$ elements into exactly $k$ nonempty blocks. The triangle of these numbers follows the recurrence $S(n, k) = k\, S(n-1, k) + S(n-1, k-1)$, its row sums are the Bell numbers, and $k!\, S(n, k)$ counts the maps from an $n$-set onto a $k$-set. They also convert ordinary powers $x^n$ into falling powers $x(x-1)\cdots(x-k+1)$, which is why they appear in sums of powers, in moments and in occupancy problems.

## In plain words

Take a group of different people and split them into a fixed number of teams. Teams have no names, and no team may be empty. The Stirling number counts these splits. With four people and two teams there are seven splits: one person alone and three together in four ways, and two pairs in three ways.

To count the splits for one more person, look at where the new person goes. They can join one of the existing teams, or they can form a new team alone. This simple rule fills a whole triangle of counts, one row at a time.

## The idea

**Notation.** $n, k \ge 0$ are integers, $[n] = \{1, \ldots, n\}$, $C(n, k) = \binom{n}{k}$, and $x^{\underline k} = x (x - 1) \cdots (x - k + 1)$ is the falling power, with $x^{\underline 0} = 1$. Graham, Knuth and Patashnik write $S(n, k)$ as $\left\{ n \atop k \right\}$.

**Definition.** $S(n, k)$ is the number of [partitions](/set-partitions/) of $[n]$ into exactly $k$ nonempty blocks. So $S(0, 0) = 1$, $S(n, 0) = 0$ for $n \ge 1$, and $S(n, k) = 0$ for $k > n$. In [restricted growth string](/restricted-growth-string/) form, $S(n, k)$ counts the strings with maximum $k - 1$.

**The recurrence.** For $n, k \ge 1$,

$$S(n, k) = k\, S(n - 1, k) + S(n - 1, k - 1).$$

*Proof.* Remove $n$ from a partition of $[n]$ into $k$ blocks. If $\{n\}$ was a block, what remains is a partition of $[n - 1]$ into $k - 1$ blocks. Otherwise what remains is a partition of $[n - 1]$ into $k$ blocks, and $n$ was in one of its $k$ blocks. Each partition of $[n - 1]$ arises in this way from exactly one partition of $[n]$ for each choice. $\square$

**Surjections and the explicit formula.** A map from $[n]$ onto $[k]$ is a partition into $k$ blocks with the blocks numbered, so there are $k!\, S(n, k)$ such maps. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/) over the set of values that are missed,

$$k!\, S(n, k) = \sum_{j=0}^{k} (-1)^j\, C(k, j)\, (k - j)^n.$$

*Proof.* For $J \subseteq [k]$ with $|J| = j$, the maps $[n] \to [k] \setminus J$ number $(k - j)^n$. Inclusion-exclusion over $J$ counts the maps that miss no value. $\square$

**Powers and falling powers.** For every integer $x \ge 0$, and so as an identity of polynomials,

$$x^n = \sum_{k=0}^{n} S(n, k)\, x^{\underline k}.$$

*Proof.* Count the maps $[n] \to [x]$. The left side counts them directly. On the right, group the maps by the partition of $[n]$ into the nonempty fibers: for a partition with $k$ blocks, there are $x^{\underline k}$ ways to give the blocks distinct values. Both sides are polynomials of degree $n$ in $x$ that agree at infinitely many points. $\square$

**Generating functions.** For a fixed $k$, $\sum_{n} S(n, k)\, x^n = \dfrac{x^k}{(1 - x)(1 - 2x) \cdots (1 - kx)}$, which follows from the recurrence by induction on $k$, and $\sum_n S(n, k) \frac{x^n}{n!} = \frac{(e^x - 1)^k}{k!}$, a set of $k$ nonempty blocks in the language of [exponential generating functions](/exponential-generating-functions/).

**Special values.** $S(n, 1) = S(n, n) = 1$ for $n \ge 1$, $S(n, 2) = 2^{n-1} - 1$ (choose the block of $1$, minus the case with no second block), and $S(n, n - 1) = C(n, 2)$ (one block of size $2$).

**Cost of computing them.**

- *A row or a triangle, exactly.* The recurrence gives all $S(m, k)$ for $m \le n$ in $O(n^2)$ additions and small multiplications of big integers. The numbers are exact integers at most $B_n \le n!$, so they have $O(n \log n)$ bits.
- *One value, exactly.* The explicit formula needs $k + 1$ powers $(k - j)^n$ of $O(n \log k)$ bits each.
- *A row modulo a prime $p$.* Write $S(n, k) = \sum_{j} \frac{(-1)^{k-j}}{(k-j)!} \cdot \frac{j^n}{j!}$. For $n < p$ this is one convolution of two sequences of length $n + 1$, so [FFT multiplication](/fft-polynomial-multiplication/) over a suitable prime gives the row in $O(n \log n)$ operations.

**The first kind.** The Stirling numbers of the [first kind](/stirling-numbers-first-kind/) count permutations by cycles and convert falling powers back into ordinary powers. The two triangles, with signs, are inverse matrices.

## Examples

**The triangle.** Rows $n = 0$ to $7$, with $k = 0, \ldots, n$:

| $n$ | $S(n, 0), \ldots, S(n, n)$ | $B_n$ |
| --- | --- | --- |
| $0$ | $1$ | $1$ |
| $1$ | $0, 1$ | $1$ |
| $2$ | $0, 1, 1$ | $2$ |
| $3$ | $0, 1, 3, 1$ | $5$ |
| $4$ | $0, 1, 7, 6, 1$ | $15$ |
| $5$ | $0, 1, 15, 25, 10, 1$ | $52$ |
| $6$ | $0, 1, 31, 90, 65, 15, 1$ | $203$ |
| $7$ | $0, 1, 63, 301, 350, 140, 21, 1$ | $877$ |

For example $S(5, 3) = 3 \cdot S(4, 3) + S(4, 2) = 3 \cdot 6 + 7 = 25$.

**A larger row.** For $n = 10$ the row is $0, 1, 511, 9330, 34105, 42525, 22827, 5880, 750, 45, 1$, with sum $B_{10} = 115975$. The largest entry is at $k = 5$.

**The explicit formula.** $S(4, 2) = \frac{1}{2}\big(2^4 - 2 \cdot 1^4 + 1 \cdot 0^4\big) = \frac{16 - 2}{2} = 7$.

**Powers.** $x^3 = x^{\underline 1} + 3 x^{\underline 2} + x^{\underline 3}$. At $x = 2$ this is $8 = 2 + 6 + 0$.

## Where it is used

- **Set partition generation.** $S(n, k)$ is the length of the list of partitions with $k$ blocks, and the counts of completions in [Algorithm H](/set-partition-generation/) and in the rank of an RGS refine the recurrence.
- **Surjections and occupancy.** Throw $n$ keys into $m$ hash bins uniformly. The chance that exactly $k$ bins are used is $S(n, k)\, m^{\underline k} / m^n$. The same count gives the coupon collector distribution.
- **Sums of powers.** Since $\sum_{i=0}^{N} i^{\underline k} = \frac{(N + 1)^{\underline{k+1}}}{k + 1}$, the identity for powers gives $\sum_{i=0}^{N} i^n = \sum_k S(n, k) \frac{(N+1)^{\underline{k+1}}}{k + 1}$.
- **Moments.** For a Poisson variable $X$ with mean $\lambda$, $E[X^{\underline k}] = \lambda^k$, so $E[X^n] = \sum_k S(n, k)\, \lambda^k$. With $\lambda = 1$ this is the Bell number $B_n$.
- **Finite differences.** $k!\, S(n, k)$ is the $k$-th forward difference of $x^n$ at $x = 0$, which is another way to read the explicit formula.
- **The twelvefold way.** $S(n, k)$ counts the ways to put $n$ labeled balls into $k$ unlabeled boxes with no box empty, one entry of Stanley's table in Section 1.9.

## References
