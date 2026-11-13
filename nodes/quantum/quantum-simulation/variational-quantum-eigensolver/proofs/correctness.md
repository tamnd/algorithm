---
title: Every VQE energy is an upper bound on the ground energy, the parameter-shift gradient is exact, and the shot estimate is within lambda (2 ln(2L/delta)/S)^(1/2) with probability 1 - delta
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = \sum_{j=1}^L c_jP_j$ with real $c_j$ and $n$-qubit Pauli strings $P_j$, $\lambda = \sum_j|c_j|$, $|\psi(\theta)\rangle = U(\theta)|0\cdots0\rangle$ and $E(\theta) = \langle\psi(\theta)|H|\psi(\theta)\rangle$. The circuit $U(\theta)$ is a product of fixed unitary gates and rotations $R_{Q_k}(\theta_k) = e^{-i\theta_kQ_k/2}$, one for each parameter, where each $Q_k$ is a Hermitian operator with $Q_k^2 = I$, for example a Pauli string. Three statements are proved. Nothing is proved here about the number of steps of the optimizer or about the distance between the best energy of the trial family and $E_0$; the page explains why no such general statement holds.

**Claim 1 (variational bound).** For every $\theta$, $E_0 \le E(\theta) \le E_{\max}$, where $E_0$ and $E_{\max}$ are the least and the greatest eigenvalues of $H$.

*Proof.* $H$ is Hermitian, so by the spectral theorem it has an orthonormal eigenbasis $|v_1\rangle, \ldots, |v_N\rangle$, $N = 2^n$, with real eigenvalues $E_0 = \mu_1 \le \cdots \le \mu_N = E_{\max}$. The circuit is unitary, so $\|\psi(\theta)\| = 1$. Write $|\psi(\theta)\rangle = \sum_i a_i|v_i\rangle$; then $\sum_i|a_i|^2 = 1$ and
$$E(\theta) = \sum_{i,i'}\overline{a_{i'}}a_i\langle v_{i'}|H|v_i\rangle = \sum_i\mu_i|a_i|^2.$$
This is an average of the $\mu_i$ with nonnegative weights $|a_i|^2$ that add up to 1, so it lies between $\mu_1$ and $\mu_N$. Equality $E(\theta) = E_0$ holds exactly when all weight is on eigenvectors of eigenvalue $E_0$, that is, when $|\psi(\theta)\rangle$ is in the ground space. $\square$

*Consequence for the overlap.* Let $\Delta > 0$ be the gap between $E_0$ and the next distinct eigenvalue, and let $w$ be the total weight of $|\psi(\theta)\rangle$ on the ground space. Then $E(\theta) - E_0 = \sum_i(\mu_i - E_0)|a_i|^2 \ge \Delta(1 - w)$, so $w \ge 1 - (E(\theta) - E_0)/\Delta$.

**Claim 2 (parameter-shift rule).** For each $k$,
$$\frac{\partial E}{\partial\theta_k}(\theta) = \frac{E(\theta + \tfrac\pi2e_k) - E(\theta - \tfrac\pi2e_k)}{2}.$$

*Proof.* Fix all parameters but $\theta_k$ and write $x = \theta_k$. Split the circuit at the rotation $k$: $U(\theta) = V\,R_{Q_k}(x)\,W$, where $V$ and $W$ do not depend on $x$. Let $|\phi\rangle = W|0\cdots0\rangle$ and $M = V^\dagger HV$, a Hermitian operator. Then $E = f(x) = \langle\phi|R(x)^\dagger MR(x)|\phi\rangle$ with $R(x) = e^{-ixQ/2}$, $Q = Q_k$. Since $Q^2 = I$, the power series of the exponential gives $R(x) = \cos(x/2)I - i\sin(x/2)Q$. Substituting,
$$f(x) = \cos^2\tfrac x2\langle M\rangle + \sin^2\tfrac x2\langle QMQ\rangle + i\sin\tfrac x2\cos\tfrac x2\langle[Q, M]\rangle,$$
where $\langle X\rangle = \langle\phi|X|\phi\rangle$. With $\cos^2(x/2) = (1 + \cos x)/2$, $\sin^2(x/2) = (1 - \cos x)/2$ and $\sin(x/2)\cos(x/2) = (\sin x)/2$, this is
$$f(x) = A + B\cos x + C\sin x,\quad A = \tfrac12(\langle M\rangle + \langle QMQ\rangle),\ B = \tfrac12(\langle M\rangle - \langle QMQ\rangle),\ C = \tfrac i2\langle[Q, M]\rangle.$$
$A$ and $B$ are real because $M$ and $QMQ$ are Hermitian, and $C$ is real because $[Q, M]$ is anti-Hermitian, so $\langle[Q, M]\rangle$ is purely imaginary. Then $f'(x) = -B\sin x + C\cos x$, and
$$f(x + \tfrac\pi2) - f(x - \tfrac\pi2) = B(\cos(x + \tfrac\pi2) - \cos(x - \tfrac\pi2)) + C(\sin(x + \tfrac\pi2) - \sin(x - \tfrac\pi2)) = -2B\sin x + 2C\cos x = 2f'(x).$$
The same parameter may appear in no other gate (each rotation has its own parameter in the circuit of the page). If one parameter appears in several rotations, the chain rule gives the sum of the shift rules for each appearance. $\square$

*The exact derivative.* From $U = VR(x)W$, $\partial_x|\psi\rangle = V(-\tfrac i2Q)R(x)W|0\cdots0\rangle$, which is the state with the operator $-\tfrac i2Q$ inserted right after rotation $k$. Then $\partial_xE = \langle\partial_x\psi|H|\psi\rangle + \langle\psi|H|\partial_x\psi\rangle = 2\,\mathrm{Re}\langle H\psi|\partial_x\psi\rangle$, since $H$ is Hermitian. The code computes this value as an independent check of the shift rule.

**Claim 3 (shot estimate).** Let $\hat E = \sum_jc_jm_j$ be the value returned by ENERGY with $S$ shots per term. Then $\mathbb{E}[\hat E] = E(\theta)$, and for every $\delta \in (0, 1)$,
$$\Pr\Big[|\hat E - E(\theta)| \ge \lambda\sqrt{2\ln(2L/\delta)/S}\Big] \le \delta.$$

*Proof.* Fix $j$. Line L10 applies a product $B_j$ of one-qubit gates with $B_jP_jB_j^\dagger = Z_{T}$, the product of $Z$ on the support $T$ of $P_j$: on a qubit with $X$ the gate is the Hadamard gate $H_d$, and $H_dXH_d = Z$; on a qubit with $Y$ the gate is $H_dS^\dagger$, and $(H_dS^\dagger)Y(SH_d) = H_dXH_d = Z$, because $S^\dagger YS = X$. A computational basis measurement of $B_j|\psi\rangle$ gives the outcome $x$ with probability $|\langle x|B_j|\psi\rangle|^2$ by the Born rule, and $Z_T|x\rangle = (-1)^{\sum_{q\in T}x_q}|x\rangle$. So the recorded parity $r = (-1)^{\sum_{q\in T}x_q}$ has
$$\mathbb{E}[r] = \sum_x(-1)^{\sum_{q\in T}x_q}|\langle x|B_j|\psi\rangle|^2 = \langle\psi|B_j^\dagger Z_TB_j|\psi\rangle = \langle\psi|P_j|\psi\rangle.$$
The $S$ shots are independent runs, so $m_j$ is the mean of $S$ independent values in $\{-1, 1\}$ with mean $\langle P_j\rangle$, and by linearity $\mathbb{E}[\hat E] = \sum_jc_j\langle P_j\rangle = E(\theta)$.

By the Hoeffding inequality for $S$ independent variables with values in an interval of length 2, $\Pr[|m_j - \langle P_j\rangle| \ge r] \le 2e^{-2S^2r^2/(4S)} = 2e^{-Sr^2/2}$. Take $r = \sqrt{2\ln(2L/\delta)/S}$, so that this is $\delta/L$. By the union bound, with probability at least $1 - \delta$ every $j$ has $|m_j - \langle P_j\rangle| < r$, and then
$$|\hat E - E(\theta)| \le \sum_j|c_j||m_j - \langle P_j\rangle| < \lambda r.$$
For the error $\epsilon$ it is enough to take $S \ge 2\lambda^2\ln(2L/\delta)/\epsilon^2$, which is the shot count of the page. An identity term ($T$ empty) has $r = 1$ always and needs no shots. $\square$

**What the three claims give together.** The pseudocode follows exact gradients when $S$ is infinite and noisy unbiased gradients otherwise. Every exact energy it visits is at least $E_0$ (Claim 1), so the returned value is an upper bound on $E_0$ up to the error of Claim 3; with probability $1 - \delta$ it is at least $E_0 - \lambda\sqrt{2\ln(2L/\delta)/S}$. $\blacksquare$
