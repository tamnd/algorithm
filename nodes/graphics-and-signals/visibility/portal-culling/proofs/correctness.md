---
title: Portal culling reaches exactly the visible cells in the plane
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. For a cone $K = (a, b)$ we write $\operatorname{int} K$ for its open interior, the directions $d$ with $\operatorname{cross}(a, d) > 0$ and $\operatorname{cross}(d, b) > 0$. For a portal $\pi = (p, q, c')$ of a cell, $C_\pi$ is the cone from $p - E$ to $q - E$. A *path* is a sequence $c_0, \pi_1, c_1, \ldots, \pi_m, c_m$ where $\pi_i$ is a portal of $c_{i-1}$ to $c_i$. The walk pushes $(c_m, K_m)$ for such a path when each $\pi_i$ passes line L5 and $K_i = K_{i-1} \cap C_{\pi_i}$ has an interior.

**Lemma 1.** Line L6 computes $K \cap C_\pi$, and line L7 drops it exactly when it has no interior.

*Proof.* Both cones are convex and less than 180 degrees wide, so the intersection is a convex cone $\{0\}$, a ray, or a cone with an interior, and in the last two cases its two boundary rays are boundary rays of $K$ or $C_\pi$ that lie in both. The function `meet` keeps these candidates, takes the most clockwise and the most counterclockwise, and reports no interior when their cross product is not positive. $\square$

**Lemma 2.** If $d \in \operatorname{int} K_m$ for a pushed path, then the ray $E + t d$, $t > 0$, crosses $\pi_1, \ldots, \pi_m$ in this order, each in its relative interior, and lies in $c_{i}$ between its crossings of $\pi_i$ and $\pi_{i+1}$.

*Proof.* Since $d \in \operatorname{int} C_{\pi_i}$, the ray meets the line of $\pi_i$ at one point $X_i$ in the relative interior of $\pi_i$, and it crosses from the side of $c_{i-1}$ to the side of $c_i$, because $E$ is strictly on the side of $c_{i-1}$ by line L5. We show by induction that $t(X_1) < t(X_2) < \cdots$ and that the ray is in $c_i$ just after $X_i$. For $i = 1$, the ray starts in $c_0$, which is convex, so it leaves $c_0$ once, and $X_1$ is on the boundary of $c_0$, so the part of the ray before $X_1$ is in $c_0$. Just after $X_1$ the ray is in $c_1$, because $X_1$ is in the relative interior of the portal. For the step, the ray is in the convex cell $c_{i}$ just after $X_i$, so it meets the boundary of $c_i$ at exactly one later point, where it leaves $c_i$. The point $X_{i+1}$ is on the boundary of $c_i$, it is different from $X_i$ (the portal $\pi_{i+1}$ is not $\pi_i$, because $\pi_i$ seen from $c_i$ fails line L5), and the ray crosses the line of $\pi_{i+1}$ from the side of $c_i$, so it is not the entry point. Hence $X_{i+1}$ is the exit point, after $X_i$, and just after it the ray is in $c_{i+1}$. $\square$

**Termination.** By Lemma 2, a direction $d \in \operatorname{int} K_m$ gives a ray that is in $c_0, c_1, \ldots, c_m$ in this order, on disjoint intervals of $t$. A ray meets each convex cell in one interval, so the cells of a pushed path are distinct. There are finitely many paths with distinct cells, each pushed at most once, so the loop of line L2 stops.

**Theorem 1 (no visible cell is missed).** If $c$ is visible, then $c \in V$.

*Proof.* Let $X$ be in the interior of $c$, with $X - E \in \operatorname{int} K_0$ and $EX$ meeting no wall. The set of such $X$ is open, because walls are closed and the other conditions are open. So we can choose $X$ such that the segment $EX$ passes through no endpoint of a portal or wall. The segment starts in $c_0$, and each time it leaves a cell it passes through a point of the boundary that is not a wall, so through the relative interior of a portal. This gives a path $c_0, \pi_1, c_1, \ldots, \pi_m, c_m = c$, crossed transversally. Let $d = X - E$. For each $i$, $E$ is strictly on the side of $c_{i-1}$ of the line of $\pi_i$, since the segment goes from $c_{i-1}$ to $c_i$ across it, so line L5 passes. The direction $d$ is in $\operatorname{int} C_{\pi_i}$, because the ray crosses the relative interior of $\pi_i$. By induction, $d \in \operatorname{int} K_i$ for each $i$, so each $K_i$ has an interior and line L8 pushes $(c_i, K_i)$. Hence $c \in V$. $\square$

**Theorem 2 (each cell reached is visible).** If line L8 adds $c_m$, then $c_m$ is visible.

*Proof.* Take $d \in \operatorname{int} K_m \subseteq \operatorname{int} K_0$ with a ray that passes through no endpoint of a wall; such $d$ exist because $\operatorname{int} K_m$ is open and the endpoints are finitely many. By Lemma 2 the ray reaches the interior of $c_m$, through the relative interiors of $\pi_1, \ldots, \pi_m$, and inside cells elsewhere. Let $X$ be a point of the ray just after $X_m$, in the interior of $c_m$. The segment $EX$ lies in the cells $c_0, \ldots, c_m$ except at the points $X_i$, which are portal points, not wall points. So it meets no wall, and $c_m$ is visible. $\square$

So $V$ is exactly the set of visible cells, plus $c_0$. In 3D, with the portal cones widened to screen rectangles, Theorem 1 holds with the same proof, because each widened cone contains the exact one, and Theorem 2 fails. $\blacksquare$
