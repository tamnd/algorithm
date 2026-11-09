---
title: The greedy edge set is a triangulation, and it is the lexicographically shortest one
proves: [correctness, termination]
status: full
---

**Setting.** $S$ is a set of $n$ distinct points in the plane. A **candidate** is a segment $pq$ with $p, q \in S$ whose relative interior contains no point of $S$. Two candidates **cross** if they share no end point and their relative interiors meet. Since no point of $S$ lies inside a candidate, two candidates without a common end point meet only in a proper crossing, which is what the orientation test of line L5 detects. Line L2 sorts the candidates by squared length and breaks ties by the index pair, which gives a strict total order $\prec$.

**Claim.** The set $E$ returned by GREEDY-TRIANGULATION is a triangulation of $S$: its edges do not cross, and together with the points they cut the convex hull of $S$ into triangles (or, if all points are collinear, they form the path through the points). Moreover, if $T$ is any triangulation of $S$ and both edge lists are sorted by $\prec$, the list of $E$ is lexicographically no larger than the list of $T$.

**Lemma 1 (no crossings).** Line L6 adds a candidate only if it crosses no edge already in $E$, and edges are never removed. So no two edges of $E$ cross. $\square$

**Lemma 2 (maximality).** Every candidate $c \notin E$ crosses some edge of $E$ that precedes $c$ in $\prec$. *Proof.* Line L4 meets every candidate once. When it meets $c$ and rejects it, line L5 has found an edge of the current $E$ that crosses $c$. That edge was added earlier, so it precedes $c$, and it stays in $E$. $\square$

**Lemma 3 (maximal plane graphs are triangulations).** A set $F$ of pairwise non-crossing candidates to which no candidate can be added without a crossing is a triangulation of $S$. *Proof.* Each segment between two consecutive points of $S$ on the boundary of the convex hull is a candidate that no candidate crosses, so it lies in $F$. If all points are collinear, every other pair has a point of $S$ between them, so the candidates are exactly these segments and $F$ is the path. Otherwise the hull boundary lies in $F$, and every bounded face $f$ of the plane graph $(S, F)$ lies in the hull. The closure of $f$ is a polygonal region whose corners and inner points belong to $S$, and such a region can be triangulated with corners in $S$ (every polygon, with holes and with points inside, has a triangulation that uses all its points). If $f$ is not a triangle without further points of $S$ on its boundary or inside, any such triangulation has an edge $g$ that is not on the boundary of $f$, and the relative interior of $g$ lies in the interior of $f$. The piece of $g$ between two consecutive points of $S$ on it is a candidate. It crosses no edge of $F$, since it runs inside $f$, and it is not in $F$. This contradicts maximality. So every bounded face is an empty triangle, and $F$ is a triangulation. $\square$

The details of Lemma 3 are the standard proof that every maximal plane straight-line graph on $S$ triangulates the hull; see the [triangulation of a point set](/triangulation-of-point-set/) page, which also gives the counts $3n - h - 3$ edges and $2n - h - 2$ triangles.

**Correctness.** By Lemmas 1 and 2, $E$ is a non-crossing set of candidates to which no candidate can be added. By Lemma 3, it is a triangulation.

**Lexicographic minimality.** Let $e_1 \prec e_2 \prec \cdots$ be the edges of $E$ and $t_1 \prec t_2 \prec \cdots$ those of a triangulation $T$; both have the same number of edges. Suppose the lists differ, and let $k$ be the first index with $e_k \ne t_k$. If $t_k \prec e_k$, then $t_k \notin E$: it is not among $e_1, \ldots, e_{k-1}$ (these are $t_1, \ldots, t_{k-1}$), and every later edge of $E$ follows $e_k$. By Lemma 2, $t_k$ crosses an edge $e_i$ of $E$ with $e_i \prec t_k \prec e_k$, so $i < k$ and $e_i = t_i \in T$. Then two edges of $T$ cross, which is impossible. So $e_k \prec t_k$, and the list of $E$ is lexicographically smaller. In particular, the greedy triangulation is unique once the tie rule is fixed. $\square$

**Termination.** There are at most $n(n - 1)/2$ candidates, line L4 visits each once, and line L5 scans the current $E$, which has at most $3n$ edges. Line L1 tests each pair against each point. So the procedure stops after $O(n^3)$ steps. $\blacksquare$
