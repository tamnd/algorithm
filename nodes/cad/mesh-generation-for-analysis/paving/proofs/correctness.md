---
title: A quad mesh has an even number of boundary edges, and an accepted paving row is a valid quad mesh of the band between two fronts
proves: [correctness, termination]
status: full
---

**What is proved and what is not.** Two results are proved: the parity rule, which every all-quad mesher must respect, and the correctness of one accepted row, the core step of paving as it is implemented here. Nothing is proved about the whole paving method. Blacker and Stephenson give no quality guarantee and no proof that the fronts always close; paving relies on smoothing, seaming, row adjustment and closure rules that are tuned by experiment. The step here can fail, and it says so.

**Theorem 1 (parity).** In a mesh of a planar region by $Q$ quads, in which every edge lies in one quad (a boundary edge) or two quads (an interior edge), the number $E_b$ of boundary edges is even.

*Proof.* Count pairs (quad, edge of that quad), the edge sides. Each quad has 4 edges, so there are $4Q$ pairs. Each interior edge is in two pairs and each boundary edge in one, so $4Q = 2E_i + E_b$. Then $E_b = 4Q - 2E_i$ is even. $\square$

So a paving front, which becomes the boundary of the quads inside it, must have an even number of edges. Paving makes the boundary discretisation even before it starts, and the step below keeps the parity.

**Setting.** The old front $F$ is a simple polygon $x_0, \dots, x_{n-1}$ in counterclockwise order around the empty region. A row end $c$ has no new node, and the point $q_c = x_{c-1} + x_{c+1} - x_c$ is the new node of both of its neighbours. Row ends are at least 3 apart along the front. Every other node $i$ has the new node $y_i$. The quads are $(x_i, x_{i+1}, y_{i+1}, y_i)$ for an edge whose ends are both row sides, and $(x_{c-1}, x_c, x_{c+1}, q_c)$ for a row end $c$, which covers its two edges. The new front $F'$ lists the new nodes in the order of the old nodes, with each $q_c$ once.

**Lemma 2 (boundary chain).** As 1-chains, $\sum_Q \partial Q = \partial F - \partial F'$.

*Proof.* Each old front edge is in exactly one quad, forward: the side quad on that edge, or the corner quad of the row end at one of its ends. No edge is in two quads, because row ends are at least 3 apart, so an edge has at most one row end at its ends. Each row side node $i$ has one radial edge between $x_i$ and its new node. The quad on the edge to the left of $x_i$ uses it as $x_i \to y_i$, and the quad on the edge to its right uses it as $y_i \to x_i$; this holds also when one of these quads is a corner quad, since its edges $x_{c+1} \to q_c$ and $q_c \to x_{c-1}$ are the radial edges of the two neighbours of the row end. So the radial edges cancel. The remaining edges are the top edges $y_{i+1} \to y_i$ of the side quads, which are the edges of $F'$ reversed; between two neighbours of a row end the top edge would join $q_c$ to itself and is absent from both sides. $\square$

**Theorem 3 (one row).** If every quad is strictly convex and counterclockwise and $F'$ is a simple polygon with positive signed area, then the quads have pairwise disjoint interiors, their union is the closure of the region between $F$ and $F'$, the region inside $F'$ lies inside $F$, and the sum of the quad areas equals the area inside $F$ minus the area inside $F'$. The new front has $n - 2e$ nodes, where $e$ is the number of row ends, so its length has the parity of $n$.

*Proof.* By Lemma 2, for every point $x$ not on an edge, the winding numbers satisfy $\sum_Q w(\partial Q, x) = w(F, x) - w(F', x)$. Both fronts are simple and counterclockwise, so $w(F, \cdot)$ and $w(F', \cdot)$ are 1 inside and 0 outside. Each strictly convex counterclockwise quad has winding number 1 inside and 0 outside. So the left side is a sum of terms in $\{0, 1\}$, and the right side is in $\{-1, 0, 1\}$, hence in $\{0, 1\}$. A point inside $F'$ therefore lies inside $F$. A point inside $F$ and outside $F'$ is in exactly one quad, and every other point is in none. Edges have measure zero, which gives the claims on the interiors and the union. The shoelace sums are additive like the chains, which gives the area identity. For the count, each row end removes itself and merges the two new nodes of its neighbours into one, so the new front has $n - e - e = n - 2e$ nodes. $\square$

The code checks every hypothesis of Theorem 3 exactly (L6 and L7), so an accepted row is always a valid conforming quad mesh of its band. The tests check the area identity in exact arithmetic, the boundary of the row, the parity count $4Q = 2E_i + E_b$, and, for 4000 random points, that no point lies in two quads. On the square $[0,4]^2$ with unit spacing, the row is exactly the outer ring of 12 unit squares of the structured grid.

**Termination.** One step does $O(n^2)$ work and stops. Repeating the step on the new front makes a sequence of fronts with strictly decreasing area, by Theorem 3, as long as the steps succeed; with a fixed node spacing the fronts also lose nodes at row ends. But a step can fail, as on the inner $2 \times 2$ square, whose row ends are only 2 apart, or on a thin strip, where the rows from the two sides cross. There, paving needs its other operations: seams, which join front nodes across a narrow gap, row adjustments, and closure rules for small fronts. Those operations are not proved to always succeed.

**What is not proved.** No bound on the angles or the aspect ratio of the quads is proved, for the step or for paving. The step's angle thresholds are parameters of this code, not values from the paper. When rows from different parts of the front meet, the quads near the meeting line can be poor, and paving smooths them; the result of that smoothing is measured, not proved.
