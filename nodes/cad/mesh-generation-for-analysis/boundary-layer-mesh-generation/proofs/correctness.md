---
title: Accepted boundary layers are valid quad meshes with geometric heights, and on a convex wall every layer is accepted
proves: [correctness, termination]
status: full
---

**Setting.** The wall is a simple polygon $x_0, \dots, x_{n-1}$ in counterclockwise order (indices mod $n$). Edge $i$ goes from $x_i$ to $x_{i+1}$, with length $L_i > 0$, unit direction $t_i$, and unit outward normal $n_i$, which is $t_i$ turned by $-90°$. The turning angle $\alpha_i \in (-\pi, \pi)$ at $x_i$ is the signed angle from $t_{i-1}$ to $t_i$; it is positive at a convex corner and negative at a reflex one. The miter vector is $m_i = (n_{i-1} + n_i) / (1 + n_{i-1}\cdot n_i)$. The layer-$k$ vertex is $x_i^k = x_i + d_k m_i$, the front $P_k$ is the polygon $x_0^k, \dots, x_{n-1}^k$, and the layer-$k$ quad on edge $i$ is $Q_i^k = (x_{i+1}^{k-1}, x_i^{k-1}, x_i^k, x_{i+1}^k)$.

**Lemma 1 (heights).** $d_k = h_1 (r^k - 1)/(r - 1)$ for $r \ne 1$, and the thickness of layer $k$ is $d_k - d_{k-1} = h_1 r^{k-1}$, so consecutive thicknesses have the ratio $r$.

*Proof.* L3 sets $d_0 = 0$ and $d_k = d_{k-1} + h_1 r^{k-1}$. The sum of the geometric series gives the formula. $\square$

**Lemma 2 (miter).** $m_i \cdot n_{i-1} = m_i \cdot n_i = 1$. So $x_i^k$ is at the distance $d_k$ from the lines of both edges at $x_i$, on their outer sides.

*Proof.* With $c = n_{i-1}\cdot n_i$, $(n_{i-1} + n_i)\cdot n_i = c + 1$, and the same for $n_{i-1}$. The division is defined because $c > -1$ when $|\alpha_i| < \pi$. The signed distance of $x_i + d m_i$ to the line of edge $i$ is $(d m_i)\cdot n_i = d$. $\square$

**Lemma 3 (offset edge).** For every $d \ge 0$, the segment from $x_i + d m_i$ to $x_{i+1} + d m_{i+1}$ is parallel to edge $i$, at the distance $d$ on its outer side, has the direction $t_i$ when its length is positive, and its signed length is $\ell_i(d) = L_i + d\,(\tau_i + \tau_{i+1})$ with $\tau_j = \tan(\alpha_j / 2)$.

*Proof.* Put the frame at $x_i$ with $t_i = (1, 0)$, so $n_i = (0, -1)$. Then $t_{i-1}$ is $t_i$ turned by $-\alpha_i$ and $n_{i-1} = (-\sin\alpha_i, -\cos\alpha_i)$, so $m_i \cdot t_i = -\sin\alpha_i / (1 + \cos\alpha_i) = -\tau_i$. In the same way $t_{i+1}$ is $t_i$ turned by $\alpha_{i+1}$, $n_{i+1} = (\sin\alpha_{i+1}, -\cos\alpha_{i+1})$, and $m_{i+1} \cdot t_i = \tau_{i+1}$. By Lemma 2 both end points have the normal component $d$. So the segment runs from $(-d\tau_i, -d)$ to $(L_i + d\tau_{i+1}, -d)$. $\square$

**Theorem 4 (one quad).** $Q_i^k$ is strictly convex and counterclockwise if and only if $\ell_i(d_k) > 0$. Since $\ell_i$ is affine with $\ell_i(0) = L_i > 0$, this holds for every $k$ if $\tau_i + \tau_{i+1} \ge 0$, and otherwise exactly while $d_k < L_i / (-(\tau_i + \tau_{i+1}))$, the collapse height.

*Proof.* Let $h = d_{k-1}$, $h' = d_k$, $\Delta = h' - h > 0$ by Lemma 1, $\ell = \ell_i(h)$ and $\ell' = \ell_i(h')$. By induction on $k$ (layer $k - 1$ was accepted), $\ell > 0$. Use the frame of Lemma 3, which is a rotation and a translation of the plane, so it keeps orientations. The quad has the vertices $(L_i + h\tau_{i+1}, -h)$, $(-h\tau_i, -h)$, $(-h'\tau_i, -h')$ and $(L_i + h'\tau_{i+1}, -h')$. The four orientation values at its corners, in order, are $\ell\Delta$, $\ell'\Delta$, $\ell'\Delta$ and $\ell\Delta$. All four are positive exactly when $\ell' > 0$. $\square$

**Theorem 5 (one layer).** Suppose $P_{k-1}$ is a simple counterclockwise polygon, every quad of layer $k$ is strictly convex and counterclockwise, and $P_k$ is simple. Then $P_k$ is counterclockwise, the region $R_{k-1}$ bounded by $P_{k-1}$ lies in the region $R_k$ bounded by $P_k$, and the quads of layer $k$ have pairwise disjoint interiors whose union is the closure of $R_k \setminus R_{k-1}$. Also $\sum_i \operatorname{area}(Q_i^k) = \operatorname{area}(R_k) - \operatorname{area}(R_{k-1})$.

*Proof.* As 1-chains, the boundary of $Q_i^k$ is the reversed edge $x_{i+1}^{k-1} x_i^{k-1}$, the edge $x_i^k x_{i+1}^k$, and two radial edges $x_i^{k-1} x_i^k$ and $x_{i+1}^k x_{i+1}^{k-1}$. Each radial edge appears once in each direction in the two neighbouring quads, so they cancel, and $\sum_i \partial Q_i^k = \partial P_k - \partial P_{k-1}$. The winding number $w(\gamma, x)$ of a closed chain about a point $x$ off it is additive in the chain, so for every $x$ off all edges

$$\sum_i w(\partial Q_i^k, x) = w(P_k, x) - w(P_{k-1}, x).$$

The shoelace sums are additive in the same way, which gives the area identity, and its left side is positive, so the signed area of $P_k$ is larger than that of $P_{k-1}$, hence positive: the simple polygon $P_k$ is counterclockwise, and $w(P_k, \cdot)$ is 1 inside and 0 outside, as is $w(P_{k-1}, \cdot)$. A strictly convex counterclockwise quad has winding number 1 inside and 0 outside. So the left side is a sum of terms in $\{0, 1\}$, and the right side is in $\{-1, 0, 1\}$. It cannot be $-1$, so $x \in R_{k-1}$ implies $x \in R_k$. Where it is 1, exactly one quad contains $x$; where it is 0, none does. Points on edges are a set of measure zero, so the interiors are disjoint and the union is the closure of $R_k \setminus R_{k-1}$. $\square$

**Corollary 6 (the output).** Every accepted layer satisfies Theorem 5, by the exact tests in L7 and L8 and by induction from the wall $P_0$, which is simple and counterclockwise. The regions $R_k \setminus R_{k-1}$ are disjoint for different $k$, because the $R_k$ are nested. Neighbouring quads share whole edges, by construction, and no directed edge is used twice (L7). So the output is a conforming mesh of strictly convex quads without inverted cells, which covers the region between the wall and the last front, with layer heights as in Lemma 1. The tests check all of this exactly, and they check the absence of overlap again by counting, for 3000 random points, the quads that contain each point.

**Theorem 7 (convex walls).** If the wall is strictly convex, that is, every $\alpha_i \in (0, \pi)$, every layer is accepted.

*Proof.* Every $\tau_i > 0$, so every $\ell_i(d)$ is positive and Theorem 4 makes every quad valid. The front $P_k$ has edges with the directions $t_0, \dots, t_{n-1}$ (Lemma 3), so its turning angles are the $\alpha_i$, all in $(0, \pi)$, with sum $2\pi$. A closed polygon with that property is convex and simple. $\square$

**Termination.** The loop L4 runs at most `nlayers` times, and each pass does $O(n^2)$ exact tests. So the procedure stops.

**What is not proved.** For a wall with reflex corners, the collapse height of Theorem 4 is exact, but the front can also hit itself before any quad degenerates, for example across a narrow gap, and the code finds that only by the simplicity test. The method stops the whole layer at the first failure; it does not prove that a better local rule exists. Nothing is proved about the shape of the quads, which are stretched on purpose, or about the miter length $1/\cos(\alpha_i/2)$, which grows without bound at sharp convex corners. Multiple bodies, normal smoothing and the 3D prism case are not covered.
