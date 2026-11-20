---
title: The particle-mesh method solves the discrete Poisson equation exactly, gives forces that sum to zero, and its leapfrog conserves momentum and is time reversible
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. Grid indices $(i, j)$ are taken mod $(n_x, n_y)$. Write $D$ for the periodic 5-point Laplacian, $(D\phi)_{i,j} = (\phi_{i+1,j} - 2\phi_{i,j} + \phi_{i-1,j}) / \Delta x^2 + (\phi_{i,j+1} - 2\phi_{i,j} + \phi_{i,j-1}) / \Delta y^2$, and $e_k(i, j) = \exp(2\pi \mathrm{i} (k_x i / n_x + k_y j / n_y))$ for the Fourier mode $k = (k_x, k_y)$.

**Claim 1 (the Poisson solve).** Lines L2 to L4 return the unique grid function $\phi$ with $\sum_{i,j} \phi_{i,j} = 0$ and $D\phi = s (\rho - \bar\rho)$.

*Proof.* A direct computation gives $D e_k = \lambda(k) e_k$ with $\lambda(k) = (2\cos(2\pi k_x / n_x) - 2) / \Delta x^2 + (2\cos(2\pi k_y / n_y) - 2) / \Delta y^2$, which equals the formula on the page because $2 - 2\cos\theta = 4 \sin^2(\theta/2)$. Each term is at most 0, and the sum is 0 only if $k_x \equiv 0$ and $k_y \equiv 0$. The $M$ modes form a basis of the grid functions, and line L2 computes the coefficients of $\rho$ in this basis (up to the factor $1/M$ that the inverse in L4 restores). The mode $(0, 0)$ is the constant function, and its coefficient is $M \bar\rho$. Line L3 sets the coefficient of $\phi$ to $s \hat\rho(k) / \lambda(k)$ for $k \ne 0$ and to 0 for $k = 0$. Then $D\phi$ has the coefficients $s \hat\rho(k)$ for $k \ne 0$ and 0 for $k = 0$, which are the coefficients of $s (\rho - \bar\rho)$; and $\phi$ has zero mean. For uniqueness, if $D\psi = 0$ then every coefficient of $\psi$ with $k \ne 0$ is 0, so $\psi$ is constant, and a constant with zero mean is 0. $\square$

**Claim 2 (zero total force).** The forces of line L7 satisfy $\sum_p \mathbf{F}_p = 0$. For $N = 1$ the force is zero.

*Proof.* By Claim 1, $\phi = G * (\rho - \bar\rho)$ for the grid function $G$ with coefficients $s / \lambda(k)$ for $k \ne 0$ and 0 for $k = 0$ (the star is the periodic convolution). Since $\lambda(-k) = \lambda(k)$ and $\lambda$ is real, $G$ is real and even: $G_{-i,-j} = G_{i,j}$. Line L5 is the convolution with the stencil $c_x$ that has $c_x(1, 0) = -1/(2\Delta x)$, $c_x(-1, 0) = 1/(2\Delta x)$ and 0 elsewhere, which is odd. So $g_x = K * (\rho - \bar\rho)$ with $K = c_x * G$, and $K_{-i,-j} = -K_{i,j}$. An odd kernel sums to 0, so $K * \bar\rho = 0$ and $g_x = K * \rho$. The same holds for $g_y$.

Let $W_{p,a}$ be the CIC weight of particle $p$ on grid point $a$, summed over the periodic images. Line L1 gives $\rho_a = \sum_p w_p W_{p,a} / (\Delta x \Delta y)$, and line L6 gives $g_x(\mathbf{x}_p) = \sum_a W_{p,a} g_{x,a}$ with the same $W$ (the cloud-in-cell page proves both forms). So
$$\sum_p w_p \, g_x(\mathbf{x}_p) = \sum_a g_{x,a} \sum_p w_p W_{p,a} = \Delta x \Delta y \sum_a \rho_a g_{x,a} = \Delta x \Delta y \sum_a \sum_b \rho_a K_{a-b} \rho_b.$$
Exchanging the names $a$ and $b$ and using $K_{b-a} = -K_{a-b}$ shows that the double sum equals its own negative, so it is 0. The same holds for the $y$ component. For $N = 1$ the sum is the force on the single particle. $\square$

**Claim 3 (momentum).** Each pass through lines L10 to L13 leaves $\mathbf{P} = \sum_p m_p \mathbf{v}_p$ unchanged.

*Proof.* Line L10 adds $(h/2) \sum_p \mathbf{F}_p$ to $\mathbf{P}$, which is 0 by Claim 2 for the forces of line L8 or of the last L12. Line L11 does not change any velocity. Line L13 adds $(h/2) \sum_p \mathbf{F}_p = 0$ for the new forces. $\square$

**Claim 4 (time reversibility).** Let one pass of lines L10 to L13 map $(x, v)$ with forces $F(x)$ to $(x', v')$. Then the same pass maps $(x', -v')$ to $(x, -v)$.

*Proof.* The forces depend only on the positions (Claim 1 and lines L1, L5 to L7). Write $u = v + (h/2) F(x)/m$ for the velocity after line L10, so $x' = x + h u$ and $v' = u + (h/2) F(x')/m$. Start the pass at $(x', -v')$. Line L10 gives $-v' + (h/2) F(x')/m = -u$. Line L11 gives $x' - h u = x$, mod the box. Line L12 computes $F(x)$, and line L13 gives $-u + (h/2) F(x)/m = -v$. The wrap mod the box does not matter, because the forces are periodic functions of the positions. $\blacksquare$
