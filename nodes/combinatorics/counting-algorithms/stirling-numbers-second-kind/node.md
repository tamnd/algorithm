---
tag: 8HF649
kind: definition
slug: stirling-numbers-second-kind
name: Stirling numbers of the second kind
aliases:
- S(n,k)
- set partition numbers
- Stirling set numbers
area: combinatorics/counting-algorithms
level: core
summary: Number of ways to partition n elements into k nonempty blocks.
prereqs: [binomial-coefficient, set-partitions]
see_also: [bell-numbers, stirling-numbers-first-kind, counting-set-partitions, set-partition-generation, restricted-growth-string, inclusion-exclusion-principle, exponential-generating-functions, stirling-numbers]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.1, Stirling Numbers (Table 258, the recurrence 6.3 and the conversion formula 6.10)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.9, The twelvefold way (set partitions and S(n,k))
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.6, Binomial Coefficients (the Stirling numbers, equations 40 to 52)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Section II.3, Surjections, set partitions, and words
---

The Stirling number of the second kind $S(n, k)$, also written ${n \brace k}$, is the number of ways to split a set of $n$ elements into $k$ nonempty blocks, when neither the blocks nor the elements inside a block have an order. For example, $S(4, 2) = 7$. Summed over $k$ these numbers give the [Bell numbers](/bell-numbers/), and $k!\, S(n, k)$ is the number of maps from an $n$-set onto a $k$-set. They also convert ordinary powers $x^n$ into falling factorials, which makes them a tool for sums of powers and for moments of random variables.

## Definition

**Notation.** $n \ge 0$ is the size of the ground set $[n] = \{1, \ldots, n\}$ and $k \ge 0$ is the number of blocks. A [set partition](/set-partitions/) of $[n]$ is a set of nonempty, pairwise disjoint subsets of $[n]$, the *blocks*, whose union is $[n]$.

For integers $n, k \ge 0$,

$$S(n, k) = \bigl|\{\pi : \pi \text{ is a set partition of } [n] \text{ with exactly } k \text{ blocks}\}\bigr|.$$

The empty set has one partition, with no blocks, so $S(0, 0) = 1$. For $n \ge 1$, $S(n, 0) = 0$, and $S(n, k) = 0$ for $k > n$, since each block holds at least one element.

**Recurrence.** For $n \ge 1$ and $k \ge 1$,

$$S(n, k) = k\, S(n-1, k) + S(n-1, k-1).$$

*Proof.* Split the partitions of $[n]$ into $k$ blocks by the block of the element $n$. If $\{n\}$ is a block, removing it leaves a partition of $[n-1]$ into $k - 1$ blocks, and each such partition arises once: $S(n-1, k-1)$ cases. Otherwise, removing $n$ from its block leaves a partition of $[n-1]$ into $k$ blocks, and each such partition arises from exactly $k$ partitions of $[n]$, one for each block that $n$ can join: $k\, S(n-1, k)$ cases. $\square$

**Explicit formula.** For $n, k \ge 0$,

$$S(n, k) = \frac{1}{k!} \sum_{j=0}^{k} (-1)^{k-j} \binom{k}{j} j^n.$$

*Proof.* A map from $[n]$ onto $[k]$ is the same thing as a partition of $[n]$ into $k$ blocks (the nonempty fibers) together with a one to one assignment of the $k$ values to the blocks. So there are $k!\, S(n, k)$ such maps. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/) over the set $T \subseteq [k]$ of values that are missed, the number of onto maps is $\sum_{T} (-1)^{|T|} (k - |T|)^n = \sum_{i=0}^{k} (-1)^i \binom{k}{i} (k - i)^n$. Put $j = k - i$. $\square$ With $0^0 = 1$ the formula also gives $S(0, 0) = 1$.

**Powers and falling factorials.** With $x^{\underline k} = x(x-1)\cdots(x-k+1)$ and $x^{\underline 0} = 1$,

$$x^n = \sum_{k=0}^{n} S(n, k)\, x^{\underline k}.$$

*Proof.* For a positive integer $x$, the left side counts the maps from $[n]$ to $[x]$. Group them by the partition of $[n]$ into nonempty fibers. For a partition with $k$ blocks, the maps that have it give distinct values to the $k$ blocks, which can be done in $x^{\underline k}$ ways. So both sides agree at every positive integer $x$. Both sides are polynomials in $x$ of degree $n$, and two polynomials that agree at infinitely many points are equal. $\square$

**Generating functions.** For each fixed $k \ge 0$,

$$\sum_{n \ge 0} S(n, k)\, z^n = \frac{z^k}{(1 - z)(1 - 2z)\cdots(1 - kz)}, \qquad \sum_{n \ge 0} S(n, k) \frac{z^n}{n!} = \frac{(e^z - 1)^k}{k!}.$$

*Proof.* Let $G_k(z)$ be the left sum. The recurrence holds for all $n \ge 1$, and $S(0, k) = 0$ for $k \ge 1$, so multiplying by $z^n$ and summing gives $G_k = k z G_k + z G_{k-1}$ for $k \ge 1$, with $G_0 = 1$. So $G_k = \frac{z}{1 - kz} G_{k-1}$, and induction on $k$ gives the product. The [exponential generating function](/exponential-generating-functions/) of the nonempty sets is $e^z - 1$, and a set of $k$ of them on a split of $[n]$ has the series $(e^z - 1)^k / k!$ by the exponential formula. $\square$

### Computing the numbers

- **The table.** The recurrence fills the triangle $S(m, j)$ for $m \le n$ and $j \le k$ in $O(nk)$ additions and multiplications by small integers. Exact values have up to about $n \lg k$ bits, since $S(n, k) \le k^n / k!$, so the bit cost is $O(n^2 k \log k)$. Modulo a prime $p$, the cost is $O(nk)$ word operations.
- **One value.** The explicit formula gives $S(n, k)$ with $k + 1$ terms. Modulo a prime $p > k$, each power $j^n$ costs $O(\log n)$ by [binary exponentiation](/binary-exponentiation/), so one value costs $O(k \log n)$.
- **One row.** The explicit formula is a convolution: $S(n, k) = \sum_j \frac{j^n}{j!} \cdot \frac{(-1)^{k-j}}{(k-j)!}$. So all of $S(n, 0), \ldots, S(n, n)$ modulo a suitable prime $p > n$ come from one product of polynomials of degree $n$, in $O(n \log n)$ time with the [number-theoretic transform](/number-theoretic-transform/).
- **Floating point.** The alternating sum cancels badly in floating point. Use exact integers or residues.

## Examples and non-examples

**Example 1.** $S(4, 2) = 7$. The partitions of $\{1, 2, 3, 4\}$ into two blocks are

$$1|234, \quad 2|134, \quad 3|124, \quad 4|123, \quad 12|34, \quad 13|24, \quad 14|23.$$

The recurrence gives $2\, S(3, 2) + S(3, 1) = 2 \cdot 3 + 1 = 7$, and the explicit formula gives $\frac{1}{2}(2^4 - 2 \cdot 1^4 + 0) = 7$.

**Example 2.** The triangle for $n = 0$ to $7$ and $k = 0$ to $7$ (OEIS A008277 lists it without the column $k = 0$).

| n \ k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | sum |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| 3 | 0 | 1 | 3 | 1 | 0 | 0 | 0 | 0 | 5 |
| 4 | 0 | 1 | 7 | 6 | 1 | 0 | 0 | 0 | 15 |
| 5 | 0 | 1 | 15 | 25 | 10 | 1 | 0 | 0 | 52 |
| 6 | 0 | 1 | 31 | 90 | 65 | 15 | 1 | 0 | 203 |
| 7 | 0 | 1 | 63 | 301 | 350 | 140 | 21 | 1 | 877 |

The row sums are the [Bell numbers](/bell-numbers/).

**Example 3: special values.** $S(n, 1) = 1$ and $S(n, n) = 1$ for $n \ge 1$. $S(n, 2) = 2^{n-1} - 1$ for $n \ge 1$: a partition into two blocks is fixed by the block of the element 1 minus that element, which can be any subset of the other $n - 1$ elements except all of them. $S(n, n-1) = \binom{n}{2}$ for $n \ge 1$: one block has two elements and the others are single.

**Example 4: a sum of powers.** $x^3 = x^{\underline 1} + 3 x^{\underline 2} + x^{\underline 3}$. Since $\sum_{x=0}^{m-1} x^{\underline k} = m^{\underline{k+1}}/(k+1)$, this gives $\sum_{x=0}^{m-1} x^3 = \frac{m^{\underline 2}}{2} + m^{\underline 3} + \frac{m^{\underline 4}}{4}$. At $m = 4$ the sum is $0 + 1 + 8 + 27 = 36$, and the right side is $6 + 24 + 6 = 36$.

**Example 5: balls in boxes.** The number of ways to put $10$ different balls into $3$ identical boxes with no box empty is $S(10, 3) = 9330$. With distinct boxes, it is $3! \cdot 9330 = 55980$.

**Non-example 1: ordered blocks.** $1|23$ and $23|1$ are the same partition. A count that lists blocks in order is $k!\, S(n, k)$, the number of onto maps, or the ordered set partitions.

**Non-example 2: empty blocks.** Splitting $[n]$ into $k$ blocks where blocks may be empty is not counted by $S(n, k)$. With identical boxes, it is $\sum_{j=0}^{k} S(n, j)$.

**Non-example 3: identical elements.** Splitting the number $n$ into $k$ parts, with identical units, counts integer partitions with $k$ parts, not $S(n, k)$. For $n = 4$ and $k = 2$ there are 2 such partitions ($3 + 1$ and $2 + 2$), not 7.

## Related definitions

- [Bell numbers](/bell-numbers/): $B_n = \sum_k S(n, k)$, all partitions of an $n$-set.
- [Stirling numbers of the first kind](/stirling-numbers-first-kind/): they count permutations by cycles. The two kinds are inverse matrices: $\sum_k S(n, k)\, s(k, m) = [n = m]$, with the signed numbers $s(k, m)$.
- [Restricted growth strings](/restricted-growth-string/) encode a partition of $[n]$ into $k$ blocks as a string with maximum $k - 1$, and [set partition generation](/set-partition-generation/) lists them.
- [Counting set partitions](/counting-set-partitions/) is the problem of computing $B_n$ and $S(n, k)$.
- [Eulerian numbers](/eulerian-numbers/) are linked by Worpitzky's identity, and $k!\, S(n, k)$ appears in the ordered Bell numbers $\sum_k k!\, S(n, k)$.
- The [Stirling numbers](/stirling-numbers/) concept page of the partitions area gives the generation view of the same numbers.

## References
