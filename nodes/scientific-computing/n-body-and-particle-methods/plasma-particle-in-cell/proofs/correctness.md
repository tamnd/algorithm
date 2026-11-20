---
title: The electrostatic PIC loop keeps the grid neutral, solves the discrete Poisson equation and conserves the total momentum
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. The grid has $M$ points, $\Delta x = L / M$, indices are taken mod $M$, and there are $N$ electrons with charge $q_p = -L/N$, mass $m_p = L/N$ and $q/m = -1$. We use two results proved on the [cloud-in-cell assignment](/cloud-in-cell-assignment/) page: (A) the CIC weights $W_{p,j}$ of one particle add to 1, and the deposit is $\rho_j = \sum_p q_p W_{p,j} / \Delta x$ while the interpolation is $E_p = \sum_j W_{p,j} E_j$ with the same $W$; (B) if $E = K * \rho$ with an odd kernel, $K_{-m} = -K_m$, then $\sum_p q_p E_p = 0$.

**Claim 1 (neutral grid).** After lines L1 and L8, $\sum_j \rho_j \Delta x = 0$.

*Proof.* The background adds $1$ to each of the $M$ points, so $M \Delta x = L$ in total. By (A) the electrons add $\sum_p q_p = N \cdot (-L/N) = -L$. $\square$

**Claim 2 (the field solve).** Lines L2 and L9 return $E_j = -(\phi_{j+1} - \phi_{j-1}) / (2\Delta x)$, where $\phi$ is the unique mean-free solution of $-(\phi_{j+1} - 2\phi_j + \phi_{j-1}) / \Delta x^2 = \rho_j - \bar\rho$.

*Proof.* The routine forms $H_j = \sum_{i \le j} \Delta x (\rho_i - \bar\rho)$ for $j = 0, \ldots, M - 1$, subtracts the mean $c$ of the $H_j$, and sets $E_j = (H_j - c + H_{j-1} - c)/2$, where $H_{-1}$ means $H_{M-1}$. Since $\sum_i (\rho_i - \bar\rho) = 0$, $H_{M-1} = 0$, so the index $-1$ is consistent with the periodic extension $H_{-1} = H_{M-1} = H_{-1+M}$ and $H_j - H_{j-1} = \Delta x(\rho_j - \bar\rho)$ holds for every $j$ mod $M$. Let $\phi$ be the mean-free solution of the 3-point equation; it exists and is unique because the periodic 3-point Laplacian has the constants as its kernel and its range is the grid functions of zero mean. Set $G_j = -(\phi_{j+1} - \phi_j)/\Delta x$, the field at the half point $j + 1/2$. Then $G_j - G_{j-1} = -(\phi_{j+1} - 2\phi_j + \phi_{j-1})/\Delta x = \Delta x(\rho_j - \bar\rho)$, and $\sum_j G_j = 0$ because the sum telescopes round the ring. So $G$ and $H - c$ have the same differences and both have mean zero, hence $G = H - c$. Then $E_j = (G_j + G_{j-1})/2 = -(\phi_{j+1} - \phi_{j-1})/(2\Delta x)$. $\square$

**Claim 3 (the kernel is odd).** $E = K * \rho$ for an odd kernel $K$.

*Proof.* By Claim 2, $\phi = G' * (\rho - \bar\rho)$, where $G'$ is the Green's function of the periodic 3-point Laplacian on mean-free functions. The stencil $(1, -2, 1)$ is symmetric under $j \mapsto -j$, and the solution is unique, so $G'$ is even. The centred difference is a convolution with the odd stencil $c_1 = -1/(2\Delta x)$, $c_{-1} = 1/(2\Delta x)$. So $E = K * (\rho - \bar\rho)$ with $K = c * G'$ odd. An odd kernel sums to zero, so $K * \bar\rho = 0$ and $E = K * \rho$. $\square$

**Claim 4 (momentum).** Lines L4 and L6 leave $P = \sum_p m_p v_p$ unchanged, and line L7 does not change any velocity. So $P$ after line L12 equals $P$ at the start.

*Proof.* Line L4 changes $P$ by $-(h/2) \sum_p m_p (q/m) E_p = -(h/2) \sum_p q_p E_p$, since $m_p (q/m) = q_p$. Line L6 changes it by $h \sum_p q_p E_p$. In both cases $E_p$ comes from a deposit and an interpolation with the same weights (lines L1 and L3, or L8 and L10) and from a field $E = K * \rho$ with an odd $K$ (Claim 3). By (B), $\sum_p q_p E_p = 0$. The background is a constant, which the field solve removes with the mean, so it does not change $E$. $\blacksquare$
