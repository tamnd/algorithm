---
title: Each step of example-based facial rigging minimizes the energy in one block, so the energy never increases
proves: [correctness]
status: full
---

We use the notation of the page.
Flatten each $D_i$, $R_j$ and $H_i$ over all triangles and entries into vectors $d_i, r_j, h_i \in \mathbb{R}^P$.
Then $E(D, \alpha) = \sum_j \lVert \sum_i \alpha_{ij} d_i - r_j \rVert^2 + \beta \sum_i \lVert d_i - h_i \rVert^2$, with $\beta > 0$.
The arithmetic is exact.

## The blendshape step

**Theorem 1.** For fixed weights, line L4 returns the unique minimizer of $E$ in $D$.

*Proof.*
$E$ is a sum over the entries $p = 1, \ldots, P$ of terms that each depend only on $z_p = (d_1[p], \ldots, d_n[p])$:
$$E = \sum_p \left( \lVert A z_p - \rho_p \rVert^2 + \beta \lVert z_p - \eta_p \rVert^2 \right),$$
where $A_{ji} = \alpha_{ij}$, $\rho_p = (r_1[p], \ldots, r_m[p])$ and $\eta_p = (h_1[p], \ldots, h_n[p])$.
Each term is a quadratic in $z_p$ with the Hessian $2 (A^\top A + \beta I)$, which is positive definite, because $A^\top A \succeq 0$ and $\beta > 0$.
So each term has a unique minimizer, where the gradient $2 A^\top (A z_p - \rho_p) + 2 \beta (z_p - \eta_p)$ vanishes, that is, $(A^\top A + \beta I) z_p = A^\top \rho_p + \beta \eta_p$.
This is the system that `blendshape_step` solves, with one right hand side per entry. $\square$

## The weight step

For one example, drop the index $j$ and write $\varphi(a) = \lVert M a - r \rVert^2 = a^\top G a - 2 b^\top a + \lVert r \rVert^2$, with $M = (d_1, \ldots, d_n)$, $G = M^\top M$ and $b = M^\top r$.
$E$ is the sum of the $\varphi$ of the examples plus a term that does not depend on $\alpha$, and the examples do not share weights, so minimizing $E$ in $\alpha$ is minimizing each $\varphi$ on $[0, 1]^n$.

**Lemma 1.** A coordinate update with $G_{ii} > 0$ sets $a_i$ to the minimizer of $\varphi$ over $a_i \in [0, 1]$ with the other coordinates fixed, and if it moves $a_i$ from $u$ to $v$, then $\varphi$ decreases by at least $G_{ii} (u - v)^2$.

*Proof.*
As a function of $a_i$, $\varphi$ is $q(x) = G_{ii} x^2 - 2 c x + \text{const}$ with $c = b_i - \sum_{k \ne i} G_{ik} a_k$.
Its minimizer on $\mathbb{R}$ is $c / G_{ii}$, and since $q$ is a convex parabola, its minimizer on $[0, 1]$ is the clipped value $v$, which the code computes.
At $v$, the optimality on the interval gives $q'(v) (u - v) \ge 0$ for every $u \in [0, 1]$.
Then $q(u) = q(v) + q'(v)(u - v) + G_{ii} (u - v)^2 \ge q(v) + G_{ii} (u - v)^2$. $\square$

If $G_{ii} = 0$, then $d_i = 0$, $\varphi$ does not depend on $a_i$, and the code leaves $a_i$ unchanged.

**Theorem 2.** The weights of line L5 are in $[0, 1]$, $\varphi$ never increases during the sweeps, and every limit point of the sweeps minimizes $\varphi$ on $[0, 1]^n$.
If $G$ is positive definite, the sweeps converge to the unique minimizer.

*Proof.*
The start is clipped to $[0, 1]$ and every update is clipped, so the weights stay in the box.
By Lemma 1, $\varphi$ never increases.
Let $a^k$ be the point after sweep $k$, and let $\Pi$ be the map of one sweep, which is continuous as a composition of affine maps and clipping.
The sum over all updates of $G_{ii} (u - v)^2$ is at most $\varphi(a^0) - \min \varphi$, which is finite, so the moves go to 0, and $\lVert \Pi(a^k) - a^k \rVert \to 0$.
The box is compact, so a subsequence converges to some $a^*$, and by continuity $\Pi(a^*) = a^*$.
A fixed point of $\Pi$ is left unchanged by its first update, so $a^*_1$ is the minimizer of $\varphi$ in $a_1$; then the second update sees the same point, and so on for every coordinate.
So for every $i$, $a^*_i$ minimizes $\varphi$ in $a_i$ on $[0, 1]$, which means $\partial_i \varphi(a^*) \ge 0$ if $a^*_i = 0$, $\le 0$ if $a^*_i = 1$, and $= 0$ otherwise.
These are the KKT conditions of a convex function on a box, so $a^*$ is a minimizer.
If $G \succ 0$, the minimizer is unique, every convergent subsequence has the same limit, and the whole sequence converges to it. $\square$

The code stops when no coordinate moves by more than $10^{-14}$, which is a fixed point of $\Pi$ up to rounding.

## The energy never increases

**Theorem 3.** The values of $E$ recorded at line L6 and after line L4 are nonincreasing, and they converge.

*Proof.*
Line L4 replaces $D$ by the minimizer of $E(\cdot, \alpha)$, which is at most the value at the old $D$, by Theorem 1.
Line L5 starts the sweeps of each example at the current weights, and by Theorem 2 the sweeps do not increase $\varphi$, so they do not increase $E$.
A nonincreasing sequence of numbers with $E \ge 0$ converges. $\square$

## The fixed point

**Theorem 4.** Let $B_0 = A_0$, let each example be the exact blend $S_j = A_0 + \sum_i \alpha^0_{ij} (A_i - A_0)$ with $\alpha^0_j \in [0, 1]^n$, and let $h_1, \ldots, h_n$ be linearly independent.
Then the method returns $\alpha = \alpha^0$ and $B_i = A_i$, up to the fixed vertex.

*Proof.*
The gradient of a triangle is linear in the deformed positions for a fixed rest mesh, so $r_j = \sum_i \alpha^0_{ij} h_i$.
At the start, $D = H$ and $\alpha = \alpha^0$, so both terms of $E$ are 0.
$E \ge 0$, so this point minimizes $E$ in $D$, and by the uniqueness of Theorem 1, line L4 returns $D = H$.
With $D = H$, $\varphi_j(\alpha^0_j) = 0$, which is the minimum, and $G$ is the Gram matrix of independent vectors, so it is positive definite and the minimizer is unique.
The sweeps start at $\alpha^0_j$, and by Lemma 1 no update moves a minimizer, so line L5 keeps $\alpha^0$.
By induction, every alternation keeps $(H, \alpha^0)$, and line L7 gets the gradients $I + H_i$, which are the gradients of $A_i$ relative to $A_0 = B_0$, so by Theorem 5 it returns $A_i$. $\square$

## The Poisson step

**Theorem 5.** On a connected mesh, if the target gradients $I + D_{i,t}$ are the gradients $F_t(X)$ of a mesh $X$, line L7 returns $X$ translated so that the fixed vertex is at its rest position.

*Proof.*
The objective $\sum_t \lVert F_t(Y) - F_t(X) \rVert_F^2$ is at least 0, and it is 0 at $Y = X + c$ for the translation $c$ that moves the fixed vertex to its rest position, because a translation does not change edges.
It remains to show that this zero is unique.
If $Y$ and $Y'$ both give 0 with the same fixed vertex, then $W = Y - Y'$ satisfies $[w_b - w_a, w_c - w_a] Q_t = 0$ for every triangle, where $Q_t$ is the inverse of the rest edge matrix, so $w_a = w_b = w_c$.
Neighboring triangles share vertices, so on a connected mesh $W$ is constant, and it is 0 at the fixed vertex. $\square$

For gradients that do not come from a mesh, line L7 returns the least squares fit, which is the deformation transfer step.

## The check values

For $n = m = 1$ and one entry, Theorem 1 gives $(\alpha^2 + \beta) z = \alpha r + \beta h$.
With $\alpha = 0.5$ and $\beta = 0.25$, $\alpha^2 + \beta = 0.5$, so $z = (0.5 r + 0.25 h) / 0.5 = r + h / 2$.
For $n = 1$ and $d = (1, 0, 0, 0)$, Lemma 1 gives $a = \operatorname{clip}(d^\top r / d^\top d, 0, 1) = \operatorname{clip}(r_1, 0, 1)$, which is 1, 0.3 and 0 for $r_1 = 2$, $0.3$ and $-0.4$.
