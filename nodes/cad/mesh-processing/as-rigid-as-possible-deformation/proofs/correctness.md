---
title: The local step of as-rigid-as-possible deformation is optimal, the global step is a least squares solve, the energy never increases, and a rigid motion has zero energy and is a fixed point
proves: [correctness, termination]
status: full
---

**Setup.** The mesh has the rest positions $p_1, \ldots, p_n$. Each edge $\{i, j\}$ has a weight $w_{ij} = w_{ji} \ge 0$, and $N(i)$ is the set of the neighbours of vertex $i$. Write $e_{ij} = p_i - p_j$. A nonempty set $H$ of handle vertices has fixed targets $h_k$, and the other vertices are free. Every connected component of the graph of the edges with $w_{ij} > 0$ holds a handle. The positions $q_1, \ldots, q_n$ have $q_k = h_k$ for $k \in H$, and each vertex has a rotation $R_i \in SO(3)$. The energy is

$$E(q, R) = \sum_{i=1}^{n}\sum_{j \in N(i)} w_{ij}\,\bigl|(q_i - q_j) - R_i e_{ij}\bigr|^2 \ \ge\ 0.$$

The local step keeps $q$ and sets each $R_i$ to a rotation that maximizes $\operatorname{tr}(R_i S_i)$, with $S_i = \sum_{j \in N(i)} w_{ij}\, e_{ij} (q_i - q_j)^{\mathsf T}$. The global step keeps $R$ and solves, at each free vertex $i$,

$$\sum_{j \in N(i)} w_{ij}(q_i - q_j) = \sum_{j \in N(i)} \frac{w_{ij}}{2}(R_i + R_j)\, e_{ij}, \tag{1}$$

with $q_k = h_k$ for $k \in H$. The algorithm starts with $R_i = I$, does one global step, and then does $s$ rounds of a local step followed by a global step.

**Lemma 1 (the local step is optimal).** For a fixed $q$, the local step gives the least value of $E(q, \cdot)$ over all choices of rotations.

*Proof.* $E$ is a sum of one term $E_i$ for each vertex, and $E_i$ depends only on $R_i$. Write $f_{ij} = q_i - q_j$. A rotation keeps lengths, so $|f_{ij} - R_i e_{ij}|^2 = |f_{ij}|^2 + |e_{ij}|^2 - 2 f_{ij}^{\mathsf T} R_i e_{ij}$, and $f_{ij}^{\mathsf T} R_i e_{ij} = \operatorname{tr}(R_i e_{ij} f_{ij}^{\mathsf T})$. So

$$E_i = \sum_{j \in N(i)} w_{ij}\bigl(|f_{ij}|^2 + |e_{ij}|^2\bigr) - 2\operatorname{tr}(R_i S_i).$$

The first sum does not depend on $R_i$, so $E_i$ is least where $\operatorname{tr}(R_i S_i)$ is largest. Let $S_i = U \Sigma V^{\mathsf T}$ be a singular value decomposition and $d = \det U \det V$. By Lemma 2 of the proof of the [Kabsch algorithm](/kabsch-algorithm/), the maximum of $\operatorname{tr}(R S_i)$ over $SO(3)$ is attained by $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$, which is what the local step returns. $\square$

The code computes $d$ as the sign of $\det(V U^{\mathsf T})$. That determinant is $+1$ or $-1$ up to rounding, far from 0, so the sign is safe in floating point.

**Lemma 2 (the global step is a least squares solve).** For fixed rotations, the system (1) has exactly one solution, and that solution is the unique minimum of $E(\cdot, R)$ over the positions with $q_k = h_k$ on the handles.

*Proof.* Each edge $\{i, j\}$ appears twice in $E$, once from $i$ with $R_i e_{ij}$ and once from $j$ with $R_j e_{ji} = -R_j e_{ij}$. With $d = q_i - q_j$, $a = R_i e_{ij}$ and $b = R_j e_{ij}$, the two terms add to $w_{ij}(|d - a|^2 + |d - b|^2)$. By the identity $|d - a|^2 + |d - b|^2 = 2|d - \tfrac{a + b}{2}|^2 + \tfrac12|a - b|^2$,

$$E(q, R) = \sum_{\{i, j\}} w_{ij}\Bigl(2\,\bigl|q_i - q_j - c_{ij}\bigr|^2 + \tfrac12\bigl|(R_i - R_j) e_{ij}\bigr|^2\Bigr), \qquad c_{ij} = \tfrac12 (R_i + R_j) e_{ij}.$$

The second part does not depend on $q$. The first part is a quadratic function of the free positions, and it splits into one function for each of the three coordinates. Its gradient with respect to a free $q_i$ is $4\sum_{j \in N(i)} w_{ij}(q_i - q_j - c_{ij})$, so its critical points are the solutions of (1). Move the known $q_j = h_j$ of the handle neighbours to the right side. The matrix $A$ of the system on the free vertices has $A_{ii} = \sum_{j \in N(i)} w_{ij}$ and $A_{ij} = -w_{ij}$ for free $j$. For a vector $x$ on the free vertices, extended by 0 on the handles,

$$x^{\mathsf T} A x = \sum_{\{i, j\}} w_{ij}(x_i - x_j)^2 \ \ge\ 0.$$

If $x^{\mathsf T} A x = 0$, then $x_i = x_j$ on every edge with $w_{ij} > 0$, so $x$ is constant on each connected component of those edges. Each component holds a handle, where $x = 0$, so $x = 0$. Thus $A$ is symmetric positive definite, the system has exactly one solution, and the quadratic, whose Hessian in each coordinate is $4A$, has that solution as its unique minimum. The Cholesky factorization $A = L L^{\mathsf T}$ exists because $A$ is positive definite, and $A$ depends only on the weights and on $H$, so one factorization serves every global step. $\square$

**Theorem 1 (the energy never increases, and the algorithm stops).** Let $q^{(0)}$ be the result of the first global step with $R^{(0)} = I$, and for $t \ge 1$ let $R^{(t)}$ be the result of the local step on $q^{(t-1)}$ and $q^{(t)}$ the result of the global step with $R^{(t)}$. Then

$$E(q^{(0)}, R^{(0)}) \ \ge\ E(q^{(0)}, R^{(1)}) \ \ge\ E(q^{(1)}, R^{(1)}) \ \ge\ E(q^{(1)}, R^{(2)}) \ \ge\ \cdots \ \ge\ 0.$$

*Proof.* The step from $E(q^{(t-1)}, R^{(t-1)})$ to $E(q^{(t-1)}, R^{(t)})$ keeps $q$ and replaces the rotations by the best ones, so it does not increase $E$ by Lemma 1. The step from $E(q^{(t-1)}, R^{(t)})$ to $E(q^{(t)}, R^{(t)})$ keeps $R$ and replaces $q$ by the minimum over all admissible positions, which include $q^{(t-1)}$, so it does not increase $E$ by Lemma 2. The energy is a sum of squares, so it is at least 0. The algorithm does $s$ rounds, each of one local step and one global step, so it stops. $\square$

A nonincreasing sequence that is bounded below converges, so the energies converge. It is not proved here that the positions $q^{(t)}$ converge, nor that their limit is a global minimum of $E$. The energy is not convex in $(q, R)$, because $SO(3)$ is not a convex set. In the measurements on the page the energy decreases slowly and roughly linearly.

**Theorem 2 (a rigid motion).** Let $Q \in SO(3)$ and $t \in \mathbb{R}^3$, and let $q^\ast_i = Q p_i + t$ for all $i$.

1. $E(q^\ast, (Q, \ldots, Q)) = 0$, the least value of $E$.
2. If the edge vectors $e_{ij}$ of the edges at $i$ with $w_{ij} > 0$ span a plane, the local step on $q^\ast$ returns $R_i = Q$.
3. If all handle targets are $h_k = Q p_k + t$, the global step with all $R_i = Q$ returns $q^\ast$.

So, when the handles move rigidly and the condition of part 2 holds at every vertex, $(q^\ast, Q)$ is a fixed point of the algorithm with energy 0.

*Proof.* (1) $q^\ast_i - q^\ast_j = Q e_{ij}$, so every term of $E$ is $w_{ij}|Q e_{ij} - Q e_{ij}|^2 = 0$, and $E \ge 0$.

(2) With $f_{ij} = Q e_{ij}$, $S_i = \sum_j w_{ij} e_{ij} e_{ij}^{\mathsf T} Q^{\mathsf T} = C Q^{\mathsf T}$, where $C = \sum_j w_{ij} e_{ij} e_{ij}^{\mathsf T}$ is symmetric positive semidefinite. For a rotation $R$ let $Z = Q^{\mathsf T} R \in SO(3)$. Then $\operatorname{tr}(R S_i) = \operatorname{tr}(R C Q^{\mathsf T}) = \operatorname{tr}(Q^{\mathsf T} R C) = \operatorname{tr}(Z C)$. Write $C = \sum_k \lambda_k u_k u_k^{\mathsf T}$ with orthonormal $u_k$ and $\lambda_k \ge 0$. Then $\operatorname{tr}(Z C) = \sum_k \lambda_k\, u_k^{\mathsf T} Z u_k \le \sum_k \lambda_k$, because $|u_k^{\mathsf T} Z u_k| \le |u_k|\,|Z u_k| = 1$, and equality needs $Z u_k = u_k$ for each $k$ with $\lambda_k > 0$. The range of $C$ is the span of the $e_{ij}$ with $w_{ij} > 0$, which is at least a plane, so at least two of the $\lambda_k$ are positive and $Z$ fixes two orthonormal vectors $u, v$. A rotation keeps cross products, so $Z(u \times v) = Zu \times Zv = u \times v$, and $Z$ fixes a basis, so $Z = I$. Hence $R = Q$ is the only maximizer of $\operatorname{tr}(R S_i)$, and by Lemma 1 the local step returns it.

(3) With all $R_i = Q$, $c_{ij} = Q e_{ij}$ and $q^\ast_i - q^\ast_j - c_{ij} = 0$ for every edge, so $q^\ast$ satisfies (1), and it takes the handle values. By Lemma 2 the solution of (1) is unique, so it is $q^\ast$. $\square$

Theorem 2 does not say that the algorithm reaches $q^\ast$ from the rest shape. With the handles moved rigidly, the tests and the page measure that it tends to $q^\ast$, at a rate that depends on how many vertices are handles.
