---
title: The LORAKS rank bound and the monotone decrease of its objective
proves: [correctness]
status: full
---

The setting is that of the algorithm. The grid is $\{0, \ldots, n_1 - 1\} \times \{0, \ldots, n_2 - 1\}$, and a grid point $q = (a, b)$ holds the signed frequency $\kappa(q) = (a - \lfloor n_1/2 \rfloor, b - \lfloor n_2/2 \rfloor)$. The neighborhood is a list of $w$ integer offsets $o_1, \ldots, o_w$. The centers are the grid points $c_1, \ldots, c_N$ with $c_i + o_j$ on the grid for every $j$. The operator $P$ maps a grid $k$ to the $N \times w$ matrix $P(k)_{ij} = k(c_i + o_j)$. Its adjoint $P^H$ adds the entry $L_{ij}$ to grid point $c_i + o_j$. So $P^H P = \operatorname{diag}(D)$, where $D(q)$ is the number of pairs $(i, j)$ with $c_i + o_j = q$. The mask $M(q) \in \{0, 1\}$ marks the sampled points.

## 1. The rank bound

**Theorem 1.** Let $x$ be an image on an $n_1 \times n_2$ grid of pixels, and let $S$ be the set of pixels where $x \ne 0$, with $s = |S|$. Let $k = F_u x$ in centered order:

$$k(q) = (n_1 n_2)^{-1/2} \sum_{\rho \in S} x(\rho)\, e^{-2\pi i\, \kappa(q) \cdot (\rho_1 / n_1, \rho_2 / n_2)}.$$

Then $\operatorname{rank} P(k) \le \operatorname{rank} B \le \min(s, w)$, where $B$ is the $w \times s$ matrix $B_{j\rho} = e^{-2\pi i\, o_j \cdot (\rho_1/n_1, \rho_2/n_2)}$. Every vector $h \in \mathbb{C}^w$ with $B^T h = 0$ satisfies $P(k)\, h = 0$.

*Proof.* Write $e_\rho(v) = e^{-2\pi i\, v \cdot (\rho_1/n_1, \rho_2/n_2)}$ for an integer vector $v$. Then $e_\rho(u + v) = e_\rho(u)\, e_\rho(v)$, and $\kappa(c_i + o_j) = \kappa(c_i) + o_j$. So

$$P(k)_{ij} = (n_1 n_2)^{-1/2} \sum_{\rho \in S} e_\rho(\kappa(c_i))\, x(\rho)\, e_\rho(o_j).$$

This is the product $P(k) = A \operatorname{diag}(x_S) B^T$ with $A_{i\rho} = (n_1 n_2)^{-1/2} e_\rho(\kappa(c_i))$, an $N \times s$ matrix. The rank of a product is at most the rank of each factor, so $\operatorname{rank} P(k) \le \operatorname{rank} B^T = \operatorname{rank} B \le \min(s, w)$. If $B^T h = 0$, then $P(k) h = A \operatorname{diag}(x_S) B^T h = 0$. $\square$

The vector $h$ is a filter on the neighborhood. Its image-domain function $H(\rho) = \sum_j h_j e_\rho(o_j)$ is $(B^T h)_\rho$, so the condition $B^T h = 0$ says that $H$ vanishes on the support $S$. Then $H x = 0$ pixel by pixel, and in k-space the filter annihilates every neighborhood. This is the annihilating filter reading of the bound.

**Remark.** The bound is exact for the discrete model. For a continuous image with a support of positive area, a trigonometric polynomial with frequencies in the neighborhood cannot vanish on the whole support, so the rank deficiency is only approximate. This is why the method penalizes the tail of the singular values instead of imposing an exact rank.

## 2. The best rank r approximation

**Lemma 2 (Eckart-Young).** For a complex $N \times w$ matrix $C$ with singular values $\sigma_1 \ge \sigma_2 \ge \cdots$ and an integer $r \ge 0$,

$$\min_{\operatorname{rank} L \le r} \|C - L\|_F^2 = \sum_{j > r} \sigma_j^2 =: T_r(C),$$

and $L = C V_r V_r^H$ attains the minimum, where the columns of $V_r$ are the top $r$ right singular vectors.

This is the Eckart-Young theorem in the Frobenius norm; see [singular-value-decomposition](/singular-value-decomposition/). The code forms $V_r V_r^H$ from the eigenvectors of the real symmetric matrix $\Phi(C^H C)$, where $\Phi(Z) = \begin{pmatrix} \operatorname{Re} Z & -\operatorname{Im} Z \\ \operatorname{Im} Z & \operatorname{Re} Z \end{pmatrix}$. The map $\Phi$ is a ring homomorphism from complex to real matrices, and $\Phi(Z^H) = \Phi(Z)^T$. If $G v = \lambda v$, then $\Phi(G)$ has the two orthogonal eigenvectors $(\operatorname{Re} v, \operatorname{Im} v)$ and $(-\operatorname{Im} v, \operatorname{Re} v)$ with the eigenvalue $\lambda$. So each eigenvalue of $G$ appears twice, and the sum of $q q^T$ over the top $2r$ eigenvectors $q$ of $\Phi(G)$ is $\Phi(V_r V_r^H)$, when $\sigma_r > \sigma_{r+1}$. The test file checks the result against the real SVD of $\Phi(C)$.

## 3. Monotone decrease

The objective is

$$J(k) = \sum_q M(q)\, |k(q) - d(q)|^2 + \lambda\, T_r(P(k)) \qquad (\lambda > 0).$$

**Theorem 3.** Let $k_i$ be the iterate at the start of a pass of line L2, $L_i$ the matrix of line L4, and $k_{i+1}$ the result of line L8. Then $J(k_{i+1}) \le J(k_i)$.

*Proof.* Define the surrogate $Q(k; L) = \sum_q M(q) |k(q) - d(q)|^2 + \lambda \|P(k) - L\|_F^2$. By Lemma 2, $Q(k; L) \ge J(k)$ for every $L$ of rank at most $r$, and $Q(k_i; L_i) = J(k_i)$, because $L_i$ is the best rank $r$ approximation of $P(k_i)$.

Now minimize $Q(\cdot\,; L_i)$ over $k$. Expand $\|P(k) - L\|_F^2 = \sum_q D(q) |k(q)|^2 - 2 \operatorname{Re} \sum_q \overline{k(q)}\, (P^H L)(q) + \|L\|_F^2$, using $P^H P = \operatorname{diag}(D)$. So $Q$ is a sum of independent terms, one per grid point:

$$M(q) |k(q) - d(q)|^2 + \lambda D(q) |k(q)|^2 - 2 \lambda \operatorname{Re}\big(\overline{k(q)}\, z(q)\big) + \text{const}, \qquad z = P^H L_i.$$

Each term is a convex quadratic in $k(q)$ with the leading coefficient $M(q) + \lambda D(q)$. Where this coefficient is positive, its minimizer is $k(q) = (M(q) d(q) + \lambda z(q)) / (M(q) + \lambda D(q))$, which is line L8. Where it is zero, $M(q) = 0$ and $D(q) = 0$, so the term does not depend on $k(q)$, and line L8 sets $k(q) = 0$, which is a minimizer. So $k_{i+1}$ minimizes $Q(\cdot\,; L_i)$, and

$$J(k_{i+1}) \le Q(k_{i+1}; L_i) \le Q(k_i; L_i) = J(k_i). \qquad \square$$

**Theorem 4 (exact data).** With $\lambda$ = none, line L7 keeps $k(q) = d(q)$ where $M(q) = 1$, and $J(k) = T_r(P(k))$ does not increase.

*Proof.* The same argument applies to the surrogate $\|P(k) - L_i\|_F^2$ over the set of grids with $k(q) = d(q)$ on the samples. On a free point with $D(q) > 0$ the minimizer of $D(q) |k(q)|^2 - 2 \operatorname{Re}(\overline{k(q)} z(q))$ is $z(q) / D(q)$, which is line L7. A free point with $D(q) = 0$ does not enter the surrogate. $\square$

Since $J \ge 0$ and $J$ does not increase, the values $J(k_i)$ converge. The theorems do not say that the limit is the true k-space, or that it is a global minimizer: the rank penalty is not convex. Recovery from a given sampling pattern is a measured property.

## 4. Fixed points

If $M = 1$ everywhere and $\operatorname{rank} P(d) \le r$, then $L_0 = P(d)$, $z = P^H P(d) = D \cdot d$, and line L8 gives $(d + \lambda D d)/(1 + \lambda D) = d$. Line L7 gives $d$ at once. So the true k-space is a fixed point in both modes.
