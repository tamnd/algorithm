---
title: The accumulated transition matrix is the sum of the walk over all times, and diffusion pseudotime has an exact eigen formula
proves: [correctness]
status: full
---

We prove what the steps compute. Lines L1 to L4 give a symmetric matrix $T_s$ that is similar to a random walk on the cells, with top eigenvector $\psi_0$ (Lemma 1). The eigenvalue 1 is simple and all other eigenvalues lie strictly between $-1$ and 1 (Lemma 2). So the matrix of line L5 exists and is the sum of the walk over all times $t \ge 1$ with its limit removed (Theorem 3), and the pseudotime has an exact formula in the eigenvectors (Theorem 4). The elimination of the code needs no pivoting (Lemma 5). That the pseudotime follows the order of a real process is a heuristic, and the tests measure it.

**Setting.** Cells $x_1, \dots, x_n \in \mathbb{R}^d$ with $n \ge 3$ and a width $\sigma > 0$. Line L1 sets $K_{ij} = e^{-\|x_i - x_j\|^2/(2\sigma^2)}$ for $i \ne j$ and $K_{ii} = 0$. Line L2 sets $q_i = \sum_jK_{ij}$ and $\tilde K_{ij} = K_{ij}/(q_iq_j)$. Line L3 sets $z_i = \sum_j\tilde K_{ij}$, $Z = \mathrm{diag}(z)$ and $T_s = Z^{-1/2}\tilde KZ^{-1/2}$. Line L4 sets $\psi_0 = \sqrt z/\|\sqrt z\|$ and $\Pi = \psi_0\psi_0^\top$. Line L5 sets $M = (I - T_s + \Pi)^{-1} - I$, and line L6 returns $\tau_i = \|M_{r\cdot} - M_{i\cdot}\|$ for the root $r$. We assume every $q_i > 0$; the code raises an error otherwise.

**Lemma 1 (the walk).** $T = Z^{-1}\tilde K$ has nonnegative entries and rows that sum to 1, so it is the transition matrix of a random walk on the cells. $T_s = Z^{1/2}TZ^{-1/2}$ is symmetric, has the same eigenvalues as $T$, and $T_s\psi_0 = \psi_0$.

*Proof.* $\tilde K$ is symmetric with nonnegative entries, and row $i$ of $Z^{-1}\tilde K$ sums to $z_i/z_i = 1$. $Z^{1/2}TZ^{-1/2} = Z^{-1/2}\tilde KZ^{-1/2}$, which is symmetric because $\tilde K$ is, and similar matrices have the same eigenvalues. Finally $T_s\sqrt z = Z^{-1/2}\tilde K\mathbf 1 = Z^{-1/2}z = \sqrt z$. $\square$

**Lemma 2 (the spectrum).** Let $1 = \lambda_0 \ge \lambda_1 \ge \dots \ge \lambda_{n-1}$ be the eigenvalues of $T_s$ with orthonormal eigenvectors $\psi_0, \dots, \psi_{n-1}$. Then $-1 < \lambda_l < 1$ for every $l \ge 1$.

*Proof.* Let $Tu = \lambda u$ with $u \ne 0$ real, and let $i$ be an index with $|u_i|$ largest. Then $|\lambda||u_i| = |\sum_jT_{ij}u_j| \le \sum_jT_{ij}|u_j| \le |u_i|$, so $|\lambda| \le 1$. Every $T_{ij}$ with $j \ne i$ is positive, because $K_{ij} > 0$. If $\lambda = 1$, equality holds in both steps, so $u_j = u_i$ for every $j \ne i$ and $u$ is constant: the eigenspace of 1 for $T$ has dimension 1, and so has that of $T_s$, which is $Z^{1/2}$ times it. Because $T_s$ is symmetric, the eigenvalue 1 is then simple. If $\lambda = -1$, equality gives $u_j = -u_i$ for every $j \ne i$. Then every $|u_j|$ is the largest, and the same argument at an index $j \ne i$ gives $u_l = -u_j = u_i$ for every $l \ne j$. Since $n \ge 3$ there is an $l$ different from $i$ and $j$, with $u_l = -u_i$ and $u_l = u_i$, so $u_i = 0$ and $u = 0$, a contradiction. $\square$

**Theorem 3 (accumulated matrix).** $A = I - T_s + \Pi$ is symmetric positive definite, with eigenvalue 1 on $\psi_0$ and $1 - \lambda_l > 0$ on $\psi_l$ for $l \ge 1$. Its inverse exists and
$$M = A^{-1} - I = \sum_{l \ge 1}\frac{\lambda_l}{1 - \lambda_l}\psi_l\psi_l^\top = \sum_{t \ge 1}\left(T_s^t - \Pi\right).$$

*Proof.* Write $T_s = \sum_l\lambda_l\psi_l\psi_l^\top$ and $I = \sum_l\psi_l\psi_l^\top$. Then $A = \psi_0\psi_0^\top + \sum_{l \ge 1}(1 - \lambda_l)\psi_l\psi_l^\top$, whose eigenvalues are positive by Lemma 2. So $A^{-1} - I = \sum_{l \ge 1}\left(\frac{1}{1 - \lambda_l} - 1\right)\psi_l\psi_l^\top$, which is the middle expression. Also $T_s^t - \Pi = \sum_{l \ge 1}\lambda_l^t\psi_l\psi_l^\top$, and since $|\lambda_l| < 1$, $\sum_{t \ge 1}\lambda_l^t = \lambda_l/(1 - \lambda_l)$, a convergent geometric series. $\square$

So $M$ adds up the walk of $t$ steps for all $t \ge 1$, each with the stationary part $\Pi$ removed. There is no time parameter left to choose.

**Theorem 4 (eigen formula).** For all cells $x$ and $y$,
$$\tau(x, y)^2 = \|M_{x\cdot} - M_{y\cdot}\|^2 = \sum_{l \ge 1}\left(\frac{\lambda_l}{1 - \lambda_l}\right)^2\big(\psi_l(x) - \psi_l(y)\big)^2.$$
So $\tau$ is a pseudometric on the cells: it is symmetric, it is 0 from a cell to itself, and it obeys the triangle inequality.

*Proof.* By Theorem 3, row $x$ of $M$ is $\sum_{l \ge 1}\frac{\lambda_l}{1 - \lambda_l}\psi_l(x)\psi_l^\top$. The difference of two rows is $\sum_{l \ge 1}\frac{\lambda_l}{1 - \lambda_l}(\psi_l(x) - \psi_l(y))\psi_l^\top$, and its squared norm is the sum of the squared coefficients because the $\psi_l$ are orthonormal. A Euclidean distance between rows of a matrix is a pseudometric. $\square$

This is the difference from a [diffusion map](/diffusion-maps/). A diffusion map at a time $t$ gives cell $x$ the coordinates $\lambda_l^t\psi_l(x)$ for a few $l$, and its distance depends on $t$. Diffusion pseudotime uses the weights $\sum_{t \ge 1}\lambda_l^t = \lambda_l/(1 - \lambda_l)$ for all $l$, so it adds the steps of all lengths. The weight grows without bound as $\lambda_l \to 1$, so the slowest directions of the walk, which run along the trajectory, count most.

**Lemma 5 (elimination).** Gauss-Jordan elimination on a symmetric positive definite matrix without row exchanges meets only positive pivots, so it computes the inverse.

*Proof.* The first pivot is $A_{11} = e_1^\top Ae_1 > 0$. After one step, the remaining block is the Schur complement $A_{22} - A_{21}A_{11}^{-1}A_{12}$, which is symmetric positive definite: for $v \ne 0$ put $w = (-A_{11}^{-1}A_{12}v, v)$, then $v^\top(A_{22} - A_{21}A_{11}^{-1}A_{12})v = w^\top Aw > 0$. By induction every pivot is positive. $\square$

**Invariance.** $K$ depends only on the distances between cells, so moving, rotating or renumbering the cells changes $\tau$ only by the same renumbering.

**What the lines compute.** Line L1 is the kernel. Line L2 is the density normalization of Coifman and Lafon (2006) with $\alpha = 1$: in their analysis, as the cells become dense on a smooth curve or surface, the walk then no longer depends on how densely the cells are sampled. Line L3 is Lemma 1, line L4 the top eigenvector of Lemma 1, line L5 Theorem 3 by the elimination of Lemma 5, and line L6 Theorem 4 from the root.

**Complexity.** The kernel takes $O(n^2d)$ time. The normalizations take $O(n^2)$. The elimination of line L5 takes $O(n^3)$ time. Line L6 takes $O(n^2)$. The space is $O(n^2)$ for the dense matrices.

**What the tests check.** The test file checks the page example, Lemma 1 and Lemma 2 on random cells, the matrix $M$ against the partial sums of the series of Theorem 3, the eigen formula of Theorem 4 against the eigenvectors from the Jacobi method, the pseudometric and the invariance, and the elimination of Lemma 5 against a general inverse. Two simulations are measurements, not theorems: the rank correlation of the pseudotime with the true time for noisy cells near a line, and for cells on an arc whose two ends are close in space.
