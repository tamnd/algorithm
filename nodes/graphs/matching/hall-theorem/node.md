---
tag: QVNCXM
kind: theorem
slug: hall-theorem
name: Hall's marriage theorem
aliases:
- Hall's theorem
- marriage theorem
area: graphs/matching
level: core
summary: A bipartite graph has a matching saturating one side iff every subset of that side has enough neighbours.
prereqs: [bipartite-graph, berge-lemma]
see_also: [konig-theorem, bipartite-matching, tutte-theorem, perfect-matching, dulmage-mendelsohn-decomposition, menger-theorem, hopcroft-karp, regular-graph]
sources:
  - paper: doi:10.1112/jlms/s1-10.37.26
    title: Philip Hall, On representatives of subsets, Journal of the London Mathematical Society 10(1), 26 to 30 (1935)
    locator: the theorem on systems of distinct representatives
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Hall's theorem, the proof by alternating paths, and the corollary on regular bipartite graphs)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 2.1, Matching in bipartite graphs (the marriage theorem and three proofs)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 22.1, Transversals, Section 22.1a, Alternative proofs of Hall's marriage theorem, and Section 16.7h, Historical notes on bipartite matching
---

Hall's marriage theorem says that a [bipartite graph](/bipartite-graph/) with sides $X$ and $Y$ has a matching that covers every vertex of $X$ if and only if every set $S \subseteq X$ has at least $|S|$ neighbours in $Y$. The condition is necessary for an obvious reason, and the theorem says that this obvious obstacle is the only one. It is a statement about bipartite, unweighted graphs; its analogue for general graphs is [Tutte's theorem](/tutte-theorem/). It is equivalent to [Kőnig's theorem](/konig-theorem/) and is a special case of [Menger's theorem](/menger-theorem/) and of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## Statement

Let $G = (X \cup Y, E)$ be a finite bipartite graph, with every edge joining $X$ to $Y$. For $S \subseteq X$, let $N(S) = \{ y \in Y : xy \in E \text{ for some } x \in S \}$ be the neighbourhood of $S$. A matching $M$ *saturates* $X$ if every vertex of $X$ is an end of an edge of $M$.

**Theorem (Hall, 1935).** $G$ has a matching that saturates $X$ if and only if

$$|N(S)| \ge |S| \qquad \text{for every } S \subseteq X. \tag{Hall's condition}$$

**Deficiency form (Kőnig and Ore).** For every finite bipartite graph, the size of a maximum matching is

$$\nu(G) = |X| - \max_{S \subseteq X} \bigl(|S| - |N(S)|\bigr).$$

The maximum is at least 0, by $S = \emptyset$. The theorem is the case where the maximum is 0.

## In plain words

Some people each name the jobs they can do, and each job can go to one person only. Can every person get a job? If some group of people can do, between them, fewer jobs than there are people in the group, then the answer is clearly no. Hall's theorem says that this is the only thing that can go wrong. If every group, of every size, can do at least as many jobs as it has members, then everyone can get a job at the same time.

The counting form says more: the number of people left without a job, in the best assignment, is the largest shortfall of any group.

## Proof

**Necessity.** Let $M$ saturate $X$ and let $S \subseteq X$. The partners in $M$ of the vertices of $S$ are $|S|$ distinct vertices of $N(S)$, so $|N(S)| \ge |S|$.

**Sufficiency.** Assume Hall's condition, and let $M$ be a maximum matching. Suppose, for a contradiction, that some $x \in X$ is free. Let $Z$ be the set of vertices that are ends of [$M$-alternating paths](/alternating-path/) that start at $x$ (including $x$, by the path with no edge). Let $S = Z \cap X$ and $T = Z \cap Y$.

1. *Parity.* Along any path from $x$, the vertices alternate between $X$ and $Y$. Since $x$ is free, the first edge of an alternating path from $x$ is not in $M$, so the path enters each vertex of $Y$ by an edge outside $M$ and each vertex of $X$ other than $x$ by an edge of $M$.
2. *Each $y \in T$ is matched, and its partner is in $S$.* Let $P$ be an alternating path from $x$ to $y$. If $y$ were free, $P$ would be an $M$-augmenting path, and by [Berge's lemma](/berge-lemma/) $M$ would not be maximum. So $y$ has a partner $x'$ with $yx' \in M$. The vertex $x'$ is not on $P$: it is not $x$, which is free, and an inner vertex of $P$ has its matched edge on $P$, so $x'y$ would be the last edge of $P$, which by step 1 is not in $M$. So $P$ followed by the edge $yx'$ is an alternating path, and $x' \in S$.
3. *Each $x' \in S \setminus \{x\}$ is the partner of a vertex of $T$.* By step 1, the last edge of an alternating path from $x$ to $x'$ is an edge $yx' \in M$ whose end $y$ lies on the path, so $y \in T$.
4. Steps 2 and 3 show that $M$ restricted to $Z$ pairs $T$ with $S \setminus \{x\}$ one to one. So $|S| = |T| + 1$.
5. *$N(S) = T$.* Each $y \in T$ is entered from a vertex of $S$, so $T \subseteq N(S)$. Conversely, let $s \in S$ and $sy \in E$. If $sy \in M$, then $s \ne x$ and $y$ is the vertex before $s$ on an alternating path to $s$ (step 3), so $y \in T$. If $sy \notin M$, take an alternating path $P$ from $x$ to $s$; it ends with an edge of $M$ or has no edge. If $y \in P$, then $y$ is the end of a prefix of $P$, so $y \in T$. Otherwise $P$ followed by $sy$ is alternating, and $y \in T$.
6. So $|N(S)| = |T| = |S| - 1 < |S|$, which contradicts Hall's condition. Hence no vertex of $X$ is free, and $M$ saturates $X$.

**Deficiency form.** Let $d = \max_S (|S| - |N(S)|)$. A matching leaves at least $|S| - |N(S)|$ vertices of each $S$ free, since the vertices of $S$ can only be matched into $N(S)$; so $\nu(G) \le |X| - d$. For the other inequality, add $d$ new vertices to $Y$, each joined to every vertex of $X$. In the new graph each nonempty $S$ has $|N(S)| + d \ge |S|$ neighbours, so by the theorem a matching $M'$ saturates $X$. At most $d$ edges of $M'$ use new vertices, so $G$ has a matching with at least $|X| - d$ edges. $\blacksquare$

## Consequences

- **Regular bipartite graphs.** If $G$ is bipartite and $k$-regular with $k \ge 1$, then $G$ has a [perfect matching](/perfect-matching/). *Proof.* For $S \subseteq X$, the $k|S|$ edges at $S$ all end in $N(S)$, and $N(S)$ receives at most $k|N(S)|$ edges, so $|N(S)| \ge |S|$. Counting all edges gives $k|X| = k|Y|$, so a matching that saturates $X$ is perfect. $\square$ Applied again and again, this splits a $k$-regular bipartite graph into $k$ perfect matchings, which is Kőnig's edge colouring theorem: such a graph has [chromatic index](/chromatic-index/) $k$.
- **Systems of distinct representatives.** Sets $A_1, \ldots, A_n$ have distinct elements $a_i \in A_i$ if and only if every union of $k$ of the sets has at least $k$ elements. This is the theorem for the graph that joins $i$ to the elements of $A_i$, and it is the form in which Hall stated it.
- **Kőnig's theorem.** The deficiency form, applied to a set $S$ that attains the maximum, gives the vertex cover $(X \setminus S) \cup N(S)$ of size $|X| - |S| + |N(S)| = \nu(G)$. So the largest matching and the smallest [vertex cover](/vertex-cover/) have the same size, which is [Kőnig's theorem](/konig-theorem/).
- **Certificates.** A maximum matching that misses a vertex $x$ yields, through steps 1 to 6, a set $S$ with $|N(S)| < |S|$. So [Hopcroft-Karp](/hopcroft-karp/) or any augmenting-path algorithm either finds a matching that saturates $X$ or a short proof that none exists, in polynomial time, although Hall's condition has $2^{|X|}$ sets to check.
- **Doubly stochastic matrices.** The theorem gives the Birkhoff and von Neumann result that every doubly stochastic matrix is a convex combination of permutation matrices: the support of such a matrix satisfies Hall's condition, so it contains a permutation, and induction on the number of nonzero entries finishes the proof. In polyhedral terms, the bipartite perfect matching polytope is the set of [fractional perfect matchings](/fractional-matching/).

## Tightness

- **All subsets are needed.** Let $X = \{1, 2, 3, 4\}$, $Y = \{a, b, c, d\}$, and let 1 be adjacent to $a, b$; 2 and 3 to $a$ only; 4 to $c, d$. Each single vertex has a neighbour, and $N(X) = Y$ has 4 vertices. But $S = \{2, 3\}$ has $N(S) = \{a\}$, so no matching saturates $X$. The largest value of $|S| - |N(S)|$ is 1, reached at $\{2, 3\}$ and at $\{1, 2, 3\}$, so $\nu(G) = 3$.
- **Edge cases.** If $X = \emptyset$, the empty matching saturates $X$, and the condition holds trivially. If some $x \in X$ has no neighbour, then $S = \{x\}$ violates the condition.
- **Infinite families.** The theorem fails for infinitely many sets. Let $A_0 = \{1, 2, 3, \ldots\}$ and $A_i = \{i\}$ for $i \ge 1$. Any $k$ of the sets have at least $k$ elements in their union, but $A_1, A_2, \ldots$ force $a_i = i$, and then $A_0$ has no element left. Hall's theorem does hold for infinite families of finite sets, a result of Marshall Hall Jr.
- **General graphs.** Without bipartiteness a neighbourhood condition is not enough. In the triangle, every set of vertices $S$ has $|N(S)| \ge |S|$, but there is no perfect matching, because the number of vertices is odd. For general graphs the right condition counts the odd components left after removing a set, as in [Tutte's theorem](/tutte-theorem/).

## History

Philip Hall published the theorem in 1935, in the language of systems of distinct representatives. Equivalent results were known before: Kőnig's 1931 theorem on bipartite graphs and Frobenius's 1917 theorem on determinants imply it, and Schrijver's historical notes in Section 16.7h describe these links. Halmos and Vaughan gave the short induction proof in 1950 and named it the marriage problem. The proof above, by alternating paths, is the one that gives an algorithm.

## References
