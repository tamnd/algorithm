---
tag: YXPP84
kind: theorem
slug: matroid-intersection-theorem
name: Matroid intersection theorem
aliases:
- Edmonds' min-max theorem for matroid intersection
- Edmonds' matroid intersection theorem
area: optimization/combinatorial-optimization
level: advanced
summary: The maximum common independent set size equals the minimum of a rank-based expression over subsets.
prereqs: [matroid, matroid-intersection, submodular-function]
see_also: [matroid-intersection, matroid-intersection-algorithm, konig-theorem, hall-theorem, rado-edmonds-theorem, partition-matroid, three-dimensional-matching, max-flow-min-cut-theorem]
sources:
  - paper: "Jack Edmonds, Submodular functions, matroids, and certain polyhedra, in Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, 1969), Gordon and Breach, 1970, 69 to 87"
    locator: the matroid intersection theorem and the integrality of the intersection of two matroid polytopes
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 41, Matroid intersection (the min-max formula, its proofs and its consequences)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 13, Matroids (the section on matroid intersection)
  - book: isbn:9780486414539
    title: Eugene L. Lawler, Combinatorial Optimization, Networks and Matroids, Holt, Rinehart and Winston, 1976 (Dover reprint 2001)
    locator: Chapter 8, Matroid intersections
  - paper: "Richard Rado, A theorem on independence relations, Quarterly Journal of Mathematics 13, 83 to 89, 1942"
    locator: the condition for an independent transversal
---

The matroid intersection theorem, proved by Jack Edmonds in 1970, says that the largest size of a set that is independent in two [matroids](/matroid/) $M_1$ and $M_2$ on the same ground set $E$ equals $\min_{U \subseteq E} \bigl( r_1(U) + r_2(E \setminus U) \bigr)$, where $r_1$ and $r_2$ are the rank functions. The inequality "max at most min" is easy. The content of the theorem is that the two numbers are always equal, so a largest common independent set always has a short proof of optimality. The theorem contains [Kőnig's theorem](/konig-theorem/) on bipartite matching, [Hall's theorem](/hall-theorem/) and Rado's theorem on independent transversals, and it is the basis of the polynomial-time [matroid intersection algorithm](/matroid-intersection-algorithm/). It fails for three matroids, where the corresponding problem is [NP-hard](/np-hard/).

## Statement

Let $M_1 = (E, \mathcal{I}_1)$ and $M_2 = (E, \mathcal{I}_2)$ be matroids on the same finite set $E$, with rank functions $r_1$ and $r_2$. For $S \subseteq E$, $r_i(S)$ is the size of a largest subset of $S$ that is independent in $M_i$.

**Theorem (Edmonds, 1970).**
$$\max \{ |I| : I \in \mathcal{I}_1 \cap \mathcal{I}_2 \} = \min_{U \subseteq E} \bigl( r_1(U) + r_2(E \setminus U) \bigr).$$

A set $U$ that attains the minimum is a *certificate*: together with a common independent set of the same size, it proves that both are optimal.

## In plain words

Two sets of rules decide which groups of items you may take. Each set of rules is of the matroid kind, so it alone is easy. You want the largest group that both sets of rules allow.

Split the items into two piles in any way you like. From the first pile, the first rules let you take only so many. From the second pile, the second rules let you take only so many. Any allowed group takes items from the two piles, so it is never larger than the sum of these two limits. The theorem says that some split makes this sum exactly as large as the best group. So a best group can always be proved best with one well-chosen split.

## Proof

We use the following facts about a matroid with rank function $r$:

- (R1) $0 \le r(S) \le |S|$, and $r(S) = |S|$ exactly when $S$ is independent.
- (R2) $r(S) \le r(T)$ for $S \subseteq T$.
- (R3) $r$ is [submodular](/submodular-function/): $r(S) + r(T) \ge r(S \cup T) + r(S \cap T)$.

We also use two minors. Let $e \in E$. The *deletion* $M \setminus e$ is the matroid on $E - e$ with the same independent sets that avoid $e$, and its rank function is $r$ restricted to subsets of $E - e$. If $\{e\}$ is independent, the *contraction* $M / e$ is the matroid on $E - e$ whose independent sets are the sets $J$ with $J + e \in \mathcal{I}$. Its rank function is $r_{M/e}(S) = r(S + e) - 1$. Both minors are matroids.

**Weak duality.** Let $I$ be common independent and $U \subseteq E$. The set $I \cap U$ is independent in $M_1$ and lies in $U$, so $|I \cap U| \le r_1(U)$. Likewise $|I \setminus U| \le r_2(E \setminus U)$. Adding,
$$|I| = |I \cap U| + |I \setminus U| \le r_1(U) + r_2(E \setminus U).$$

**Equality.** Let $k(M_1, M_2)$ denote the minimum on the right. We show by induction on $|E|$ that some common independent set has size $k = k(M_1, M_2)$. For $E = \emptyset$, $k = 0$ and $I = \emptyset$ works. Let $|E| \ge 1$ and pick $e \in E$.

*Case 1: $e$ is a loop of $M_1$ or of $M_2$*, that is, $\{e\}$ is dependent in one of them. Then no common independent set contains $e$, and we delete it. For $U \subseteq E - e$, if $e$ is a loop of $M_1$, then $r_1(U) + r_2(E - e - U) = r_1(U + e) + r_2(E \setminus (U + e))$; if $e$ is a loop of $M_2$, then $r_1(U) + r_2(E - e - U) = r_1(U) + r_2(E \setminus U)$. In both cases this value is at least $k$, so $k(M_1 \setminus e, M_2 \setminus e) \ge k$, and the induction hypothesis gives a common independent set of size at least $k$ that avoids $e$.

*Case 2: $\{e\}$ is independent in both.* Apply the induction hypothesis to the deletions and to the contractions.

- If $k(M_1 \setminus e, M_2 \setminus e) \ge k$, the deletions have a common independent set of size $k$, and it is common independent in $M_1$ and $M_2$.
- If $k(M_1 / e, M_2 / e) \ge k - 1$, the contractions have a common independent set $J$ of size $k - 1$. Then $J + e$ is common independent in $M_1$ and $M_2$, of size $k$.

Suppose that neither holds. Then there are $U, W \subseteq E - e$ with
$$r_1(U) + r_2(E - e - U) \le k - 1, \qquad \bigl( r_1(W + e) - 1 \bigr) + \bigl( r_2(E - W) - 1 \bigr) \le k - 2,$$
where the second line uses the contraction rank and $(E - e) \setminus W + e = E \setminus W$. So $r_1(W + e) + r_2(E \setminus W) \le k$. Add the two inequalities and apply (R3) twice. In $M_1$,
$$r_1(U) + r_1(W + e) \ge r_1(U \cup W + e) + r_1(U \cap W).$$
In $M_2$, the sets $E - e - U$ and $E \setminus W$ have union $E \setminus (U \cap W)$, because $e \notin W$, and intersection $E \setminus (U \cup W + e)$. So
$$r_2(E - e - U) + r_2(E \setminus W) \ge r_2\bigl(E \setminus (U \cap W)\bigr) + r_2\bigl(E \setminus (U \cup W + e)\bigr).$$
Adding, and grouping the terms for $X = U \cup W + e$ and for $Y = U \cap W$,
$$2k - 1 \ge \bigl( r_1(X) + r_2(E \setminus X) \bigr) + \bigl( r_1(Y) + r_2(E \setminus Y) \bigr) \ge k + k,$$
since each bracket is at least the minimum $k$. This is a contradiction. So one of the two bullets holds, and there is a common independent set of size $k$.

With weak duality, the maximum equals $k$. $\blacksquare$

**A constructive proof.** The [matroid intersection algorithm](/matroid-intersection-algorithm/) gives a second proof. It grows a common independent set along shortest paths in an exchange graph. When no path exists, the set $U$ of elements that can reach the target satisfies $|I| = r_1(U) + r_2(E \setminus U)$. Its [correctness proof](/matroid-intersection-algorithm/) shows this in full.

**Example.** Take six links between towns 1 to 5: $a$ = 1-5 red, $b$ = 2-5 yellow, $c$ = 3-4 yellow, $d$ = 1-2 green, $e$ = 2-5 blue, $f$ = 1-4 yellow. Let $M_1$ be the [graphic matroid](/graphic-matroid/) and $M_2$ the [partition matroid](/partition-matroid/) with at most one link per color. Each matroid has rank 4, but the set $U = \{a, d, e\}$ gives $r_1(U) + r_2(E \setminus U) = 2 + 1 = 3$: the links of $U$ use only the towns 1, 2 and 5, and the other links are all yellow. The set $\{a, c, d\}$ is common independent of size 3, so the maximum is 3.

## Consequences

- **[Kőnig's theorem](/konig-theorem/).** For a [bipartite graph](/bipartite-graph/) with sides $L$ and $R$, let $M_1$ and $M_2$ be the partition matroids on the edges that allow at most one edge at each vertex of $L$, and of $R$. Common independent sets are matchings. For a set $U$ of edges, $r_1(U)$ is the number of vertices of $L$ covered by $U$, and $r_2(E \setminus U)$ the number of vertices of $R$ covered by the other edges. These vertices form a [vertex cover](/vertex-cover/), so the theorem gives maximum matching = minimum vertex cover.
- **Rado's theorem.** A family of sets $A_1, \ldots, A_m \subseteq S$ has a transversal (distinct representatives $a_i \in A_i$) that is independent in a matroid $M$ on $S$ if and only if $r_M\bigl(\bigcup_{i \in K} A_i\bigr) \ge |K|$ for every $K \subseteq \{1, \ldots, m\}$. Apply the theorem to the pairs $(i, a)$ with $a \in A_i$, with a partition matroid by $i$ and the matroid $M$ applied to $a$. For the free matroid this is [Hall's theorem](/hall-theorem/).
- **Common bases.** Two matroids of rank $r$ have a common basis if and only if $r_1(U) + r_2(E \setminus U) \ge r$ for every $U$. For example, a graph whose edges have colors has a spanning tree with all colors distinct, or with prescribed color counts, under such a condition.
- **Matroid union and tree packing.** Applied to a direct sum of matroids and a matroid that merges copies of each element, the theorem gives the matroid union theorem of Nash-Williams (1966). This contains the theorem of Tutte (1961) and Nash-Williams (1961) on $k$ edge-disjoint spanning trees.
- **Polyhedra.** Edmonds proved in the same paper the stronger statement that the intersection of the two matroid polytopes $\{x \ge 0 : x(S) \le r_i(S) \text{ for all } S\}$ is integral, and that the system is totally dual integral. So the weighted version also has a min-max formula, and [LP duality](/lp-duality/) applies to it. For one matroid, this is the polyhedral side of the [Rado-Edmonds theorem](/rado-edmonds-theorem/).
- **Algorithms.** Since both sides can be checked with rank evaluations, [matroid intersection](/matroid-intersection/) is in NP ∩ coNP for matroids given by oracles, and the [matroid intersection algorithm](/matroid-intersection-algorithm/) finds both a maximum set and a minimizing $U$ in polynomial time.

## Tightness

- **Three matroids.** For three matroids, weak duality still gives $\max |I| \le \min \bigl( r_1(U_1) + r_2(U_2) + r_3(U_3) \bigr)$ over partitions of $E$ into $U_1, U_2, U_3$, but equality can fail. Take $E = \{1, 2, 3\}$ and three partition matroids that allow at most one element from $\{1, 2\}$, from $\{2, 3\}$ and from $\{1, 3\}$, in turn. Every pair of elements is dependent in one of them, so the maximum is 1. Each element is a non-loop in each matroid, so a partition with two nonempty parts costs at least 2, and a partition with one part $E$ costs $r_i(E) = 2$. So the minimum is 2. In general the problem for three partition matroids is [three-dimensional matching](/three-dimensional-matching/), which is NP-hard, so no min-max formula with a polynomial-time checkable certificate is expected.
- **The minimum needs the split.** The bound $\min(r_1(E), r_2(E))$, which uses only $U = E$ or $U = \emptyset$, is not tight: in the example both ranks are 4 and the answer is 3.
- **Submodularity is the key.** The uncrossing step in the proof uses only (R3). Edmonds proved the more general polymatroid intersection theorem, for two integer [submodular functions](/submodular-function/) in place of the rank functions.

## History

Richard Rado proved in 1942 his theorem on independent transversals, which is the special case with one partition matroid. Jack Edmonds presented the general theorem at the Calgary conference of 1969, published in 1970, together with the integrality of the intersection of two matroid polytopes and the polymatroid intersection theorem. Lawler (1975) and Edmonds (1979) gave the augmenting path algorithm, which gives a constructive proof. The theorem is one of the main examples of a combinatorial min-max relation, next to the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) and the [Tutte-Berge formula](/tutte-berge-formula/).

## References
