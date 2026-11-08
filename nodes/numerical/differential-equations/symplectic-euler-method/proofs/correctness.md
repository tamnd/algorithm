---
title: Symplectic Euler is a symplectic method of order 1, and its adjoint composition is Störmer-Verlet
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $H(p, q) = T(p) + V(q)$ with $p, q \in \mathbb{R}^k$, $T, V \in C^2$ and $\nabla T$, $\nabla V$ Lipschitz with constant $L$. The system is $p' = -\nabla V(q)$, $q' = \nabla T(p)$; with $y = (q, p) \in \mathbb{R}^{2k}$ it has the form $y' = f(y)$. We use the Euclidean norm. One step of variant A (lines L4 and L5) is $\Phi_h = D_h \circ K_h$ with the kick $K_h(q, p) = (q, p - h\nabla V(q))$ and the drift $D_h(q, p) = (q + h\nabla T(p), p)$. Variant B is $\Phi_h^* = K_h \circ D_h$.

**Termination.** Line L1 gives a finite $N \ge 0$ and the loop runs $N$ times with one evaluation of $\nabla V$ and one of $\nabla T$ per pass. The last step ends exactly at $T$, and $T = t_0$ gives zero steps.

**Lemma 1 (symplectic).** $\Phi_h$ and $\Phi_h^*$ are symplectic: $J^T \Omega J = \Omega$ for their Jacobians $J$, with $\Omega = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$ in the variables $(q, p)$.

*Proof.* The Jacobian of $K_h$ is $\begin{pmatrix} I & 0 \\ -hS & I \end{pmatrix}$ with $S = \nabla^2 V(q)$, and that of $D_h$ is $\begin{pmatrix} I & hU \\ 0 & I \end{pmatrix}$ with $U = \nabla^2 T(p)$. Both $S$ and $U$ are symmetric. For $J = \begin{pmatrix} I & 0 \\ B & I \end{pmatrix}$, $J^T \Omega J = \begin{pmatrix} B - B^T & I \\ -I & 0 \end{pmatrix}$, which equals $\Omega$ when $B$ is symmetric; the upper triangular case is the same computation. By the chain rule, the Jacobian of a composition is the product of Jacobians at the intermediate points, and products of symplectic matrices are symplectic. $\square$

For a general, non-separable $H$, the implicit variant $p_{n+1} = p_n - hH_q(p_{n+1}, q_n)$, $q_{n+1} = q_n + hH_p(p_{n+1}, q_n)$ is also symplectic (Hairer, Lubich and Wanner 2006, Theorem VI.3.3); we cite this and check it numerically.

**Lemma 2 (adjoint and Störmer-Verlet).** $\Phi_{-h}^* = \Phi_h^{-1}$, and $\Phi_{h/2}^* \circ \Phi_{h/2}$ is one step of the Störmer-Verlet method with step $h$.

*Proof.* $K_h^{-1} = K_{-h}$ and $D_h^{-1} = D_{-h}$, so $\Phi_h^{-1} = K_{-h} \circ D_{-h} = \Phi_{-h}^*$. For the second claim, $\Phi_{h/2}^* \circ \Phi_{h/2} = K_{h/2} \circ D_{h/2} \circ D_{h/2} \circ K_{h/2} = K_{h/2} \circ D_h \circ K_{h/2}$, because two drifts compose to one ($p$ does not change during a drift). This is kick, drift, kick, the [Verlet](/verlet-integration/) step. $\square$

**Lemma 3 (local error).** $\Phi_h(y) - \varphi_h(y) = O(h^2)$ uniformly on bounded sets, where $\varphi_h$ is the exact flow, and the $h^2$ term is in general not zero.

*Proof.* $p_1 = p - h\nabla V(q)$ and $q_1 = q + h\nabla T(p_1) = q + h\nabla T(p) + O(h^2)$. The exact flow gives $p(h) = p - h\nabla V(q) + O(h^2)$ and $q(h) = q + h\nabla T(p) + O(h^2)$. For the harmonic oscillator below, the $h^2$ terms differ: the method gives $q_1 = q + hp - h^2 q$ and the flow gives $q + hp - \frac{h^2}{2}q + O(h^3)$. $\square$

**Theorem (convergence, proved).** On $[t_0, T]$, $\|y(t_n) - y_n\| \le C h$ with $C$ depending on $T - t_0$, $L$ and the bound of Lemma 3.

*Proof.* $K_h$ and $D_h$ are Lipschitz with constant $1 + hL$, so $\Phi_h$ is Lipschitz with constant $(1 + hL)^2 \le 1 + \Lambda h$ with $\Lambda = L(2 + h_0 L)$ for $h \le h_0$. The recursion $\|e_{n+1}\| \le (1 + \Lambda h)\|e_n\| + c h^2$ gives $\|e_n\| \le c h (T - t_0) e^{\Lambda(T - t_0)}$, as for the [Euler method](/euler-method/). $\square$

**Harmonic oscillator.** For $H = (p^2 + q^2)/2$, variant A is $p_1 = p - hq$, $q_1 = q + hp_1$, the matrix $M = \begin{pmatrix} 1 - h^2 & h \\ -h & 1 \end{pmatrix}$ on $(q, p)$, with $\det M = 1$ and $\operatorname{tr} M = 2 - h^2$. The quantity $\tilde H = q^2 + p^2 - hqp$ is conserved exactly. Indeed $q_1^2 - hq_1p_1 = q_1(q_1 - hp_1) = q_1 q$, so $q_1^2 + p_1^2 - hq_1p_1 = qq_1 + p_1^2 = q^2 + p_1(hq + p_1) = q^2 + p_1 p = q^2 + p^2 - hqp$. For $0 < h < 2$ the form $\tilde H$ is positive definite, so the iterates lie on a fixed ellipse and stay bounded. For $h > 2$, $|\operatorname{tr} M| > 2$ gives a real eigenvalue of modulus greater than 1, and the iterates grow exponentially.

**Long times (cited, asymptotic).** For analytic $H$, backward error analysis gives a modified Hamiltonian $\tilde H = H - \frac{h}{2} H_p^T H_q + O(h^2)$ that the method conserves up to exponentially small errors, so $|H(y_n) - H(y_0)| = O(h)$ over times exponentially long in $1/h$ (Hairer, Lubich and Wanner 2006, Sections IX.3 and IX.8). For the oscillator, $\tilde H / 2$ above is exactly this series.
