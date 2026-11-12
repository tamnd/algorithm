---
title: The Euclidean distance between diffusion coordinates equals the diffusion distance
proves: [correctness]
status: full
---

Let $K$ be the kernel after the $\alpha$ normalization of line L2. It is symmetric with nonnegative entries, because dividing $K_{ij}$ by $q_i^\alpha q_j^\alpha$ keeps the symmetry. Assume its graph is connected and every $d_i = \sum_jK_{ij}$ is positive. Let $D = \operatorname{diag}(d)$, $P = D^{-1}K$, $\pi_i = d_i/\sum_jd_j$ and $S = D^{-1/2}KD^{-1/2}$.

**Lemma 1 (the walk).** The rows of $P$ sum to 1, $\pi_iP_{ij} = \pi_jP_{ji}$, and $\pi^\top P = \pi^\top$.

*Proof.* $\sum_jP_{ij} = d_i/d_i = 1$. With $V = \sum_jd_j$, $\pi_iP_{ij} = K_{ij}/V$, which is symmetric in $i$ and $j$. Summing the detailed balance over $i$ gives $\sum_i\pi_iP_{ij} = \pi_j\sum_iP_{ji} = \pi_j$. $\square$

**Lemma 2 (the eigenvectors).** Let $S = \sum_{l=0}^{n-1}\lambda_lv_lv_l^\top$ with orthonormal $v_l$. Put $\psi_l(i) = v_l(i)/\sqrt{\pi_i}$ and $\varphi_l(i) = v_l(i)\sqrt{\pi_i}$. Then $P\psi_l = \lambda_l\psi_l$, $\sum_i\pi_i\psi_l(i)\psi_k(i) = [l = k]$, and

$$P^t_{xz} = \sum_{l=0}^{n-1}\lambda_l^t\,\psi_l(x)\varphi_l(z) \quad \text{for } t = 0, 1, 2, \dots$$

The largest eigenvalue is $\lambda_0 = 1$, with $v_0 = \sqrt\pi$ and $\psi_0 = \mathbf{1}$, and all eigenvalues satisfy $|\lambda_l| \le 1$.

*Proof.* $P = D^{-1/2}SD^{1/2}$, and $D^{1/2} = \sqrt V\operatorname{diag}(\sqrt\pi)$, so $P = \operatorname{diag}(\sqrt\pi)^{-1}S\operatorname{diag}(\sqrt\pi)$, and $P^t = \operatorname{diag}(\sqrt\pi)^{-1}S^t\operatorname{diag}(\sqrt\pi)$. Insert $S^t = \sum_l\lambda_l^tv_lv_l^\top$: entry $(x, z)$ is $\sum_l\lambda_l^t\frac{v_l(x)}{\sqrt{\pi_x}}v_l(z)\sqrt{\pi_z}$. Applying $P$ to $\psi_l = \operatorname{diag}(\sqrt\pi)^{-1}v_l$ gives $\operatorname{diag}(\sqrt\pi)^{-1}Sv_l = \lambda_l\psi_l$. The orthonormality is $v_l^\top v_k = [l = k]$. The vector $\sqrt\pi$ satisfies $S\sqrt\pi = \frac{1}{\sqrt V}D^{-1/2}K\mathbf{1} = \frac{1}{\sqrt V}D^{1/2}\mathbf{1} = \sqrt\pi$, so 1 is an eigenvalue with $\psi_0 = \mathbf{1}$. $P$ is a stochastic matrix, so each eigenvalue has $|\lambda| \le \max_i\sum_j|P_{ij}| = 1$. Since the graph is connected, the eigenvalue 1 of $P$ is simple by the Perron-Frobenius theorem; no other eigenvalue equals 1, and it is the largest. $\square$

**Theorem 1 (the distance identity).** For all vertices $x, y$ and $t \ge 0$,

$$D_t(x, y)^2 = \sum_z\frac{\big(P^t_{xz} - P^t_{yz}\big)^2}{\pi_z} = \sum_{l=1}^{n-1}\lambda_l^{2t}\big(\psi_l(x) - \psi_l(y)\big)^2 .$$

So with all $n - 1$ coordinates, $D_t(x, y) = \|\Psi_t(x) - \Psi_t(y)\|$.

*Proof.* Put $c_l = \lambda_l^t(\psi_l(x) - \psi_l(y))$. By Lemma 2, $P^t_{xz} - P^t_{yz} = \sum_lc_l\varphi_l(z) = \sqrt{\pi_z}\sum_lc_lv_l(z)$. Then

$$\sum_z\frac{(P^t_{xz} - P^t_{yz})^2}{\pi_z} = \sum_z\Big(\sum_lc_lv_l(z)\Big)^2 = \Big\|\sum_lc_lv_l\Big\|^2 = \sum_lc_l^2,$$

by the orthonormality of the $v_l$. Finally $c_0 = 0$ because $\psi_0$ is constant. $\square$

**Corollary (truncation).** Order $\lambda_1, \dots, \lambda_{n-1}$ by decreasing $|\lambda_l|$ and keep the first $m$. Then

$$0 \le D_t(x, y)^2 - \|\Psi_t(x) - \Psi_t(y)\|^2 \le |\lambda_{m+1}|^{2t}\Big(\frac{1}{\pi_x} + \frac{1}{\pi_y}\Big).$$

*Proof.* The difference is $\sum_{l > m}\lambda_l^{2t}(\psi_l(x) - \psi_l(y))^2 \le |\lambda_{m+1}|^{2t}\sum_{l \ge 0}(\psi_l(x) - \psi_l(y))^2$. By Theorem 1 with $t = 0$, where $P^0 = I$, the last sum is $D_0(x, y)^2 = \sum_z(\delta_{xz} - \delta_{yz})^2/\pi_z$, which is $1/\pi_x + 1/\pi_y$ for $x \ne y$ and 0 for $x = y$. $\square$

The example on the page checks Theorem 1 by hand on a three-vertex path, and the test suite checks it with $P^t$ computed in exact rational arithmetic.
