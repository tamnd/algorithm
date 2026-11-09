---
title: The Shamos-Hoey sweep reports an intersecting pair exactly when one exists
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be a finite list of closed segments with rational end points, with no restriction: vertical segments, segments of length zero, shared end points, repeated segments and collinear overlaps are allowed. SHAMOS-HOEY$(S)$ returns a pair of segments of $S$ that have a common point when such a pair exists, and returns none otherwise.

**Notation.** Points are compared lexicographically: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. Line L1 names the end points of each segment $s$ so that $l(s) \le r(s)$. A segment is *degenerate* when $l(s) = r(s)$. The event points are the distinct end points, processed in increasing order by line L3, and $E(p)$ is the set of segments with an end point at $p$ (line L4). For a segment $t$ with $l(t) \ne r(t)$, $\mathrm{side}_p(t) = -\mathrm{orient}(l(t), r(t), p)$, as in the code. The status $T$ is a sequence; "before" refers to its order, from the bottom to the top.

**Fact 1.** If $x, y, z$ are on one line, then $z \in [x, y]$ if and only if $\min(x, y) \le z \le \max(x, y)$. (On a line, the lexicographic order is the order along the line.)

**Fact 2.** For a non-vertical segment $t$ and a point $p$ with $l(t)_x \le p_x \le r(t)_x$, let $y_t(p_x)$ be the $y$-coordinate of the point of $t$ above $p_x$. Then $\mathrm{orient}(l(t), r(t), p) = (r(t)_x - l(t)_x)(p_y - y_t(p_x))$, so $\mathrm{side}_p(t)$ is the sign of $y_t(p_x) - p_y$. For a vertical $t$, $\mathrm{side}_p(t) = 0$ for every $p$ with $p_x = l(t)_x$.

**Lemma 1 (contents of $T$).** At the start of the iteration for an event point $p$, $T$ holds exactly the non-degenerate segments $t$ with $l(t) < p \le r(t)$, each once.

*Proof.* Line L10 inserts a non-degenerate $s$ at the event $l(s)$, line L11 deletes it at the event $r(s)$, and line L9 skips degenerate segments. Since $l(s) < r(s)$ for a non-degenerate segment, the claim follows by induction over the events. $\square$

**Lemma 2 (soundness).** Every pair that the algorithm returns has a common point.

*Proof.* At line L5 both segments contain $p$. At line L8, the segment $t = T[k]$ has $\mathrm{side}_p(t) = 0$ and $t \ne s$. Since $|E(p)| = 1$, $p$ is not an end point of $t$, so by Lemma 1 $l(t) < p < r(t)$, and $p$ is on the line of $t$; by Fact 1, $p \in t$, and $p \in s$. At lines L10 and L11 the pair is checked with the exact pairwise test. $\square$

Lemma 2 holds whatever the order of $T$ is. Completeness needs the order. If some pair of segments meets, let $q$ be the lexicographically smallest point that lies on two segments of $S$. It exists because each pairwise intersection is empty, a point or a closed segment, and there are finitely many pairs. If no pair meets, set $q = +\infty$.

**Lemma 3 (order).** Let $p$ be an event point with $p \le q$, and suppose the algorithm reaches the start of the iteration for $p$. For $t \in T$ let $y_t = y_t(p_x)$ when $t$ is not vertical and $y_t = p_y$ when $t$ is vertical. Then $y_t$ does not decrease along $T$. Consequently $\mathrm{side}_p$, which is the sign of $y_t - p_y$ by Fact 2 and Lemma 1, does not decrease along $T$, and the two binary searches of line L7 return the bounds $i \le j$ of the block of segments with $\mathrm{side}_p = 0$.

*Proof.* By strong induction on the events. Take two segments $w, u \in T$ and let $p_0 < p$ be the event at which the later of them, say $u$, was inserted, so $p_0 = l(u)$ and $w$ was in $T$ at $p_0$. By the induction hypothesis at $p_0$ (note $p_0 < p \le q$), line L7 at $p_0$ found the correct block. The algorithm did not return at $p_0$, so line L8 found no segment with side zero, $\mathrm{side}_{p_0}(w) \ne 0$, and $u$ was inserted after exactly the segments with side $-1$. Inserts and deletes keep the relative order of the other elements, so $w$ is before $u$ in $T$ if and only if $\mathrm{side}_{p_0}(w) = -1$.

The segment $w$ is not vertical. Otherwise $w \in T$ at $p_0$ gives $l(w) < p_0 \le r(w)$ with all three points on one vertical line, so $p_0 \in w$; $p_0$ is not an end point of $w$ because $|E(p_0)| = 1$, so $\mathrm{side}_{p_0}(w) = 0$, which we excluded.

Suppose $w$ is before $u$, so $y_w(p_{0,x}) < p_{0,y}$. If $u$ is vertical, then $u \in T$ at $p$ gives $p_x = p_{0,x}$ and $p_y > p_{0,y}$, so $y_w(p_x) = y_w(p_{0,x}) < p_{0,y} < p_y = y_u$. If $u$ is not vertical, let $g(x) = y_u(x) - y_w(x)$ on $[p_{0,x}, p_x]$, where both segments are defined by Lemma 1. $g$ is affine and $g(p_{0,x}) > 0$. If $g(p_x) < 0$, then $p_{0,x} < p_x$ and $g$ has a zero $x^* < p_x$, which gives a common point of $u$ and $w$ that is smaller than $p \le q$, a contradiction. So $y_w \le y_u$ at $p$.

Suppose $w$ is after $u$, so $y_w(p_{0,x}) > p_{0,y}$. If $u$ is not vertical, the same argument with $g = y_w - y_u$ gives $y_w \ge y_u$ at $p$. If $u$ is vertical, then $p_x = p_{0,x}$, $u$ contains the vertical segment from $p_0$ to $p$, and $y_w(p_x) > p_{0,y}$. If $y_w(p_x) < p_y$, the point of $w$ above $p_x$ lies on $u$ and is smaller than $p \le q$, a contradiction. So $y_w \ge p_y = y_u$. In all cases, any two segments of $T$ are in the order of $y_t$, up to ties. $\square$

**Lemma 4 (completeness).** If $q < +\infty$, the algorithm returns at an event point $p \le q$.

*Proof.* Suppose it reaches $q$, or passes it, without returning. Each event up to that point is $\le q$, so Lemma 3 applies to it.

1. *$q$ is an end point of two or more segments.* Then $q$ is an event with $|E(q)| \ge 2$, and line L5 returns.

2. *$q$ is an end point of exactly one segment $s$.* Some $t \ne s$ contains $q$, and $q$ is not an end point of $t$, so $l(t) < q < r(t)$, $t \in T$ at the start of event $q$ by Lemma 1, and $\mathrm{side}_q(t) = 0$. By Lemma 3, $t$ is in the block $[i, j)$ of line L7, and line L8 returns.

3. *$q$ is not an end point.* Let $A$ be the set of segments that contain $q$; $|A| \ge 2$, and $q$ is in the relative interior of each. No two segments of $A$ overlap in a segment: the smallest point of such an overlap is an end point of one of them and lies on both, so it would be $< q$ or equal to the end point $q$. Let $p^*$ be the last event point before $q$ (the left end points of the segments of $A$ are before $q$). After $p^*$ is processed, $T$ holds the non-degenerate segments $t$ with $l(t) < q < r(t)$, which includes $A$.

   *If some $s \in A$ is vertical*, let $p_0 = l(s) \le p^*$ and take $t \in A$, $t \ne s$. It is not vertical (two vertical segments through $q$ would overlap), so $l(t)_x < q_x = p_{0,x} < r(t)_x$, $t \in T$ at $p_0$, and $\mathrm{side}_{p_0}(t) = +1$ since $y_t(p_{0,x}) = q_y > p_{0,y}$. Line L10 inserts $s$ just before the first segment $u$ with side $+1$, and $u$ is not after $t$ by Lemma 3. A vertical segment of $T$ at $p_0$ would contain $p_0$ and have side $0$, so $u$ is not vertical, and $p_{0,y} < y_u(p_{0,x}) \le y_t(p_{0,x}) = q_y$. So $u$ meets $s$ at a point $\le q$, and the test of line L10 finds the pair $s, u$ and returns at $p_0 < q$.

   *If no segment of $A$ is vertical*, then $T$ has no vertical segment after $p^*$: such a segment would contain $q$ and be in $A$. The argument of Lemma 3, with $q$ in place of $p$, shows that $y_t(q_x)$ does not decrease along $T$ after $p^*$. Let $s, t \in A$ be consecutive among the members of $A$ in $T$. A segment $w$ between them has $q_y = y_s(q_x) \le y_w(q_x) \le y_t(q_x) = q_y$, so $w \in A$, which is impossible. So $s$ and $t$ are adjacent in $T$ after $p^*$. Let $p_1 \le p^*$ be the event at which they became adjacent for the last time. At $p_1$ either one of them was inserted next to the other, and line L10 tests the new segment against both neighbors, or a segment between them was deleted, and line L11 tests the new adjacent pair. Either test finds the common point $q$, and the algorithm returns at $p_1 < q$. $\square$

**Proof of the claim.** If some pair meets, Lemma 4 shows the algorithm returns at an event $\le q$, and Lemma 3 holds at every event it processes, so the assertion of line L11 holds (at $p = r(s)$ the block of side zero contains $s$, and line L8 has excluded every other member). By Lemma 2, the returned pair meets. If no pair meets, Lemma 2 shows that the algorithm never returns a pair, Lemma 3 holds at every event, and the loop ends at line L12 with none.

**Termination.** The loop of line L3 runs once per distinct end point, at most $2n$ times, and each iteration does two binary searches, at most two list updates and at most two pairwise tests. $\blacksquare$
