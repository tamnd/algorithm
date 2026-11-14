---
title: The local and global steps of ARAP parameterization are exact, so the energy never increases
proves: [correctness, termination]
status: full
---

**Setting.** $M$ is a triangle mesh with a connected dual graph, and every triangle $t$ has a frame: corner points $q_1, q_2, q_3 \in \mathbb{R}^2$ of a counterclockwise triangle congruent to $t$, with area $A_t > 0$. A map assigns $u_v \in \mathbb{R}^2$ to each vertex. On the frame of $t$, let $\varphi_k$ be the affine function with $\varphi_k(q_k) = 1$ that is 0 on the opposite edge, and $g_k = \nabla \varphi_k$, a column vector. The Jacobian of the affine map of the frame to the image is

$$J_t(u) = \sum_{k=1}^{3} u_{v_k}\, g_k^\top,$$

a linear function of $u$. The energy is $E(u, R) = \sum_t A_t \lVert J_t(u) - R_t \rVert_F^2$ for rotations $R_t$, and $\hat E(u) = \min_R E(u, R)$. A vertex $p$ is pinned. Round $k$ of the algorithm computes $R^{(k+1)}$ from $u^{(k)}$ by the local step and then $u^{(k+1)}$ from $R^{(k+1)}$ by the global step, with $u^{(k+1)}_p = u^{(k)}_p$.

**Claim.**

1. (Edge form.) $A_t \lVert J_t(u) - R \rVert_F^2 = \frac12 \sum \cot \theta_m \lVert (u_k - u_l) - R (q_k - q_l) \rVert^2$, summed over the three edges $\{k, l\}$ of $t$, with $\theta_m$ the angle of the frame at the third corner $m$.
2. (Local step.) For $J = J_t(u)$, the rotation by the angle of the vector $(J_{11} + J_{22}, J_{21} - J_{12})$ minimizes $\lVert J - R \rVert_F^2$ over all rotations $R$.
3. (Global step.) For fixed rotations and a fixed $u_p$, $E(\cdot, R)$ has exactly one minimizer, and it is the solution of a linear system whose matrix is the cotangent Laplacian of $M$ with the row and column of $p$ removed. That matrix is positive definite.
4. (Monotone energy.) $\hat E(u^{(k+1)}) \le \hat E(u^{(k)})$ for all $k$.
5. (Termination.) The values $\hat E(u^{(k)})$ converge. For every $\varepsilon > 0$, the rule "stop after the first round that lowers $\hat E$ by less than $\varepsilon$" stops after at most $\lceil \hat E(u^{(0)}) / \varepsilon \rceil + 1$ rounds.

**Step 1 (facts about the corner gradients).** The functions $\varphi_k$ add up to 1, and $\sum_k \varphi_k(x)\, q_k = x$ for every point $x$ of the plane, because both sides are affine and agree at the three corners. Taking gradients, $\sum_k g_k = 0$ and $\sum_k q_k g_k^\top = I$. The vector $g_k$ is perpendicular to the edge opposite $q_k$, points into the triangle, and has length $1/h_k$, where $h_k = 2A_t / \lVert e_k \rVert$ is the height on that edge of length $\lVert e_k \rVert$. For $k \ne l$ and the third corner $m$, the edges opposite $q_k$ and $q_l$ meet at $q_m$ with the angle $\theta_m$ between them, so their inward normals make the angle $\pi - \theta_m$. Hence

$$g_k \cdot g_l = -\frac{\lVert e_k \rVert \lVert e_l \rVert \cos \theta_m}{4 A_t^2}, \qquad 2 A_t = \lVert e_k \rVert \lVert e_l \rVert \sin \theta_m,$$

and so $A_t\, g_k \cdot g_l = -\tfrac12 \cot \theta_m$.

**Step 2 (part 1).** First take $R = 0$. With $\lVert J \rVert_F^2 = \operatorname{tr}(J^\top J)$,

$$\lVert J_t(w) \rVert_F^2 = \sum_{k, l} (w_k \cdot w_l)(g_k \cdot g_l).$$

Since $\sum_l g_l = 0$, $g_k \cdot g_k = -\sum_{l \ne k} g_k \cdot g_l$. Put this in, and group the terms of each pair $k \ne l$: $|w_k|^2 + |w_l|^2 - 2 w_k \cdot w_l = \lVert w_k - w_l \rVert^2$, so

$$\lVert J_t(w) \rVert_F^2 = -\sum_{\{k, l\}} (g_k \cdot g_l) \lVert w_k - w_l \rVert^2.$$

Multiply by $A_t$ and use Step 1: $A_t \lVert J_t(w) \rVert_F^2 = \frac12 \sum_{\{k,l\}} \cot\theta_m \lVert w_k - w_l \rVert^2$. Now take any rotation $R$ and put $w_k = u_k - R q_k$. By Step 1, $J_t(w) = J_t(u) - R \sum_k q_k g_k^\top = J_t(u) - R$, and $w_k - w_l = (u_k - u_l) - R(q_k - q_l)$. This is part 1.

**Step 3 (part 2).** For a rotation $R$, $R^\top R = I$, so $\lVert J - R \rVert_F^2 = \lVert J \rVert_F^2 - 2 \operatorname{tr}(R^\top J) + 2$. Minimizing it is the same as maximizing $\operatorname{tr}(R^\top J)$. For $R$ the rotation by $\theta$, with entries $R_{11} = R_{22} = \cos\theta$, $R_{21} = -R_{12} = \sin\theta$,

$$\operatorname{tr}(R^\top J) = \sum_{a, b} R_{ab} J_{ab} = \cos\theta\, (J_{11} + J_{22}) + \sin\theta\, (J_{21} - J_{12}) = (\cos\theta, \sin\theta) \cdot (\alpha, \beta),$$

with $\alpha = J_{11} + J_{22}$ and $\beta = J_{21} - J_{12}$. By the Cauchy-Schwarz inequality this is at most $\sqrt{\alpha^2 + \beta^2}$, with equality when $(\cos\theta, \sin\theta)$ is the unit vector in the direction of $(\alpha, \beta)$. If $\alpha = \beta = 0$, the value is 0 for every $\theta$, and every rotation is a minimizer.

**Step 4 (part 3).** Fix the rotations. By part 1, $E(u, R)$ is a sum of terms $\frac12 \cot\theta_m \lVert (u_k - u_l) - d \rVert^2$ with constant vectors $d$, so it is a quadratic polynomial in the free values $u_v$, $v \ne p$, of the form $Q(u) - (\text{linear}) + \text{const}$, where $Q(u) = \sum_t A_t \lVert J_t(u) \rVert_F^2 = \sum_t \frac12 \sum_{\{k,l\}} \cot\theta_m \lVert u_k - u_l \rVert^2$. The $x$ and $y$ coordinates do not mix in $Q$, and for each coordinate the matrix of $Q$ is the cotangent Laplacian $L$, with the off-diagonal entry $-\frac12(\cot\alpha_{ij} + \cot\beta_{ij})$ for an edge $ij$ with the opposite angles $\alpha_{ij}$ and $\beta_{ij}$ ($\beta_{ij}$ absent on the boundary). Fix $u_p = 0$ in $Q$, which removes the row and column of $p$. $Q(u) \ge 0$ always. If $Q(u) = 0$ then $J_t(u) = 0$ on every triangle, so $u$ is constant on every triangle; two triangles that share an edge share two vertices, so the constants agree, and because the dual graph is connected, $u$ is one constant, which is $u_p = 0$. So $Q$ is positive definite on the free values. A quadratic function with a positive definite quadratic part has exactly one minimizer, the unique zero of its gradient, and the gradient is zero exactly when the free values solve $L' u = b$, with $L'$ the reduced Laplacian. This is part 3. Since $E(u + c, R) = E(u, R)$ for a translation $c$ (it does not change any $J_t$), pinning $u_p$ at any value does not change the minimum value over all maps.

**Step 5 (part 4).** The local step of round $k$ takes $R^{(k+1)}_t$ as in part 2 for $J_t(u^{(k)})$, so it minimizes each term separately and $E(u^{(k)}, R^{(k+1)}) = \min_R E(u^{(k)}, R) = \hat E(u^{(k)})$. The global step takes the minimizer of $E(\cdot, R^{(k+1)})$ with $u_p$ fixed, and $u^{(k)}$ is one of the candidates, so $E(u^{(k+1)}, R^{(k+1)}) \le E(u^{(k)}, R^{(k+1)})$. Finally $\hat E(u^{(k+1)})$ is a minimum over all rotations, so it is at most the value at $R^{(k+1)}$. Together,

$$\hat E(u^{(k+1)}) \le E(u^{(k+1)}, R^{(k+1)}) \le E(u^{(k)}, R^{(k+1)}) = \hat E(u^{(k)}).$$

**Step 6 (part 5).** The sequence $\hat E(u^{(k)})$ does not increase (Step 5) and is at least 0, so it converges. Suppose the first $N$ rounds each lower $\hat E$ by at least $\varepsilon$. Then $0 \le \hat E(u^{(N)}) \le \hat E(u^{(0)}) - N \varepsilon$, so $N \le \hat E(u^{(0)}) / \varepsilon$. So some round among the first $\lceil \hat E(u^{(0)}) / \varepsilon \rceil + 1$ lowers $\hat E$ by less than $\varepsilon$, and the rule stops there. Each round does a finite amount of work: one pass over the triangles and two solves with a matrix factored once.

**What is not claimed.** The energy is not convex in $u$, because the set of rotations is not convex, so the limit of the values need not be the global minimum, and the proof says nothing about the convergence of the maps themselves. Nothing in the energy forbids a triangle with $\det J_t < 0$, so the result is not proved to be free of flips. $\blacksquare$
