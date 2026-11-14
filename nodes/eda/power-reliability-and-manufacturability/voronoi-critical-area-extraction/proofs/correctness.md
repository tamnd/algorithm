---
title: The incremental second order L-infinity structure gives the exact critical area for shorts of rectangles
proves: [correctness]
status: full
---

**Setting.** The layout is a finite list of closed axis-parallel rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$ with net labels $\nu_i$, and $W$ is a closed axis-parallel rectangle. A defect of radius $r \ge 0$ centred at $p$ is the closed square $Q(p, r) = p + r[-1, 1]^2 = \{q : \|q - p\|_\infty \le r\}$. For a net $N$ and a set $I$ of inserted rectangles, $d^I_N(p) = \min\{\delta_i(p) : i \in I, \nu_i = N\}$, with $\min \emptyset = +\infty$. The critical radius $t(p)$ is the second smallest entry of the list $(d_N(p))_N$ over all nets, with one entry per net. The critical area for shorts is $A(r) = \operatorname{area}\{p \in W : Q(p, r) \text{ meets rectangles of two different nets}\}$.

**Lemma 1 (distance to a rectangle).** $\delta_i(p) := \min_{q \in R_i} \|q - p\|_\infty = \max(a_i - x, x - b_i, c_i - y, y - d_i, 0)$ for $p = (x, y)$.

*Proof.* For $q = (u, v) \in R_i$, $\|q - p\|_\infty = \max(|u - x|, |v - y|)$. The choices of $u \in [a_i, b_i]$ and $v \in [c_i, d_i]$ are independent and $\max$ is nondecreasing in each argument, so the minimum is $\max(\min_u |u - x|, \min_v |v - y|)$. The distance from $x$ to $[a_i, b_i]$ is $\max(a_i - x, x - b_i, 0)$, since at most one of $a_i - x$ and $x - b_i$ is positive. The same holds for $y$, and the maximum of the two expressions is the formula. $\square$

**Lemma 2 (shorts and the critical radius).** $Q(p, r)$ meets $R_i$ if and only if $\delta_i(p) \le r$. Hence $Q(p, r)$ meets rectangles of two different nets if and only if $t(p) \le r$, and $A(r) = \operatorname{area}\{p \in W : t(p) \le r\}$.

*Proof.* $Q(p, r) \cap R_i \ne \emptyset$ if and only if some $q \in R_i$ has $\|q - p\|_\infty \le r$. Since $R_i$ is compact, the minimum $\delta_i(p)$ is attained, so this holds if and only if $\delta_i(p) \le r$. The square meets net $N$ if and only if $d_N(p) \le r$, and it meets two different nets if and only if at least two entries of the list $(d_N(p))_N$ are at most $r$, which is the case if and only if the second smallest entry is at most $r$. $\square$

**Lemma 3 (pieces).** Let $g_1, \dots, g_5$ be affine and $P$ a convex polygon. Line L6 splits $P$ by $g_2 - m$, then each part by $g_3 - m$, and so on, where $m$ is the piece recorded on the part, starting with $m = g_1$. The resulting parts are convex, have disjoint interiors, cover $P$, and on each part the recorded piece $g$ equals $\max_k g_k$.

*Proof.* Splitting a convex polygon by a line gives two closed convex polygons whose union is the polygon and whose interiors are disjoint; if the line misses the interior, one part is the whole polygon. By induction on $j$, after the splits by $g_2, \dots, g_j$ the recorded piece on each part is $\ge g_1, \dots, g_j$ on that part: on the part where $g_j - m \le 0$ the old $m$ stays and is $\ge g_j$; on the part where $g_j - m \ge 0$ the new piece $g_j$ is $\ge m$, which is $\ge g_1, \dots, g_{j-1}$. After $j = 5$ the recorded piece is the maximum. $\square$

**Lemma 4 (vertex test).** If an affine $u$ satisfies $u \ge 0$ at every vertex of a convex polygon $P$, then $u \ge 0$ on $P$. So if one piece $g_k$ of $\delta_R$ has $g_k \ge h$ at every vertex of $P$, then $\delta_R \ge h$ on $P$.

*Proof.* Every point of $P$ is a convex combination of its vertices, and an affine function maps a convex combination to the same combination of values. The second claim applies this to $u = g_k - h$ and uses $\delta_R = \max_j g_j \ge g_k$. $\square$

**Invariant.** Let $I_k$ be the first $k$ inserted rectangles. After their insertion:

1. the faces are convex polygons with disjoint interiors whose union is $W$;
2. on each face with state $(\nu, h_1, h_2)$ and for every point $p$ of the face, $h_1(p) = d^{I_k}_\nu(p) = \min_N d^{I_k}_N(p)$ and $h_2(p) = \min_{N \ne \nu} d^{I_k}_N(p)$;
3. $h_1$ and $h_2$ are affine on the face or $+\infty$; when $k = 0$ the state is $(\text{none}, +\infty, +\infty)$.

*Base.* For $k = 0$ the one face is $W$ and all distances are $+\infty$.

*Step.* Insert $R$ of net $M$, and write $g = \delta_R$ and $d_N = d^{I_k}_N$. The new distances are $d'_M = \min(d_M, g)$ and $d'_N = d_N$ for $N \ne M$. Fix a face $(P, \nu, h_1, h_2)$. Part 1 holds after the step because every operation splits a convex polygon into convex parts that cover it, by Lemma 3 and the remark in its proof. For part 2 and part 3, consider the cases.

*Quick test, $M = \nu$.* By Lemma 4, $g \ge h_1 = d_\nu$ on $P$, so $d'_\nu = d_\nu$ and nothing changes. *Quick test, $M \ne \nu$.* By Lemma 4, $g \ge h_2$ on $P$. Then $d'_M = \min(d_M, g) \ge h_2$, because $d_M \ge h_2$ by part 2. So $\min_{N \ne \nu} d'_N = h_2$, and the nearest net is still $\nu$ with $h_1 \le h_2$. Nothing changes.

Otherwise the face is split by Lemma 3 into parts $Q$ on which $g$ is one affine piece. On a part $Q$:

- *$\nu = $ none.* This happens only for the first rectangle, since after it every point has a finite distance to its net. All $d_N = +\infty$, so $d'_M = g$ is the only finite distance: the state $(M, g, +\infty)$ is correct.
- *$M = \nu$.* $d'_\nu = \min(h_1, g)$, and every other net has $d'_N = d_N \ge h_1 \ge d'_\nu$, so $\nu$ is still nearest and $h_2$ is unchanged. Splitting $Q$ by $g - h_1$ gives the part $g \le h_1$, where $h_1 \leftarrow g$, and the part $g \ge h_1$, where nothing changes. Both are affine.
- *$M \ne \nu$.* Before the step $d_M \ge h_2 \ge h_1$, by part 2.
    - Where $g \le h_1$: $d'_M = g \le h_1 = d'_\nu \le d'_N$ for every $N \notin \{M, \nu\}$. So $M$ is nearest with $h_1' = g$, and the second smallest is $\min(d'_\nu, \min_{N \notin \{M, \nu\}} d'_N) = h_1$, since all the other entries are $\ge h_1$. The state $(M, g, h_1)$ is correct.
    - Where $h_1 \le g \le h_2$ (or $h_2 = +\infty$): $d'_M = \min(d_M, g) = g$ because $d_M \ge h_2 \ge g$. Since $g \ge h_1$, $\nu$ stays nearest. The other entries $N \notin \{M, \nu\}$ satisfy $d'_N = d_N \ge h_2 \ge g$, so $\min_{N \ne \nu} d'_N = g$. The state $(\nu, h_1, g)$ is correct.
    - Where $g \ge h_2$: $d'_M = \min(d_M, g) \ge h_2$, and $d'_N = d_N \ge h_2$ for the other $N \ne \nu$, with equality for the net that attained $h_2$ (if that net is $M$, then $d_M = h_2$ there and $d'_M = h_2$). So $\min_{N \ne \nu} d'_N = h_2$ and nothing changes.

Each case sets $h_1$ and $h_2$ to affine functions on its part, so part 3 holds. This completes the step. $\square$

**Theorem 1 (exact critical area).** After all rectangles are inserted, every face satisfies $h_2 = t$ on its polygon, and line L13 returns $A(r)$ exactly.

*Proof.* By the invariant, on each face $h_1 = \min_N d_N$ and the nearest net is $\nu$, so the second smallest entry of the list $(d_N)_N$ is $\min_{N \ne \nu} d_N = h_2$, which is $t$. Since there are at least two nets, $t$ is finite everywhere. The faces cover $W$ and their boundaries have zero area, so $\operatorname{area}\{p \in W : t(p) \le r\} = \sum_{\text{faces}} \operatorname{area}(P \cap \{h_2 \le r\})$. By Lemma 2 the left side is $A(r)$. Each term is the area of the convex polygon $P \cap \{h_2 - r \le 0\}$, computed exactly by one split and the shoelace formula in rational arithmetic. $\square$

**Lemma 5 (quadratic pieces).** Let $P$ be a convex polygon and $h$ affine, not constant, with vertex values $v_0 < v_1 < \dots < v_m$ (distinct values only). Then $a(r) = \operatorname{area}(P \cap \{h \le r\})$ is $0$ for $r \le v_0$, equal to $\operatorname{area}(P)$ for $r \ge v_m$, and a polynomial of degree at most 2 on each $[v_j, v_{j+1}]$. If $h$ is constant on $P$ with value $v$, then $a(r) = 0$ for $r < v$ and $\operatorname{area}(P)$ for $r \ge v$.

*Proof.* Rotate coordinates so that $h = |\nabla h|\, s + \text{const}$ with $s$ the first coordinate. Then $a(r) = \int_{-\infty}^{r} \ell(\rho)\, d\rho / |\nabla h|$, where $\ell(\rho)$ is the length of the chord $P \cap \{h = \rho\}$. For $\rho$ strictly between $v_j$ and $v_{j+1}$, no vertex lies on the line $h = \rho$, so the line crosses the same two edges of $P$ for all such $\rho$. The crossing points depend affinely on $\rho$ along those fixed edges, so their distance $\ell(\rho)$ is affine in $\rho$ there. Its integral is quadratic on $[v_j, v_{j+1}]$, and $a$ is continuous. Below $v_0$ the chord is empty, above $v_m$ all of $P$ is included. The constant case is direct. $\square$

**Theorem 2 (average).** Let $f$ be a density of the defect radius with survival function $S(t) = \int_t^\infty f$. Then $\int_0^\infty A(r) f(r)\, dr = \sum_{\text{faces}} \int_0^\infty a_P(r) f(r)\, dr$, and line L14 computes each term exactly up to rounding in the closed forms.

*Proof.* The first equality is Theorem 1 summed under the integral; all terms are nonnegative. By Lemma 5, on $[v_j, v_{j+1}]$ the function $a_P$ is the unique polynomial of degree at most 2 through its values at $v_j$, $(v_j + v_{j+1})/2$ and $v_{j+1}$, which the implementation computes exactly and interpolates. Above $v_m$, $a_P = \operatorname{area}(P)$ contributes $\operatorname{area}(P) S(v_m)$. For Stapper's density, $\int r^k \cdot r/r_0^2\, dr$ and $\int r^k \cdot r_0^2 r^{-3}\, dr$ for $k = 0, 1, 2$ are $r^{k+2}/((k+2) r_0^2)$, $-r_0^2/(2r^2)$, $-r_0^2/r$ and $r_0^2 \ln r$, which are the closed forms used, with each interval split at $r_0$. $\square$

**Remark (general polygons).** For rectilinear polygons that are not unions of a few rectangles, a polygon can be cut into rectangles of the same net, and the theorems apply unchanged, since only net distances enter. Papadopoulou and Lee (IEEE TCAD 18(4), 1999) compute the same function $t$ from the second order $L_\infty$ Voronoi diagram of the polygons, built by a plane sweep, and integrate over trapezoids. Their construction and its running time are not proved here.
