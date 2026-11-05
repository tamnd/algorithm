---
tag: X7DPRF
kind: algorithm
slug: bjorklund-chromatic-number
name: Björklund's chromatic number algorithm
aliases:
- inclusion-exclusion chromatic number
area: graphs/coloring-and-cliques
level: research
summary: Computes the chromatic number in O*(2^n) time by inclusion-exclusion over covers with independent sets.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(2^n n^2)}
  space: {extra: O(2^n n)}
properties: {deterministic: true, recursive: false}
prereqs: [chromatic-number, inclusion-exclusion-principle, independent-set, sos-dp]
see_also: [lawler-chromatic-number, chromatic-number, counting-graph-colorings, chromatic-polynomial, graph-coloring, dsatur, bitmask-dp, clique-cover]
sources:
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the whole paper (covers and partitions by k members of a set family in 2^n n^O(1) time by inclusion-exclusion and the zeta transform; chromatic number as the main application)
  - paper: doi:10.1016/0020-0190(76)90065-X
    title: Eugene L. Lawler, A note on the complexity of the chromatic number problem, Information Processing Letters 5(3), 66 to 67 (1976)
    locator: the whole note (the dynamic program over maximal independent sets, the previous best bound)
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 4, Inclusion-Exclusion (the chromatic number by counting covers with independent sets)
---

Björklund's algorithm computes the [chromatic number](/chromatic-number/) $\chi(G)$ of a graph with $n$ vertices in $O^*(2^n)$ time, the best known bound. It does not search for a coloring. It counts, for $k = 1, 2, \ldots$, the ways to cover all vertices with $k$ [independent sets](/independent-set/), using the [inclusion-exclusion principle](/inclusion-exclusion-principle/) and a zeta transform over subsets, and returns the first $k$ with a positive count. Björklund, Husfeldt and Koivisto published it in 2009; it improved Lawler's $O(2.4423^n)$ dynamic program from 1976.

## In plain words

Coloring a network with $k$ colors is the same as choosing $k$ groups of points, with no two points in a group joined, so that every point is in some group.

Counting such choices directly is hard. Counting them while ignoring the rule "every point must be covered" is easy: for any part of the network, count the allowed groups inside it, and raise that number to the power $k$.

Now correct for the choices that miss points. Add the counts for the whole network, subtract those for each network with one point removed, add back those with two points removed, and so on. What is left counts exactly the choices that cover every point. The smallest $k$ that leaves a positive count is the answer.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$, given as adjacency lists. The output is $\chi(G)$, the least $k$ such that $V$ can be split into $k$ independent sets; $\chi = 0$ for $n = 0$. Deciding $\chi(G) \le 3$ is NP-complete, so an exponential running time is expected; see [$k$-coloring](/k-coloring/).

## The algorithm

Subsets of $V$ are bit masks. For $S \subseteq V$ let $f(S)$ be the number of independent sets $T \subseteq S$, the empty set included.

```pseudo id=main
BJORKLUND-CHROMATIC(G)
L1  if n = 0 then return 0
L2  for each nonempty S ⊆ V, in increasing order of the mask do
L3      v ← the smallest vertex of S;  ind[S] ← ind[S − v] and (N(v) ∩ S = ∅)    ▷ ind[∅] = 1
L4  f ← ind;  for each v ∈ V do
L5      for each S ∋ v do f[S] ← f[S] + f[S − v]        ▷ now f[S] = number of independent T ⊆ S
L6  for k ← 1 to n do
L7      c ← Σ over S ⊆ V of (−1)^(n − |S|) · f[S]^k
L8      if c > 0 then return k
```

Lines L2 and L3 mark the independent sets: $S$ is independent when $S - v$ is independent and $v$ has no neighbor in $S$. Lines L4 and L5 are the zeta transform over subsets, the [sum over subsets](/sos-dp/) dynamic program, which replaces each entry by the sum over its subsets in $O(2^n n)$ additions. Line L7 counts the ordered $k$-tuples of independent sets whose union is $V$. The powers $f[S]^k$ are kept from one $k$ to the next, so each round costs one multiplication per subset.

## Example

Take the 5-cycle $C_5$ with edges $01, 12, 23, 34, 40$. The values of $f$ depend only on the shape of $G[S]$:

| $\lvert S \rvert$ | shape of $G[S]$ | number of such $S$ | $f(S)$ |
|---|---|---|---|
| 0 | empty | 1 | 1 |
| 1 | one vertex | 5 | 2 |
| 2 | an edge | 5 | 3 |
| 2 | two non-adjacent vertices | 5 | 4 |
| 3 | a path on 3 vertices | 5 | 5 |
| 3 | an edge and a separate vertex | 5 | 6 |
| 4 | a path on 4 vertices | 5 | 8 |
| 5 | the cycle | 1 | 11 |

Line L7 groups the terms by $|S|$, with sign $(-1)^{5 - |S|}$:

| $k$ | $\lvert S \rvert = 0$ | 1 | 2 | 3 | 4 | 5 | $c$ |
|---|---|---|---|---|---|---|---|
| 1 | $-1$ | $10$ | $-35$ | $55$ | $-40$ | $11$ | 0 |
| 2 | $-1$ | $20$ | $-125$ | $305$ | $-320$ | $121$ | 0 |
| 3 | $-1$ | $40$ | $-455$ | $1705$ | $-2560$ | $1331$ | 60 |

For $k = 2$, for instance, the $|S| = 2$ column is $-(5 \cdot 3^2 + 5 \cdot 4^2) = -125$. The first positive count is at $k = 3$, so $\chi(C_5) = 3$. The 60 covers include the $30$ proper 3-colorings, read as triples of color classes, and 30 more triples in which some vertex lies in two of the sets.

## Correctness

**Lemma (covers).** For each $k \ge 1$, the number of $k$-tuples $(I_1, \ldots, I_k)$ of independent sets with $I_1 \cup \cdots \cup I_k = V$ is $\sum_{S \subseteq V} (-1)^{n - |S|} f(S)^k$.

*Sketch.* $f(S)^k$ counts the $k$-tuples whose union $U$ lies in $S$. So the sum counts each tuple with weight $\sum_{U \subseteq S \subseteq V} (-1)^{n - |S|}$, which is 1 if $U = V$ and 0 otherwise, by the binomial theorem applied to $V \setminus U$.

A cover by $k$ independent sets gives a proper coloring with at most $k$ colors: give each vertex the color of the first set that contains it. Conversely, the color classes of a coloring with at most $k$ colors, padded with empty sets, form a cover. So the count is positive exactly when $\chi(G) \le k$, and line L8 returns the least such $k$. The loop stops by $k = n$, since the $n$ singletons cover $V$. Lines L2 to L5 compute $f$ correctly by induction on the mask and on the number of processed vertices. The full proof is below.

## Complexity

The costs are in the [word RAM](/word-ram/) model. The tables have $2^n$ cells, so a word has at least $n$ bits, and each $f(S) \le 2^n$ fits in one word.

- **Independence table, lines L2 and L3.** $O(2^n)$ word operations, with the neighbor sets as masks.
- **Zeta transform, lines L4 and L5.** $n \cdot 2^{n-1}$ additions, so $O(2^n n)$.
- **Counting, lines L6 to L8.** The power $f(S)^k$ has at most $nk$ bits, so at most $k$ words, and multiplying it by $f(S)$ takes $O(k)$ time. Round $k$ costs $O(2^n k)$, and the $n$ rounds cost $O(2^n n^2)$.
- **Total.** $O(2^n n^2)$ time and $O(2^n n)$ words of space for the stored powers. Recomputing $f(S)^k$ from $f(S)$ in each round, or working modulo a prime, saves space at the cost of a polynomial factor.
- **Fewer rounds.** Since the count is monotone in $k$, a binary search over $k$ needs $O(\log n)$ rounds instead of $n$.

## Properties

- **Exact and deterministic.** No randomness and no search; the answer follows from exact integer counts.
- **Bound independent of structure.** The running time is $\Theta^*(2^n)$ on every graph, sparse or dense, unlike branch and bound methods such as [DSATUR](/dsatur/), which are fast on easy instances and slow on hard ones.
- **Counts, not colorings.** The algorithm returns $\chi(G)$ but no coloring. A coloring can be found by self-reduction: add edges or merge vertices one at a time and keep each change that does not raise $\chi$, at the cost of $O(n^2)$ more runs.
- **Exponential space.** The table of $2^n$ entries is the main practical limit.

## Variants and improvements

- **Polynomial space.** Computing $f(S)$ for each $S$ separately, by counting the independent sets of $G[S]$, uses polynomial space. Björklund, Husfeldt and Koivisto obtain $O(2.2461^n)$ time in polynomial space for the chromatic number this way.
- **Chromatic polynomial.** Counting partitions instead of covers, with the ranked zeta transform, gives the number of $k$-colorings and the whole [chromatic polynomial](/chromatic-polynomial/) in $O^*(2^n)$ time; see [counting graph colorings](/counting-graph-colorings/).
- **Other partition problems.** The same method partitions $V$ into $k$ members of any family that can be listed or tested: domatic number, [clique cover](/clique-cover/) on the complement, bin packing and list coloring are all covered by the 2009 paper.
- **Lawler's algorithm (1976).** The earlier dynamic program over subsets, $\chi(S) = 1 + \min \chi(S \setminus I)$ over maximal independent sets $I$ of $G[S]$, runs in $O(2.4423^n)$ time; see [Lawler's algorithm](/lawler-chromatic-number/).

## When to use it

Use it when an exact chromatic number is needed for a graph of up to about 30 vertices with no structure to exploit, or as a reference against which to test heuristics. For larger sparse graphs, branch and bound with good lower bounds is usually faster in practice. For a fixed small $k$, such as 3, specialized algorithms decide $k$-colorability faster than $O^*(2^n)$.

## Pitfalls

- **Sets versus partitions.** The count at line L7 is of covers, which may overlap, not of colorings. It is positive exactly when a $k$-coloring exists, but its value is not the number of colorings; for $C_5$ and $k = 3$ it is 60, not 30.
- **The empty set.** Here $f(S)$ counts the empty independent set. Without it, line L7 counts covers by $k$ nonempty sets, which exist exactly when $\chi \le k \le n$; the answer stays right inside the loop, but the counts change, and mixing the two conventions gives wrong numbers.
- **Integer overflow.** $f(S)^k$ has up to $n^2$ bits. Fixed-width integers overflow; use big integers, or compute modulo a large prime and accept a small chance of a false zero.
- **Sign.** The sign is $(-1)^{n - |S|}$, the parity of the vertices left out, not of the vertices in $S$; for odd $n$ the two differ.

## Implementations

## History

Lawler in 1976 gave the dynamic program over maximal independent sets with $O(2.4423^n)$ time, using the Moon-Moser bound on the number of maximal independent sets. In 2006 Björklund and Husfeldt, and independently Koivisto, reached the $O^*(2^n)$ bound by inclusion-exclusion; the joint journal version, "Set partitioning via inclusion-exclusion", appeared in SIAM Journal on Computing in 2009. Fomin and Kratsch present it as a main example of inclusion-exclusion in their book on exact exponential algorithms.

## References
