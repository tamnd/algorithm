---
tag: BP7SAV
kind: problem
slug: three-dimensional-matching
name: Three-dimensional matching
aliases:
- 3-dimensional matching
- 3DM
area: complexity/np-completeness
level: core
summary: Given disjoint sets W, X, Y of size q and a set of triples, decide whether q of the triples cover every element exactly once. NP-complete.
prereqs: [np-complete, 3-sat, bipartite-matching]
see_also: [exact-cover-by-3-sets, exact-cover, bipartite-matching, partition-problem, three-partition, set-packing, unrelated-makespan-inapproximability, karps-21-np-complete-problems]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problem 3-DIMENSIONAL MATCHING and its reduction from EXACT COVER
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.2 (3DM is NP-complete, by a reduction from 3SAT), Section 3.1 (the reductions from 3DM to X3C and to PARTITION), Section 4.2 (the reduction from 3DM to 4-PARTITION) and the appendix, problem SP1
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 8.6, Partitioning Problems (3-dimensional matching)
---

Three-dimensional matching, or 3DM, asks whether a given set of triples contains a perfect matching: a choice of triples that uses every element exactly once. The elements come from three disjoint sets of the same size $q$, and each triple has one element from each set. With two sets instead of three, the problem is perfect [bipartite matching](/bipartite-matching/), which is in P. With three sets it is [NP-complete](/np-complete/). Karp proved this in 1972, and Garey and Johnson made 3DM one of their six basic NP-complete problems. It is the usual starting point for NP-hardness proofs of covering and packing problems, of [partition](/partition-problem/), and of [3-partition](/three-partition/).

## In plain words

A school has $q$ teachers, $q$ classes and $q$ time slots. Each allowed meeting is a triple: one teacher, one class, one slot. You want a timetable in which every teacher, every class and every slot is used exactly once.

If you drop the slots, you only pair teachers with classes. This pairing problem has fast and well-known methods. With the third set, the choices interact much more. A triple that looks good for a teacher and a class may take the only free slot of another pair. No fast method is known for the three-way problem, and it is one of the standard hard problems.

## Definition

**Instance.** Disjoint finite sets $W$, $X$ and $Y$ with $\lvert W \rvert = \lvert X \rvert = \lvert Y \rvert = q$, and a set of triples $M \subseteq W \times X \times Y$.

**Question.** Is there a set $M' \subseteq M$ of $q$ triples such that no two triples of $M'$ agree in any coordinate? Such an $M'$ contains each element of $W \cup X \cup Y$ exactly once, and it is called a perfect three-dimensional matching.

**Encoding.** The instance is a list of the elements and of the $\lvert M \rvert \le q^3$ triples. There are no large numbers, so the input length is $\Theta(q + \lvert M \rvert)$ up to logarithmic factors. The set $M'$ is a certificate that a verifier checks in linear time, so the problem is in NP.

**Complexity.** 3DM is NP-complete under Karp reductions. Karp (1972) reduced exact cover to it. Garey and Johnson (Section 3.1.2) give a reduction from [3-SAT](/3-sat/), described under Reductions. 3DM has no numbers, so it is NP-complete in the [strong sense](/strong-np-hardness/).

## Variants

- **Two dimensions.** With $M \subseteq X \times Y$, the question is whether a bipartite graph has a [perfect matching](/perfect-matching/). The Hopcroft-Karp algorithm and other [bipartite matching](/bipartite-matching/) algorithms solve it in polynomial time.
- **Exact cover by 3-sets.** Drop the condition that the triples are taken across three fixed sets: any 3-element subsets of a set of size $3q$ are allowed. This is [exact cover by 3-sets](/exact-cover-by-3-sets/), and 3DM is its special case.
- **Optimization.** Find a largest set of disjoint triples. It is NP-hard. Each maximal set of disjoint triples has at least a third of the size of a largest one, because each triple meets at most three triples of an optimal solution. It is a case of [set packing](/set-packing/).
- **Higher dimensions.** $k$-dimensional matching uses $k$ sets and $k$-tuples. It is NP-complete for each fixed $k \ge 3$, since 3DM is the case $k = 3$ and padding with new elements reduces $k$ to $k + 1$.
- **Numerical 3DM.** Each element carries a positive integer, and each triple of the matching must have the same total. It is a number problem that is NP-complete in the strong sense (Garey and Johnson, problem SP16).

## Examples

**A yes-instance.** Let $W = \{1, 2, 3\}$, $X = \{a, b, c\}$, $Y = \{x, y, z\}$, and let $M$ contain the 7 triples

$$(1, a, x), (1, b, y), (2, a, y), (2, c, z), (3, b, y), (3, c, x), (3, a, z).$$

The only perfect matching is $\{(1, a, x), (2, c, z), (3, b, y)\}$.

**A no-instance.** With the same sets, let $M$ contain the 8 triples

$$(1, a, x), (1, b, y), (2, a, y), (2, b, x), (3, c, x), (3, c, y), (1, c, z), (2, c, z).$$

Each of the three two-dimensional pictures of $M$ (the pairs on $W \times X$, on $W \times Y$, and on $X \times Y$) has a perfect matching. But there is no perfect three-dimensional matching. The element 3 occurs only in triples with $c$, and so does the element $z$, so a matching cannot cover both. Matchings on the three pairs of coordinates cannot be combined freely, and this is the reason the problem is hard.

**The reduction from 3-SAT on a small formula.** For $\varphi = (x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2 \lor \neg x_3)$, with $n = 3$ variables and $m = 2$ clauses, the construction below gives $q = 2mn = 12$ and $66$ triples: $12$ in the truth-setting components, $6$ in the clause components and $48$ for garbage collection. The formula is satisfiable, and the instance has a perfect matching.

## Known algorithms

- **Dynamic programming over subsets.** Process the elements of $W$ in a fixed order and keep the sets of used elements of $X$ and of $Y$. After $k$ steps both sets have size $k$, so there are at most $\sum_k \binom{q}{k}^2 = \binom{2q}{q} \le 4^q$ states. For $q = 20$ this is $137{,}846{,}528{,}820$ states. The time is $O^*(4^q)$ on a [word RAM](/word-ram/).
- **Exact cover solvers.** As a case of exact cover, 3DM is solved in practice by [Algorithm X](/algorithm-x/) with [dancing links](/dancing-links/) and by SAT and integer programming solvers, with no guarantee on the time. See [exact cover](/exact-cover/).
- **Parameterized algorithms.** Finding $k$ disjoint triples is [fixed-parameter tractable](/fixed-parameter-tractable/) in $k$; see [parameterized set packing](/parameterized-set-packing/).
- **Two dimensions.** Bipartite perfect matching takes $O(E \sqrt{V})$ time by the Hopcroft-Karp algorithm; see [bipartite matching](/bipartite-matching/).

## Bounds

- **NP-completeness.** NP-complete under Karp reductions (Karp 1972; Garey and Johnson, Section 3.1.2). So there is no polynomial-time algorithm unless P = NP.
- **Strong NP-completeness.** The problem has no numbers, so it is strongly NP-complete. It can therefore be the source of pseudo-polynomial transformations, as in the proof for 3-partition.
- **Contrast with two dimensions.** 2DM is in P and 3DM is NP-complete. This is one of the clearest boundaries between P and NP-complete problems, unless P = NP.

## Reductions

- **From 3-SAT (Karp reduction, Garey and Johnson Section 3.1.2).** Let the formula have variables $u_1, \ldots, u_n$ and clauses $c_1, \ldots, c_m$. Make the elements $u_i[j]$ and $\bar u_i[j]$ of $W$ for each variable $i$ and each clause index $j$. Each variable has a ring of triples on new elements $a_i[j] \in X$ and $b_i[j] \in Y$: the triples $(\bar u_i[j], a_i[j], b_i[j])$ form the set $T_i^t$, and the triples $(u_i[j], a_i[j+1], b_i[j])$, with $a_i[m+1] = a_i[1]$, form $T_i^f$. The elements $a_i[j]$ and $b_i[j]$ occur only in this ring, so a matching takes all of $T_i^t$ or all of $T_i^f$. Taking $T_i^t$ means $u_i$ is true, and leaves the elements $u_i[j]$ free. For each clause $c_j$, new elements $s_1[j] \in X$ and $s_2[j] \in Y$ occur in the triples $(u_i[j], s_1[j], s_2[j])$ for each literal $u_i$ of $c_j$, and $(\bar u_i[j], s_1[j], s_2[j])$ for each literal $\bar u_i$. So the clause is covered only by a free literal element, that is, a true literal. Finally, garbage elements $g_1[k] \in X$ and $g_2[k] \in Y$ for $k = 1, \ldots, m(n-1)$ occur with every element of $W$, and they cover the free literal elements that are not used by a clause. The total is $q = 2mn$, and the reduction takes polynomial time.
- **To exact cover by 3-sets (restriction).** Take the universe $W \cup X \cup Y$ and replace each triple by the 3-element set of its entries. See [exact cover by 3-sets](/exact-cover-by-3-sets/).
- **To partition (Karp reduction, Garey and Johnson Section 3.1).** Encode each triple as a number with one block of digits for each element, and add two balancing numbers. See the [partition problem](/partition-problem/).
- **To 4-partition and 3-partition (pseudo-polynomial transformations, Garey and Johnson Section 4.2).** The numbers that the reduction makes are bounded by a polynomial in $q$, which proves that [3-partition](/three-partition/) is NP-complete in the strong sense.
- **To scheduling on unrelated machines.** The reduction from 3DM gives the bound that no polynomial-time algorithm approximates the makespan on unrelated machines within a ratio below $3/2$ unless P = NP; see [unrelated makespan inapproximability](/unrelated-makespan-inapproximability/).

## Applications

- **Timetabling.** Assigning teachers, classes and time slots, or workers, tasks and machines, so that each is used once, is a three-dimensional matching problem when each allowed combination is given.
- **NP-hardness proofs.** 3DM is a standard source for hardness of covering and packing problems, number problems, scheduling and coding problems such as the [nearest codeword problem](/nearest-codeword-problem/).
- **Hypergraph matching.** A perfect matching in a 3-partite 3-uniform hypergraph is exactly a 3DM solution, so results on hypergraph matching apply.

## References
