---
title: The Weiler-Atherton walk traces the boundary of the result
proves: [correctness]
status: full
---

**Setup.** $S$ and $C$ are simple polygons, both in counterclockwise order (the code reverses a clockwise input). General position: no vertex of one polygon lies on the boundary of the other. Then two edges, one from each polygon, meet in at most one point, which is interior to both edges, and there they cross: if they touched without crossing, or overlapped, a vertex would lie on the other boundary. Call these points the crossings; there are $k$ of them. Let $R$ be $S \cap C$, $S \cup C$ or $S \setminus C$, with $\partial S$ and $\partial C$ the boundaries. For a point $q$ off $\partial S \cup \partial C$, $\chi(q) = 1$ if $q$ is in the interior of $R$ and $\chi(q) = 0$ otherwise.

**Claim.** WEILER-ATHERTON$(S, C, \mathrm{op})$ returns closed polygons $Q_1, \ldots, Q_r$ with $\sum_j \operatorname{wind}(Q_j, q) = \chi(q)$ for every $q$ off $\partial S \cup \partial C$. So the sum of their signed areas is the area of $R$, the counterclockwise ones are outer boundaries and the clockwise ones are holes.

Two facts about a simple counterclockwise polygon $P$ are used. (F1) Near a point in the interior of an edge, the points just to the left of the edge are inside $P$ and the points just to the right are outside. (F2) When a point moves across an edge of a closed polygon $Q$ at a point interior to that edge and off all other edges, from the right side to the left side, $\operatorname{wind}(Q, \cdot)$ increases by 1, and the winding number is constant on every connected set that misses $Q$. Both follow from the ray count of the [winding number algorithm](/winding-number-algorithm/) (Lemma 2 of its correctness proof): take a ray from the moving point that crosses only that edge near it; the count changes by exactly that crossing. (F1) is (F2) applied to $P$, whose winding number is 1 inside and 0 outside, since it is 0 far away.

## Step 1: arcs

The crossings cut $\partial S$ into arcs, each running from one crossing to the next in the counterclockwise order of $S$; if $k = 0$ there are no crossings and no arcs. An open arc of $\partial S$ does not meet $\partial C$, and it is connected, so it lies entirely inside $C$ or entirely outside $C$. The same holds for the arcs of $\partial C$ with respect to $S$.

**Lemma 1 (line L2).** At a crossing of the subject edge $ab$ with the clip edge $cd$, the arc of $\partial S$ that starts at the crossing lies inside $C$ exactly when $(b - a) \times (d - c) < 0$.

*Proof.* The cross product is negative exactly when $b - a$ points to the left of the directed line $cd$. By (F1) for $C$, the points of $ab$ just after the crossing are then inside $C$, and the arc that starts there is inside $C$ along its whole length. $\square$

Call the crossing *entering* when this holds and *exiting* otherwise. Along $\partial S$ the arcs alternate between inside and outside $C$, because at each crossing the edge of $S$ passes from one side of $cd$ to the other.

## Step 2: the selected arcs

Call an arc *selected* if $\chi$ takes different values on its two sides. Give each selected arc the direction that has the interior of $R$ on its left. Near a point of an arc of $\partial S$, crossing the arc changes membership in $S$ and keeps membership in $C$; this gives the table below, which uses (F1) for $S$ and for $C$, and for $\partial C$ traversed clockwise, where the left side is the outside of $C$.

| op | selected arcs of $\partial S$, direction | selected arcs of $\partial C$, direction |
|---|---|---|
| intersection | inside $C$, forward | inside $S$, forward |
| union | outside $C$, forward | outside $S$, forward |
| difference | outside $C$, forward | inside $S$, backward |

For example, for the difference, an arc of $\partial C$ inside $S$ has points of $S \setminus C$ on its outer side and points of $C$ on its inner side, so it is selected, and $R$ is on its left when $C$ is walked clockwise. An arc of $\partial C$ outside $S$ has points outside $S$ on both sides, so $\chi = 0$ on both sides and it is not selected.

**Lemma 2.** At every crossing exactly one selected arc arrives and exactly one leaves, and they belong to different polygons.

*Proof.* Near a crossing $x$ the two edges cut a small disk into four sectors, one for each combination of inside or outside $S$ and inside or outside $C$. For the intersection and the difference, $R$ covers exactly one sector; for the union it covers three. In both cases the boundary between $R$ and the rest, near $x$, is two of the four half-edges at $x$, one from each polygon, those that bound the single sector of $R$ or of its complement. With $R$ on the left, one of the two points toward $x$ and the other away from $x$. $\square$

**Lemma 3.** The selected arc of $\partial S$ that leaves a crossing $x$ exists exactly when $x$ is entering for the intersection, and exactly when $x$ is exiting for the union and the difference.

*Proof.* The arc of $\partial S$ that starts at $x$, walked forward, is selected when it lies inside $C$ for the intersection and outside $C$ for the other two (table). Lemma 1 says when that is. $\square$

## Step 3: the walk

By Lemma 2, the directed selected arcs form disjoint closed cycles through the crossings, every crossing on exactly one cycle, and each cycle alternates between arcs of $\partial S$ and arcs of $\partial C$. The walk of lines L5 to L9 starts at a crossing $x_0$ that, by Lemma 3, starts a selected arc of $\partial S$. Line L7 follows the list of $S$ forward through the vertices until the next crossing, which is the end of that arc. Line L9 switches to the other polygon, and the next leg follows $C$ forward, or backward for the difference, which is the direction of the selected arc of $\partial C$ that leaves this crossing by Lemma 2 and the table. Then it switches back, and so on. The walk reproduces the cycle through $x_0$ and stops when it reaches $x_0$ again (line L8). Every cycle contains an arc of $\partial S$, so it contains a crossing of the start type, and the loop of line L5 reaches it unless the cycle is already marked. So the output is exactly the set of cycles, each once.

**Winding numbers.** Let $\Gamma$ be the union of the output cycles and $W(q) = \sum_j \operatorname{wind}(Q_j, q)$. Take $q$ off $\partial S \cup \partial C$ and a path from $q$ to a point far away that meets $\partial S \cup \partial C$ only in finitely many points, each interior to an edge and away from the crossings. Both $W$ and $\chi$ are 0 at the far end. They are constant along the path between those points. At a point of a selected arc both change by the same amount: $+1$ when the path crosses from right to left, by (F2) for $W$ and by the choice of direction for $\chi$, and $-1$ the other way. At a point of an arc that is not selected, $\chi$ does not change by definition, and $W$ does not change because no output edge passes there. So $W(q) = \chi(q)$. $\square$

## Step 4: no crossings

If $k = 0$, then $\partial S$ and $\partial C$ are disjoint, and since each is connected, $\partial S$ lies inside $C$ or outside $C$, and $\partial C$ inside $S$ or outside $S$. Three cases are possible: $S$ inside $C$, $C$ inside $S$, or the two interiors disjoint (both inside each other is impossible, as the areas would be equal and the boundaries would meet). Line L3 tells them apart with one vertex of each polygon, which is off the other boundary by general position, and returns $S$, $C$, both, none, or $S$ with $C$ reversed as a hole. In each case the winding numbers of the returned polygons add up to $\chi$ by (F1). $\blacksquare$

**Termination.** Each walk moves through a finite cyclic list, and it stops at its start crossing, because it follows one cycle of the finite set of selected arcs. Each crossing is marked once, so the loop of line L5 starts at most $k$ walks.
