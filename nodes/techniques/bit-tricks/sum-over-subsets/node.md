---
tag: E5P198
kind: problem
slug: sum-over-subsets
name: Sum over subsets
aliases:
- subset sums for all masks
- zeta transform over subsets
area: techniques/bit-tricks
level: advanced
summary: For every mask, computing the sum of f over all submasks of that mask.
model: word-ram
complexity:
  vars: {n: the number of bits of a mask, so the input has 2^n values}
  time: {worst: O(n 2^n)}
prereqs: [bitmask, submask-enumeration, mobius-inversion]
see_also: [sos-dp, sum-over-subsets-dp, submask-enumeration, fast-walsh-hadamard-transform, inclusion-exclusion-principle, bjorklund-chromatic-number, bitmask-dp]
sources:
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 7, Subset Convolution, Section 7.1, Fast zeta Transform, and Section 7.2, Fast Subset Convolution
  - paper: doi:10.1145/1250790.1250801
    title: Andreas Björklund, Thore Husfeldt, Petteri Kaski and Mikko Koivisto, Fourier meets Möbius, fast subset convolution, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC), 2007
    locator: pp. 67 to 74
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

The sum over subsets problem takes a function $f$ on the $2^n$ subsets of an $n$-element set and asks, for every subset $m$, for $F(m) = \sum_{s \subseteq m} f(s)$. The map $f \mapsto F$ is the zeta transform of the lattice of subsets, and its inverse is [Möbius inversion](/mobius-inversion/). The direct method with [submask enumeration](/submask-enumeration/) does $3^n$ additions, and [SOS DP](/sos-dp/) does $n 2^{n-1}$ additions. The transform is the core step of fast subset convolution, of inclusion-exclusion algorithms such as [Björklund's chromatic number algorithm](/bjorklund-chromatic-number/), and of many [bitmask DP](/bitmask-dp/) problems.

## In plain words

You have a small set of items, for example ten items. Each group of items has a number attached to it. For every group, you want the total of the numbers of all its smaller groups, including the empty group and the group itself.

Doing this group by group adds up the same numbers many times. With ten items there are about a thousand groups, and the plain method does about sixty thousand additions. A better method adds the items one at a time and reuses the totals already found, and it needs only about five thousand additions.

The groups are usually stored as rows of on and off switches, so the problem is about bit masks.

## Definition

**Input.** An integer $n \ge 0$ and an array $f[0 \ldots 2^n - 1]$ of values in a commutative monoid $(R, +, 0)$, for example the integers under addition. Index $m$ stands for the set $\{\, i : \text{bit } i \text{ of } m \text{ is } 1 \,\}$, and $s \subseteq m$ means $s \mathbin{\&} \lnot m = 0$.

**Output.** The array $F = \zeta f$ with
$$ F[m] = \sum_{s \subseteq m} f[s] \qquad \text{for all } 0 \le m < 2^n . $$

**Inverse.** If $R$ is a commutative group, $\zeta$ is a bijection, and its inverse is the Möbius transform
$$ f[m] = \sum_{s \subseteq m} (-1)^{\operatorname{pop}(m) - \operatorname{pop}(s)} F[s] . $$
This is [Möbius inversion](/mobius-inversion/) on the lattice of subsets, the algebraic form of the [inclusion-exclusion principle](/inclusion-exclusion-principle/).

**Monoid.** Only associativity, commutativity and the identity of $+$ are used by the transform. So $+$ can be $\max$, $\min$, OR or $\gcd$; the inverse then does not exist in general.

## Variants

- **Sum over supersets.** $G[m] = \sum_{s \supseteq m} f[s]$. Complement the indices, $G[m] = F'[\lnot m]$ where $F'$ is the zeta transform of $s \mapsto f[\lnot s]$, or run SOS DP with the test of the bit reversed.
- **Möbius transform.** Given $F$, find $f$. Same cost as the zeta transform, with subtraction.
- **OR convolution.** $h[m] = \sum_{a \mathbin{|} b = m} f[a] \, g[b]$. Since $\zeta h = \zeta f \cdot \zeta g$ pointwise, $h = \mu(\zeta f \cdot \zeta g)$, where $\mu$ is the Möbius transform: three transforms and $2^n$ products.
- **AND convolution.** $h[m] = \sum_{a \mathbin{\&} b = m} f[a] \, g[b]$, the same with sums over supersets.
- **Subset convolution.** $h[m] = \sum_{s \subseteq m} f[s] \, g[m \setminus s]$, where the two parts must be disjoint. Björklund, Husfeldt, Kaski and Koivisto compute it with $O(n^2 2^n)$ ring operations by zeta transforms ranked by the number of ones.
- **XOR convolution.** $h[m] = \sum_{a \oplus b = m} f[a] \, g[b]$. This is not a sum over subsets; it uses the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/).
- **Counting form.** $f$ is the indicator of a set $A$ of masks, and $F[m]$ counts the members of $A$ that are submasks of $m$.

## Examples

For $n = 2$ and $f = [1, 2, 3, 4]$ (indices $00, 01, 10, 11$), $F = [1, 1 + 2, 1 + 3, 1 + 2 + 3 + 4] = [1, 3, 4, 10]$.

For $n = 3$ and $f = [3, 1, 4, 1, 5, 9, 2, 6]$:

| $m$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $f[m]$ | 3 | 1 | 4 | 1 | 5 | 9 | 2 | 6 |
| $F[m]$, subsets | 3 | 4 | 7 | 9 | 8 | 18 | 14 | 31 |
| $G[m]$, supersets | 31 | 17 | 13 | 7 | 22 | 15 | 8 | 6 |

For example $F[101_2] = f[000] + f[001] + f[100] + f[101] = 3 + 1 + 5 + 9 = 18$, and $G[010_2] = f[010] + f[011] + f[110] + f[111] = 4 + 1 + 2 + 6 = 13$. The Möbius transform of the row $F$ gives back the row $f$.

OR convolution, $n = 2$: with $f = [1, 2, 0, 1]$ and $g = [0, 1, 1, 1]$, $\zeta f = [1, 3, 1, 4]$, $\zeta g = [0, 1, 1, 3]$, the pointwise product is $[0, 3, 1, 12]$, and its Möbius transform is $h = [0, 3, 1, 8]$, which equals the direct sum over all pairs $(a, b)$ with $a \mathbin{|} b = m$.

A non-example: the sum over the masks $s \le m$ in numeric order is a prefix sum, not a sum over subsets. For $m = 2 = 10_2$ it includes $s = 1 = 01_2$, which is not a submask of $10_2$.

## Known algorithms

- Direct: for each $m$, [submask enumeration](/submask-enumeration/) over the $2^{\operatorname{pop}(m)}$ submasks. In all $\sum_m 2^{\operatorname{pop}(m)} = 3^n$ terms, so $3^n - 2^n$ additions.
- [SOS DP](/sos-dp/), also called the fast zeta transform: $n$ passes, one for each bit, each of $2^{n-1}$ additions. In all $n 2^{n-1}$ additions and $O(2^n)$ memory, in place.
- The same pass structure with subtraction gives the Möbius transform in $n 2^{n-1}$ subtractions.

## Bounds

- **Upper bound.** $n 2^{n-1}$ monoid additions and $O(n 2^n)$ time on the [word RAM](/word-ram/), by [SOS DP](/sos-dp/). For $n = 20$ that is about $10^7$ additions, against $3^{20} \approx 3.5 \times 10^9$ for the direct method.
- **Lower bound.** The output has $2^n$ values, each of which depends on its own input value, so $\Omega(2^n)$ time is needed. This page does not claim a matching lower bound for $n 2^{n-1}$ additions.
- **Model.** The counts are operations of the monoid. When the values are large integers, as in inclusion-exclusion counting, each addition costs time in the size of the numbers, and Fomin and Kratsch analyze these algorithms in the log-cost RAM.

## Reductions

- **OR and AND convolution reduce to it**, with three transforms and $2^n$ products, as above.
- **Subset convolution reduces to $n + 1$ ranked transforms** for each input, $O(n^2 2^n)$ ring operations in all.
- **Counting covers by inclusion-exclusion.** The number of $k$-tuples of sets from a family $\mathcal{F}$ whose union is the whole set $U$ is $\sum_{X \subseteq U} (-1)^{|U \setminus X|} a(X)^k$, where $a(X)$ is the number of members of $\mathcal{F}$ inside $X$. The values $a(X)$ for all $X$ are one zeta transform of the indicator of $\mathcal{F}$. This is the step that [Björklund's chromatic number algorithm](/bjorklund-chromatic-number/) uses, with $\mathcal{F}$ the independent sets.
- **From the problem to the direct method.** Each instance reduces to $2^n$ runs of [submask enumeration](/submask-enumeration/).

## Applications

- **Counting by masks.** For an array of numbers below $2^n$, count for each $m$ how many numbers $x$ satisfy $x \mathbin{\&} m = x$; or, with supersets, how many have $x \mathbin{\&} m = m$. This is the form in programming contests, where the method is known as [SOS DP](/sos-dp/) and as the technique of [sum over subsets DP](/sum-over-subsets-dp/).
- **Set cover and coloring.** The cover counts above decide whether $k$ sets of a family cover the ground set in $O^*(2^n)$ time.
- **Belief functions.** In Dempster-Shafer theory, the belief of a set is the sum of the masses of its subsets, which is one zeta transform.
- **Fast subset convolution.** It speeds up DPs over pairs of disjoint subsets, such as the Dreyfus-Wagner recurrence for the [Steiner tree problem](/steiner-tree-problem/), from $O(3^k)$ to $O^*(2^k)$ for the merge step when the edge weights are small integers.

## References
