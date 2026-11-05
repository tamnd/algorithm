---
tag: EVVF4C
kind: theorem
slug: dilworth-theorem
name: Dilworth's theorem
aliases:
- chain-antichain theorem
area: sequences/subsequence-problems
level: core
summary: In a finite partially ordered set, the largest antichain equals the minimum number of chains covering it.
prereqs: [konig-theorem, bipartite-matching]
see_also: [erdos-szekeres-theorem, longest-increasing-subsequence, path-cover-by-bipartite-matching, hopcroft-karp, patience-sorting, hall-theorem, max-flow-min-cut-theorem]
sources:
  - paper: "R. P. Dilworth, A decomposition theorem for partially ordered sets, Annals of Mathematics 51(1), 1950, 161-166"
    locator: the main decomposition theorem for finite partially ordered sets and its proof by induction
  - paper: "D. R. Fulkerson, Note on Dilworth's decomposition theorem for partially ordered sets, Proceedings of the American Mathematical Society 7(4), 1956, 701-702"
    locator: the proof by reduction to a bipartite matching problem (Konig's theorem)
  - paper: "L. Mirsky, A dual of Dilworth's decomposition theorem, American Mathematical Monthly 78(8), 1971, 876-877"
    locator: the dual theorem (the longest chain equals the least number of antichains that cover the set)
---

Dilworth's theorem says that in each finite partially ordered set, the largest size of an antichain (a set of pairwise incomparable elements) equals the least number of chains (sets of pairwise comparable elements) that cover the set. Dilworth proved it in 1950. Fulkerson's 1956 proof reduces it to [König's theorem](/konig-theorem/) on [bipartite matchings](/bipartite-matching/), which also gives a polynomial algorithm for both sides. For sequences, it and its dual by Mirsky connect the [longest increasing subsequence](/longest-increasing-subsequence/) with partitions into monotone subsequences, and imply the [Erdős-Szekeres theorem](/erdos-szekeres-theorem/).

## Statement

A *partially ordered set* (poset) is a set $P$ with a relation $\le$ that is reflexive, antisymmetric and transitive. Write $x < y$ for $x \le y$ and $x \ne y$. Two elements are *comparable* if $x \le y$ or $y \le x$. A *chain* is a subset in which each two elements are comparable. An *antichain* is a subset in which no two distinct elements are comparable. The *width* $w(P)$ is the largest size of an antichain.

**Theorem (Dilworth 1950).** Let $P$ be a finite poset. Then the least number of chains whose union is $P$ equals $w(P)$. Moreover, $P$ can be partitioned into $w(P)$ disjoint chains.

**Theorem (Mirsky 1971, the dual).** Let $P$ be a finite poset. Then the least number of antichains whose union is $P$ equals the largest size of a chain.

**For sequences.** Let $A = \langle a_1, \ldots, a_n \rangle$ be a sequence of numbers. Order the positions by $i \prec j$ if $i < j$ and $a_i < a_j$. The chains are the increasing subsequences, and the antichains are the non-increasing subsequences. So:

- (Dilworth) the least number of increasing subsequences that cover $A$ equals the length of a longest non-increasing subsequence;
- (Mirsky) the least number of non-increasing subsequences that cover $A$ equals the length of a longest increasing subsequence.

## In plain words

Some tasks must come before other tasks, and some pairs of tasks do not care about each other. A chain is a list of tasks in which each pair has an order, so one worker can do them one after the other. An antichain is a group of tasks in which no pair has an order.

How many workers do you need so that each worker does a chain and all tasks get done? Each task of an antichain needs its own worker, so you need at least as many workers as the size of the biggest antichain. Dilworth's theorem says that this many workers is always enough.

## Proof

**The easy direction.** A chain and an antichain share at most one element, since two shared elements would be both comparable and incomparable. So if $C_1, \ldots, C_k$ cover $P$ and $A$ is an antichain, each element of $A$ is in some $C_i$, and no $C_i$ holds two of them, so $|A| \le k$. Hence the number of chains in each cover is at least $w(P)$.

**The hard direction (Fulkerson).** Let $|P| = N$. Build a bipartite graph $G$ with a left copy $x'$ and a right copy $x''$ of each element $x$, and an edge $x' y''$ for each pair with $x < y$.

*Step 1: matchings give chain partitions.* Let $M$ be a matching of $G$. Read each edge $x' y''$ of $M$ as "$y$ comes right after $x$". Each element has at most one successor (its left copy is in at most one edge) and at most one predecessor (its right copy is in at most one edge). There is no cycle: along the successor links the elements strictly increase, and $x_1 < x_2 < \cdots < x_1$ would give $x_1 < x_1$ by transitivity. So the links form disjoint paths that cover $P$, where an element with no link is a path of length 0. Each path $x_1 < x_2 < \cdots$ is a chain, by transitivity. Each element except the first of its path has a predecessor, so the number of paths is $N - |M|$. Hence $P$ has a partition into $N - |M|$ chains.

*Step 2: vertex covers give antichains.* By [König's theorem](/konig-theorem/), $G$ has a vertex cover $C$ (a set of vertices that touches each edge) with $|C| = \nu(G)$, the size of a maximum matching. Let $A$ be the set of elements $x$ with $x' \notin C$ and $x'' \notin C$. Each vertex of $C$ removes at most one element from $A$, so $|A| \ge N - |C| = N - \nu(G)$. $A$ is an antichain: if $x, y \in A$ with $x < y$, the edge $x' y''$ has neither end in $C$, which contradicts that $C$ is a cover.

*Step 3: combine.* Take a maximum matching $M$, with $|M| = \nu(G)$. Step 1 gives a partition into $N - \nu(G)$ chains, and Step 2 gives an antichain of size at least $N - \nu(G)$. By the easy direction, each antichain has size at most the number of chains of each cover. So

$$N - \nu(G) \le w(P) \le N - \nu(G),$$

and the partition of Step 1 has exactly $w(P)$ chains. $\square$

**Proof of Mirsky's theorem.** An antichain meets a chain in at most one element, so a chain of length $h$ needs $h$ antichains to cover it, and each cover by antichains has at least $h$ parts, where $h$ is the largest chain size. For the other direction, let $\mathrm{ht}(x)$ be the largest size of a chain whose largest element is $x$. Then $1 \le \mathrm{ht}(x) \le h$. If $x < y$, a chain that ends at $x$ extended by $y$ ends at $y$, so $\mathrm{ht}(y) > \mathrm{ht}(x)$. Hence the sets $A_k = \{x : \mathrm{ht}(x) = k\}$, $k = 1, \ldots, h$, are antichains, and they cover $P$. $\blacksquare$

## Consequences

- **Algorithm for the width.** Steps 1 and 2 are constructive. A maximum matching of $G$, for example by [Hopcroft-Karp](/hopcroft-karp/), gives a minimum chain partition, and a minimum vertex cover from the same matching gives a maximum antichain. With $N$ elements and $E \le \binom{N}{2}$ comparable pairs, this takes $O(E \sqrt{N})$ time. The same method gives a minimum path cover of a DAG after transitive closure: see [path cover by bipartite matching](/path-cover-by-bipartite-matching/).
- **Sequences in $O(n \log n)$.** For the order of positions in a sequence, no matching is needed. The piles of [patience sorting](/patience-sorting/) are non-increasing subsequences (each pile, from bottom to top, does not increase), and their number is the LIS length, which by Mirsky's theorem is the least possible. The same greedy method with the order reversed gives a least cover by increasing subsequences.
- **Erdős-Szekeres.** Let $A$ be a sequence of $N$ distinct numbers. The non-increasing subsequences are then decreasing. By Mirsky, $A$ is covered by $L_{\uparrow}(A)$ decreasing subsequences, each of length at most $L_{\downarrow}(A)$, so $N \le L_{\uparrow}(A) \cdot L_{\downarrow}(A)$. This is the product form of the [Erdős-Szekeres theorem](/erdos-szekeres-theorem/).
- **Equivalences.** Dilworth's theorem, König's theorem, Hall's marriage theorem and the max-flow min-cut theorem on unit networks can each be derived from the others.

## Tightness

- **Chains, not paths.** In a DAG, a cover by vertex-disjoint *paths* can need more parts than the width, because a chain may skip vertices that a path must visit. The theorem is about chains of the order, which is the transitive closure of the DAG.
- **Partition and cover.** The least cover and the least partition have the same size, because removing an element from a chain leaves a chain.
- **Example where both sides are equal.** In the divisibility order on $\{1, \ldots, 10\}$, the set $\{6, 7, 8, 9, 10\}$ is an antichain (no one of them divides another), and the five chains $\{1, 2, 4, 8\}$, $\{3, 6\}$, $\{5, 10\}$, $\{7\}$, $\{9\}$ cover the set. So the width is 5.
- **Example on a sequence.** For $A = \langle 3, 1, 4, 1, 5, 9, 2, 6 \rangle$ with the order "$i < j$ and $a_i < a_j$", a maximum matching of $G$ has size 5, so the least chain cover has $8 - 5 = 3$ increasing subsequences: $\langle 3, 6 \rangle$, $\langle 1, 4, 5, 9 \rangle$ and $\langle 1, 2 \rangle$. The values 3, 1, 1 at positions 1, 2 and 4 are a non-increasing subsequence of length 3, so 3 chains are necessary.

## History

Dilworth published the theorem in the Annals of Mathematics in 1950, with a proof by induction on the size of the poset. Fulkerson gave the proof by bipartite matching in 1956. Mirsky published the dual statement, which is much easier, in 1971.

## References
