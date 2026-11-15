---
title: Each half step of ALS minimizes the objective over one block, the objective values converge, and limit points are stationary
proves: [correctness]
status: full
---

The notation is that of the page. $J(P, Q)$ is the regularized objective with weights $c_u, c_i$, and $\lambda > 0$. For the plain penalty $c_u = c_i = 1$. For the weighted penalty $c_u = |I_u|$ and $c_i = |U_i|$, and we assume that every user and every item has at least one rating, so that all weights are at least 1 (a user or item with no rating does not enter $J$ under this penalty, and line L7 keeps its vector at 0). Let $Q_0$ be the start of line L1, and let $P_{k+1}$ and $Q_{k+1}$ be the results of lines L3 and L4 in sweep $k + 1$. All statements are about exact arithmetic.

**Lemma 1 (separation).** For fixed $Q$,

$$J(P, Q) = \sum_u g_u(p_u) + \lambda \sum_i c_i \lVert q_i \rVert^2, \qquad g_u(p) = \sum_{i \in I_u} (r_{ui} - p^\top q_i)^2 + \lambda c_u \lVert p \rVert^2.$$

*Proof.* Group the terms of the sum over $K$ by user: the term of $(u, i)$ depends on $P$ only through $p_u$, and so does $\lambda c_u \lVert p_u \rVert^2$. $\square$

**Lemma 2 (one ridge regression).** Let $A_u = \sum_{i \in I_u} q_i q_i^\top + \lambda c_u I$ and $b_u = \sum_{i \in I_u} r_{ui} q_i$. Then $A_u$ is symmetric positive definite, and $g_u$ has the unique minimizer $p_u^* = A_u^{-1} b_u$. If $I_u$ is empty and the penalty is plain, $p_u^* = 0$.

*Proof.* Expanding, $g_u(p) = p^\top A_u p - 2 b_u^\top p + \sum_{i \in I_u} r_{ui}^2$. For $x \ne 0$, $x^\top A_u x = \sum_{i \in I_u} (q_i^\top x)^2 + \lambda c_u \lVert x \rVert^2 \ge \lambda c_u \lVert x \rVert^2 > 0$, so $A_u$ is positive definite. A quadratic function with a positive definite matrix is strictly convex, its gradient $2 A_u p - 2 b_u$ is zero exactly at $p = A_u^{-1} b_u$, and this point is its unique minimizer. With $I_u$ empty, $b_u = 0$ and the minimizer is 0. $\square$

**Theorem 3 (the half steps are exact).** Line L3 returns the unique minimizer of $J(\cdot, Q)$ over $P$, and line L4 returns the unique minimizer of $J(P, \cdot)$ over $Q$.

*Proof.* By Lemma 1, minimizing $J(\cdot, Q)$ is the same as minimizing each $g_u$ alone, since the last term does not depend on $P$. Lines L7 to L9 compute the matrix and the vector of Lemma 2 and solve the system; the Cholesky decomposition exists because $A_u$ is positive definite. So each $p_u$ is the unique minimizer of $g_u$, and $P$ is the unique minimizer of $J(\cdot, Q)$. The argument for the items is the same with the roles of users and items exchanged. $\square$

**Corollary 4 (monotone values).** For every $k \ge 0$,

$$J(P_{k+1}, Q_{k+1}) \le J(P_{k+1}, Q_k) \le J(P_k, Q_k),$$

with $P_0 = 0$. The sequence $J_k = J(P_k, Q_k)$ converges to a limit $J^* \ge 0$.

*Proof.* By Theorem 3, $P_{k+1}$ minimizes $J(\cdot, Q_k)$, so its value is at most that of $P_k$, and $Q_{k+1}$ minimizes $J(P_{k+1}, \cdot)$, so its value is at most that of $Q_k$. The sequence $J_k$ does not increase and $J \ge 0$, and a monotone sequence bounded below converges. $\square$

**Lemma 5 (bounded iterates).** For all $k \ge 1$, $\lVert P_k \rVert^2 + \lVert Q_k \rVert^2 \le J_0 / \lambda$, where $\lVert \cdot \rVert$ is the Frobenius norm.

*Proof.* Since every $c \ge 1$, $J(P, Q) \ge \lambda (\lVert P \rVert^2 + \lVert Q \rVert^2)$. By Corollary 4, $J(P_k, Q_k) \le J_0$. $\square$

**Theorem 6 (limit points are stationary).** Every limit point $(P^*, Q^*)$ of the sequence $(P_k, Q_k)$ satisfies $\nabla_P J(P^*, Q^*) = 0$ and $\nabla_Q J(P^*, Q^*) = 0$. At least one limit point exists.

*Proof.* By Lemma 5 the sequence is bounded, so it has a convergent subsequence $(P_{k_j}, Q_{k_j}) \to (P^*, Q^*)$, with $k_j \ge 1$. $J$ and its gradient are continuous, being polynomials.

The gradient in $Q$. By Theorem 3, $Q_{k}$ minimizes $J(P_{k}, \cdot)$ for $k \ge 1$, so $\nabla_Q J(P_{k}, Q_{k}) = 0$. Taking the limit along the subsequence gives $\nabla_Q J(P^*, Q^*) = 0$.

The gradient in $P$. The points $P_{k_j + 1}$ are bounded by Lemma 5, so after passing to a further subsequence, $P_{k_j + 1} \to P'$. For every $P$, Theorem 3 gives $J(P_{k_j + 1}, Q_{k_j}) \le J(P, Q_{k_j})$, and in the limit $J(P', Q^*) \le J(P, Q^*)$. So $P'$ minimizes $J(\cdot, Q^*)$. By Corollary 4, $J(P_{k_j + 1}, Q_{k_j})$ lies between $J_{k_j + 1}$ and $J_{k_j}$, which both tend to $J^*$, so $J(P', Q^*) = J^*$. Also $J(P^*, Q^*) = \lim J_{k_j} = J^*$. Thus $P^*$ reaches the minimum value of $J(\cdot, Q^*)$ too, and by the uniqueness of Lemma 2 (applied with $Q^*$), $P^* = P'$. A minimizer of a differentiable function has zero gradient, so $\nabla_P J(P^*, Q^*) = 0$. $\square$

**Proposition 7 (stationary is not minimal).** If $Q_0 = 0$, then $P_k = 0$ and $Q_k = 0$ for all $k$, and $(0, 0)$ is a stationary point of $J$. On the toy matrix of the page with $\lambda = 1$, $r = 1$ and the plain penalty, $(0, 0)$ is not a minimum.

*Proof.* With $Q = 0$ every $b_u = 0$, so $P = 0$ by Lemma 2, and then every item vector is 0 by the same argument; induction on $k$. At $(0, 0)$, $\nabla_{p_u} J = -2 \sum_{i \in I_u} r_{ui} q_i + 2 \lambda c_u p_u = 0$ and likewise for $q_i$. On the toy matrix, $J(0, 0)$ is the sum of the squared ratings, 155. With $q_i = 1$ for all items and $p = (5/2, 3, 2, 3/2)$ the squared errors sum to $10.75 + 7 + 10 + 6.75 = 34.5$ and the penalty is $21.5 + 4$, so $J = 60 < 155$. $\square$

**Cost of a sweep.** Line L8 adds one $r \times r$ outer product for each rating of the row, in $O(r^2)$ time, and each rating belongs to one user and one item, so forming all systems costs $O(s r^2)$ per half step. Each Cholesky solve costs $O(r^3)$. One sweep therefore costs $O(s r^2 + (m + n) r^3)$.

**What is not claimed.** Theorem 6 does not say that the sequence converges, only that its limit points are stationary, and Proposition 7 shows that a stationary point can be far from the minimum. Without the penalty, the global problem is NP-hard already for rank one (Gillis and Glineur, 2011), so no such guarantee should be expected from a method of this kind.
