---
tag: Y8HCE3
kind: problem
slug: partial-sums-problem
name: Partial sums problem
aliases:
- dynamic prefix sums
- dynamic range sum with point updates
area: sequences/prefix-sums-and-differences
level: advanced
summary: Maintain an array under point updates and answer prefix-sum queries; Fenwick and segment trees solve it in O(log n).
model: cell-probe-model
complexity:
  vars: {n: the length of the array}
  time: {amortized: Ω(log n)}
prereqs: [prefix-sums]
see_also: [point-update-range-sum-query, fenwick-tree, dynamic-partial-sums-lower-bound, fredman-saks-partial-sums-lower-bound, fredman-saks-lower-bound, order-statistic-tree, succinct-data-structures, arithmetic-coding]
sources:
  - paper: doi:10.1145/322290.322305
    title: "Michael L. Fredman, The Complexity of Maintaining an Array and Computing Its Partial Sums, Journal of the ACM 29(1) (1982), 250-260"
    locator: the definition of the problem and the logarithmic bound in the group model for oblivious algorithms
  - paper: doi:10.1137/0214022
    title: "Andrew C. Yao, On the Complexity of Maintaining Partial Sums, SIAM Journal on Computing 14(2) (1985), 277-288"
    locator: the semigroup model with additive updates
  - paper: doi:10.1137/S0097539795291598
    title: "Haripriyan Hampapuram and Michael L. Fredman, Optimal Biweighted Binary Trees and the Complexity of Maintaining Partial Sums, SIAM Journal on Computing 28(1) (1998), 1-9"
    locator: the Omega(log n) bound in the semigroup model with additive updates
  - paper: "Paul F. Dietz, Optimal algorithms for list indexing and subset rank, Proceedings of the Workshop on Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer Science 382, 39-46"
    locator: the O(log n / log log n) structures for list indexing and subset rank
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (STOC 1989), 345-354"
    locator: the cell-probe bounds for partial sums over Z/2, list indexing and subset rank
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (Theorems 2.1, 2.2 and 2.3, the trade-offs for sum and select and the matching upper bound for small values)
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the whole paper (update, prefix sum and search in O(log n))
---

The partial sums problem asks for a data structure that keeps an array $A[1..n]$ under updates of single entries and answers *prefix sum* queries $A[1] + \dots + A[k]$, and often also the inverse query, *select*, which finds the first prefix that reaches a given value. It is the dynamic form of [prefix sums](/prefix-sums/), it was posed in this form by Fredman in 1982, and it became the standard test problem for lower bounds on dynamic data structures. Its answer depends on the algebra of the entries and on the model of computation: over word-sized integers the [Fenwick tree](/fenwick-tree/) is optimal at $\Theta(\log n)$ per operation, while for one-bit entries on a word RAM the tight cost is $\Theta(\log n / \log \log n)$.

## In plain words

Keep a row of counters, one for each letter of an alphabet, and count how often each letter has been seen. Two questions come in, mixed with new letters. How many letters seen so far come at or before a given letter? And which letter is at a given position when all letters seen are put in order?

A new letter changes one counter. The first question adds up a front part of the row. The second question searches for where the front parts pass a target number. The problem is to keep the row in a form in which a change and both kinds of question are all fast. Over the years it became the test case for the question "how fast can any memory layout be", and its answer depends on how large the counters are.

## Definition

**Data.** An array $A[1..n]$ of elements of a commutative monoid $(S, +, 0)$. The standard cases are an abelian group, such as $\mathbb{Z}$, $\mathbb{Z}/2^{\delta}$ or $\mathbb{Z}/2$, and a commutative semigroup without inverses, such as $(\mathbb{N}, \max)$. At the start every entry is $0$, or the array is given and preprocessing is allowed.

**Operations.** Online, each answered before the next one is read:

- $\textsc{update}(k, \Delta)$: set $A[k] \leftarrow A[k] + \Delta$. Fredman's original form also allows $A[k] \leftarrow \Delta$, which is the same over a group if a copy of $A$ is kept.
- $\textsc{sum}(k)$: return $A[1] + A[2] + \dots + A[k]$.
- $\textsc{select}(s)$, when the entries are non-negative integers: return the least $k$ with $\textsc{sum}(k) \ge s$.

**Cost.** Let $t_u$, $t_q$ and $t_s$ be the worst-case or amortized costs of the three operations. In the [cell-probe model](/cell-probe-model/) they count the memory cells of $w$ bits that an operation reads or writes. In the algebraic models they count the semigroup or group operations. The parameters are $n$, the cell size $w$, and the number of bits $\delta$ of an update argument.

**Relation to range sums.** Over a group, the range sum $A[l] + \dots + A[r]$ is $\textsc{sum}(r) - \textsc{sum}(l - 1)$, so this problem and the [point update range sum query](/point-update-range-sum-query/) problem have the same complexity. Over a semigroup the range form can be harder, because a prefix cannot be subtracted. This page is about the prefix form and its models. The range form, with its data structures, is on the page of the point update range sum query.

## Variants

- **The group model.** The structure stores group elements, each a fixed linear combination of the entries, and updates and queries may add and subtract them. Fredman (1982) studied this model.
- **The semigroup model.** Only addition is allowed, so a stored value is a sum of entries with non-negative coefficients. Yao (1985) and Hampapuram and Fredman (1998) studied this model with additive updates.
- **The cell-probe model with $\delta$-bit values.** Entries are integers modulo $2^{\delta}$ and only memory probes are counted. The parity form $\delta = 1$ is the one of Fredman and Saks.
- **Increments only.** Each update adds $+1$ or $-1$. With entries in $\{0, 1\}$ this is the dynamic *subset rank* problem: keep a subset of $\{1, \dots, n\}$ under insertions and deletions and answer how many members are at most $k$.
- **Searchable partial sums.** The select query is added, as in arithmetic coders and in dynamic [order statistic trees](/order-statistic-tree/) over a small universe of keys.
- **Succinct versions.** The structure must use $n\delta + o(n\delta)$ bits, see [succinct data structures](/succinct-data-structures/).

## Examples

Take $n = 8$ and $A = [3, 1, 4, 1, 5, 9, 2, 6]$ over the integers.

| operation | array after | answer |
|---|---|---|
| $\textsc{sum}(5)$ | $[3, 1, 4, 1, 5, 9, 2, 6]$ | $3 + 1 + 4 + 1 + 5 = 14$ |
| $\textsc{update}(2, +4)$ | $[3, 5, 4, 1, 5, 9, 2, 6]$ | |
| $\textsc{sum}(5)$ | $[3, 5, 4, 1, 5, 9, 2, 6]$ | $18$ |
| $\textsc{select}(20)$ | $[3, 5, 4, 1, 5, 9, 2, 6]$ | $6$, since the prefix sums are $3, 8, 12, 13, 18, 27, \dots$ |
| $\textsc{select}(13)$ | $[3, 5, 4, 1, 5, 9, 2, 6]$ | $4$ |

Over $\mathbb{Z}/2$ with $A = [1, 0, 1, 1, 0, 1]$, the query $\textsc{sum}(4)$ returns the parity $1 + 0 + 1 + 1 \equiv 1$, and after $\textsc{update}(3, 1)$ it returns $0$.

As a subset rank instance, $A = [0, 1, 0, 1, 1, 0, 0, 1]$ is the set $\{2, 4, 5, 8\}$. The rank of $6$ is $\textsc{sum}(6) = 3$, and the third smallest member is $\textsc{select}(3) = 5$.

## Known algorithms

| method | update | sum | select | model or notes |
|---|---|---|---|---|
| plain array | $O(1)$ | $O(n)$ | $O(n)$ | any monoid |
| [prefix sums](/prefix-sums/) array | $O(n)$ | $O(1)$ | $O(\log n)$ by [binary search](/binary-search/) | group |
| balanced tree of subtree sums, [segment tree](/segment-tree/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | any commutative monoid |
| [Fenwick tree](/fenwick-tree/) | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ by one descent | group, $n$ cells |
| tree of fan-out $B$ with child prefix sums | $O(B \log_B n)$ | $O(\log_B n)$ | $O(\log_B n)$ with a search per node | group; every point of the trade-off curve |
| word-packed $B$-ary tree for $\delta$-bit values | $O(\log n / \log(w/\delta))$ | $O(\log n / \log(w/\delta))$ | same | word RAM; Patrascu and Demaine, Theorem 2.3 |

The last row is the one that matters for small values. With $\delta = 1$ and $w = \Theta(\log n)$ a node can pack the counts of about $\log n / \log \log n$ children in one word, so the tree has $O(\log n / \log \log n)$ levels and each level costs $O(1)$ word operations. Dietz gave such a structure in 1989 for list indexing and subset rank.

## Bounds

| model | bound per operation | source |
|---|---|---|
| group model, oblivious algorithms | $\Theta(\log n)$ | Fredman 1982 |
| semigroup model, additive updates | $\Omega(\log n / \log \log n)$, later $\Theta(\log n)$ | Yao 1985; Hampapuram and Fredman 1998 |
| cell probe, $\delta = 1$, $w = \Theta(\log n)$ | $\Theta(\log n / \log \log n)$ | Fredman and Saks 1989 |
| cell probe, $\delta = w$ | $\Theta(\log n)$, amortized and Las Vegas | Patrascu and Demaine 2006 |
| cell probe, general $\delta$ | $\Theta(\log n / \log(w/\delta))$ | Patrascu and Demaine 2006 |

The cell-probe bounds are the strongest, because they allow any computation and only count memory accesses. Two of them have their own pages. The [Fredman-Saks partial sums lower bound](/fredman-saks-partial-sums-lower-bound/) proves the $\Omega(\log n / \log \log n)$ bound for parity with the chronogram method. The [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) proves the $\Omega(\log n)$ bound and the full trade-off $t_q \log(t_u / t_q) = \Omega(\log n)$ with the information transfer method. The general chronogram method is also on the page [Fredman-Saks lower bound](/fredman-saks-lower-bound/), where it gives the bound for union-find.

Each bound is matched by an upper bound: the Fenwick tree for $\delta = w$, the word-packed tree for small $\delta$, and the trees of fan-out $B$ for every point of the trade-off.

## Reductions

- **Prefix and range forms.** Over a group the two are equivalent with one extra query, as in the definition.
- **Subset rank and list indexing.** Dynamic subset rank is the problem with $\{0, 1\}$ entries. List indexing (keep a list under insertions and deletions and return the element at position $i$) reduces to subset rank with select on a universe of positions, and Fredman and Saks proved the same $\Omega(\log n / \log \log n)$ bound for it.
- **Parity to word-sized sums.** An integer structure answers parity queries by taking the low bit of each answer, so every lower bound for $\mathbb{Z}/2$ is also a lower bound for larger values. This is why the $\Theta(\log n)$ bound needs a different proof: the parity bound is too weak for it.
- **Range update, point query.** Adding $\Delta$ to $A[l..r]$ is two updates on the [difference array](/difference-array/), and reading $A[k]$ is a prefix sum of it, see [range update point query](/range-update-point-query/).
- **Counting and order statistics.** Counting inversions, rank in a dynamic multiset over a known universe, and order statistics by select all reduce to this problem with counts as entries.

## Applications

- **Arithmetic coding.** An adaptive [arithmetic coder](/arithmetic-coding/) keeps the frequency of each symbol, encodes with prefix sums of the frequencies and decodes with select. This is the use for which Fenwick designed his tree.
- **Lower bound technique.** Chronograms, information transfer and later methods were first tried on this problem, and the bounds for union-find, dynamic connectivity and predecessor search reuse their ideas.
- **Rank and select on dynamic bit vectors.** Compressed and succinct text indexes keep dynamic bit vectors whose rank and select are this problem with one-bit entries.
- **Order statistics.** Counts per key value with select give the $k$-th smallest of a dynamic multiset of small integers.

## References
