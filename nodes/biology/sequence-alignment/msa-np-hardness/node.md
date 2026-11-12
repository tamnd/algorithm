---
tag: B820F9
kind: theorem
slug: msa-np-hardness
name: NP-hardness of multiple sequence alignment
aliases:
- Wang-Jiang theorem
- NP-completeness of SP alignment
area: biology/sequence-alignment
level: advanced
summary: Multiple alignment under sum-of-pairs with k sequences is NP-hard when k is unbounded, already for a fixed small alphabet and a fixed cost table.
prereqs: [multiple-sequence-alignment, sum-of-pairs-score, shortest-common-supersequence, np-complete, polynomial-time-reduction]
see_also: [center-star-method, center-star-approximation-bound, turing-reduction, np-hard, longest-common-subsequence, apx]
sources:
  - paper: doi:10.1089/cmb.1994.1.337
    title: Lusheng Wang and Tao Jiang, On the complexity of multiple sequence alignment, Journal of Computational Biology 1(4), 1994, pages 337 to 348
    locator: the NP-completeness of SP alignment by reduction from shortest common supersequence, with the score table on 0, 1, a, b that satisfies the triangle inequality
  - paper: "Kari-Jouko Räihä and Esko Ukkonen, The shortest common supersequence problem over binary alphabet is NP-complete, Theoretical Computer Science 16(2), 1981, pages 187 to 198"
    locator: the NP-completeness of shortest common supersequence over a binary alphabet
  - paper: doi:10.1089/106652701753307511
    title: Winfried Just, Computational complexity of multiple sequence alignment with SP-score, Journal of Computational Biology 8(6), 2001, pages 615 to 623
    locator: NP-hardness for every scoring matrix in a broad class that contains most matrices used in practice
  - paper: "Paola Bonizzoni and Gianluca Della Vedova, The complexity of multiple sequence alignment with SP-score that is a metric, Theoretical Computer Science 259(1-2), 2001, pages 63 to 79"
    locator: NP-hardness for a fixed SP score that is a metric
  - paper: doi:10.1089/cmb.2006.13.1323
    title: Isaac Elias, Settling the intractability of multiple alignment, Journal of Computational Biology 13(7), 2006, pages 1323 to 1339
    locator: NP-hardness of SP, star and tree alignment for every metric symbol distance over a binary or larger alphabet
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14, Section 14.6.1 (the exact dynamic program for SP alignment and its speed-up)
---

The NP-hardness of multiple sequence alignment states that finding an alignment of $k$ sequences with the least [sum-of-pairs cost](/sum-of-pairs-score/) is NP-hard when $k$ is part of the input. Lusheng Wang and Tao Jiang proved it in 1994 by a reduction from the [shortest common supersequence](/shortest-common-supersequence/) problem, with a fixed alphabet of four letters and a fixed cost table that satisfies the triangle inequality. Later work by Just (2001), Bonizzoni and Della Vedova (2001) and Elias (2006) extended the result to almost every cost table in use, including every metric. The theorem explains why exact aligners are exponential in $k$ and why practical tools are heuristics.

## Statement

**SP alignment (decision version).** The input is an alphabet $\Sigma$, a cost $\delta : \Sigma' \times \Sigma' \to \mathbb{Z}_{\ge 0}$ on $\Sigma' = \Sigma \cup \{-\}$ with $\delta(-, -) = 0$, sequences $S_1, \ldots, S_k$ over $\Sigma$, and an integer $C$. The question is whether some alignment $A$ of the sequences has $\mathrm{SP}(A) \le C$, where $\mathrm{SP}(A) = \sum_{i<j} \sum_p \delta(A_i[p], A_j[p])$ and an alignment is a set of rows of equal length, row $i$ spelling $S_i$ with gaps added, with no column of gaps only.

Write $\|S\|$ for $\sum_i |S_i|$. Let $\delta_{WJ}$ be the symmetric cost on $\{0, 1, a, b, -\}$ given by this table:

| $\delta_{WJ}$ | 0 | 1 | a | b | − |
|---|---|---|---|---|---|
| **0** | 2 | 2 | 1 | 2 | 1 |
| **1** | 2 | 2 | 2 | 1 | 1 |
| **a** | 1 | 2 | 0 | 2 | 1 |
| **b** | 2 | 1 | 2 | 0 | 1 |
| **−** | 1 | 1 | 1 | 1 | 0 |

It satisfies $\delta_{WJ}(x, z) \le \delta_{WJ}(x, y) + \delta_{WJ}(y, z)$ for all $x, y, z$, but it is not a metric, since $\delta_{WJ}(0, 0) = 2$.

**Theorem (Wang and Jiang 1994).** SP alignment is NP-complete for the fixed alphabet $\{0, 1, a, b\}$ and the fixed cost $\delta_{WJ}$, when $k$ is part of the input.

**Theorem (many-one form).** Let $\delta_R$ on $\{0, 1, c, -\}$ have $\delta_R(0, 1) = \delta_R(1, 0) = 1$, $\delta_R(c, -) = \delta_R(-, c) = 1$, and $\delta_R(x, y) = 0$ for every other pair. Then SP alignment with this fixed cost is NP-complete under polynomial-time many-one reductions.

## In plain words

The problem of the shortest common supersequence asks for the shortest string that contains each given string as a scattered subsequence. It is known to be hard, even for strings of zeros and ones.

The proof turns that problem into an alignment problem. It adds one or two extra rows that act as a ruler: each column of the ruler stands for one letter of the supersequence. The costs are chosen so that an alignment is as cheap as possible exactly when every letter of every string sits in a ruler column, and no column mixes a zero with a one. Such an alignment spells out a common supersequence along the ruler.

So a fast exact aligner for many sequences would also find shortest common supersequences fast, which is believed to be impossible.

## Proof

**Membership in NP.** In a valid alignment each column has a letter, so it has at most $\|S\|$ columns. An alignment is therefore a certificate of size polynomial in the input, and its SP cost is computed in $O(k^2 \|S\|)$ time.

**The source problem.** The shortest common supersequence problem over $\{0, 1\}$ asks, for binary strings $s_1, \ldots, s_k$ and an integer $m$, whether some string $w$ with $|w| \le m$ has every $s_t$ as a subsequence. Räihä and Ukkonen (1981) proved it NP-complete. If such a $w$ exists, adding letters at its end gives one of length exactly $m$, so the question is the same for length exactly $m$. If $m \ge \|S\|$, the answer is yes (the concatenation works), so we may assume $m < \|S\|$.

**The reduction with the ruler row $c^m$ (many-one form).** Map $(s_1, \ldots, s_k, m)$ to the sequences $s_1, \ldots, s_k, c^m$, the cost $\delta_R$ and $C = \sum_t (m - |s_t|)$. This takes polynomial time. Take any alignment $A$ of these sequences, and call the row of $c^m$ the ruler.

- A pair of binary rows costs the number of columns where one has 0 and the other has 1. Gaps against letters cost 0.
- The pair of a binary row $s_t$ and the ruler costs the number of columns where the ruler has $c$ and $s_t$ has a gap, since $\delta_R(0, c) = \delta_R(1, c) = \delta_R(-, -) = 0$. The ruler has $m$ letters $c$, and at most $|s_t|$ of them face a letter of $s_t$, so this pair costs $m - f_t \ge m - |s_t|$, where $f_t$ is the number of letters of $s_t$ in columns where the ruler has $c$.

Hence $\mathrm{SP}(A) \ge C$, with equality if and only if (i) no column has both a 0 and a 1, and (ii) every letter of every $s_t$ is in a column where the ruler has $c$.

If a common supersequence $w$ of length $m$ exists, build $A$ with $m$ columns: column $p$ has $c$ in the ruler, and row $s_t$ has its letter in column $p$ if a fixed embedding of $s_t$ in $w$ maps a letter to position $p$, and a gap otherwise. All letters in column $p$ equal $w[p]$, so (i) holds, (ii) holds, and $\mathrm{SP}(A) = C$.

If some $A$ has $\mathrm{SP}(A) \le C$, then (i) and (ii) hold. Let $w$ list, for each of the $m$ columns where the ruler has $c$, the common binary letter of the column, or 0 if it has none. By (ii), every letter of $s_t$ is in one of these columns, in order, so $s_t$ is a subsequence of $w$, and $|w| = m$.

So the binary supersequence instance is a yes-instance if and only if the alignment instance is. With membership in NP, this proves the many-one form.

**The reduction of Wang and Jiang, with the table $\delta_{WJ}$.** For each split $i + j = m$ with $i, j \ge 0$, form the instance $X_{ij} = (s_1, \ldots, s_k, a^i, b^j)$ with threshold $C = k\|S\| + (k+1) m$. Take an alignment $A$ of $X_{ij}$.

- Two binary rows: each column where both have a letter costs 2, and each column with one letter and one gap costs 1. So the pair costs exactly $|s_t| + |s_u|$, one per letter, and all pairs of binary rows together cost $(k - 1)\|S\|$.
- The rows $a^i$ and $b^j$: by the same count ($\delta_{WJ}(a, b) = 2$, a letter against a gap costs 1), they cost exactly $i + j = m$.
- A binary row $s_t$ and $a^i$: a column with 0 against $a$ costs 1, and every other column with at least one letter costs one per letter. So the pair costs $|s_t| + i - z_t$, where $z_t$ is the number of 0s of $s_t$ facing an $a$. In the same way, $s_t$ and $b^j$ cost $|s_t| + j - o_t$, where $o_t$ is the number of 1s of $s_t$ facing a $b$.

Adding up, with $z_t + o_t \le |s_t|$,

$$\mathrm{SP}(A) = (k - 1)\|S\| + m + \sum_t \big(2|s_t| + m - z_t - o_t\big) \ge (k-1)\|S\| + m + 2\|S\| + km - \|S\| = k\|S\| + (k+1) m,$$

with equality if and only if every 0 faces an $a$ and every 1 faces a $b$.

If $w$ is a common supersequence of length $m$ with $i$ zeros and $j$ ones, align $X_{ij}$ along $w$: column $p$ has $a$ in the row $a^i$ if $w[p] = 0$, $b$ in the row $b^j$ if $w[p] = 1$, and the letters of each $s_t$ placed by an embedding into $w$. The cost is the bound. Conversely, if some $X_{ij}$ has an alignment of cost at most the bound, every letter of $S$ is in a column with an $a$ (for a 0) or a $b$ (for a 1). Write, for each column that has an $a$ or a $b$, the letter 0 if it has only $a$, 1 if it has only $b$, and $01$ if it has both. The resulting $w$ has length $i + j = m$, and each $s_t$, which has at most one letter per column, is a subsequence of $w$.

So $(s_1, \ldots, s_k, m)$ is a yes-instance if and only if at least one of the $m + 1 \le \|S\|$ instances $X_{ij}$ is. A polynomial-time algorithm for SP alignment with $\delta_{WJ}$ would decide all of them in polynomial time, so the problem is NP-hard under polynomial-time [Turing reductions](/turing-reduction/), and NP-complete with the membership above. $\blacksquare$

## Consequences

- **No polynomial exact algorithm in $k$ unless P = NP.** The exact dynamic program over the $k$-dimensional lattice takes $O(2^k n^k)$ time for $k$ sequences of length $n$, which is polynomial for each fixed $k$ but exponential in $k$. The Carrillo-Lipman (1988) bounds prune this lattice and make exact alignment of a few sequences possible in practice, but not in the worst case.
- **Approximation is the best guarantee.** For metric costs the [center-star method](/center-star-method/) is a $(2 - 2/k)$-approximation ([bound](/center-star-approximation-bound/)), improved to $2 - l/k$ for fixed $l$ by Bafna, Lawler and Pevzner.
- **Heuristics in practice.** [Progressive](/progressive-alignment/) and [iterative](/iterative-refinement-alignment/) methods such as [Clustal](/clustal/), [MUSCLE](/muscle/) and [MAFFT](/mafft/) give no guarantee on the SP cost.
- **Related objectives.** In the same paper Wang and Jiang proved that tree alignment, where the sequences are leaves of a given tree, is MAX SNP-hard, so it has no polynomial-time approximation scheme unless P = NP. Elias (2006) proved that SP, star and tree alignment are NP-hard for every metric on a binary or larger alphabet.

## Tightness

The hardness needs $k$ to grow. For a fixed number of sequences, the lattice dynamic program solves the problem in polynomial time, so the theorem is about the dependence on $k$, not on the lengths.

Neither cost table above is a metric: $\delta_R$ breaks the triangle inequality ($\delta_R(0, 1) = 1 > \delta_R(0, c) + \delta_R(c, 1) = 0$), and $\delta_{WJ}$ has $\delta_{WJ}(0, 0) > 0$. Just (2001) proved NP-hardness for a broad class of scoring matrices that contains most matrices used in practice, Bonizzoni and Della Vedova (2001) for a fixed metric, and Elias (2006) for every metric symbol distance over an alphabet of at least two letters. So the hardness does not depend on an unusual cost.

## History

Wang and Jiang settled the sum-of-pairs version in 1994, in the Journal of Computational Biology, building on the NP-completeness of shortest common supersequence (Maier 1978, and Räihä and Ukkonen 1981 for the binary alphabet). Their cost table satisfies the triangle inequality but is not a metric, which left open whether the problem stays hard for a metric. Bonizzoni and Della Vedova, and Just, gave further cases in 2001, and Elias closed the question for all metrics in a paper presented at ISAAC 2003 and published in 2006.

## References
