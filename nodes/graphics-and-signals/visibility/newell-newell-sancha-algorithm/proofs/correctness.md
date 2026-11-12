---
title: The Newell-Newell-Sancha algorithm stops and paints the visible polygon at each pixel
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. Each fragment $f$ has the plane $n_f \cdot X = d_f$ of its input polygon, with $n_{f,z} > 0$. For a point $v = (x, y, z)$, the side value is $\sigma_f(v) = n_f \cdot v - d_f = n_{f,z} (z - z_f(x, y))$. So $\sigma_f(v) > 0$ exactly when $v$ is nearer than the plane of $f$ above $(x, y)$. We write $\Pi(f)$ for the closed projection of $f$ onto the $xy$ plane, and $f \succ g$ when some $c \in \Pi(f) \cap \Pi(g)$ has $z_f(c) > z_g(c)$.

**Lemma 1 (the tests are exact).** The tests T0 to T6 are all false if and only if $P \succ Q$.

*Proof.* Each of T0 to T5 that is true excludes $P \succ Q$. T0: for $c$ in both projections, $z_P(c) \le \max_P \le \min_Q \le z_Q(c)$. T1, T2 and T5: the projections do not meet. T3: $\sigma_Q \le 0$ at the vertices of $P$, so on all of $P$, because $\sigma_Q$ is affine and $P$ is convex; hence $z_P(c) \le z_Q(c)$ on the common projection. T4 is the same with the roles of the planes changed. If T0 to T5 are false, the closed common region $\Pi(P) \cap \Pi(Q)$ is a nonempty convex polygon, a segment or a point, and the clip of T5 returns its vertices. The function $z_P - z_Q$ is affine, so its maximum on the region is at a vertex. Thus T6 is false exactly when $z_P > z_Q$ at some point of the region, that is, when $P \succ Q$. $\square$

**Lemma 2 (free sets have a valid order).** Let $S$ be a finite set of fragments in which no fragment has vertices strictly on both sides of the plane of another. Then $S$ has an order in which no fragment obscures a later one.

*Proof.* By induction on $|S|$; the empty set is clear. Pick $f_0 \in S$. Each other fragment $g$ has $\sigma_{f_0} \le 0$ at all its vertices or $\sigma_{f_0} \ge 0$ at all its vertices. Put $g$ in $C$ if $\sigma_{f_0} = 0$ at all its vertices (it is in the plane of $f_0$), else in $B$ if $\sigma_{f_0} \le 0$ at all its vertices, else in $F$. By induction, $B$ and $F$ have valid orders. Take the order of $B$, then $f_0$ and $C$ in any order, then the order of $F$. Let $c$ be a common point of the projections of $g$ before $h$. If $g \in B$ and $h \notin B$, then $z_g(c) \le z_{f_0}(c) \le z_h(c)$, by the sign of $\sigma_{f_0}$ on $g$ and on $h$; the case $g \notin F$, $h \in F$ is the same. If $g, h \in C \cup \{f_0\}$, they have the same plane, so $z_g(c) = z_h(c)$. Pairs inside $B$ or inside $F$ are handled by induction. So no fragment obscures a later one. $\square$

**Lemma 3 (marks).** At line L4, the marked fragments of $L$ are its first $t$ elements $m_0, \ldots, m_{t-1}$, for some $t \ge 0$, and $m_{i+1} \succ m_i$ for $0 \le i < t - 1$.

*Proof.* At the start no fragment is marked. Line L5 removes the first element, which keeps a prefix and its chain. Line L6 marks an unmarked $Q$, removes it from behind the prefix, and puts it at the front. The old front $P$ is now second, and $P \succ Q$ by Lemma 1. If $P$ was marked, the new pair $(Q, P)$ is the only new adjacent pair of marked fragments, and it has $P \succ Q$; if $P$ was not marked, $Q$ is the only marked fragment. Lines L7 to L10 split and then clear all marks. $\square$

**Lemma 4 (line L9 can split).** When line L9 runs, some $R \in L$ has vertices strictly on both sides of the plane of some $S \in L$.

*Proof.* Line L9 runs only when line L6 is false and lines L7 and L8 are false. If the swap test of line L6 fails, then $Q$ has a vertex with $\sigma_P > 0$. Because T4 is false, $Q$ also has a vertex with $\sigma_P < 0$, so line L7 is true. Hence line L9 runs only when $Q$ is marked. By Lemma 3, $Q = m_s$ for some $s \ge 1$ and $P = m_0$, and $m_s \succ m_{s-1} \succ \cdots \succ m_0 = P \succ Q = m_s$. So the fragments of $L$ have no valid order. By Lemma 2, $L$ is not free, which is the claim. $\square$

**Lemma 5 (fragments).** Each fragment of an input polygon $p$ is a union of closed faces of the arrangement, in the plane of $p$, of the lines where the planes of the other polygons meet it. The fragments of $p$ have disjoint interiors and positive area, and their union is $p$. So $p$ has at most $1 + (n-1) + \binom{n-1}{2}$ fragments, and $L$ never holds more than $M = n(1 + (n-1) + \binom{n-1}{2})$ fragments.

*Proof.* At the start the fragment of $p$ is $p$. A split cuts a fragment $f$ of $p$ by the plane of another fragment, which is the plane of an input polygon $q$. Since $f$ has vertices strictly on both sides, the planes of $p$ and $q$ are different, they meet in a line of the arrangement, and both pieces have positive area and union $f$. A union of closed faces cut by a line of the arrangement gives two unions of closed faces. A set of fragments with disjoint interiors and positive area, each a union of faces, has at most as many elements as the arrangement has faces, and an arrangement of $k$ lines has at most $1 + k + \binom{k}{2}$ faces. $\square$

**Termination.** Each iteration of line L2 does an output (L5), a move (L6) or a split (L7 to L9). A split adds one fragment, and by Lemma 5 at most $M - n$ splits occur. Between two splits, each move marks an unmarked fragment, and no mark is removed, so at most $M$ moves occur; and at most $M$ outputs occur in all. So the loop stops after at most $(M - n + 1) \cdot M + M$ iterations. Lemma 4 shows that line L9 always finds a fragment to split.

**Invariant.** After each iteration: no fragment of the output obscures a later fragment of the output or a fragment of $L$.

*Proof.* At the start the output is empty. Line L5 appends $P$ only when no fragment $Q$ of $L$ after $P$ has $P \succ Q$, by Lemma 1, and $P$ is then later than all earlier output fragments, which do not obscure it. Line L6 only reorders $L$. A split replaces a fragment $g$ by pieces $g', g''$ in the same plane with $\Pi(g') \subseteq \Pi(g)$, so $f \succ g'$ implies $f \succ g$. So no step breaks the invariant. $\square$

**Theorem.** NEWELL-NEWELL-SANCHA stops, and at each pixel the image holds a polygon of largest depth among those that cover the pixel, or the background if none covers it.

*Proof.* By termination the loop stops with $L$ empty, so by the invariant the output is a valid order of fragments. By Lemma 5, the fragments of a polygon $p$ have the union $p$, so a pixel center $c$ is covered by some fragment of $p$ exactly when it is covered by $p$, and the depth of each fragment of $p$ is $z_p$. Line L11 paints in order, so the image at $c$ holds the polygon of the last fragment $f$ that covers $c$. For each polygon $q$ that covers $c$, take a fragment $g$ of $q$ that covers $c$. If $g = f$ or $g$ is in the same polygon, $z_q(c) = z_f(c)$. Else $g$ is before $f$, so $g \not\succ f$, and $z_q(c) = z_g(c) \le z_f(c)$. $\blacksquare$
