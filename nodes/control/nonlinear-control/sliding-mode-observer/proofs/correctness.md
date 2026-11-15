---
title: The super-twisting sliding mode observer gives the exact state after a finite time, and its averaged injection equals the unknown term
proves: [correctness]
status: full
---

The plant is

$$\dot x_1 = x_2, \qquad \dot x_2 = f_0(x_1, u) + F(t, x), \qquad y = x_1,$$

with $f_0$ known and continuous, $u(t)$ known, and $F(t, x(t))$ measurable in $t$ with $|F(t, x(t))| \le L$ along the motion considered. The continuous-time form of lines L1 to L4 is

$$\dot{\hat x}_1 = \hat x_2 + \lambda |e|^{1/2} \operatorname{sgn}(e), \qquad \dot{\hat x}_2 = f_0(y, u) + \alpha \operatorname{sgn}(e), \qquad e = y - \hat x_1,$$

with $\lambda, \alpha > 0$. Solutions are taken in the sense of Filippov. Here $|\cdot|$ is the absolute value.

## Lemma 1: the error equations

Let $e_1 = x_1 - \hat x_1$ and $e_2 = x_2 - \hat x_2$. Then $e = y - \hat x_1 = e_1$ and

$$\dot e_1 = x_2 - \hat x_2 - \lambda |e_1|^{1/2} \operatorname{sgn}(e_1) = e_2 - \lambda |e_1|^{1/2} \operatorname{sgn}(e_1),$$

$$\dot e_2 = f_0(x_1, u) + F - f_0(y, u) - \alpha \operatorname{sgn}(e_1) = F(t, x) - \alpha \operatorname{sgn}(e_1),$$

because $y = x_1$, so the known term cancels exactly. In the Filippov sense, $\operatorname{sgn}(e_1)$ is replaced by a value $\sigma(t) \in [-1, 1]$ when $e_1(t) = 0$. $\square$

## Theorem 1: finite-time convergence

Assume $\alpha > L + 2L^2/\lambda^2$. The error equations are system (1) of the super-twisting proof (proofs/correctness.md of the [super-twisting algorithm](/super-twisting-algorithm/)) with $s = e_1$, $v = e_2$, $k_1 = \lambda$, $k_2 = \alpha$, and the term $\dot d(t)$ replaced by $\rho(t) = F(t, x(t))$, which satisfies $|\rho(t)| \le L$. That proof uses only the bound $|\dot d| \le L$, not the fact that $\dot d$ is a derivative, so it applies without change. Hence $e_1 = e_2 = 0$ for all $t \ge T$, with

$$T = \frac{2 \lambda_{\max}(P)^{1/2}\, V(0)^{1/2}}{q}, \qquad V(0) = \zeta(0)^T P \zeta(0), \qquad \zeta(0) = (|e_1(0)|^{1/2} \operatorname{sgn} e_1(0),\ e_2(0)),$$

where $P$ and $q$ are those of that proof with $k_1 = \lambda$, $k_2 = \alpha$. So $\hat x(t) = x(t)$ for $t \ge T$. $\square$

For the page example, $\lambda = 3$, $\alpha = 4$, $L = 2$: $L + 2L^2/\lambda^2 = 2 + 8/9 < 4$, so the condition holds.

## Theorem 2: equivalent output injection

For $t \ge T$, $e_2 = 0$ on an interval, so $\dot e_2 = 0$ for almost every $t \ge T$. By Lemma 1, $0 = F(t, x(t)) - \alpha \sigma(t)$ for almost every $t \ge T$, where $\alpha \sigma(t)$ is the Filippov value of the injection $v_2$. So $\alpha \sigma(t) = F(t, x(t))$ almost everywhere. The value $\sigma(t) \in [-1, 1]$ is consistent with this because $|F| \le L < \alpha$. For every interval $[a, b] \subset [T, \infty)$, $\frac{1}{b - a} \int_a^b \alpha \sigma\, dt = \frac{1}{b - a} \int_a^b F\, dt$: the mean of the injection over any window equals the mean of the unknown term. $\square$

## The sampled implementation

Lines L3 and L4 take explicit Euler steps of length $h$, with $e$ sampled at the start of each step. Over one step, the sum of $h v_2$ equals $\hat x_2(t_{j+1}) - \hat x_2(t_j) - h f_0(y_j, u_j)$, and the integral of $F$ equals $x_2(t_{j+1}) - x_2(t_j) - \int f_0(x_1, u)\, dt$. Summing over a window of $m$ steps of total length $W = m h$,

$$\frac{1}{m} \sum v_2 - \frac{1}{W} \int F\, dt = \frac{e_2(\text{start}) - e_2(\text{end})}{W} + \frac{1}{W} \left( \int f_0\, dt - h \sum f_0(y_j, u_j) \right),$$

so the windowed mean of the injection estimates the mean of $F$ with an error at most $2 \max |e_2| / W$ plus the error of the rectangle rule for $f_0$. In the page example, $\max |e_2| = 0.0207$ and $W = 0.5$ give $0.083$, and the tests measure $0.079$.

The size of the errors with sampling, of order $h^2$ in $e_1$ and $h$ in $e_2$, follows from the homogeneity of the super-twisting algorithm (Levant 1993); this page does not reprove it, and the tests measure it.
