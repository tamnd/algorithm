---
tag: 52G3N3
kind: theorem
slug: static-dictionary-lower-bound
name: Static dictionary lower bound
aliases:
- Yao static dictionary bound
- should tables be sorted
- implicit dictionary lower bound
area: foundations/lower-bounds
level: research
summary: If a table of n cells holds n keys from a large enough universe in some order, a membership query needs ceil(lg(n+1)) probes, so sorted order with binary search is optimal (Yao 1981).
prereqs: [cell-probe-model, binary-search, ramsey-theorem, adversary-argument]
see_also: [dictionary-problem, fks-perfect-hashing, perfect-hashing, sorted-search-lower-bound, predecessor-lower-bound, cell-probe-lower-bound, counting-argument, information-theoretic-bound]
sources:
  - paper: doi:10.1145/322261.322274
    title: "Andrew Chi-Chih Yao, Should Tables Be Sorted?, Journal of the ACM 28(3) (1981), 615-628"
    locator: the cell-probe model, the implicit table model, and the Ramsey argument that sorted tables are optimal for large universes
  - paper: doi:10.1145/828.1884
    title: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a Sparse Table with O(1) Worst Case Access Time, Journal of the ACM 31(3) (1984), 538-544"
    locator: the two-level hashing scheme with O(n) cells and O(1) probes
  - paper: doi:10.1137/0222001
    title: "Amos Fiat and Moni Naor, Implicit O(1) Probe Search, SIAM Journal on Computing 22(1) (1993), 1-10"
    locator: implicit schemes with a constant number of probes for universes that are not too large
  - paper: doi:10.1137/S0097539795294165
    title: "Andrej Brodnik and J. Ian Munro, Membership in Constant Time and Almost-Minimum Space, SIAM Journal on Computing 28(5) (1999), 1627-1640"
    locator: constant-time membership in space close to the counting bound
---

A static dictionary stores a set $S$ of $n$ keys from a universe $\{1, \dots, m\}$ and answers membership queries. Yao (1981) asked whether a table that holds exactly the $n$ keys, one per cell, should keep them sorted. He proved that once $m$ is large enough compared to $n$, every such table needs $\lceil \lg(n+1) \rceil$ probes for some query, which is exactly what [binary search](/binary-search/) on a sorted table uses. The proof applies [Ramsey's theorem](/ramsey-theorem/) to force any storage rule to look sorted on a large part of the universe, and then runs an [adversary](/adversary-argument/) against the search. The same paper introduced the [cell-probe model](/cell-probe-model/).

## Statement

**The implicit model.** Fix $n \ge 1$ and $m \ge n$. A *scheme* has two parts.

- A *storage rule*. For every set $S \subseteq \{1, \dots, m\}$ with $|S| = n$, the table $T_S$ has exactly $n$ cells, and it holds the elements of $S$, one per cell, in an order chosen by the rule. No other data is stored.
- A *search rule*. For every query $x \in \{1, \dots, m\}$, a decision tree probes cells of the table. Each probe reveals the key in that cell, and the choice of the next cell may depend on all keys seen so far. Each leaf answers whether $x \in S$.

The cost is the number of probes on the worst pair $(S, x)$. All other computation is free.

**Theorem (Yao 1981).** For every $n \ge 2$ there is a number $N(n)$ such that every scheme with $m \ge N(n)$ uses at least $\lceil \lg(n+1) \rceil$ probes on some pair $(S, x)$. One may take $N(n) = R_n(2n-1;\ n!)$, the least $N$ such that every coloring of the $n$-element subsets of an $N$-element set with $n!$ colors has a set of $2n-1$ elements whose $n$-element subsets all have the same color.

The sorted table with binary search uses $\lceil \lg(n+1) \rceil$ probes, so for $m \ge N(n)$ it is an optimal scheme.

## In plain words

You must store some numbers in a row of slots, one number per slot, with nothing else. Later someone asks if a given number is there, and you may look at slots one at a time. Keeping the row sorted and halving the range each time is the classic answer. This theorem says that when the possible numbers come from a huge range, no other order does better. The first step shows that any storage rule, on some large group of possible numbers, behaves like sorting. The second step plays an opponent who answers each look in the way that keeps the most slots unsettled. Each look settles at most about half of the unsettled slots, so the search needs as many looks as halving the row takes.

## Proof

**Step 1: Ramsey makes the rule sorted.** Fix a scheme with $m \ge N(n)$. For each $n$-set $S$, let $\sigma_S$ be the permutation that says in which cell the $r$-th smallest element of $S$ lies. Color $S$ by $\sigma_S$. There are $n!$ colors. By the [hypergraph Ramsey theorem](/ramsey-theorem/) and the choice of $N(n)$, there is a set $H = \{h_1 < h_2 < \dots < h_{2n-1}\}$ such that all $n$-subsets of $H$ have the same permutation $\sigma$. Rename the cells by $\sigma$. Then for every $n$-set $S \subseteq H$, cell $j$ holds the $j$-th smallest element of $S$. It is enough to show that the query $x = h_n$ needs $\lceil \lg(n+1) \rceil$ probes on the sets $S \subseteq H$.

**Step 2: what one key reveals.** Let $S \subseteq H$ be an $n$-set, stored sorted. If cell $j$ holds $h_j$, then cells $1, \dots, j-1$ hold $h_1, \dots, h_{j-1}$, because exactly $j - 1$ elements of $S$ are below $h_j$ and only $j - 1$ elements of $H$ are below $h_j$. In the same way, if cell $j$ holds $h_{j+n-1}$, then cells $j+1, \dots, n$ hold $h_{j+n}, \dots, h_{2n-1}$.

**Step 3: the adversary.** The adversary keeps a *gap*, an interval $[g, g']$ of cells. Every probed cell lies outside the gap. All cells $j < g$ are fixed to $h_j$, and all cells $j > g'$ are fixed to $h_{j+n-1}$. At the start the gap is $[1, n]$ and nothing is fixed.

*While the gap is not empty, both answers are possible.* Let the gap have $k \ge 1$ cells. The cells of the gap must hold $k$ increasing keys from the $k + n - 1$ elements $h_g, \dots, h_{g'+n-1}$, and any such choice is consistent with the fixed cells. This range contains $h_n$, since $g \le n$ and $g' \ge 1$. A choice with $h_n$ exists because $k \ge 1$. A choice without $h_n$ exists because $k \le k + n - 2$ when $n \ge 2$.

*The answer to a probe.* A probe to a fixed cell reveals nothing new. A probe to cell $j$ of the gap gets one of two answers. The answer $h_j$ fixes cells $g, \dots, j$ (by Step 2) and leaves the gap $[j+1, g']$ of $g' - j$ cells. The answer $h_{j+n-1}$ fixes cells $j, \dots, g'$ and leaves the gap $[g, j-1]$ of $j - g$ cells. The adversary picks the answer with the larger new gap. One of the two sizes is at least $\lceil (k-1)/2 \rceil$. If there is a tie, the adversary avoids the key $h_n$: the answer $h_j$ equals $h_n$ only if $j = n = g'$, where its gap is empty and the other gap is at least as large, and the answer $h_{j+n-1}$ equals $h_n$ only if $j = 1 = g$, the mirror case. Since $n \ge 2$, these two cases do not happen together. So no answer ever reveals $h_n$, and both answers keep a choice for the gap cells.

**Step 4: count.** The search can stop only when the gap is empty, because before that both answers are possible. Let $f(k)$ be the number of probes the adversary forces from a gap of $k$ cells. Then $f(0) = 0$ and $f(k) \ge 1 + f(\lceil (k-1)/2 \rceil)$ for $k \ge 1$. By induction $f(k) \ge \lceil \lg(k+1) \rceil$, since

$$1 + \left\lceil \lg\!\left(\left\lceil \tfrac{k-1}{2} \right\rceil + 1\right) \right\rceil = 1 + \left\lceil \lg \left\lceil \tfrac{k+1}{2} \right\rceil \right\rceil = 1 + \left\lceil \lg \tfrac{k+1}{2} \right\rceil = \lceil \lg(k+1) \rceil,$$

where the middle step uses $\lceil \lg \lceil y \rceil \rceil = \lceil \lg y \rceil$ for real $y \ge 1$. With $k = n$ this gives $\lceil \lg(n+1) \rceil$ probes. $\blacksquare$

## Consequences

- *Sorted order is optimal without extra space.* If the table may hold only the keys, nothing beats a sorted array once the universe is large.
- *Constant time needs more than the keys.* The FKS scheme of Fredman, Komlos and Szemeredi stores $n$ keys in $O(n)$ cells of $O(\lg m)$ bits and answers membership with $O(1)$ probes in the worst case, see [FKS perfect hashing](/fks-perfect-hashing/). It escapes the theorem because its cells also hold hash parameters and its table is larger than $n$ cells. So in the general [cell-probe model](/cell-probe-model/) with linear space and words of $\lg m$ bits, membership has no superconstant lower bound.
- *Space close to the minimum is enough.* Any representation needs $B = \lceil \lg \binom{m}{n} \rceil$ bits for some set, by a [counting argument](/counting-argument/). For $m = 2^{32}$ and $n = 10^6$, $B \approx 13{,}510{,}948$, about $13.5$ bits per key, while a sorted array of 32-bit keys uses $32$ bits per key. Brodnik and Munro (1999) answer membership in constant time with $B + o(B)$ bits.
- *A small case.* For $n = 2$ an exhaustive search over all schemes shows that one probe suffices for $m \le 3$ and two probes ($= \lceil \lg 3 \rceil$) are needed for every $m \ge 4$. For $m = 3$, store $\{1,2\}$ as $(1, 2)$, $\{2,3\}$ as $(2, 3)$ and $\{1,3\}$ as $(3, 1)$. Cell $1$ then holds a key $c$ whose cyclic successor is the other key, so one probe of cell $1$ answers every query. The theorem itself guarantees two probes only from $N(2) = R_2(3; 2) = 6$ on, the classical Ramsey number $R(3,3)$.

### Pitfalls

- *The case $n = 1$ is an exception.* For $n = 1$ and $m = 1$ no probe is needed, and the bound $\lceil \lg 2 \rceil = 1$ fails. The proof uses $n \ge 2$ to keep $h_n$ out of the set.
- *The universe must be large.* For small $m$ unsorted tables can win, as the case $n = 2$, $m = 3$ shows. Fiat and Naor (1993) give implicit schemes with $O(1)$ probes when $m$ is not too large compared to $n$. The Ramsey threshold $N(n)$ grows extremely fast, so the theorem is about very sparse sets.
- *The model allows nothing but the keys.* One extra cell, a hash function, or a key stored twice takes a scheme out of the model. The theorem says nothing about such schemes.
- *Comparisons are not assumed.* The search may use the full value of each probed key, not just comparisons with $x$. The [sorted search lower bound](/sorted-search-lower-bound/) for comparison algorithms is a different result, with a different proof.

## Tightness

The bound is tight for $m \ge N(n)$: binary search on the sorted table probes the middle cell of the remaining range and stops after at most $\lceil \lg(n+1) \rceil$ probes. The threshold on $m$ is necessary in some form, since $m = n$ needs no probe at all and, for $n = 2$, $m = 3$ needs only one. The value $R_n(2n-1;\ n!)$ is far from the true threshold, which for $n = 2$ is $4$, not $6$.

## History

Yao introduced the cell-probe model in "Should Tables Be Sorted?" (1981) and proved there that sorted tables are optimal in the implicit model for large universes, by Ramsey's theorem. He also showed that for small universes a cleverer order can beat binary search. Fredman, Komlos and Szemeredi (1984) showed that $O(n)$ cells give $O(1)$ probes, which made clear that the lower bound depends on having no extra space. Fiat and Naor (1993) studied how large the universe may be for an implicit scheme with $O(1)$ probes. Brodnik and Munro (1999) reached constant time in space close to the counting bound. Later cell-probe lower bounds for data structures, such as the [predecessor bound](/predecessor-lower-bound/), grew from Yao's model.

## References
