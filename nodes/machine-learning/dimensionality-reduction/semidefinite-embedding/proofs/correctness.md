---
title: The MVU program is a bounded convex problem whose solution keeps local distances
proves: [correctness]
status: full
---

Let $E$ be the constrained pairs, $D_{ij} = \|x_i - x_j\|^2$ for $(i, j) \in E$, $J = I - \frac1n\mathbf{1}\mathbf{1}^\top$, and let $\mathcal{C}$ be the set of symmetric $K \succeq 0$ with $K\mathbf{1} = 0$. For a pair $c = (i, j)$, let $A_c = (e_i - e_j)(e_i - e_j)^\top$, so that $\langle A_c, K\rangle = K_{ii} + K_{jj} - 2K_{ij}$. The feasible set is $\mathcal{F} = \{K \in \mathcal{C} : \langle A_c, K\rangle = D_c \text{ for } c \in E\}$.

**Lemma 1 (Gram matrices).** For $K \succeq 0$, $\sum_{i,j}K_{ij} = 0$ holds if and only if $K\mathbf{1} = 0$. Every $K \in \mathcal{C}$ is the Gram matrix $K_{ij} = y_i^\top y_j$ of points with $\sum_iy_i = 0$, and then $\langle A_c, K\rangle = \|y_i - y_j\|^2$ and

$$\operatorname{tr}(K) = \sum_i\|y_i\|^2 = \frac{1}{2n}\sum_{i,j}\|y_i - y_j\|^2 .$$

*Proof.* $\sum_{i,j}K_{ij} = \mathbf{1}^\top K\mathbf{1}$, and for $K \succeq 0$, $\mathbf{1}^\top K\mathbf{1} = \|K^{1/2}\mathbf{1}\|^2$, which is 0 exactly when $K^{1/2}\mathbf{1} = 0$, so when $K\mathbf{1} = 0$. Write $K = YY^\top$ with rows $y_i$, for example $Y = V\Lambda^{1/2}$ from the eigendecomposition. Then $K\mathbf{1} = 0$ gives $\|Y^\top\mathbf{1}\|^2 = \mathbf{1}^\top K\mathbf{1} = 0$, so $\sum_iy_i = 0$. Expanding $\|y_i - y_j\|^2 = \|y_i\|^2 + \|y_j\|^2 - 2y_i^\top y_j$ and summing over $i, j$ gives $2n\sum_i\|y_i\|^2 - 2\|\sum_iy_i\|^2 = 2n\operatorname{tr}(K)$. $\square$

**Lemma 2 (feasibility).** The centered Gram matrix $G = JXX^\top J$ of the input is in $\mathcal{F}$.

*Proof.* $G$ is the Gram matrix of the centered points $x_i - \bar x$, so it is positive semidefinite, $G\mathbf{1} = 0$, and $\langle A_c, G\rangle = \|(x_i - \bar x) - (x_j - \bar x)\|^2 = D_c$. $\square$

**Theorem 1 (existence and the lower bound).** If the graph $(\{1, \dots, n\}, E)$ is connected, the maximum of $\operatorname{tr}(K)$ over $\mathcal{F}$ exists and is at least $\operatorname{tr}(G)$. If the graph is not connected, the trace is unbounded on $\mathcal{F}$.

*Proof.* Let $\ell = \sum_{c \in E}\sqrt{D_c}$. For $K \in \mathcal{F}$ with points $y_i$ as in Lemma 1, any two points are joined by a path of pairs in $E$, and by the triangle inequality $\|y_i - y_j\| \le \ell$. So $\operatorname{tr}(K) \le \frac{1}{2n}n^2\ell^2$, and every entry $|K_{ij}| \le \sqrt{K_{ii}K_{jj}} \le \operatorname{tr}(K)$ is bounded. $\mathcal{F}$ is an intersection of closed sets, so it is compact, and it is nonempty by Lemma 2. The linear function $\operatorname{tr}$ has a maximum on it, which is at least $\operatorname{tr}(G)$. If the graph is not connected, take $G$ with points $x_i - \bar x$, pick one component with $n_1$ points, and let $n_2 = n - n_1$ be the number of the other points. Translate the points of that component by $s\,u$ and all other points by $-s\,u\,n_1/n_2$, with $u$ a unit vector. No constrained pair joins the two groups, so all constraints still hold, and the centering holds because $n_1 s - n_2 s n_1/n_2 = 0$. The trace becomes $\operatorname{tr}(G) + bs + s^2(n_1 + n_1^2/n_2)$ for a constant $b$ that comes from the cross terms, so it grows without bound as $s \to \infty$. $\square$

**Theorem 2 (convexity and weak duality).** $\mathcal{F}$ is convex, so every local maximum of $\operatorname{tr}$ on $\mathcal{F}$ is global. Moreover, if $\mu \in \mathbb{R}^E$ satisfies $J\big(\sum_c\mu_cA_c - I\big)J \succeq 0$, then $\operatorname{tr}(K) \le \sum_c\mu_cD_c$ for all $K \in \mathcal{F}$.

*Proof.* $\mathcal{C}$ is a convex cone, and the constraints are linear, so $\mathcal{F}$ is convex; a linear function on a convex set has no local maxima that are not global. For the bound, let $Z = \sum_c\mu_cA_c - I$. For $K \in \mathcal{F}$, $JKJ = K$, so $\langle Z, K\rangle = \langle Z, JKJ\rangle = \langle JZJ, K\rangle \ge 0$, because the inner product of two positive semidefinite matrices is nonnegative. Then $\sum_c\mu_cD_c - \operatorname{tr}(K) = \sum_c\mu_c\langle A_c, K\rangle - \langle I, K\rangle = \langle Z, K\rangle \ge 0$. $\square$

In the tests, the multipliers $\mu$ of the augmented Lagrangian method satisfy this condition up to $10^{-3}$, and $\sum_c\mu_cD_c$ agrees with the trace of the solver's $K$ to within a relative $10^{-3}$, which shows that the solver has found the optimum.

**Lemma 3 (the projection).** For a symmetric matrix $M$, let $JMJ = \sum_l\lambda_lu_lu_l^\top$. Then $\Pi(M) = \sum_{l : \lambda_l > 0}\lambda_lu_lu_l^\top$ is the point of $\mathcal{C}$ nearest to $M$ in the Frobenius norm.

*Proof.* Let $V \in \mathbb{R}^{n \times (n-1)}$ have orthonormal columns spanning $\mathbf{1}^\perp$, so $J = VV^\top$, and complete it with $\mathbf{1}/\sqrt n$ to an orthogonal matrix $U$. A matrix is in $\mathcal{C}$ exactly when it is $VNV^\top$ with $N \succeq 0$. The Frobenius norm is invariant under $U$, and $\|M - VNV^\top\|_F^2 = \|V^\top MV - N\|_F^2 + (\text{terms that do not depend on } N)$. The nearest $N \succeq 0$ to the symmetric matrix $V^\top MV$ keeps its eigenvectors and sets its negative eigenvalues to 0. Mapping back with $V$ gives $\Pi(M)$, because $V(V^\top MV)V^\top = JMJ$ and $\mathbf{1}$ is an eigenvector of $JMJ$ with eigenvalue 0. $\square$

So each inner step of the implementation is a true projected gradient step on the convex set $\mathcal{C}$, and the augmented Lagrangian method is a standard method for the linear constraints. Its convergence on convex problems is a classical result; the tests check the outcome directly through the constraint errors and Theorem 2.

**Theorem 3 (the example).** For $x_A = (0, 0)$, $x_B = (1, 0)$, $x_C = (1, 1.5)$ and $E = \{AB, BC\}$, the optimal value is $19/6$, attained only by the Gram matrix of $y_A = -7/6$, $y_B = -1/6$, $y_C = 4/3$.

*Proof.* By Lemma 1, $\operatorname{tr}(K) = \frac13(1 + 2.25 + \|y_A - y_C\|^2)$, and $\|y_A - y_C\| \le 1 + 1.5$ by the triangle inequality, with equality exactly when $y_B$ lies on the segment from $y_A$ to $y_C$. Then all three distances are fixed, and centered points with fixed distances have a fixed Gram matrix, because $K = -\frac12J\Delta J$ with $\Delta_{ij} = \|y_i - y_j\|^2$, as in classical MDS. The points on a line at $-7/6$, $-1/6$ and $4/3$ have these distances and sum to 0. $\square$
