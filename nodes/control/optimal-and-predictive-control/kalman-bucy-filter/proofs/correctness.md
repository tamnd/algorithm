---
title: The Riccati differential equation is the error covariance of the filter, no other gain gives a smaller covariance, and the solution settles at the stabilizing algebraic solution
proves: [correctness]
status: full
---

The plant is $dx = (A x + B u)\, dt + dw$, $dz = C x\, dt + dv$, where $w$ and $v$ are independent Wiener processes with intensities $W \ge 0$ and $V > 0$ (so $\mathbb{E}\, dw\, dw^T = W dt$), $x(0)$ has mean $\hat x_0$ and covariance $S_0$, and $x(0)$, $w$, $v$ are independent. The input $u$ is known. A linear filter with a gain function $G(t)$ is

$$d\hat x = (A \hat x + B u)\, dt + G(t) (dz - C \hat x\, dt), \qquad \hat x(0) = \hat x_0.$$

The Kalman-Bucy filter is the choice $G = L_o(t) = S(t) C^T V^{-1}$, where $S$ solves $\dot S = A S + S A^T + W - S C^T V^{-1} C S$ with $S(0) = S_0$. The proof has four parts: the error covariance of any gain (Part 1), the optimality of $L_o$ (Part 2), the limit of $S(t)$ (Part 3), and what the discrete steps of the code compute (Part 4).

## Part 1: the error covariance of a gain

**Lemma 1.** Let $e = x - \hat x$ and $P_G(t) = \mathbb{E}\, e e^T$. Then $\mathbb{E}\, e(t) = 0$ and

$$\dot P_G = (A - G C) P_G + P_G (A - G C)^T + W + G V G^T, \qquad P_G(0) = S_0.$$

*Proof.* Subtract the filter from the plant. The input terms cancel, so $de = (A - G C) e\, dt + dw - G\, dv$. The mean obeys $\frac{d}{dt}\mathbb{E}\,e = (A - GC)\,\mathbb{E}\,e$ with $\mathbb{E}\,e(0) = 0$. The Itô product rule gives $d(e e^T) = de\, e^T + e\, de^T + de\, de^T$, and $\mathbb{E}\, de\, de^T = (W + G V G^T) dt$ because $w$ and $v$ are independent. Take expectations; the Itô integrals have mean 0. $\square$

**Lemma 2.** With $G = L_o = S C^T V^{-1}$, the covariance $P_{L_o}$ equals $S$.

*Proof.* $L_o V L_o^T = S C^T V^{-1} C S$ and $L_o C S = S C^T V^{-1} C S$. Put them into Lemma 1:

$$(A - L_o C) S + S (A - L_o C)^T + W + L_o V L_o^T = A S + S A^T + W - S C^T V^{-1} C S.$$

So $S$ solves the equation of Lemma 1 with the same initial value, and the solution is unique (the right side is locally Lipschitz, and $S$ exists for all $t \ge 0$ by Part 3). $\square$

## Part 2: no gain does better

**Lemma 3.** For every bounded measurable gain $G(t)$ and every $t \ge 0$, $P_G(t) - S(t) \ge 0$. Equality on an interval holds only when $G = L_o$ there, up to the null space of $V$, which is $\{0\}$.

*Proof.* Let $D = P_G - S$ and $F = A - G C$. Subtract the two equations, write $F P_G = F D + F S$, and use $C S = V L_o^T$ (from $L_o V = S C^T$):

$$\dot D = F D + D F^T + \left(- G C S - S C^T G^T + G V G^T + L_o V L_o^T\right) = F D + D F^T + (G - L_o) V (G - L_o)^T.$$

Since $D(0) = 0$, the solution is $D(t) = \int_0^t \Phi(t, s) (G - L_o) V (G - L_o)^T \Phi(t, s)^T ds$, where $\Phi$ is the transition matrix of $F$. The integrand is positive semidefinite, so $D(t) \ge 0$. $\square$

So the Kalman-Bucy gain minimizes $\mathbb{E}\, a^T e(t) e(t)^T a$ for every direction $a$ and every $t$, among all filters of the given form. Kalman and Bucy (1961) show more: when $x(0)$, $w$ and $v$ are Gaussian, $\hat x(t)$ is the conditional mean $\mathbb{E}[x(t) \mid z(s), s \le t]$, so no estimator, linear or not, has a smaller error covariance. Without the Gaussian assumption, $\hat x$ is the best linear estimate.

## Part 3: the limit of the Riccati solution

**Lemma 4.** If $(C, A)$ is detectable and $(A, W^{1/2})$ is stabilizable, then for every $S_0 \ge 0$ the solution $S(t)$ exists for all $t \ge 0$ and tends to the unique stabilizing solution $S_\infty \ge 0$ of $A S + S A^T - S C^T V^{-1} C S + W = 0$; $A - S_\infty C^T V^{-1} C$ is Hurwitz.

*Proof.* Set $\tilde A = A^T$, $\tilde B = C^T$, $\tilde Q = W$, $\tilde R = V$. Then $S(t) = \Pi(T - t)$, where $\Pi$ solves the backward Riccati equation of the [finite horizon LQR](/finite-horizon-lqr/) problem for $(\tilde A, \tilde B, \tilde Q, \tilde R)$ on $[0, T]$ with terminal weight $S_0$: the two equations are the same after the time reversal $\tau = T - t$. The LQR value $\xi^T \Pi \xi$ is the minimum of a cost that is nonnegative, so $\Pi \ge 0$, and it is at most the cost of any fixed stabilizing feedback, so $\Pi$ is bounded uniformly in the horizon; hence no finite escape. The hypotheses translate into $(\tilde A, \tilde B)$ stabilizable and $(\tilde Q^{1/2}, \tilde A)$ detectable, and under them the finite horizon solution converges, as the horizon grows, to the stabilizing solution of the CARE for any terminal weight $S_0 \ge 0$ (Anderson and Moore 1990, the chapter on the infinite-time regulator). The transpose of that CARE is the filter equation, and $\tilde A - \tilde B \tilde R^{-1} \tilde B^T S_\infty$ Hurwitz means $A - S_\infty C^T V^{-1} C$ Hurwitz. $\square$

## Part 4: what the code computes

- **Lines L1 and L2.** The state $(\hat x, S)$ starts at $(\hat x_0, S_0)$ and the loop takes one step per input and measurement increment.
- **Line L3** forms $L_o = S C^T V^{-1}$ from the current $S$, as in the definition.
- **Line L4** is one Euler-Maruyama step of the filter equation, with $dz$ replaced by the measured increment $\Delta z_k = z(t_{k+1}) - z(t_k)$. The noise enters additively in the filter equation (the gain does not depend on $\hat x$), so the scheme converges in mean square with order 1 in the step $h$ as $h \to 0$. For a plant that is itself simulated by the same scheme, the discrete error obeys $e_{k+1} = (I + h (A - L_o C)) e_k + \Delta w_k - L_o \Delta v_k$ exactly, which is what the tests use.
- **Line L5** is one RK4 step of the Riccati equation, with a local error $O(h^5)$ on any bounded interval where $S$ is smooth. The symmetrization after the step only removes rounding.
- **Lines L7 to L9.** A fixed point of the RK4 map with $\dot S = 0$ is a solution of the algebraic equation. The loop stops when the residual $\|\dot S\|$ is at most the tolerance, so the returned $S$ solves the algebraic equation with that residual. By Lemma 4 the exact flow reaches every neighborhood of $S_\infty$; RK4 with a small enough step keeps the stable fixed point stable, so the loop ends. The linearized flow at $S_\infty$ is $\dot \Delta = F \Delta + \Delta F^T$ with $F = A - L_o C$, whose eigenvalues are the sums $\lambda_i + \lambda_j$ of eigenvalues of $F$; the step $h$ must be small compared with the inverse of their largest modulus.
