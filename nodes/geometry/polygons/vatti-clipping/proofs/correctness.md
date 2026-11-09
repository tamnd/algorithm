---
title: The scanbeam sweep emits the result as trapezoids and closes their boundary into contours
proves: [correctness]
status: full
---

**Setup.** The subject $S$ and the clip $C$ are finite lists of closed contours, with $n$ vertices in all. Self-intersections, holes, shared edges, horizontal edges and repeated vertices are allowed. For a point $q$ off every edge, $w_S(q)$ and $w_C(q)$ are the total winding numbers of the contours of $S$ and of $C$. The fill rule turns a winding number into membership: $\mathrm{fill}(w)$ is $w \ne 0$ (nonzero) or $w$ odd (even-odd). Let $\chi(q) = 1$ if $\mathrm{op}(\mathrm{fill}(w_S(q)), \mathrm{fill}(w_C(q)))$ holds and $\chi(q) = 0$ otherwise, where op is one of $\wedge$, $\vee$, $a \wedge \neg b$, $\oplus$. Write $E$ for the union of all input edges.

**Claim.** VATTI$(S, C, \mathrm{op}, \mathrm{rule})$ returns closed contours $Q_1, \ldots, Q_r$, contained in $E$, with $\sum_j \operatorname{wind}(Q_j, q) = \chi(q)$ for every $q \notin E$. So their total signed area is the area of the result.

We use the ray count of the [winding number algorithm](/winding-number-algorithm/) (Lemma 2 of its correctness proof): for a closed polygon $Q$, a point $q$ off $Q$, and a ray from $q$ through no vertex of $Q$, $\operatorname{wind}(Q, q)$ is the number of edges that cross the ray counterclockwise around $q$ minus the number that cross it clockwise. It is written for one ray direction, and holds for every direction by rotation.

## Step 1: beams and sub-beams

The heights of line L1 are the $y$-coordinates of all vertices, $y_0 < y_1 < \cdots$. In the open strip $y_i < y < y_{i+1}$ there is no vertex, so every edge that meets the strip crosses it from bottom to top. These are exactly the non-horizontal edges with $y_{\min} \le y_i$ and $y_{\max} \ge y_{i+1}$, the list of line L3. For two such edges $a$ and $b$, the difference $f(y) = x_a(y) - x_b(y)$ is linear in $y$.

**Lemma 1 (line L4).** The swaps of the insertion sort are exactly the pairs of active edges that cross at a height strictly between $y_i$ and $y_{i+1}$, and each recorded height is that crossing height.

*Proof.* Two edges cross strictly inside the beam exactly when $f(y_i)$ and $f(y_{i+1})$ are nonzero with opposite signs: a linear function that is zero somewhere inside and not zero everywhere changes sign there. After the sort of line L3 by $(x(y_i), x(y_{i+1}))$, a pair $a$ before $b$ has $x_a(y_{i+1}) > x_b(y_{i+1})$ only if $x_a(y_i) < x_b(y_i)$, since equal bottom values are ordered by top value; so such a pair crosses. Conversely, a crossing pair is ordered by its bottom values and reversed at the top. Insertion sort with a strict comparison swaps each pair that is out of order exactly once and no other pair. The crossing height is $y_i + f(y_i)(y_{i+1} - y_i)/(f(y_i) - f(y_{i+1}))$, the zero of $f$. $\square$

So in an open sub-beam $(y_a, y_b)$ between consecutive cut heights (line L5), no two active edges cross, and for any two of them $f$ is either identically zero or of one sign on the whole open interval. The left-to-right order at mid-height (line L6) is the order at every height in $(y_a, y_b)$, and edges with the same $x$ at mid-height coincide on the whole sub-beam.

## Step 2: winding numbers along a sub-beam

**Lemma 2.** Let $q = (x, y)$ with $y_a < y < y_b$, off every edge. Then $w_S(q)$ is the sum of the weights $w_e$ of the active subject edges with $x_e(y) < x$, where $w_e = +1$ for an edge directed downward and $-1$ for one directed upward. The same holds for $C$.

*Proof.* Take the ray from $q$ to the left. The height $y$ is not a vertex height, so the ray passes through no vertex, and it crosses exactly the active edges with $x_e(y) < x$, each once. Seen from $q$, a point that moves downward on the left side of $q$ turns counterclockwise around $q$, so a downward edge counts $+1$ and an upward edge $-1$. Apply the ray count to each contour of $S$ and add. $\square$

Line L6 walks the groups of coincident edges from left to right and adds their weights, so between two consecutive groups the running values $w_S$, $w_C$ are the winding numbers of Lemma 2, the same for every point of the open region between the two groups. Line L7 opens a span when $\chi$ turns from 0 to 1 at a group and closes it when $\chi$ turns from 1 to 0. So the set $\{q : \chi(q) = 1\}$ inside the open sub-beam, off the edges, is the union of the open trapezoids $T$ bounded by the left edge $l$ and the right edge $r$ of each span, between the heights $y_a$ and $y_b$. A trapezoid may be a triangle when $l$ and $r$ meet at $y_a$ or $y_b$. Different trapezoids are disjoint, and so

$$\chi(q) = \sum_T \mathbf{1}_T(q) \qquad \text{for all } q \notin E \text{ not at a cut height.} \tag{1}$$

## Step 3: the emitted segments form closed contours

For a trapezoid $T$ with span $(l, r)$ over $[y_a, y_b]$, its counterclockwise boundary $\partial T$ consists of the right side $r(y_a) \to r(y_b)$ upward, the top $r(y_b) \to l(y_b)$ westward, the left side $l(y_b) \to l(y_a)$ downward, and the bottom $l(y_a) \to r(y_a)$ eastward. Line L8 emits the two sides of every $T$.

Treat a set of directed segments as a formal sum, a 1-chain, where a segment and its reverse cancel and a segment equals the sum of its pieces. At one height $y$, the bottoms of the trapezoids just above $y$ add up to the eastward chain over the set $A_y$ covered by their intervals, and the tops of those just below add up to the westward chain over the set $B_y$. Their sum is eastward over $A_y \setminus B_y$ and westward over $B_y \setminus A_y$. Line L9 emits exactly these pieces, cut at every interval endpoint, testing coverage at the middle of each piece. So the chain $\Gamma$ of all emitted segments equals $\sum_T \partial T$.

The boundary of a chain, the sum of (end point minus start point) over its segments, is linear and does not change when a segment is cut into pieces. Each $\partial T$ is closed and has boundary 0, so $\Gamma$ has boundary 0. The boundary of the list of emitted segments is $\sum (\text{end} - \text{start})$ over the list, which is the boundary of $\Gamma$, so it is 0: at every point, as many emitted segments start as end. No emitted segment has length zero, since sides span $y_a < y_b$ and horizontal pieces lie between distinct breakpoints.

**Lemma 3 (line L10).** The linking loop uses every segment once and returns closed contours.

*Proof.* A walk from a start point $p_0$ enters every other point $p$ along an unused segment; since $p$ has as many outgoing as incoming segments and fewer outgoing ones have been used, one is left. So the walk can only stop at $p_0$. Every segment leaves some point, and the loop over start points empties every outgoing list. Removing a vertex where the contour goes straight on does not change the contour as a point set or its winding numbers. A contour with fewer than three vertices left goes from $a$ to $b$ and back, and its winding number is 0 off it, so dropping it changes nothing. $\square$

## Step 4: winding numbers of the output

Take $q \notin E$ not at a cut height, and the ray from $q$ to the left. It is horizontal at a height that is not a cut height, so it meets no horizontal piece and no vertex of the output, and it crosses exactly the side segments that lie to the left of $q$ at its height. These are the sides of the trapezoids, so by the ray count, the total winding number of the output at $q$ is the sum over $T$ of the count for $\partial T$, which is $\mathbf{1}_T(q)$ because $\partial T$ is a convex counterclockwise polygon. By (1) this is $\chi(q)$.

The side segments lie on input edges. A horizontal piece of line L9 has the same coverage above and below at every point of it that is off $E$: there $w_S$ and $w_C$ are continuous, so $\chi$ is the same just above and just below, and a point of an interval of $A_y$ off $E$ is strictly inside the matching interval of $B_y$. So each horizontal piece lies in $E$, and so does the whole output. For $q \notin E$ at a cut height, the output winding number and $\chi$ are both constant on a small disk around $q$ that misses $E$, and the disk contains points off the cut heights, where they agree. $\blacksquare$

**Termination.** There are fewer than $n$ beams, each with a finite list of active edges and finitely many swaps, and the linking loop removes one segment per step.
