---
title: Proof of the Hanani-Tutte theorem
proves: [statement]
status: full
---

We prove that a graph $G$ is planar if and only if it has a drawing in which every pair of independent edges crosses an even number of times. The proof follows Tutte (1970) and the survey of Schaefer (2013): a parity invariant shows that $K_5$ and $K_{3,3}$ have no such drawing, and [Kuratowski's theorem](/kuratowski-theorem/) does the rest. Graphs are finite; loops and parallel edges do not change planarity, and a loop is not independent of any edge at its vertex, so we may assume $G$ is simple.

**Drawings.** A drawing puts each vertex at a distinct point and each edge $uv$ as a curve from $u$ to $v$, such that: no curve passes through a vertex other than its ends; any two curves, and any curve with itself, meet in finitely many points away from the vertices, each a proper crossing; and no point lies on three curves. Two edges are independent if they have no common end. $\mathrm{cr}(e, f)$ is the number of crossings of $e$ with $f$, for $e \ne f$. For a drawing $D$ let

$$\sigma(D) = \sum_{\{e, f\} \text{ independent}} \mathrm{cr}(e, f).$$

## Step 1: deformations

**Lemma 1.** Let $D$ and $D'$ be drawings of the same graph. Then $D$ can be changed into $D'$ by a homeomorphism of the plane, which changes no crossing count, followed by finitely many of these moves, each between drawings:

(M1) a change of one crossing count $\mathrm{cr}(e, f)$ by an even number, or of no count;

(M2) an edge $e$ passes over a vertex $v$: $\mathrm{cr}(e, f)$ changes by exactly 1 for each edge $f \ne e$ at $v$, and no other count of a pair of distinct edges changes.

*Proof.* First, take a homeomorphism $h$ of the plane that moves each vertex point of $D$ to the point of the same vertex in $D'$. Such an $h$ exists for any two lists of distinct points, for example as a composition of finitely many homeomorphisms that each move one point along a path that avoids the others and fix everything outside a thin neighbourhood of the path. Applying $h$ to $D$ changes no crossing count, since it is a bijection of the plane.

Now the vertices of $hD$ and $D'$ are at the same points. Change the edges one at a time. For an edge $e = ab$, the curves $\gamma_0$ of $e$ in $hD$ and $\gamma_1$ of $e$ in $D'$ have the same ends, and $\gamma_t = (1 - t) \gamma_0 + t \gamma_1$, with both curves parametrized over $[0, 1]$, is a homotopy between them with the ends fixed. By the standard general position argument, this homotopy can be perturbed, with the ends fixed, so that the curves $\gamma_t$ together with the other edges form a drawing for all but finitely many values of $t$, and at each exceptional value exactly one of these events happens: $\gamma_t$ passes over a vertex $v$; $\gamma_t$ touches another curve, or itself, at one point; $\gamma_t$ passes through a crossing of two other curves, or of itself with another curve. Between two consecutive events the crossings move continuously and none appears or disappears, so all counts stay the same.

At a touching point, two crossings of the same pair of curves appear or disappear together, or a self-crossing appears or disappears; this is (M1). At a triple point the crossings of each pair keep their number; this is (M1) with no change. When $\gamma_t$ passes over a vertex $v$, the edges $f$ at $v$ start at $v$, so near $v$ each of them is cut once more, or once less, by the sweeping curve, and no other pair changes; this is (M2). (If $v$ is an end of $e$, the changed pairs are the pairs $\{e, f\}$ with $f$ at that end.) After all edges have been changed, the drawing is $D'$. $\square$

## Step 2: the parity invariant

**Lemma 2.** If $G$ is $K_5$ or $K_{3,3}$, then $\sigma(D) \bmod 2$ is the same for every drawing $D$ of $G$.

*Proof.* By Lemma 1 it suffices to check that each move changes $\sigma$ by an even number. A move (M1) changes one count by an even number, or none. In a move (M2), the edge $e = ab$ passes over $v$, and $\sigma$ changes by $\pm 1$ for each edge $f$ at $v$ that is independent of $e$, so by an even number if the number $k$ of such edges is even.

If $v \in \{a, b\}$, every edge at $v$ shares $v$ with $e$, so $k = 0$.

If $G = K_5$ and $v \notin \{a, b\}$, the edges at $v$ go to the four other vertices, and the ones independent of $ab$ are the two going to the vertices other than $a$ and $b$. So $k = 2$.

If $G = K_{3,3}$ with sides $X$ and $Y$, $a \in X$, $b \in Y$, and $v \notin \{a, b\}$: if $v \in X$, the edges at $v$ go to the three vertices of $Y$, and the ones independent of $ab$ avoid $b$, so $k = 2$; if $v \in Y$, in the same way they avoid $a$, and $k = 2$. $\square$

**Lemma 3.** For every drawing $D$ of $K_5$ and for every drawing $D$ of $K_{3,3}$, $\sigma(D)$ is odd.

*Proof.* By Lemma 2, it suffices to find one drawing of each with $\sigma$ odd.

$K_5$: put the vertices at the corners of a convex pentagon and draw the edges as straight segments. Two segments between corners of a convex polygon cross, at one point, exactly when their four ends are distinct and alternate around the polygon. So only independent pairs cross, each once, and the crossing pairs correspond to the sets of 4 corners: each set of 4 corners has exactly one alternating pair, its two diagonals. So $\sigma = \binom{5}{4} = 5$. Three segments through one point would cross pairwise, so they would be pairwise independent and need 6 distinct ends; so no point lies on three segments, and this is a drawing.

$K_{3,3}$: put the vertices at the corners $p_0, \ldots, p_5$ of a convex hexagon, in this order around it, with $X = \{p_0, p_2, p_4\}$ and $Y = \{p_1, p_3, p_5\}$. The edges are the 6 sides $p_i p_{i+1}$ (indices mod 6) and the 3 long diagonals $p_0 p_3$, $p_1 p_4$, $p_2 p_5$, as straight segments. Choose the hexagon not regular, so that the three diagonals do not pass through one point. By the rule above, two of these segments cross exactly when their ends alternate around the hexagon. A side has two consecutive corners as ends, so nothing alternates with it. Any two long diagonals have alternating ends, for example $p_0, p_1, p_3, p_4$ for the first two. So exactly the 3 pairs of long diagonals cross, each once, and they are independent. So $\sigma = 3$. $\square$

## Step 3: the theorem

**Theorem.** $G$ is planar if and only if $G$ has a drawing in which $\mathrm{cr}(e, f)$ is even for every pair of independent edges.

*Proof.* If $G$ is planar, a plane drawing has no crossings, so every count is 0, which is even.

Conversely, suppose $G$ has such a drawing $D$ but is not planar. By Kuratowski's theorem $G$ has a subgraph $S$ that is a subdivision of $K = K_5$ or $K = K_{3,3}$. Delete from $D$ all vertices and edges not in $S$. For each edge $hh'$ of $K$, join the curves of the edges of the path $P_{hh'}$ of $S$ into one curve from $h$ to $h'$. This gives a drawing $D_K$ of $K$: the inner vertices of the paths become inner points of these curves, and no other curve passes through them, because in $D$ no edge passes through a vertex other than its ends; crossings and the absence of triple points are inherited from $D$.

Take two independent edges $hh'$ and $jj'$ of $K$. The paths $P_{hh'}$ and $P_{jj'}$ have no common vertex: their ends are distinct branch vertices, and the inner vertices of different paths of a subdivision are distinct. So every edge of $P_{hh'}$ is independent in $G$ of every edge of $P_{jj'}$, and the number of crossings of the two curves in $D_K$ is

$$\sum_{e \in P_{hh'}} \sum_{f \in P_{jj'}} \mathrm{cr}_D(e, f),$$

a sum of even numbers. So $\sigma(D_K)$ is even, which contradicts Lemma 3. So $G$ is planar. $\blacksquare$

## Small cases

- A single vertex, and any graph with no two independent edges, such as a star or a triangle: the condition holds in every drawing, and these graphs are planar.
- A tree is planar, so it has a drawing with no crossings; a drawing of a path $abcd$ in which $ab$ crosses $cd$ once can be turned into one with an even count by passing $ab$ over $d$, the move (M2), which changes only the pair $\{ab, cd\}$.
- $K_4$ is planar. Passing $ab$ over $c$ toggles only $\{ab, cd\}$, so $K_4$ has drawings with $\sigma$ odd and with $\sigma$ even; Lemma 2 fails for $K_4$, as it must.
- $K_5$ and $K_{3,3}$: every drawing has $\sigma$ odd by Lemma 3, so some independent pair crosses an odd number of times, and in particular at least once.
