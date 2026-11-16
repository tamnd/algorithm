---
title: Spanning tree initialization of a pose graph satisfies every tree edge, and the assembled system has the sparsity of the graph
proves: [correctness]
status: full
---

**Setting.** A pose graph has vertices $V$ with poses $X_i \in SE(2)$ and edges $k = (i, j, Z_k, \Omega_k)$ with $i \ne j$, $Z_k \in SE(2)$ and $\Omega_k$ symmetric positive semidefinite. The residual of an edge is $e_k = \mathrm{Log}(Z_k^{-1} X_i^{-1} X_j)$, and the cost is $F = \sum_k e_k^\top \Omega_k e_k$. $\mathrm{Log}$ maps $SE(2)$ onto the set of $(\rho_x, \rho_y, \theta)$ with $\theta \in [-\pi, \pi)$, and it is the inverse of $\mathrm{Exp}$ on that set.

**Assumptions.**

- (A1) Exact arithmetic for the group operations.
- (A2) For the claim on the gradient, every residual angle lies in the open interval $(-\pi, \pi)$, so that $\mathrm{Log}$ is smooth at the current poses.

**Claim 1 (initialization).** Let $C$ be the connected component of the root $r$. INITIALIZE($G$, $r$) returns the set $C$, keeps $X_r$, and gives every edge of a spanning tree of $C$ the residual $0$. It does not change the poses outside $C$.

*Proof.* Lines L5 to L12 are a [breadth-first search](/breadth-first-search/) from $r$ over the edge lists. A vertex enters the set $\mathit{seen}$ only when an edge from a vertex already in $\mathit{seen}$ reaches it, so every vertex in $\mathit{seen}$ is in $C$. Conversely, let $v \in C$ with the path $r = v_0, v_1, \dots, v_\ell = v$. By induction on $s$, every $v_s$ enters $\mathit{seen}$: $v_0$ is there at the start; when $v_{s}$ is popped at line L7, which happens because every vertex in $\mathit{seen}$ is pushed once, the loop of line L8 visits the edge to $v_{s+1}$ and adds $v_{s+1}$ if it is not already there. So $\mathit{seen} = C$. Only line L11 writes a pose, and only for a vertex not in $\mathit{seen}$ and reached from $C$, so poses outside $C$ do not change and $X_r$ is never written.

For each $j \ne r$ in $C$, let $k(j)$ be the edge through which $j$ entered $\mathit{seen}$. These $|C| - 1$ edges join each vertex to one that entered before it, so they form a spanning tree of $C$. Each pose is written once, at the moment of entry, and the pose $X_i$ of the other end is already final then. If $k(j)$ goes from $i$ to $j$, line L11 sets $X_j = X_i Z$, so $Z^{-1} X_i^{-1} X_j = I$ and $e = \mathrm{Log}(I) = 0$. If it goes from $j$ to $i$, line L11 sets $X_j = X_i Z^{-1}$, and then the residual of this edge, with $j$ as its first end, is $\mathrm{Log}(Z^{-1} X_j^{-1} X_i) = \mathrm{Log}(Z^{-1} Z X_i^{-1} X_i) = 0$. $\square$

**Corollary.** If all measurements are consistent, that is, there are poses $X^\dagger$ with $Z_k = (X_i^\dagger)^{-1} X_j^\dagger$ for every edge, and $X_r = X_r^\dagger$, then after INITIALIZE every pose of $C$ equals $X^\dagger$ and every residual in $C$ is $0$. Indeed, by Claim 1 and induction along the tree, $X_j = X_i Z_k = X_i^\dagger (X_i^\dagger)^{-1} X_j^\dagger = X_j^\dagger$ for each tree edge (and the same for the reversed case). Then every edge of $C$, in the tree or not, has $Z_k^{-1} X_i^{-1} X_j = I$.

**Claim 2 (assembly).** ASSEMBLE returns $H_{uv} = \sum_k J_{k,u}^\top \Omega_k J_{k,v}$ and $g_u = \sum_k J_{k,u}^\top \Omega_k e_k$, where $J_{k,u}$ is the Jacobian of $e_k$ with respect to the right perturbation $X_u \exp(\delta_u)$ at $\delta_u = 0$, and $J_{k,u} = 0$ if $u$ is not an end of $k$. A block $H_{uv}$ with $u \ne v$ is present only if an edge joins $u$ and $v$. Under (A2), $2 g_u$ is the gradient of $F(X_u \exp(\delta_u))$ at $\delta_u = 0$.

*Proof.* The residual $e_k$ depends only on $X_i$ and $X_j$, so $J_{k,u} = 0$ unless $u \in \{i, j\}$. Lines L14 to L17 add, for each edge, the four products $J_{k,u}^\top \Omega_k J_{k,v}$ with $u, v \in \{i, j\}$ and the two products $J_{k,u}^\top \Omega_k e_k$. These are exactly the nonzero terms of the sums, and no block $(u, v)$ is created by any other edge than one with the ends $u$ and $v$. For the gradient, $\partial F / \partial \delta_u = \sum_k 2 J_{k,u}^\top \Omega_k e_k$ because $\Omega_k$ is symmetric, and this is $2 g_u$. $\square$

In the code the Jacobians are central differences with the step $10^{-6}$, so $J$ has an error of order $10^{-12}$ times the third derivative. The test compares $2g$ with central differences of $F$ and finds agreement within $10^{-5}$.

**What this does not show.** The spanning tree initialization satisfies the tree edges and puts all of the error of each loop on its non-tree edges. With noise, this can be a poor start for an optimizer, and the claims say nothing about the minimum of $F$; that is the problem of [pose graph optimization](/pose-graph-optimization/).
