---
tag: FB2QSD
kind: concept
slug: permutation-pattern-avoidance
name: Permutation pattern avoidance
aliases:
- pattern-avoiding permutations
area: sequences/inversions-and-permutations
level: advanced
summary: Study of permutation classes that contain none of a given set of patterns.
prereqs: [permutation, subsequence]
see_also: [permutation-pattern-matching, stack-sortable-permutations, stack-permutation-generability, catalan-numbers, erdos-szekeres-theorem, longest-increasing-subsequence, generating-functions, inversion]
sources:
  - paper: "Rodica Simion and Frank W. Schmidt, Restricted permutations, European Journal of Combinatorics 6(4) (1985) 383-406"
    locator: the enumeration of permutations avoiding one or several patterns of length 3
  - paper: "Adam Marcus and Gábor Tardos, Excluded permutation matrices and the Stanley-Wilf conjecture, Journal of Combinatorial Theory, Series A 107(1) (2004) 153-160"
    locator: the proof that every proper permutation class grows at most exponentially
  - paper: "Miklós Bóna, Exact enumeration of 1342-avoiding permutations: a close link with labeled trees and planar maps, Journal of Combinatorial Theory, Series A 80(2) (1997) 257-272"
    locator: the generating function of 1342-avoiders and their growth rate 8
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1 (the permutations obtainable with a stack, characterized by a forbidden pattern)
---

A [permutation](/permutation/) $p$ contains a pattern $\sigma$ of length $k$ if some $k$ entries of $p$, read from left to right, are in the same relative order as $\sigma$; otherwise $p$ avoids $\sigma$. The permutations that avoid a set of patterns form a class closed under taking patterns, and every such class is described by its minimal forbidden patterns, its basis. The theory began with Knuth's result that the [stack-sortable permutations](/stack-sortable-permutations/) are those avoiding $231$, and its central questions are how many permutations of length $n$ avoid a given pattern and how fast that number grows. Every pattern of length 3 is avoided by $C_n$ permutations, and the Marcus-Tardos theorem says that every proper class grows at most like $c^n$.

## In plain words

Write a permutation as a row of numbers and look at some of its entries, keeping their left-to-right order. Forget the actual values and keep only which is smallest, which is next, and so on. That shape is a pattern of the permutation. For example, in 3 1 4 5 2 the entries 3, 4, 2 have the shape middle, high, low, which is the pattern 2 3 1.

A permutation avoids a pattern if no choice of entries has that shape. Many natural families of permutations are exactly the ones that avoid a few shapes: those a stack can sort, those with no long increasing run of entries, those built by gluing blocks. Counting such families, and testing membership quickly, are the two main tasks.

## The idea

**Order isomorphism.** Two sequences $a_1 \cdots a_k$ and $b_1 \cdots b_k$ of distinct numbers are order-isomorphic if $a_i < a_j \iff b_i < b_j$ for all $i, j$. Every sequence of distinct numbers is order-isomorphic to exactly one permutation of $[k]$, its *standardization*.

**Containment.** $p \in S_n$ contains $\sigma \in S_k$ if there are positions $i_1 < \cdots < i_k$ such that $p_{i_1} \cdots p_{i_k}$ standardizes to $\sigma$. Such positions are an *occurrence* of $\sigma$. Containment is a partial order on all permutations. The [inversions](/inversion/) of $p$ are the occurrences of $21$, and its increasing [subsequences](/subsequence/) of length $k$ are the occurrences of $12 \cdots k$.

**Classes and bases.** A set $\mathcal{C}$ of permutations is a *class* if it is closed downward: whenever $p \in \mathcal{C}$ and $p$ contains $\sigma$, then $\sigma \in \mathcal{C}$. Every class equals $\operatorname{Av}(B)$, the permutations avoiding every pattern in $B$, for the set $B$ of minimal permutations not in $\mathcal{C}$, its *basis*. The basis is an antichain, and it can be infinite.

**Symmetries.** Reversal, complement ($p_i \mapsto n + 1 - p_i$) and inverse map patterns to patterns and occurrences to occurrences. They generate a group of 8 symmetries, so $\operatorname{Av}(\sigma)$ and $\operatorname{Av}(\tau)$ have the same size when $\tau$ is an image of $\sigma$. Two patterns are *Wilf-equivalent* if $|\operatorname{Av}_n(\sigma)| = |\operatorname{Av}_n(\tau)|$ for all $n$, which can happen without a symmetry.

**Patterns of length 3.** The six patterns fall into two symmetry classes, $\{123, 321\}$ and $\{132, 231, 213, 312\}$, and both are counted by the [Catalan numbers](/catalan-numbers/) $C_n = \frac{1}{n+1}\binom{2n}{n}$. For $231$ this is the stack-sorting recurrence; for $123$ it follows from a bijection with $132$-avoiders or from the Robinson-Schensted correspondence. Simion and Schmidt counted all classes with several patterns of length 3. For instance $\operatorname{Av}_n(123, 321)$ is empty for $n \ge 5$, by the [Erdős-Szekeres theorem](/erdos-szekeres-theorem/).

**Patterns of length 4.** There are three Wilf classes, with representatives $1234$, $1342$ and $1324$. Gessel found the generating function of $1234$-avoiders, and in general the permutations avoiding $12 \cdots k$ are those whose [longest increasing subsequence](/longest-increasing-subsequence/) has length less than $k$. Bóna found the generating function of $1342$-avoiders, which is algebraic. For $1324$ no formula is known, and even its growth rate is known only within bounds.

**Growth.** The Stanley-Wilf conjecture, proved by Marcus and Tardos in 2004 through a result on 0-1 matrices that avoid a permutation matrix, says that $|\operatorname{Av}_n(\sigma)| \le c_\sigma^n$ for every pattern $\sigma$. The limit $L(\sigma) = \lim_n |\operatorname{Av}_n(\sigma)|^{1/n}$ exists and is $4$ for every pattern of length 3, $(k-1)^2$ for $12 \cdots k$ by a result of Regev, $9$ for $1234$ and $8$ for $1342$.

## Examples

**One occurrence.** $p = 3\,1\,4\,5\,2$ contains $231$ at the positions $1, 3, 5$, with entries $3\,4\,2$, and also at $1, 4, 5$ and $3, 4, 5$. These are its only occurrences of $231$. It contains $123$, for example $1\,4\,5$, but no four entries increase, so it avoids $1234$, and no three entries decrease, so it avoids $321$.

**Counts for length 4.** For $n = 4, 5, 6, 7$:

| pattern | $n = 4$ | $n = 5$ | $n = 6$ | $n = 7$ |
| --- | --- | --- | --- | --- |
| $1234$ | 23 | 103 | 513 | 2761 |
| $1342$ | 23 | 103 | 512 | 2740 |
| $1324$ | 23 | 103 | 513 | 2762 |

All three agree up to $n = 5$, which is why the difference took some time to be noticed. Here $1324$ is avoided by the most permutations.

**Separable permutations.** $\operatorname{Av}(2413, 3142)$ consists of the permutations that can be built from single points by direct sums ($\sigma \oplus \tau$, $\tau$ shifted above and to the right of $\sigma$) and skew sums ($\tau$ shifted above and to the left of $\sigma$). For $n = 1, \ldots, 7$ there are $1, 2, 6, 22, 90, 394, 1806$ of them, the large Schröder numbers. The deque classes of [stack permutation generability](/stack-permutation-generability/) give the same counts.

**Sorting machines.** The outputs of one stack form $\operatorname{Av}(312)$ and the inputs it sorts form $\operatorname{Av}(231)$. Two stacks in series give a class with an infinite basis, and so do general deques.

## Where it is used

- **Sorting with restricted devices.** Stacks, queues, deques and networks of them sort exactly the permutations of some class, and the basis of the class describes what the device cannot do.
- **Algorithms on restricted inputs.** Many problems that are hard in general become easy on a class with a small basis. [Pattern matching](/permutation-pattern-matching/) is NP-complete in general but polynomial when the pattern is separable, and the Guillemot-Marx algorithm for it rests on the Marcus-Tardos theorem.
- **Enumerative combinatorics.** Pattern classes give a large supply of counting sequences with rational, algebraic, D-finite and non-D-finite [generating functions](/generating-functions/), and the question of which kind a class has is an active area.
- **Extremal combinatorics.** The Marcus-Tardos theorem was proved through the Füredi-Hajnal conjecture on the number of 1 entries in a 0-1 matrix that avoids a given permutation matrix, and it was later used in the theory of twin-width of graphs.
- **Statistics.** Counting occurrences of $21$ between two rankings is [Kendall's tau](/kendall-tau-distance/), and counts of longer patterns give finer measures of dependence between two variables.

## References
