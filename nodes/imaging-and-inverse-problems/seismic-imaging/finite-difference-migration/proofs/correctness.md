---
title: Correctness of finite-difference migration
proves: [correctness, termination]
status: full
---

**Setting.** The model is the exploding reflector model with $v' = v/2$. For one frequency $\omega > 0$ the one-way equation of the method is the 15-degree equation
$$\frac{\partial P}{\partial z} = i\,\frac{\omega}{v'}\,P + i\,\frac{v'}{2\omega}\,\frac{\partial^2 P}{\partial x^2}.$$
For a plane wave $e^{i k_x x}$ in constant $v'$ it gives $k_z^{15} = \omega/v' - v' k_x^2/(2\omega)$, while the exact one-way equation gives $k_z = (\omega/v')\sqrt{1 - a^2}$ with $a = v' k_x/\omega = \sin\theta$, the sine of the propagation angle. The grid has $n_x$ points, $T = \operatorname{tridiag}(1, -2, 1)$ with $P = 0$ outside the grid, and $B = \operatorname{diag}(b_j)$ with $b_j = v'_j \Delta z/(2\omega\Delta x^2) > 0$ (line L6).

**Lemma 1 (the 15-degree relation).** $k_z^{15}$ is the Taylor polynomial of degree 2 in $a$ of $k_z$, and $k_z \le k_z^{15}$ for all $|a| \le 1$. The relative error $\big((1 - a^2/2) - \sqrt{1 - a^2}\big)/\sqrt{1 - a^2}$ is $6.0 \times 10^{-4}$ at $\theta = 15°$ and $0.061$ at $\theta = 45°$.

*Proof.* $\sqrt{1 - a^2} = 1 - a^2/2 - a^4/8 - \cdots$. Also $(1 - a^2/2)^2 = 1 - a^2 + a^4/4 \ge 1 - a^2$, and $1 - a^2/2 > 0$, so $1 - a^2/2 \ge \sqrt{1 - a^2}$. The numbers: $\cos 15° = 0.965926$ against $1 - \sin^2 15°/2 = 0.966506$; $\cos 45° = 0.707107$ against $0.75$. $\square$

**Lemma 2 (the Thomas algorithm succeeds).** For every $b \in (0, \infty)^{n_x}$ the matrix $I - \frac{i}{2}BT$ of line L7 has row $j$ with the diagonal $1 + i b_j$ and the off-diagonal entries $-\frac{i}{2}b_j$. The elimination in `thomas_solve` never divides by zero, and it returns the exact solution in exact arithmetic.

*Proof.* Row $j$ is strictly diagonally dominant: $|1 + i b_j| = \sqrt{1 + b_j^2} > b_j \ge |\ell_j| + |u_j|$, where $\ell_j, u_j$ are the off-diagonal entries ($|\ell_j|, |u_j| \le b_j/2$). We show by induction that the pivots $m_j$ satisfy $|m_j| > |u_j|$, so $m_j \ne 0$ and $|c_j| = |u_j/m_j| < 1$. For $j = 0$, $m_0 = 1 + i b_0$ and $|m_0| > |u_0|$. For $j \ge 1$, $|m_j| = |1 + i b_j - \ell_j c_{j-1}| \ge |1 + i b_j| - |\ell_j| > |u_j|$, by $|c_{j-1}| < 1$ and the dominance. The forward pass is the factorization of the matrix into a lower bidiagonal factor with the pivots $m_j$ and a unit upper bidiagonal factor with the entries $c_j$; the forward and backward passes solve the two triangular systems. $\square$

**Lemma 3 (the diffraction step is unitary in a weighted norm).** Let $C = (I - \frac{i}{2}BT)^{-1}(I + \frac{i}{2}BT)$, the map of line L7. Then $C$ keeps the norm $\|p\|_B^2 = \sum_j |p_j|^2/b_j$. If all $b_j = b$, $C$ multiplies the sine mode $\psi_m[j] = \sin(m\pi(j+1)/(n_x+1))$ by $e^{2i\arctan(b\lambda_m/2)}$, with $\lambda_m = -4\sin^2\big(m\pi/(2(n_x+1))\big)$, and keeps the plain norm.

*Proof.* $BT$ is self-adjoint in the inner product $\langle p, q\rangle_B = \sum_j \bar{p}_j q_j/b_j$, because $B^{-1}(BT) = T$ is real symmetric. So $BT = V\Lambda V^{-1}$ with real $\Lambda$ and $V$ unitary for $\langle\cdot,\cdot\rangle_B$, and $C = V\,\operatorname{diag}\big((1 + i\lambda/2)/(1 - i\lambda/2)\big)V^{-1}$. Each factor has modulus 1. For constant $b$, $T\psi_m = \lambda_m \psi_m$ (the Dirichlet eigenvectors of $T$), and $(1 + i y)/(1 - i y) = e^{2i\arctan y}$ with $y = b\lambda_m/2$. $\square$

**Theorem 1 (what the code computes).** Let $L_{\omega, i}$ be the thin lens of line L5 (entry $j$ times $e^{i\omega\Delta z/v'_{i,j}}$) and $C_{\omega, i}$ the step of line L7 for layer $i$. With $p_k^{(0)}$ the DFT of the traces at index $k$ (line L1) and $p_k^{(i)} = C_{\omega_k, i-1}L_{\omega_k, i-1}\cdots C_{\omega_k, 0}L_{\omega_k, 0}\, p_k^{(0)}$, line L8 returns
$$m[i][j] = \frac{2}{n_t}\operatorname{Re}\sum_{0 < k < n_t/2} p_k^{(i)}[j].$$
The algorithm stops after $n_z \lfloor (n_t - 1)/2\rfloor$ tridiagonal solves.

*Proof.* As in Theorem 1 of the proof of split-step Fourier migration: line L2 visits $0 < k < n_t/2$, the array $p$ equals $p_k^{(i)}$ at the start of pass $i$ of line L3, line L4 adds the term to row $i$, and lines L5 to L7 apply $L$ and then $C$. Each solve succeeds by Lemma 2. By Lemma 1 of that proof (the positive frequencies are enough), the sum is the field at $t = 0$ of the continued data without the frequency 0 and the Nyquist frequency, provided the negative frequencies are continued by the conjugate maps. $\blacksquare$

**Theorem 2 (consistency for constant velocity).** Let $v'$ be constant. Then $L$ is the scalar $e^{i\omega\Delta z/v'}$, so it commutes with $C$, and one depth step multiplies the sine mode $\psi_m$ by $e^{i k_z^{\mathrm{CN}}\Delta z}$ with
$$k_z^{\mathrm{CN}} = \frac{\omega}{v'} + \frac{2}{\Delta z}\arctan\Big(\frac{b\lambda}{2}\Big), \qquad \lambda = -4\sin^2\Big(\frac{k_x\Delta x}{2}\Big), \quad k_x = \frac{m\pi}{(n_x + 1)\Delta x}.$$
For fixed $\omega$ and $k_x$, $k_z^{\mathrm{CN}} - k_z^{15} = O(\Delta x^2) + O(\Delta z^2)$ as $\Delta x, \Delta z \to 0$.

*Proof.* The mode factor is Lemma 3, and $\lambda_m = -4\sin^2(k_x\Delta x/2)$ with this $k_x$. Put $y = b\lambda/2$. Since $\lambda = -k_x^2\Delta x^2\,(1 + O(k_x^2\Delta x^2))$, $y = -\frac{v' k_x^2\Delta z}{4\omega}\,(1 + O(\Delta x^2))$, which is $O(\Delta z)$. Then $\frac{2}{\Delta z}\arctan y = \frac{2y}{\Delta z} + O(y^3/\Delta z) = -\frac{v' k_x^2}{2\omega}(1 + O(\Delta x^2)) + O(\Delta z^2)$. Add $\omega/v'$. $\square$

Together, Lemma 1 and Theorem 2 give the error of the method for constant velocity: the 15-degree error, which is small for angles up to about 15 degrees and grows as $a^4$, and the grid error of order $\Delta x^2 + \Delta z^2$. The tests measure both. For a velocity that changes along $x$ the method is a splitting of the 15-degree equation into the lens term and the diffraction term; its splitting error is not bounded here (a heuristic).

**Stability.** $L$ has modulus 1 in each entry and $C$ keeps $\|\cdot\|_B$ (Lemma 3). If the velocity does not change with depth, $B$ is the same in every step, so $\|p_k^{(i)}\|_B = \|p_k^{(0)}\|_B$ for all $i$, and the plain norm is bounded by $\sqrt{\max_j b_j/\min_j b_j}$ times its first value. There is no step-size condition such as a CFL condition, because the scheme is implicit.
