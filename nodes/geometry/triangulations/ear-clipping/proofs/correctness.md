---
title: Ear clipping outputs a triangulation of the polygon
proves: [correctness, termination]
status: full
---

**Claim.** Let $P$ be a simple polygon with $n \ge 3$ distinct vertices (consecutive collinear vertices allowed). EAR-CLIPPING$(P)$ stops and outputs $n - 2$ counterclockwise triangles with corners among the vertices of $P$, with pairwise disjoint interiors, whose union is $P$.

**Setup.** After line L1 the vertex order is counterclockwise, so the interior of $P$ lies to the left of each directed edge. For a simple polygon $Q$, a *diagonal* is a segment between two vertices whose relative interior lies in the interior of $Q$. A vertex $v$ of $Q$ with neighbors $u = \mathrm{prev}(v)$ and $w = \mathrm{next}(v)$ is an *ear* if $Q$ has at least 4 vertices and $uw$ is a diagonal. Write $\Delta(v)$ for the closed triangle $uvw$.

**Lemma 1 (the ear test).** Let $Q$ be a simple counterclockwise polygon with $m \ge 4$ vertices and let $v$ be a vertex with neighbors $u, w$. Then $v$ is an ear if and only if $\mathrm{orient}(u, v, w) > 0$ and no vertex of $Q$ other than $u, v, w$ lies in $\Delta(v)$.

*Proof.* ($\Leftarrow$) Assume both conditions. Let $T$ be the open triangle $uvw$ together with the open segment $uw$.

1. No edge of $Q$ meets $T$. An edge $e$ that meets $T$ is not $uv$ or $vw$, since those lie on the boundary of $\Delta(v)$ away from the open segment $uw$. By simplicity, $e$ does not cross $uv$ or $vw$ and does not pass through $v$. Neither endpoint of $e$ lies in $\Delta(v)$ unless it is $u$ or $w$. So $e \cap \Delta(v)$ is a segment whose end points lie on the closed segment $uw$ (an edge cannot leave $\Delta(v)$ through $uv$ or $vw$), hence $e \cap \Delta(v) \subseteq uw$. If $e$ met the open segment $uw$ at an interior point of $e$ and $e$ is not on the line $uw$, $e$ would cross into the open triangle on one side, which we excluded. If $e$ lies on the line $uw$ and meets the open segment, then $e$ is a segment on that line with no endpoint strictly between $u$ and $w$, so it contains $u$ or $w$ in its relative interior, or it is the segment $uw$ itself. The first case puts a vertex inside an edge, against simplicity. In the second case $u$ and $w$ are adjacent, so $Q$ has the 3 vertices $u, v, w$, against $m \ge 4$.
2. The open triangle lies in the interior of $Q$. Since $\mathrm{orient}(u, v, w) > 0$ and the interior lies left of $uv$ and of $vw$, points of the open triangle near $v$ are interior points of $Q$. The open triangle is connected and, by step 1, does not meet the boundary of $Q$, so all of it lies in the interior.
3. The open segment $uw$ lies in the interior. By step 1 it does not meet the boundary, and each of its points is a limit of points of the open triangle, so it lies in the closure of the interior and not on the boundary, so in the interior.

So $uw$ is a diagonal and $v$ is an ear.

($\Rightarrow$) Let $uw$ be a diagonal. It splits $Q$ into two simple polygons; the one bounded by $u \to v \to w \to u$ is the triangle $uvw$, which lies in $Q$. Its boundary runs in the counterclockwise direction of $Q$ along $uv$ and $vw$, so $\mathrm{orient}(u, v, w) > 0$. Let $z$ be a vertex of $Q$ in $\Delta(v)$, $z \notin \{u, v, w\}$. The open triangle is interior to $Q$, so $z$ is not in it; the open segment $uw$ is interior to $Q$, so $z$ is not on it. So $z$ lies on $uv$ or $vw$, which by simplicity hold no vertex but their end points. This contradicts the choice of $z$. $\square$

**Lemma 2 (cutting an ear).** Let $v$ be an ear of a simple counterclockwise polygon $Q$ with $m \ge 4$ vertices, and let $Q'$ be $Q$ without $v$. Then $Q'$ is a simple counterclockwise polygon, and $Q$ is the union of $Q'$ and $\Delta(v)$ with disjoint interiors. If $m \ge 5$, then every vertex $x$ of $Q'$ with $x \ne u, w$ is an ear of $Q'$ exactly when it is an ear of $Q$.

*Proof.* The diagonal $uw$ splits $Q$ into $\Delta(v)$ and $Q'$, simple polygons with disjoint interiors and with the orientation of $Q$. This gives the first two statements.

For the third, let $s$ be a segment between two vertices of $Q'$ with $s \ne uw$. We show that $s$ is a diagonal of $Q$ exactly when it is a diagonal of $Q'$.

1. If the relative interior of $s$ lies in the interior of $Q'$, it lies in the interior of $Q$, because $Q' \subseteq Q$.
2. Let the relative interior of $s$ lie in the interior of $Q$. It does not meet $uv$ or $vw$, which are on the boundary of $Q$. The end points of $s$ lie in $\Delta(v)$ only if they are $u$ or $w$, by Lemma 1. So $s \cap \Delta(v)$ is a segment (possibly empty or one point) whose ends lie on the closed segment $uw$, and by convexity $s \cap \Delta(v) \subseteq uw$. If $s$ met the open segment $uw$ while crossing the line $uw$, it would enter the open triangle, which we just excluded. If $s$ lies on the line $uw$ and meets the open segment, its ends are not strictly between $u$ and $w$ (no vertex is there), so $s \supseteq uw$; $s \ne uw$ then puts $u$ or $w$ in the relative interior of $s$, which is impossible because $u$ and $w$ are boundary points. So the relative interior of $s$ misses the closed set $\Delta(v)$. A point of the interior of $Q$ outside $\Delta(v)$ has a small disk inside $Q$ and away from $\Delta(v)$, so inside $Q'$. Hence the relative interior of $s$ lies in the interior of $Q'$.

Now let $x \ne u, w$ be a vertex of $Q'$. Its neighbors $x^-$ and $x^+$ are the same in $Q$ and $Q'$. If $x^- x^+ = uw$, then $x$ is adjacent to both $u$ and $w$ in $Q'$, so $Q'$ is the triangle $u w x$ and $m = 4$, which the hypothesis $m \ge 5$ excludes. So $x^- x^+ \ne uw$, and by the claim, $x$ is an ear of $Q$ exactly when it is an ear of $Q'$. $\square$

**Lemma 3 (two ears).** A simple polygon with at least 4 vertices has an ear. This is the [two ears theorem](/two-ears-theorem/).

**The invariant.** Before each test of line L5, with $Q$ the polygon of the remaining vertices in list order:

> **(E)** $Q$ is a simple counterclockwise polygon. The triangles already output and $Q$ have pairwise disjoint interiors, and their union is $P$. For each remaining vertex $x$, $\mathrm{ear}[x]$ equals IS-EAR$(x)$ in $Q$, and if $\mathrm{ear}[x]$ is true then $x$ is in $W$.

*Initialization.* No triangle is output and $Q = P$. Lines L3 and L4 set every flag and put every vertex with a true flag in $W$.

*Maintenance.* Assume (E) and that $Q$ has $m \ge 4$ vertices. By Lemma 1, IS-EAR$(x)$ is true exactly when $x$ is an ear of $Q$. By Lemma 3, some ear $x$ exists; its flag is true, so $x$ is in $W$, and line L6 does not run out of entries. Line L6 skips entries that are removed or flagged false and stops at a remaining vertex $v$ with a true flag, which is an ear. Lines L7 and L8 output $\Delta(v)$ and replace $Q$ by $Q'$. By Lemma 2, $Q'$ is simple and counterclockwise, and $\Delta(v) \cup Q' = Q$ with disjoint interiors, so the second statement of (E) holds again. The output triangle $(u, v, w)$ is counterclockwise because $\mathrm{orient}(u, v, w) > 0$. If $Q'$ has 4 or more vertices, Lemma 2 shows that the flags of all vertices other than $u, w$ stay correct, and line L9 recomputes the flags of $u$ and $w$ and adds them to $W$ when they are true. If $Q'$ has 3 vertices, the loop stops at the next test of line L5 and the flags are not used again.

*Termination.* Each clip removes one vertex. Each pass of the loop either clips or removes one entry from $W$. The list $W$ receives at most $n$ entries in line L4 and at most 2 in each run of line L9, which runs once per clip. So the loop makes at most $(n - 3) + n + 2(n - 3)$ passes and stops when $Q$ has 3 vertices.

*Exit.* Then $Q$ is a simple counterclockwise polygon with 3 vertices, a counterclockwise triangle, and line L10 outputs it. By (E), the output triangles have disjoint interiors and their union is $P$. There are $n - 3$ clipped triangles and one more, so $n - 2$ in all. $\blacksquare$
