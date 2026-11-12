---
title: Watkins' scanline algorithm gives each pixel its nearest covering triangle
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page, with no vertex on a line $y = j + \tfrac12$. For a pixel $(i, j)$ let $\mathrm{ans}(i, j)$ be the covering triangle with the least pair (depth at the center, index), or the background. For a triangle $m$, let $z_m(x)$ be the depth of its plane on scanline $j$, an affine function of $x$.

**Lemma 1 (the active edge list).** At line L5 of iteration $j$, the AEL holds exactly the edges that cross the line $y = j + \tfrac12$, each with the exact $x$ of its crossing, sorted by $x$.

*Proof.* An edge from $(a_x, a_y)$ to $(b_x, b_y)$ with $a_y < b_y$ crosses the scanlines $j$ with $a_y < j + \tfrac12 < b_y$, that is $j$ from $\lceil a_y - \tfrac12 \rceil$ to $\lfloor b_y - \tfrac12 \rfloor$, since no endpoint is on a scanline. Line L1 puts it in the bucket of its first scanline with the $x$ there. By induction on $j$: line L3 adds the edges whose first scanline is $j$; an edge added earlier had its $x$ increased by $\delta = (b_x - a_x)/(b_y - a_y)$ once per scanline by line L10, which is the change of $x$ along the edge when $y$ grows by 1; and line L10 drops an edge after its last scanline. Insertion sort at line L4 sorts the list. $\square$

**Lemma 2 (the spans).** After the toggle at the crossing $e$ of line L5, the set $S$ is the set of triangles that contain the open interval from $e.x$ to the next crossing on the scanline.

*Proof.* A triangle that meets the scanline meets it in an interval, whose ends are the crossings of two of its edges, since the scanline is not through a vertex; its third edge does not cross the line. So each such triangle has exactly two crossings in the AEL by Lemma 1, and between them the points of the scanline are in the triangle. The toggles of line L5, from left to right, insert a triangle at its left crossing and remove it at its right one. When two crossings have equal $x$, the open interval between them is empty and its span has no pixel center, so the order of the toggles there does not matter. $\square$

The span from $a = e.x$ to the next crossing $b$ holds the centers $i + \tfrac12$ with $a \le i + \tfrac12 < b$, which are $i_0 = \lceil a - \tfrac12 \rceil$ to $i_1 = \lceil b - \tfrac12 \rceil - 1$ of line L6. A triangle covers a center on the scanline exactly when the center is in its half-open interval $[x_l, x_r)$, which is the top-left rule on this line. So the triangles that cover a center of the span are exactly the triangles of $S$, and $\mathrm{ans}(i, j)$ is the least of $S$ by the key $(z_m(i + \tfrac12), m)$ at each center of the span.

**Lemma 3 (both ends decide a piece).** Let $lo \le hi$ be centers of a span, and let $p$ be the least of $S$ by the key at both $lo$ and $hi$. Then $p$ is the least at every center between them.

*Proof.* Let $m \in S$, $m \ne p$, and $g(x) = z_p(x) - z_m(x)$, an affine function. Since $p$ wins at both ends, $g \le 0$ at both ends, and $g < 0$ at an end where $m < p$. If $m > p$, then $g \le 0$ at both ends gives $g \le 0$ on the whole interval, by convexity, and $p$ wins at each center by depth or by index. If $m < p$, then $g < 0$ at both ends gives $g < 0$ on the interval, and $p$ wins by depth. $\square$

**Lemma 4 (the cut).** Let $p$ win at $lo$ and $q \ne p$ win at $hi$. Then $z_p - z_q$ is not constant, the cut of line L9 satisfies $lo < cut \le hi$, and the pieces $[lo, cut - 1]$ and $[cut, hi]$ are nonempty.

*Proof.* Let $g = z_p - z_q$. At the center of $lo$, $p$ beats $q$, so $g \le 0$; at $hi$, $q$ beats $p$, so $g \ge 0$. If $g$ were constant, it would be 0, and the same triangle (the one with the smaller index) would win against the other at both ends, which is false. So $g$ has one root $x^*$, with $lo + \tfrac12 \le x^* \le hi + \tfrac12$, and $g$ grows through it. The cut is the first center $\ge x^*$, moved one to the right when a center is at $x^*$ and $p < q$. If $x^* = lo + \tfrac12$, then $g = 0$ at $lo$, and $p$ won there, so $p < q$ and the cut is $lo + 1$. In every other case the first center $\ge x^*$ is greater than $lo$. In the same way, if $x^* = hi + \tfrac12$, then $q$ won there with $g = 0$, so $q < p$ and the cut is $hi$; otherwise the cut is at most $hi$. $\square$

**Lemma 5 (the stack loop).** For each span with centers $i_0 \le i_1$, the loop of lines L7 to L9 ends, and it gives every center in $[i_0, i_1]$ its least triangle of $S$.

*Proof.* Each popped piece is either filled (line L8) or replaced by two nonempty pieces that split it (Lemma 4). So the pieces popped form a binary tree whose leaves split $[i_0, i_1]$; each internal node has two children that are strictly smaller, so the tree has at most $2(i_1 - i_0 + 1) - 1$ nodes and the loop ends. Each leaf is filled with the triangle that wins at both of its ends, which by Lemma 3 is the winner at every center of the leaf. $\square$

**Theorem.** WATKINS gives $\mathrm{ans}(i, j)$ at each pixel.

*Proof.* Every pixel center of row $j$ lies in exactly one span of the scanline, if any triangle covers it: the crossings split the scanline into half-open intervals, and a center covered by no triangle is in no span with nonempty $S$ and keeps the background, which is its answer. By Lemmas 1 and 2 the spans and their sets $S$ are correct, and by Lemma 5 each span gets the right winner at each of its centers. The loop of line L2 visits every row from the first scanline with an edge, and the rows above it are covered by no triangle. $\blacksquare$
