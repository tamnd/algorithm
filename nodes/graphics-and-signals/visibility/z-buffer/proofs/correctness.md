---
title: The z-buffer keeps the nearest covering triangle at each pixel center
proves: [correctness]
status: full
---

We use the pseudocode of the page. Fix a pixel $(i, j)$ with center $c$. Let $S_k$ be the set of indices $m < k$ such that $t_m$ covers $c$, and let $z_m$ be the depth of the plane of $t_m$ at $c$. Define the target pair $(z^*_k, m^*_k)$ as the least pair $(z_m, m)$ over $m \in S_k$ in the order of the pairs (first by depth, then by index), or $(+\infty, \bot)$ if $S_k$ is empty.

**Lemma (line L4 is the plane depth).** Let $t = (v_0, v_1, v_2)$ with positive doubled area $A$, and let $w_0, w_1, w_2$ be its edge functions at $c$. Then $(w_0 z_0 + w_1 z_1 + w_2 z_2)/A$ is the value at $c$ of the affine function that equals $z_r$ at $v_r$.

*Proof.* Each $w_r$ is affine in $c$, is $A$ at $v_r$, and is 0 at the other two vertices, because it is twice the signed area of a triangle with two vertices fixed on one edge. So the expression is affine in $c$ and takes the value $z_r$ at $v_r$ for $r = 0, 1, 2$. An affine function of $(x, y)$ is fixed by its values at three points that are not on a line, and $A \ne 0$ says the vertices are not on a line. $\square$

**Invariant.** Before the iteration $k$ of line L2 (and after the loop, with $k = n$), $D[i, j] = z^*_k$, and $C[i, j]$ is the color of $t_{m^*_k}$, or the background if $S_k$ is empty.

*Proof.* By induction on $k$. For $k = 0$, $S_0$ is empty, and line L1 sets $D[i, j] = +\infty$ and the background. Assume the invariant before iteration $k$. If $t_k$ does not cover $c$, line L3 does not visit $c$, $S_{k+1} = S_k$, and nothing at $(i, j)$ changes. If $t_k$ covers $c$, line L3 visits $c$ exactly once, and by the lemma line L4 computes $z_k$. Then $S_{k+1} = S_k \cup \{k\}$. Since $k$ is larger than every index in $S_k$, the pair $(z_k, k)$ is less than $(z^*_k, m^*_k)$ if and only if $z_k < z^*_k$. This is exactly the test of line L5. If it holds, line L6 sets the new least pair; if it fails, the least pair does not change, and neither do $D$ and $C$. Iterations for other triangles touch $(i, j)$ only when they cover $c$, which the same argument handles. $\square$

**Theorem.** Z-BUFFER returns, at each pixel, the color of the covering triangle with the least depth at the center, the first one on a tie, or the background, and $D$ holds that depth.

*Proof.* Apply the invariant with $k = n$ at each pixel. $\blacksquare$

**Order of drawing.** If the triangles are drawn in another order, the same argument holds with the index order replaced by the drawing order. The least depth $z^*_n$ is the same in each order, because a minimum over a set does not depend on the order of its elements. Only the choice among triangles with equal least depth can change.

**Exact coverage.** The theorem needs that line L3 visits exactly the covered centers. With the [top-left fill rule](/top-left-fill-rule/) and exact edge functions, a center on an edge shared by two triangles is covered by exactly one of them. With floating-point edge functions this can fail, and then a center can be drawn by both triangles or by neither.
