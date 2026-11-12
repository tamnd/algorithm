---
tag: KA3NGY
kind: theorem
slug: minimum-guard-np-hardness
name: NP-hardness of minimum guard
aliases:
- Lee-Lin hardness
area: graphics-and-signals/visibility
level: advanced
summary: Deciding if k vertex guards can see all of a simple polygon is NP-complete, by the 3-SAT reduction of Lee and Lin. The point guard version is NP-hard as well.
prereqs: [art-gallery-problem, np-hard, 3-sat, polynomial-time-reduction]
see_also: [art-gallery-problem, art-gallery-theorem, chvatal-art-gallery-theorem, orthogonal-art-gallery-theorem, visibility-polygon, np-complete, star-shaped-polygon, polygon-with-holes]
sources:
  - paper: doi:10.1109/TIT.1986.1057165
    title: D. T. Lee and A. K. Lin, Computational complexity of art gallery problems, IEEE Transactions on Information Theory 32(2), 1986, pages 276 to 282
    locator: the whole paper (the reduction from 3-SAT for guards in a simple polygon)
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 9, Section 9.2 (Theorem 9.1, polygons with holes), Section 9.3 (Lemma 9.7, Theorem 9.2 and the corollary for point guards), Sections 9.4 and 9.5 (cases that are solvable in polynomial time)
  - paper: doi:10.1109/TIT.1983.1056648
    title: Joseph O'Rourke and Kenneth J. Supowit, Some NP-hard polygon decomposition problems, IEEE Transactions on Information Theory 29(2), 1983, pages 181 to 190
    locator: the whole paper (the minimum star cover of a polygon with holes)
  - paper: doi:10.1145/3486220
    title: Mikkel Abrahamsen, Anna Adamaszek and Tillmann Miltzow, The art gallery problem is ∃ℝ-complete, Journal of the ACM 69(1), 2022, pages 1 to 70
    locator: the abstract and the main theorem (point guards in a simple polygon), first published at STOC 2018, doi:10.1145/3188745.3188868
---

The minimum guard problem asks for the fewest guards that see all of a given polygon. This theorem says that the problem is hard: deciding whether $k$ guards at vertices can see all of a simple polygon is NP-complete, and the version with guards at any points is NP-hard. D. T. Lee and A. K. Lin proved it in 1986 by a reduction from [3-SAT](/3-sat/). Before that, O'Rourke and Supowit had proved it for polygons with holes. The problem itself, its variants and its approximation algorithms are on the [art gallery problem](/art-gallery-problem/) page in geometry, and this page gives the proof of hardness. The worst case over all polygons is a different and easy question: $\lfloor n/3 \rfloor$ guards always suffice, by [Chvátal's theorem](/chvatal-art-gallery-theorem/), and they can be placed in $O(n)$ time after a triangulation. Hardness is about the fewest guards for the polygon at hand, which can be far fewer.

## Statement

**Setting.** $P$ is a [simple polygon](/simple-polygon/) with $n$ vertices and rational coordinates, taken as a closed region. A point $x \in P$ *sees* $y \in P$ if the closed segment $xy$ lies in $P$. A set $G$ of points *guards* $P$ if every point of $P$ is seen by some point of $G$.

**Vertex guard problem.** Given $P$ and an integer $K$, is there a set of at most $K$ vertices of $P$ that guards $P$?

**Point guard problem.** Given $P$ and an integer $K$, is there a set of at most $K$ points of $P$ that guards $P$?

**Theorem (Lee and Lin 1986).** The vertex guard problem is NP-complete.

**Corollary (Aggarwal 1984; Lee and Lin 1986).** The point guard problem is NP-hard.

**Later result (Abrahamsen, Adamaszek and Miltzow 2018).** The point guard problem is complete for $\exists\mathbb{R}$, the class of problems that reduce in polynomial time to the truth of a sentence $\exists x_1 \dots \exists x_m\, \varphi$ over the real numbers. So it is in NP only if $\mathrm{NP} = \exists\mathbb{R}$.

## In plain words

Some puzzles are easy to check but seem hard to solve. Given a floor plan and a list of guard places, it is easy to check that the guards see every spot. This theorem shows that finding the smallest list is as hard as a famous hard puzzle: choose true or false for each of many switches so that every rule, of the form "switch a or switch b or switch c", holds. The proof builds a floor plan from the rules. Each switch becomes a pair of deep bays where a guard must stand at one of two corners, one for true and one for false. Each rule becomes a bay that is seen only if one of its switches is set right. Few guards are enough exactly when the rules can all hold.

## Proof

**Membership in NP.** A certificate is a list of at most $K$ vertices. The [visibility polygon](/visibility-polygon/) of each one takes $O(n)$ time, for example by [Lee's algorithm](/lee-visibility-polygon-algorithm/), and its vertices have rational coordinates of size polynomial in the input. The edges of the $K$ visibility polygons and of $P$ cut $P$ into $O((Kn)^2)$ cells, and a guard sees either all of a cell or none of its interior. So the guards see $P$ if and only if they see one interior point of each cell, each cell edge and each cell vertex. This is a polynomial number of exact tests.

**NP-hardness.** The proof reduces 3-SAT to the vertex guard problem. An instance has the variables $u_1, \dots, u_n$ and the clauses $c_1, \dots, c_m$, each an "or" of three literals, where a literal is $u$ or $\bar u$. Here $n$ is the number of variables, not the size of the polygon. The construction is the one of Lee and Lin in the form that O'Rourke gives in Section 9.3. Its pieces are thin bays and spikes, placed so that only a few vertices see certain points. We state the properties of the pieces that the proof uses. The coordinates that give them are in the paper and in O'Rourke's figures.

1. **Literal pattern.** Each of the $3m$ literals of the clauses has its own small bay with two vertices $t$ and $f$ and a distinguished point $p$ that no vertex other than $t$ and $f$ sees. A guard at $t$ means "this literal is true", and a guard at $f$ means "this literal is false".
2. **Clause junction.** The three literal patterns of a clause $c$ meet at a junction with a triangle that is seen, among all vertices, only by the three $t$ vertices of $c$.
3. **Variable pattern.** Each variable $u$ has two wells, with a vertex $F$ at the top of the left well and a vertex $T$ at the top of the right well, and a distinguished point $q$ that no vertex other than $T$ and $F$ sees. Each well has one thin spike for each literal of $u$ in the clauses. A spike in the left well lies on the line through $F$ and the vertex that a guard takes when the literal agrees with $u$ being true: $t$ for a literal $u$, $f$ for a literal $\bar u$. A spike in the right well lies on the line through $T$ and the vertex for $u$ being false: $f$ for $u$, $t$ for $\bar u$. The tip of a spike is seen only by the two vertices on its line.
4. **The extra guard.** One more vertex $x$ sees all the wells of all the variable patterns, and so all of the polygon that the vertices above do not cover. The construction makes every guard set use a guard outside the pairs $\{t, f\}$ and $\{T, F\}$.

The polygon has $O(n + m)$ pieces, so it has $O(n + m)$ vertices, and it can be built in polynomial time. Set $K = 3m + n + 1$.

**Lemma (O'Rourke, Lemma 9.7).** The clauses are satisfiable if and only if the polygon can be guarded by $K$ vertex guards.

*Proof.* Suppose that an assignment satisfies all clauses. For each literal of each clause, put a guard at $t$ if the literal is true and at $f$ if it is false: $3m$ guards, which see the distinguished points of the literal patterns. Each clause has a true literal, so each junction triangle is seen. For each variable, put a guard at $T$ if it is true and at $F$ if it is false: $n$ guards, which see the points $q$. Suppose $u$ is true. The guard at $T$ sees the spikes of the right well. Each spike of the left well lies on a line with $F$ and a vertex that carries a guard, because every literal of $u$ got the guard that agrees with $u$ being true. So the left well is seen as well. The case of $u$ false is symmetric. Add the guard at $x$. In total, $3m + n + 1 = K$ guards see the polygon.

Conversely, suppose that $K$ vertex guards see the polygon. The $3m + n$ distinguished points are seen by $3m + n$ pairs of vertices, $\{t, f\}$ or $\{T, F\}$, and the pairs are disjoint. So each pair holds at least one guard, and with the extra guard of property 4 this uses all $K$ guards. So each pair holds exactly one guard, and there is no other guard. Set $u$ true if its guard is at $T$ and false if it is at $F$. Suppose $u$ is true. Then $F$ has no guard, so each spike in the left well is seen only by its other vertex, which must hold the guard. So every literal of $u$ has its guard at the vertex that agrees with $u$ being true: at $t$ for a literal $u$, at $f$ for a literal $\bar u$. The case of $u$ false is symmetric. So a literal has its guard at $t$ if and only if the literal is true under the assignment. Each junction triangle is seen, so one of its three $t$ vertices holds a guard, and the clause has a true literal. So the assignment satisfies all clauses. $\square$

3-SAT is NP-complete, the construction takes polynomial time, and the vertex guard problem is in NP. This proves the theorem. $\square$

**Point guards.** For guards at any points, a guard near $p$ that is not at a vertex can also see $p$, so the proof above does not apply as it is. O'Rourke credits the extension to point guards to Aggarwal (1984), with a changed construction, and Lee and Lin also treat point guards in their 1986 paper. The $\exists\mathbb{R}$-completeness of 2018 gives NP-hardness again, by a different reduction, since every problem in NP reduces to the truth of an existential sentence over the reals.

**Example.** Take the formula $(u_1 \lor u_2 \lor u_3) \land (\bar u_1 \lor \bar u_2 \lor u_3)$, with $n = 3$ variables and $m = 2$ clauses, so $K = 3 \cdot 2 + 3 + 1 = 10$. The assignment $u_1 = u_2 = \text{false}$, $u_3 = \text{true}$ satisfies it. The guards are: in the first clause, $f$ for $u_1$, $f$ for $u_2$ and $t$ for $u_3$; in the second clause, $t$ for $\bar u_1$, $t$ for $\bar u_2$ and $t$ for $u_3$; the variable vertices $F_1$, $F_2$ and $T_3$; and $x$. That is $6 + 3 + 1 = 10$ guards. Each clause has a guard at a $t$ vertex, so both junction triangles are seen. For $u_1$, the guard at $F_1$ sees the left well. The right well of $u_1$ has one spike on the line $T_1 f$ for the literal $u_1$ and one on the line $T_1 t$ for the literal $\bar u_1$, and both of these vertices hold guards.

## Consequences

- **No fast exact algorithm is expected.** Unless $\mathrm{P} = \mathrm{NP}$, no polynomial-time algorithm finds the fewest vertex guards or point guards of a simple polygon. Exact methods for vertex guards solve a set cover problem over the cells of the visibility arrangement, which can take exponential time (see the [art gallery problem](/art-gallery-problem/)).
- **Polygons with holes.** The result for polygons with holes (O'Rourke and Supowit 1983) follows from this one, because a simple polygon is a polygon with no holes. The proofs differ: theirs uses one hole for each variable, and Lee and Lin needed a construction without holes (see [polygon with holes](/polygon-with-holes/)).
- **The worst case and the optimum differ.** The bounds $\lfloor n/3 \rfloor$ of [Chvátal's theorem](/chvatal-art-gallery-theorem/) and $\lfloor n/4 \rfloor$ of the [orthogonal art gallery theorem](/orthogonal-art-gallery-theorem/) are easy to reach in polynomial time, but they say nothing about how close they are to the optimum of one polygon.
- **Point guards are harder still.** By the result of 2018, an optimal set of point guards can need irrational coordinates, and the point guard problem is not in NP unless $\mathrm{NP} = \exists\mathbb{R}$.

## Tightness

The theorem is about the general case, and some special cases are easy:

- **One guard.** Deciding whether one point guard is enough is deciding whether $P$ is [star-shaped](/star-shaped-polygon/), and the kernel takes $O(n)$ time.
- **Grids and partitions.** O'Rourke gives two classes with polynomial algorithms: guards in "grids", unions of horizontal and vertical segments, by a graph matching algorithm (Section 9.4), and the fewest star-shaped pieces in a partition without Steiner points, by dynamic programming (Section 9.5).

The theorem gives NP-completeness only for vertex guards. For point guards, membership in NP is not known, and it fails unless $\mathrm{NP} = \exists\mathbb{R}$.

## History

Victor Klee asked in 1973 for the number of guards that a polygon with $n$ walls may need, and Chvátal settled the worst case in 1975. The question of the fewest guards for one polygon came later. O'Rourke and Supowit proved in 1983 that the fewest star-shaped pieces that cover a polygon with holes is NP-hard to find. Lee and Lin then gave the reduction for polygons without holes. O'Rourke dates their result to 1984, and it appeared in the IEEE Transactions on Information Theory in 1986. O'Rourke's 1987 book gives their proof for vertex guards as Theorem 9.2, and credits the step to point guards to Aggarwal (1984). Abrahamsen, Adamaszek and Miltzow proved $\exists\mathbb{R}$-completeness for point guards in 2018.

## References
