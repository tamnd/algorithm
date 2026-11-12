---
title: Bezier clipping keeps every intersection and stops
proves: [correctness]
status: full
---

We use the notation of the pseudocode. $P$ has degree $m$ and control points $P_0, \dots, P_m$, and $Q$ has degree $n$ and control points $Q_0, \dots, Q_n$. For an interval $[a, b]$ with $a < b$, $P'$ is the control polygon of $u \mapsto P(a + u(b - a))$ on $[0, 1]$; for $a = b$ all its points are $P(a)$. The arithmetic is exact. $B_i^m$ are the Bernstein polynomials of degree $m$; they are nonnegative on $[0, 1]$, $\sum_i B_i^m(u) = 1$ and $\sum_i \frac im B_i^m(u) = u$.

**Lemma 1 (the strip).** Let $\ell(x) = \alpha \cdot x + \beta$ be affine, and let $d_{\min}$ and $d_{\max}$ be the smallest and largest of $\ell(Q'_j)$. Then $d_{\min} \le \ell(Q(s)) \le d_{\max}$ for every $s \in [c, d]$.

*Proof.* Put $v = (s - c)/(d - c)$, or $v = 0$ if $c = d$. Then $Q(s) = \sum_j Q'_j B_j^n(v)$, and since $\ell$ is affine and the weights are nonnegative with sum 1, $\ell(Q(s)) = \sum_j \ell(Q'_j) B_j^n(v)$, a convex combination of the values $\ell(Q'_j)$. $\square$

**Lemma 2 (the distance graph).** Let $p_i = (i/m, \ell(P'_i))$. For every $u \in [0, 1]$ the point $(u, \ell(P'(u)))$ is in the convex hull $H$ of $p_0, \dots, p_m$.

*Proof.* As in Lemma 1, $\ell(P'(u)) = \sum_i \ell(P'_i) B_i^m(u)$, and $u = \sum_i \frac im B_i^m(u)$. So $(u, \ell(P'(u))) = \sum_i B_i^m(u)\, p_i$, a convex combination of the $p_i$. $\square$

**Lemma 3 (the exact range).** Let $K = H \cap \{y : d_{\min} \le y \le d_{\max}\}$. Let $C$ be the set of the first coordinates of the $p_i$ that lie in the band, together with the first coordinates of the points where a segment $p_i p_j$ crosses the line $y = d_{\min}$ or $y = d_{\max}$ strictly between its end points. If $K$ is empty then $C$ is empty, and otherwise $\min C$ and $\max C$ are the smallest and largest first coordinates of points of $K$.

*Proof.* Every point counted in $C$ is in $H$, as a $p_i$ or a point of a segment between two of them, and in the band, so it is in $K$. So $C$ is empty if $K$ is empty, and $\min C$ and $\max C$ lie in the range of $K$.

Conversely, let $K$ be nonempty. $K$ is the intersection of a convex polygon with a closed strip, so it is a compact convex polygon, a segment or a point, and the linear function $x$ reaches its minimum and maximum on $K$ at extreme points of $K$. An extreme point $z$ of $K$ is an extreme point of $H$, which is some $p_i$ in the band, or it lies on the boundary of the strip, so $z$ is on a line $y = d$ with $d \in \{d_{\min}, d_{\max}\}$. In the second case $z$ is an extreme point of the segment $H \cap \{y = d\}$, so it is an end point of that segment, which lies on an edge of $H$. That edge is a segment $p_i p_j$. If $z$ is $p_i$ or $p_j$, it is in $C$ as a point in the band. Otherwise $z$ is strictly inside $p_i p_j$, and $p_i$ and $p_j$ are on different sides of $y = d$, or the edge lies on the line $y = d$; in the last case $z$ is an end point of the edge, which was excluded. So $z$ is a crossing counted in $C$. Hence the extreme first coordinates of $K$ are in $C$. $\square$

**Theorem 1 (no intersection is lost).** At the start of each pass of line L2, every pair $(t^*, s^*) \in [0, 1]^2$ with $P(t^*) = Q(s^*)$ lies in a box on the stack $S$ or in a box of $R$.

*Proof.* At line L1 the only box is $[0, 1]^2$. Let a pass pop the box $[a, b] \times [c, d]$, and let $(t^*, s^*)$ be an intersection in it. If line L4 moves the box to $R$, the claim holds. Otherwise let $u^* = (t^* - a)/(b - a)$ if $b > a$, and $u^* = 0$ if $b = a$. In both cases $P'(u^*) = P(t^*)$. By Lemma 2, $(u^*, \ell(P'(u^*)))$ is in $H$. Since $P'(u^*) = P(t^*) = Q(s^*)$, Lemma 1 puts $\ell(P'(u^*))$ in the band. So the point is in $K$, $K$ is not empty, and by Lemma 3, $u_0 \le u^* \le u_1$. Hence line L5 does not discard the box, and $a + u_0 (b - a) \le t^* \le a + u_1 (b - a)$. Rounding the ends outward keeps $t^*$ inside, and cutting the result back to the old $[a, b]$ also keeps it, since $t^*$ was in $[a, b]$. Lines L7 and L8 repeat the argument with $P$ and $Q$ exchanged, now with the new $P'$, and keep $s^*$. Line L9 pushes two boxes whose union is the clipped box, and line L10 pushes the clipped box. So $(t^*, s^*)$ is in a box on $S$. $\square$

When $S$ is empty, every intersection is in a box of $R$. Line L11 merges boxes into their unions, which only adds points. So the output contains every intersection, and each merged box is a union of boxes of width at most $\varepsilon$ in each direction, by line L4.

**Theorem 2 (termination).** Every chain of boxes, from $[0, 1]^2$ to a box that is popped and not pushed again, has length at most $2 \lceil \log_{5/4}(1/\varepsilon) \rceil + 2$. Since each pass pushes at most two boxes, the loop stops.

*Proof.* Follow one box through the passes that push it or one of its children. Line L6 and line L8 cut the new interval back into the old one, and a split halves an interval, so the widths $w_P = b - a$ and $w_Q = d - c$ never grow along a chain.

Consider a pass that pushes something, with old widths $w_P, w_Q$. Not both are at most $\varepsilon$, since otherwise line L4 ends the chain. If line L10 runs, the progress rule holds: an interval with old width above $\varepsilon$ now has width at most $\frac45$ of it. If line L9 runs, the wider of the two new intervals is split, and its width is more than $\varepsilon$, because not both new widths are at most $\varepsilon$. Its old width was at least its new width, so it was also above $\varepsilon$, and the half is at most $\frac12 < \frac45$ of the old width. In both cases one of the two widths is above $\varepsilon$ before the pass and is multiplied by at most $\frac45$.

Let $N = \lceil \log_{5/4}(1/\varepsilon) \rceil$. A width starts at 1, never grows, and after $N$ factors of at most $\frac45$ it is at most $\varepsilon$. Once it is at most $\varepsilon$, it is never counted again, because a counted width is above $\varepsilon$ before the pass. So each of the two widths is counted at most $N$ times, and a chain has at most $2N$ pushing passes plus the first and the last pass. $\square$

The bound on each chain does not bound the number of chains: when the curves share an arc, every box along the arc survives, and their number grows like $1/\varepsilon$. The implementation stops with an error after a fixed number of passes in that case.

**The root form.** For a polynomial $f = \sum_i c_i B_i^n$ on $[0, 1]$, apply Lemma 2 with $\ell(P'_i)$ replaced by the coefficients of $f$ on $[a, b]$, and the band $\{0\}$. A root $t^*$ in $[a, b]$ gives the point $(u^*, 0)$ of the graph, which is in the hull and in the band, so it is kept. Each pass either shrinks the interval to at most $\frac45$ of its width or splits it, so each chain has at most $N + 1$ passes, and the same proof applies.
