---
title: CIC assignment computes the linear weights, conserves charge, interpolates linear fields exactly and gives zero total force with an odd kernel
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. The grid points are $x_j = j \Delta x$ with $\Delta x = L / M$, and indices are taken mod $M$. For a particle at $x$, line L3 sets $s = x / \Delta x$, $j = \lfloor s \rfloor$ and $w = s - j$, so $0 \le w < 1$ and $x = (j + w) \Delta x$. Let $W(r) = \max(0, 1 - |r| / \Delta x)$, and let $W_P(x - x_k) = \sum_{n \in \mathbb{Z}} W(x - x_k - nL)$ be its periodic sum.

**Claim 1 (the weights).** A particle at $x$ adds $q (1 - w) / \Delta x$ to $\rho_{j \bmod M}$ and $q w / \Delta x$ to $\rho_{(j+1) \bmod M}$, and for every $k$ the total it adds to $\rho_k$ is $q W_P(x - x_k) / \Delta x$.

*Proof.* The first part is lines L4 and L5. For the second part, look at the grid points of the line, before the reduction mod $M$. The point $j \Delta x$ is at distance $w \Delta x$ from $x$, so $W(x - j \Delta x) = 1 - w$. The point $(j + 1) \Delta x$ is at distance $(1 - w) \Delta x$, so $W = w$. Every other point $m \Delta x$ with $m \le j - 1$ or $m \ge j + 2$ is at distance at least $\Delta x$, so $W = 0$. The grid point $x_k$ and its images $x_k + nL$ are the points $m \Delta x$ with $m \equiv k \pmod M$. So $W_P(x - x_k)$ is the sum of $W$ over these $m$, which is $1 - w$ if $j \equiv k$, plus $w$ if $j + 1 \equiv k$, and 0 otherwise. When $M = 1$ both cases hold for $k = 0$, and both lines L4 and L5 add to $\rho_0$, which again matches. $\square$

**Claim 2 (charge).** $\sum_{k=0}^{M-1} \rho_k \Delta x = \sum_{i=1}^{N} q_i$.

*Proof.* Line L1 sets $\rho = 0$. By Claim 1, particle $i$ adds $q_i (1 - w_i) / \Delta x + q_i w_i / \Delta x = q_i / \Delta x$ to the sum $\sum_k \rho_k$, and nothing else changes $\rho$. After line L6, $\sum_k \rho_k = \sum_i q_i / \Delta x$. $\square$

**Claim 3 (linear fields).** Let $E_k = a + b x_k$ for the points $k$ and $k + 1$ next to a particle with $j = k$, $0 \le k \le M - 2$. Then line L9 returns $a + b x$.

*Proof.* Line L8 computes the same $j$ and $w$ as line L3, with $x = x_j + w \Delta x$. Line L9 returns $(1 - w)(a + b x_j) + w (a + b x_j + b \Delta x) = a + b x_j + b w \Delta x = a + b x$. $\square$

**Claim 4 (zero total force).** Let $E_j = \sum_{k=0}^{M-1} K_{j - k} \rho_k$ with indices mod $M$, and assume that $K_{-m} = -K_m$ for every $m$ (an odd kernel). Then $\sum_i q_i E(x_i) = 0$, where $E(x_i)$ is the output of line L9. For $N = 1$ this says that the self-force $q_1 E(x_1)$ is zero.

*Proof.* By Claim 1 applied to line L9 (lines L8 and L9 use the same shares as lines L3 to L5), $E(x_i) = \sum_k W_P(x_i - x_k) E_k$. Then
$$\sum_i q_i E(x_i) = \sum_k E_k \sum_i q_i W_P(x_i - x_k) = \Delta x \sum_k \rho_k E_k = \Delta x \sum_k \sum_l \rho_k K_{k - l} \rho_l.$$
Call the double sum $S$. Exchange the names $k$ and $l$: $S = \sum_l \sum_k \rho_l K_{l - k} \rho_k = -\sum_k \sum_l \rho_k K_{k - l} \rho_l = -S$, by the oddness of $K$. So $S = 0$. $\square$

**The field of the example is odd.** The field of the page example satisfies $E_{j+1/2} - E_{j-1/2} = \Delta x (\rho_j - \bar\rho)$, $\sum_j E_{j+1/2} = 0$ and $E_j = (E_{j-1/2} + E_{j+1/2}) / 2$. Let $\phi$ be the mean-free solution of $(\phi_{j+1} - 2 \phi_j + \phi_{j-1}) / \Delta x^2 = -(\rho_j - \bar\rho)$, which is unique because the periodic 3-point Laplacian has the constants as its kernel and $\rho - \bar\rho$ has mean zero. Then $E_{j+1/2} = -(\phi_{j+1} - \phi_j) / \Delta x$ satisfies both conditions on the half point values, and these conditions fix them (the running sum fixes them up to one constant, and the zero mean fixes the constant). So $E_j = -(\phi_{j+1} - \phi_{j-1}) / (2 \Delta x)$. The map $\rho \mapsto \phi$ is a convolution with a kernel $G$ that is even, because the Laplacian stencil is symmetric under $j \mapsto -j$. The centred difference is a convolution with an odd stencil. A convolution of an even kernel with an odd stencil is odd, so $E = K * (\rho - \bar\rho)$ with an odd $K$. An odd $K$ has $\sum_m K_m = 0$, so $K * \bar\rho = 0$ and $E = K * \rho$. So Claim 4 applies. $\blacksquare$
