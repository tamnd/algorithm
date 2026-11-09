---
tag: VR469Q
kind: definition
slug: partition-lattice
name: Partition lattice
aliases:
- Lattice of set partitions
- Pi_n
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: The set partitions of [n] ordered by refinement; a graded geometric lattice with B_n elements, rank n minus the number of blocks, and Moebius function (-1)^(n-1) (n-1)! from bottom to top.
prereqs: [set-partitions, lattice]
see_also: [stirling-numbers, bell-numbers, mobius-function, mobius-inversion, graphic-matroid, disjoint-set, partition-refinement, youngs-lattice]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 3, Partially ordered sets (the partition lattice as an example of a geometric lattice, and its Moebius function)
  - paper: doi:10.1007/BF00531932
    title: Gian-Carlo Rota, On the foundations of combinatorial theory I. Theory of Moebius functions, Zeitschrift fuer Wahrscheinlichkeitstheorie und verwandte Gebiete 2 (1964), 340-368
    locator: the example of the lattice of partitions of a set and the computation of its Moebius function
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (the partial order of refinement and its exercises)
---

The partition lattice $\Pi_n$ is the set of all [partitions](/set-partitions/) of $[n] = \{1, \ldots, n\}$, ordered by refinement: one partition is below another when each of its blocks fits inside a block of the other. It has $B_n$ elements, the meet of two partitions intersects their blocks, the join merges blocks that overlap, and the rank of a partition is $n$ minus its number of blocks. It is the lattice of flats of the complete graph, so it is a geometric lattice, and its Möbius function from bottom to top is $(-1)^{n-1}(n-1)!$.

## Definition

**Notation.** $n \ge 1$, $[n] = \{1, \ldots, n\}$, and $|\pi|$ is the number of blocks of a partition $\pi$. We write a partition by its blocks separated by bars, as $13|2|4$.

**Refinement.** For partitions $\pi, \sigma$ of $[n]$, $\pi \le \sigma$ when every block of $\pi$ is a subset of some block of $\sigma$. We say $\pi$ refines $\sigma$. This is a partial order. The poset $\Pi_n$ has a least element $\hat 0 = 1|2|\cdots|n$ and a greatest element $\hat 1 = 12\cdots n$. Some authors use the reverse order, with the finest partition on top.

**Equivalence relations.** A partition is the same as an equivalence relation on $[n]$: $i \sim_\pi j$ when $i$ and $j$ share a block. Then $\pi \le \sigma$ if and only if ${\sim_\pi} \subseteq {\sim_\sigma}$ as sets of pairs.

**Meet and join.** Any two partitions have a greatest lower bound and a least upper bound, so $\Pi_n$ is a [lattice](/lattice/):

- $\pi \wedge \sigma$ has as blocks the nonempty sets $B \cap C$ for $B \in \pi$, $C \in \sigma$. Its relation is ${\sim_\pi} \cap {\sim_\sigma}$.
- $\pi \vee \sigma$ has as blocks the connected components of the graph on $[n]$ whose edges join elements that share a block of $\pi$ or of $\sigma$. Its relation is the transitive closure of ${\sim_\pi} \cup {\sim_\sigma}$.

*Proof.* The intersection of two equivalence relations is an equivalence relation, and it is the largest one inside both. The transitive closure of the union is the smallest equivalence relation that contains both. $\square$

In [restricted growth string](/restricted-growth-string/) form, the meet takes $O(n)$ expected time: label each element $i$ with the pair $(a_i, b_i)$ of its block numbers and renumber the pairs in order of first appearance. The join takes $O(n\, \alpha(n))$ time with a [disjoint-set](/disjoint-set/) structure: union $i$ with the first element of its block in each partition.

**Covers and rank.** $\sigma$ covers $\pi$ if and only if $\sigma$ is $\pi$ with two blocks merged. So every maximal chain from $\hat 0$ to $\hat 1$ has $n - 1$ steps, $\Pi_n$ is graded, and the rank function is

$$r(\pi) = n - |\pi|.$$

The number of partitions of rank $r$ is the [Stirling number](/stirling-numbers/) $S(n, n - r)$. These are the Whitney numbers of the second kind of $\Pi_n$. There are $C(n, 2)$ atoms (one pair merged, $ij|\ldots$) and $S(n, 2) = 2^{n-1} - 1$ coatoms (two blocks).

**Intervals.** If $\sigma$ has blocks of sizes $m_1, \ldots, m_k$, then $[\hat 0, \sigma] \cong \Pi_{m_1} \times \cdots \times \Pi_{m_k}$, since refining $\sigma$ means refining each block on its own. If $|\pi| = k$, then $[\pi, \hat 1] \cong \Pi_k$, since a partition above $\pi$ is a partition of the blocks of $\pi$. Every interval is a product of partition lattices.

**Geometric lattice.** $\Pi_n$ is

- *atomistic*: each $\pi$ is the join of the atoms $ij|\ldots$ with $i \sim_\pi j$;
- *upper semimodular*: if $\pi \ne \sigma$ both cover $\tau$, then $\pi \vee \sigma$ covers both. Here $\pi$ merges two blocks $A, B$ of $\tau$ and $\sigma$ merges two blocks $C, D$ of $\tau$ with $\{A, B\} \ne \{C, D\}$. Whether the two pairs are disjoint or share one block, $\pi \vee \sigma$ has $|\tau| - 2$ blocks, so its rank is $r(\tau) + 2$. A finite graded lattice with this property satisfies $r(\pi \wedge \sigma) + r(\pi \vee \sigma) \le r(\pi) + r(\sigma)$ for all $\pi, \sigma$.

A finite lattice with both properties is called geometric. Equivalently, $\Pi_n$ is the lattice of flats of the [graphic matroid](/graphic-matroid/) of the complete graph $K_n$: a set of edges is closed exactly when it is the union of the complete graphs on the blocks of some partition.

**Möbius function.** For the [Möbius function](/mobius-function/) of $\Pi_n$,

$$\mu(\hat 0, \hat 1) = (-1)^{n-1} (n - 1)!, \qquad \sum_{\sigma \in \Pi_n} \mu(\hat 0, \sigma)\, x^{|\sigma|} = x (x - 1) \cdots (x - n + 1).$$

*Proof.* Fix an integer $x \ge 1$. Each map $f : [n] \to [x]$ has a kernel $\ker f \in \Pi_n$, whose blocks are the nonempty fibers of $f$. For each $\pi$, the maps that are constant on each block of $\pi$ are the maps with $\ker f \ge \pi$, and there are $x^{|\pi|}$ of them. The maps with $\ker f = \sigma$ number $x (x - 1) \cdots (x - |\sigma| + 1)$, since distinct blocks get distinct values. So

$$x^{|\pi|} = \sum_{\sigma \ge \pi} x (x - 1) \cdots (x - |\sigma| + 1).$$

[Möbius inversion](/mobius-inversion/) from above gives $x (x - 1) \cdots (x - |\pi| + 1) = \sum_{\sigma \ge \pi} \mu(\pi, \sigma)\, x^{|\sigma|}$. Take $\pi = \hat 0$. Both sides are polynomials in $x$ that agree for all $x \ge 1$, so they are equal. Only $\sigma = \hat 1$ has $|\sigma| = 1$, so $\mu(\hat 0, \hat 1)$ is the coefficient of $x$ in $x (x - 1) \cdots (x - n + 1)$, which is $(-1)^{n-1} (n - 1)!$. $\square$

So the sum of $\mu(\hat 0, \sigma)$ over the partitions of rank $r$ is the signed [Stirling number of the first kind](/stirling-numbers-first-kind/) $s(n, n - r)$. By the interval structure, $\mu(\pi, \sigma)$ is a product of such values for every pair $\pi \le \sigma$.

## Examples and non-examples

**$\Pi_3$.** Five elements: $1|2|3$ at the bottom, the three atoms $12|3$, $13|2$, $1|23$, and $123$ at the top. Any two atoms meet in $\hat 0$ and join in $\hat 1$. So $\Pi_3$ is the lattice $M_3$, which is modular but not distributive: $12|3 \wedge (13|2 \vee 1|23) = 12|3$, but $(12|3 \wedge 13|2) \vee (12|3 \wedge 1|23) = \hat 0$. The Möbius function gives $\mu(\hat 0, \text{atom}) = -1$ and $\mu(\hat 0, \hat 1) = -(1 - 3) = 2 = (-1)^2\, 2!$.

**Rank sizes.** The numbers of elements of ranks $0, 1, \ldots, n - 1$ are

| $n$ | $B_n$ | rank sizes $S(n, n - r)$ | $\mu(\hat 0, \hat 1)$ |
| --- | --- | --- | --- |
| $3$ | $5$ | $1, 3, 1$ | $2$ |
| $4$ | $15$ | $1, 6, 7, 1$ | $-6$ |
| $5$ | $52$ | $1, 10, 25, 15, 1$ | $24$ |
| $6$ | $203$ | $1, 15, 65, 90, 31, 1$ | $-120$ |

For $n = 4$, $\sum_\sigma \mu(\hat 0, \sigma)\, x^{|\sigma|} = x^4 - 6x^3 + 11x^2 - 6x = x(x-1)(x-2)(x-3)$.

**Meet and join in $\Pi_5$.** For $\pi = 123|45$ and $\sigma = 12|345$, $\pi \wedge \sigma = 12|3|45$ and $\pi \vee \sigma = 12345$. For $\pi = 12|3|45$ and $\sigma = 1|23|4|5$, $\pi \wedge \sigma = \hat 0$ and $\pi \vee \sigma = 123|45$.

**Not modular for $n \ge 4$.** In $\Pi_4$, take $\pi = 12|34$ and $\sigma = 13|24$. Then $\pi \wedge \sigma = 1|2|3|4$ and $\pi \vee \sigma = 1234$, so $r(\pi \wedge \sigma) + r(\pi \vee \sigma) = 0 + 3 < 2 + 2 = r(\pi) + r(\sigma)$. The inequality of semimodularity is strict, so $\Pi_4$ is not modular, and neither is $\Pi_n$ for $n \ge 4$, which contains a copy of $\Pi_4$ as the interval $[\hat 0, 1234|5|\cdots|n]$.

**Non-example: noncrossing partitions.** The noncrossing partitions of $[n]$ form a subposet $NC(n)$ of $\Pi_n$ with Catalan many elements: $1, 2, 5, 14, 42, 132$ for $n = 1, \ldots, 6$. $NC(n)$ is a lattice, but it is not a sublattice of $\Pi_n$. In $NC(4)$ the join of $13|2|4$ and $1|24|3$ is $1234$, while in $\Pi_4$ it is $13|24$, which is crossing.

**Non-example: counting blocks.** The preorder "$\pi \preceq \sigma$ when $|\pi| \ge |\sigma|$" is not refinement: $12|3 \preceq 1|23$ and $1|23 \preceq 12|3$, but the two partitions are different and neither refines the other.

**Non-example: integer partitions.** Ordering the integer partitions of $n$ by refinement of parts, or by dominance, gives different posets. The lattice of all integer partitions ordered by containment of diagrams is [Young's lattice](/youngs-lattice/).

## Related definitions

- [Set partitions](/set-partitions/) and [restricted growth strings](/restricted-growth-string/) are the elements; [Bell numbers](/bell-numbers/) and [Stirling numbers](/stirling-numbers/) count them by rank.
- A [lattice](/lattice/) is a poset with all meets and joins; a [join-semilattice](/join-semilattice/) has only joins.
- The [Möbius function](/mobius-function/) and [Möbius inversion](/mobius-inversion/) on $\Pi_n$ turn sums over coarser partitions into sums over exact kernels, as in the proof above. This is the basis of the inclusion-exclusion over set partitions in moment and cumulant formulas.
- A [matroid](/matroid/) has a geometric lattice of flats, and $\Pi_n$ is the case of the [graphic matroid](/graphic-matroid/) of $K_n$. For a graph $G$ on $[n]$, the flats of its graphic matroid form the bond lattice of $G$: the subposet of $\Pi_n$ of the partitions whose blocks induce connected subgraphs. A proof in the same style, which groups the maps $[n] \to [x]$ by the components of the edges whose two ends get the same value, shows that $\sum_\sigma \mu(\hat 0, \sigma)\, x^{|\sigma|}$ over the bond lattice is the chromatic polynomial of $G$.
- [Partition refinement](/partition-refinement/) repeatedly replaces a partition $\pi$ by $\pi \wedge \{S, [n] \setminus S\}$, a walk down $\Pi_n$.
- [Young's lattice](/youngs-lattice/) is the analogous lattice for integer partitions, ordered by containment of Ferrers diagrams.

## References
