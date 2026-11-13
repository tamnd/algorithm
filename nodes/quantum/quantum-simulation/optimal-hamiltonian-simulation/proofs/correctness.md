---
title: The block of G is within kappa eta (5 + 60 rho^2 + 80 rho^4) of e^(-iHt)
proves: [correctness]
status: full
---

We use the pseudocode of the page. $U$ is a Hermitian unitary on $m + n$ qubits with $\Pi_0U\Pi_0 = H/\alpha$ on the range of $\Pi_0 = |0^m\rangle\langle 0^m| \otimes I$. $\tau = \alpha t$, $\kappa = 2s$ with $s = \sin(\pi/10)$, and $\Pi$ projects on the states with all ancillas of $G$ equal to 0. The norm is the spectral norm, and $\|g\|_\infty = \max_{x \in [-1, 1]}|g(x)|$.

**Lemma 1 (the truncation).** Let $c_R$ and $s_R$ be the sums of line L2 with the coefficients $c_{2k}$ and $s_{2k+1}$. Then $\|c_R - \cos(\tau\,\cdot)\|_\infty \le \eta$ and $\|s_R - \sin(\tau\,\cdot)\|_\infty \le \eta$ with $\eta = 2\sum_{k > 2R}|J_k(\tau)|$.

*Proof.* The generating function of the Bessel functions gives $e^{i\tau\cos\theta} = \sum_{k \in \mathbb{Z}}i^kJ_k(\tau)e^{ik\theta}$, and $J_{-k} = (-1)^kJ_k$. Taking the real and the imaginary parts, with $x = \cos\theta$ and $T_k(\cos\theta) = \cos k\theta$, gives the two series of the page, which converge absolutely because $|J_k(\tau)| \le (|\tau|/2)^k/k!$. The terms left out of $c_R$ are $2(-1)^kJ_{2k}(\tau)T_{2k}(x)$ with $2k > 2R$, and those left out of $s_R$ are $2(-1)^kJ_{2k+1}(\tau)T_{2k+1}(x)$ with $2k + 1 > 2R + 1$. Since $|T_j(x)| \le 1$ on $[-1, 1]$, each tail is at most $2\sum_{j > 2R}|J_j(\tau)| = \eta$. $\square$

**Lemma 2 (the inputs of QET are valid).** If $\eta \le 0.6$, then $p_c = \kappa c_R$ is even, $p_s = \kappa s_R$ is odd, both are real, and $|p_c|, |p_s| \le 1$ on $[-1, 1]$.

*Proof.* $T_{2k}$ is even and $T_{2k+1}$ is odd, and the coefficients are real. By Lemma 1, $|c_R| \le 1 + \eta$ and $|s_R| \le 1 + \eta$, so $|p_c|, |p_s| \le \kappa(1 + \eta) \le 0.6181 \cdot 1.6 < 1$. $\square$

So, by the theorem on the page of the [quantum eigenvalue transformation](/quantum-eigenvalue-transformation/), line L4 gives unitaries $Q_c$ and $Q_s$ with one more qubit each and the blocks $p_c(H/\alpha)$ and $p_s(H/\alpha)$ on the range of the projector with all their ancillas 0. If $\eta > 0.6$, line L4 is not defined. Every $R$ whose bound in the theorem below is less than 1 has $5\kappa\eta < 1$, so $\eta < 0.33$, and the lemma applies.

**Lemma 3 (the block of $V$).** $Z = \Pi V\Pi$, read as an operator on the system, is $\tfrac{1}{2}(p_c - ip_s)(H/\alpha)$, and $\|Z - s\,e^{-iHt}\| \le \delta = \kappa\eta$.

*Proof.* Let $D = |0\rangle\langle 0| \otimes Q_c + |1\rangle\langle 1| \otimes (-iQ_s)$. The state $|0\rangle$ of the new qubit goes to $(|0\rangle + |1\rangle)/\sqrt 2$ under Had, $D$ applies $Q_c$ or $-iQ_s$ on the two branches, and the projection of Had back on $|0\rangle$ takes $1/\sqrt 2$ of each branch. So the block is $\tfrac{1}{2}(\Pi'Q_c\Pi' - i\Pi'Q_s\Pi') = \tfrac{1}{2}(p_c - ip_s)(H/\alpha)$, with $\Pi'$ the projector of the inner ancillas. The eigenvalues $x$ of $H/\alpha$ lie in $[-1, 1]$, and $\cos(\tau x) - i\sin(\tau x) = e^{-i\tau x}$, so $s\,e^{-iHt} = \tfrac{\kappa}{2}(\cos - i\sin)(\tau H/\alpha)$. By the spectral theorem and Lemma 1,
$$\|Z - s\,e^{-iHt}\| \le \tfrac{\kappa}{2}\big(\|c_R - \cos(\tau\,\cdot)\|_\infty + \|s_R - \sin(\tau\,\cdot)\|_\infty\big) \le \kappa\eta. \qquad \square$$

**Lemma 4 (two rounds of amplification).** Let $V$ be any unitary, $Z = \Pi V\Pi$, $R = 2\Pi - I$, $G_0 = V$ and $G_{j+1} = -VRV^\dagger RG_j$. Then $\Pi G_2\Pi = f(Z)$ with $f(Z) = 5Z - 20ZZ^\dagger Z + 16ZZ^\dagger ZZ^\dagger Z$.

*Proof.* Take a singular value decomposition $Z = \sum_j\sigma_j|w_j\rangle\langle v_j|$, where $\{|v_j\rangle\}$ and $\{|w_j\rangle\}$ are orthonormal bases of the range of $\Pi$, and $\sigma_j = \sin\theta_j$ with $\theta_j \in [0, \pi/2]$. Then $V|v_j\rangle = \sin\theta_j|w_j\rangle + \cos\theta_j|w_j^\perp\rangle$ for a unit vector $|w_j^\perp\rangle$ with $\Pi|w_j^\perp\rangle = 0$ (any such vector if $\cos\theta_j = 0$). Since $V$ is unitary, $\delta_{jk} = \langle Vv_j|Vv_k\rangle = \sigma_j\sigma_k\delta_{jk} + \cos\theta_j\cos\theta_k\langle w_j^\perp|w_k^\perp\rangle$, so $\langle w_j^\perp|w_k^\perp\rangle = 0$ for $j \ne k$ when both cosines are not zero.

If $\cos\theta_j = 0$, then $V|v_j\rangle = |w_j\rangle$, $R|w_j\rangle = |w_j\rangle$ and $VRV^\dagger|w_j\rangle = VR|v_j\rangle = |w_j\rangle$, so each round multiplies $|w_j\rangle$ by $-1$ and $G_2|v_j\rangle = |w_j\rangle = \sin(5\pi/2)|w_j\rangle$. Now let $\cos\theta_j \ne 0$, and let $B_j$ be the plane spanned by $|w_j\rangle$ and $|w_j^\perp\rangle$. On $B_j$, $R$ is the reflection about $|w_j\rangle$. For $VRV^\dagger = 2V\Pi V^\dagger - I$: $\Pi V^\dagger|w_j\rangle = Z^\dagger|w_j\rangle = \sigma_j|v_j\rangle$, and $\Pi V^\dagger|w_j^\perp\rangle = \sum_k|v_k\rangle\overline{\langle w_j^\perp|Vv_k\rangle} = \cos\theta_j|v_j\rangle$, because $\langle w_j^\perp|Vv_k\rangle = \cos\theta_k\langle w_j^\perp|w_k^\perp\rangle$ is $\cos\theta_j$ for $k = j$ and 0 otherwise (for $\cos\theta_k = 0$ the term is 0). So $V\Pi V^\dagger$ maps $B_j$ into the line of $V|v_j\rangle$, it is the projector on that line within $B_j$, and $VRV^\dagger$ is the reflection of $B_j$ about $V|v_j\rangle$.

Measure angles in $B_j$ from $|w_j^\perp\rangle$ toward $|w_j\rangle$. $V|v_j\rangle$ has angle $\theta_j$. $R$ maps the angle $\phi$ to $\pi - \phi$, $VRV^\dagger$ maps $\phi$ to $2\theta_j - \phi$, and the sign $-1$ adds $\pi$. So $-VRV^\dagger R$ maps $\phi$ to $\phi + 2\theta_j$, and $G_2|v_j\rangle = \sin5\theta_j|w_j\rangle + \cos5\theta_j|w_j^\perp\rangle$. Projecting with $\Pi$ gives $\Pi G_2\Pi = \sum_j\sin(5\theta_j)|w_j\rangle\langle v_j|$. The identity $\sin5\theta = 5\sin\theta - 20\sin^3\theta + 16\sin^5\theta$ and $ZZ^\dagger Z = \sum_j\sigma_j^3|w_j\rangle\langle v_j|$, $ZZ^\dagger ZZ^\dagger Z = \sum_j\sigma_j^5|w_j\rangle\langle v_j|$ give $f(Z)$. $\square$

**Lemma 5 (Lipschitz bound).** If $\|Y\|, \|Z\| \le \rho$, then $\|f(Z) - f(Y)\| \le (5 + 60\rho^2 + 80\rho^4)\|Z - Y\|$.

*Proof.* $ZZ^\dagger Z - YY^\dagger Y = (Z - Y)Z^\dagger Z + Y(Z - Y)^\dagger Z + YY^\dagger(Z - Y)$, so its norm is at most $3\rho^2\|Z - Y\|$. In the same way, the difference of the products of five factors is a sum of five terms with one difference and four factors of norm at most $\rho$, so its norm is at most $5\rho^4\|Z - Y\|$. Then $5 + 20 \cdot 3\rho^2 + 16 \cdot 5\rho^4$ is the constant. $\square$

**Theorem.** With $\delta = \kappa\eta$ and $\rho = s + \delta$, the top-left block of $G$ satisfies $\|\Pi G\Pi - e^{-iHt}\| \le \delta(5 + 60\rho^2 + 80\rho^4)$.

*Proof.* Let $Y = s\,e^{-iHt}$. Since $e^{-iHt}$ is unitary, $Y^\dagger Y = s^2I$, so $f(Y) = (5s - 20s^3 + 16s^5)e^{-iHt} = \sin(5\pi/10)\,e^{-iHt} = e^{-iHt}$ by the identity of Lemma 4 with $\theta = \pi/10$. $\|Y\| = s \le \rho$, and $\|Z\| \le s + \delta = \rho$ by Lemma 3. Lemma 4 gives $\Pi G\Pi = f(Z)$, and Lemma 5 with Lemma 3 gives the bound. $\blacksquare$

**Corollary (the run).** For a state $|\psi\rangle$, the outcome 0 on the ancillas has probability $\|f(Z)\psi\|^2 \ge (1 - \epsilon')^2$ with $\epsilon'$ the bound of the theorem, and the normalized output is within $2\epsilon'$ of $e^{-iHt}|\psi\rangle$.

*Proof.* $\|f(Z)\psi - e^{-iHt}\psi\| \le \epsilon'$ and $\|e^{-iHt}\psi\| = 1$ give $\|f(Z)\psi\| \ge 1 - \epsilon'$. For vectors $u$ and a unit $w$ with $\|u - w\| \le \epsilon'$, $\|u/\|u\| - w\| \le \|u/\|u\| - u\| + \|u - w\| = |1 - \|u\|| + \|u - w\| \le 2\epsilon'$. $\square$

**Remark (cost).** $|J_k(\tau)| \le (\tau/2)^k/k!$ gives $\eta \le 4(\tau/2)^{2R+1}/(2R+1)!$ once $2R + 2 > \tau$, so $\eta$ falls faster than geometrically in $R$, and $R = O(\tau + \log(1/\epsilon))$ suffices. Gilyén, Su, Low and Wiebe (Lemma 59) give the exact order $\Theta(\tau + \log(1/\epsilon)/\log(e + \log(1/\epsilon)/\tau))$ of the degree.
