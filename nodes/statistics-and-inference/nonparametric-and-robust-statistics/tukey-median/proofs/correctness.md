---
title: DEPTH computes the halfspace depth, REGION computes the depth region, and TUKEY-MEDIAN returns the centre of the deepest region
proves: [correctness]
status: full
---

**Setting.** $P = (p_1, \ldots, p_n)$ is a sample of points in the plane, with repeats allowed. For a direction $u \ne 0$ and a point $x$, $N_u(x) = \#\{i : u^\top p_i \ge u^\top x\}$ is the number of points in the closed halfplane $\{y : u^\top y \ge u^\top x\}$, which has $x$ on its boundary. The depth is $\operatorname{hd}(x) = \min_u N_u(x)$, and $D_k = \{x : \operatorname{hd}(x) \ge k\}$. All arithmetic is exact.

## Part 1. DEPTH

Lines L1 and L2 set $k_0$ to the number of points equal to $x$ and $D$ to the $m$ nonzero vectors $d_i = p_i - x$. For each $u$, the points equal to $x$ are in every halfplane of the form above, so $N_u(x) = k_0 + g(u)$ with $g(u) = \#\{i : u^\top d_i \ge 0\}$. If $m = 0$, the depth is $k_0$. Assume $m \ge 1$ from now on.

Write $\angle v \in [0, 2\pi)$ for the polar angle of a vector $v$. The vectors $d$ with $u^\top d \ge 0$ are those whose angle lies in the closed arc $[\angle u - \pi/2, \angle u + \pi/2]$ of length $\pi$. So $\min_u g(u)$ is the least number of the angles $\angle d_i$ in a closed arc of length $\pi$ (a closed half-turn). For a half-open arc $[\alpha, \alpha + \pi)$, let $c(\alpha)$ be the number of angles in it. For $j = 1, \ldots, m$, put $\theta_j = \angle d_j$ and $c_j = c(\theta_j)$.

**Lemma 1.** $\min_u g(u) = \min_j \min(c_j, m - c_j)$.

*Proof.* ($\le$) The number $c(\alpha)$ of a half-open half-turn is the count of a closed half-turn: for small $\varepsilon > 0$, the closed arc $[\alpha - \varepsilon, \alpha + \pi - \varepsilon]$ holds the same angles as $[\alpha, \alpha + \pi)$, because only finitely many angles exist and none lies in $[\alpha - \varepsilon, \alpha)$ or in $(\alpha + \pi - \varepsilon, \alpha + \pi)$ when $\varepsilon$ is small. Both $c_j = c(\theta_j)$ and $m - c_j = c(\theta_j + \pi)$ are of this form. So each is at least the minimum over closed half-turns.

($\ge$) Let $[\beta, \beta + \pi]$ be a closed half-turn with the least count. Its count is at least the count of $[\beta, \beta + \pi)$. Now turn the half-open arc $[\beta + t, \beta + \pi + t)$ forward, from $t = 0$, and stop at the first $t \ge 0$ where the open end $\beta + \pi + t$ is an angle $\theta_j$. A turn of the arc can add an angle only when the end passes it, and the end is open, so no angle enters before the stop. Angles can leave at the start. So the count does not increase, and at the stop the arc is $[\theta_j - \pi, \theta_j)$, which holds $m - c_j$ angles. $\square$

**Lemma 2.** After the sort of line L3, for each index $j$ that starts a group of equal angles, the loop of line L7 ends with $e - j = c_j$. The loop of lines L5 to L8 takes $O(m)$ steps in total.

*Proof.* Line L7 tests whether the angle of $D[e \bmod m]$ lies in $[\theta_j, \theta_j + \pi)$, by the sign of the cross product, and by the dot product for a parallel vector. Because $j$ is the first index of its group, the angles in $[\theta_j, \theta_j + \pi)$ are exactly the entries $D[j], D[j+1], \ldots$ that follow $j$ in cyclic order up to the first entry outside the arc. So the loop stops at $e = j + c_j$ if it starts at some $e \le j + c_j$. For the first group start, $e$ starts at $j$. For two group starts $j < j'$, the arc of $j'$ starts later than the arc of $j$ and ends later, so $j + c_j \le j' + c_{j'}$; line L6 then starts the loop at $\max(e, j') \le j' + c_{j'}$. The index $e$ never decreases and stays below $2m$, so the inner loop runs $O(m)$ times in total. $\square$

By Lemmas 1 and 2, line L9 returns $k_0 + \min_u g(u) = \operatorname{hd}(x)$. The angular sort uses exact comparisons (the half of the plane, then the cross product), so DEPTH takes $O(n \log n)$ time.

## Part 2. The depth region as a finite intersection

For a direction $u$, let $q_u(k)$ be the $k$-th largest of the numbers $u^\top p_1, \ldots, u^\top p_n$.

**Lemma 3.** $\operatorname{hd}(x) \ge k$ if and only if $u^\top x \le q_u(k)$ for every direction $u$.

*Proof.* $N_u(x) \ge k$ means that at least $k$ of the projections are $\ge u^\top x$, which is the same as $q_u(k) \ge u^\top x$. The depth is at least $k$ when this holds for all $u$. $\square$

Let $U$ be the set of the two normals $\pm(a_2 - b_2, b_1 - a_1)$ of $a - b$, over all pairs of sample points $a \ne b$. These are the directions where two projections are equal.

**Lemma 4.** If the points are not all on one line, then $\operatorname{hd}(x) \ge k$ if and only if $u^\top x \le q_u(k)$ for every $u \in U$.

*Proof.* One direction is Lemma 3. For the other, take any direction $w$. On the unit circle, the directions of $U$ cut the circle into arcs. Inside one arc no two projections are equal, so the order of the projections is fixed, and some index $s$ is the $k$-th largest for every direction in the open arc. By continuity of $u \mapsto u^\top p_i$, $q_u(k) = u^\top p_s$ also holds at the two ends $a$ and $b$ of the arc. The points are not all on one line, so at least two non-parallel differences $a - b$ exist, $U$ has at least four directions, and $U = -U$. So each arc is shorter than $\pi$, and every direction $w$ in the closed arc is $w = \lambda a + \mu b$ with $\lambda, \mu \ge 0$. If $a^\top x \le q_a(k) = a^\top p_s$ and $b^\top x \le b^\top p_s$, then
$$w^\top x = \lambda a^\top x + \mu b^\top x \le \lambda a^\top p_s + \mu b^\top p_s = w^\top p_s = q_w(k).$$
So the condition on $U$ gives the condition for every $w$, and Lemma 3 ends the proof. $\square$

**Lemma 5 (REGION).** If the points are not all on one line and $k \ge 1$, REGION$(k)$ returns $D_k$, as a convex polygon, a segment, a point, or the empty set.

*Proof.* Each $x \in D_k$ with $k \ge 1$ is in the convex hull of $P$ (a point outside the hull has depth 0), so $D_k$ lies in the bounding box of line L19. Line L22 replaces the convex set $R$ by $R \cap \{x : u^\top x \le q\}$. For a convex polygon, the intersection with a halfplane is the convex polygon whose vertices are the old vertices that satisfy the inequality and the points where an edge crosses the boundary line, in the same cyclic order. This is what the clipping step computes; with exact arithmetic it also works when $R$ has become a segment or a point. After the loop, $R$ is the box intersected with all the halfplanes of Lemma 4, which is $D_k$. Line L23 stops early when $R$ is empty, and then $D_k$ is empty. $\square$

## Part 3. The centerpoint bound

**Theorem 6.** For a sample of $n$ points in $\mathbb{R}^d$, $D_k \ne \emptyset$ for $k = \lceil n/(d+1) \rceil$.

*Proof.* By the region property on the [halfspace depth](/halfspace-depth/) page, $D_k$ is the intersection of the closed halfspaces $H$ with $\#\{i : p_i \in H\} \ge n - k + 1$. For each such $H$, let $C_H$ be the convex hull of the sample points in $H$. Then $C_H \subseteq H$, and $C_H$ is compact and convex. The sets $\{i : p_i \in H\}$ are subsets of $\{1, \ldots, n\}$, so the family $\{C_H\}$ is finite.

Take any $d + 1$ of these halfspaces. Each misses at most $k - 1$ indices, so together they miss at most $(d+1)(k-1)$ indices. Since $k - 1 < n/(d+1)$, this is less than $n$, so some index $i$ lies in all $d + 1$ index sets, and $p_i$ lies in all $d + 1$ hulls. By [Helly's theorem](/helly-theorem/), all the sets $C_H$ have a common point $c$. Then $c$ lies in each $H$, so $c \in D_k$. $\square$

In the plane this gives $k^* \ge \lceil n/3 \rceil$. The bound is tight: for three tight groups of $n/3$ points near the corners of a large triangle, every point has a closed halfplane through it that holds only one group. The test file checks a case with $n = 9$ and $k^* = 3$.

## Part 4. TUKEY-MEDIAN

If all points are on one line (line L10), a closed halfplane meets the line in a closed half-line or in the whole line, so the depth of a point on the line is the one-dimensional depth $\min(\#\{t_i \le t\}, \#\{t_i \ge t\})$ of its parameter $t$, and points off the line have depth 0. The deepest set is the median interval, and its midpoint is returned.

Otherwise, $D_1 \supseteq D_2 \supseteq \cdots$, so the property "$D_k \ne \emptyset$" holds for all $k$ up to $k^*$ and fails above it. Line L13 starts with $lo = \lceil n/3 \rceil$, and $D_{lo} \ne \emptyset$ by Theorem 6; $hi = n$ is at least $k^*$. The loop of lines L14 to L16 keeps $D_{lo} \ne \emptyset$ and $k^* \le hi$, and the interval shrinks in each round, so it ends with $lo = k^*$. By Lemma 5, line L17 gets $D_{k^*}$, and line L18 returns its centre of gravity (area centroid, or the midpoint of a segment, or the point). The centre of gravity of a convex set lies in the set, so the returned point has depth $k^*$. $\square$

## Part 5. Cost

$|U| \le n(n - 1)$. Line L12 sorts $n$ projections for each direction: $O(n^3 \log n)$ time and $O(n^3)$ space.

**Lemma 7.** During REGION, each polygon has at most $2n + 4$ vertices.

*Proof.* Each edge of $R$ lies on a box edge or on a line $\{x : u^\top x = q_u(k)\}$, and $q_u(k) = u^\top p_s$ for some sample point $p_s$, so the line passes through $p_s$. A line that holds an edge of a convex polygon is a supporting line of it. Through one point there are at most two supporting lines that hold edges: two tangents from a point outside, the lines of the at most two edges at a point on the boundary, and none from an interior point. So at most $2n$ edges come from the sample, and 4 from the box. $\square$

So one clip takes $O(n)$ time, REGION takes $O(n^3)$ time, and the binary search calls it $O(\log n)$ times. The total is $O(n^3 \log n)$ time and $O(n^3)$ space. This is a simple exact method, not the fastest one; the page lists the faster algorithms.
