---
title: The super-twisting algorithm drives s and v to zero in finite time when k2 > L + 2 L^2 / k1^2, and k2 >= L is necessary
proves: [correctness]
status: full
---

The plant is $\dot s = u + d(t)$, where $d$ is absolutely continuous and $|\dot d(t)| \le L$ for almost every $t$. The continuous-time form of lines L1 and L2 is $u = -k_1 |s|^{1/2} \operatorname{sgn}(s) + w$ and $\dot w = -k_2 \operatorname{sgn}(s)$, with $k_1, k_2 > 0$. Put $v = w + d$. Then

$$\dot s = -k_1 |s|^{1/2} \operatorname{sgn}(s) + v, \qquad \dot v = -k_2 \operatorname{sgn}(s) + \dot d(t). \tag{1}$$

The first equation has a continuous right side. The second is discontinuous at $s = 0$, and solutions are taken in the sense of Filippov: $(s, v)$ is absolutely continuous, the first equation holds for every $t$, and $\dot v(t) \in -k_2\, \Sigma(s(t)) + \dot d(t)$ for almost every $t$, where $\Sigma(s) = \{\operatorname{sgn} s\}$ for $s \neq 0$ and $\Sigma(0) = [-1, 1]$. In this proof $|\cdot|$ is the absolute value, $\|\cdot\|$ is the Euclidean norm on $\mathbb{R}^2$, and $\lambda_{\min}$, $\lambda_{\max}$ are the least and the largest eigenvalue of a symmetric matrix.

## Lemma 1: the closed loop in the coordinates zeta

Let $\zeta_1 = |s|^{1/2} \operatorname{sgn}(s)$ and $\zeta_2 = v$. The map $s \mapsto \zeta_1$ is continuous and invertible ($s = |\zeta_1| \zeta_1$), so $\zeta(t)$ is continuous in $t$. Where $s \neq 0$, $\zeta_1$ is differentiable in $s$ with derivative $1 / (2 |s|^{1/2}) = 1 / (2 |\zeta_1|)$. So, for almost every $t$ with $s(t) \neq 0$,

$$\dot \zeta_1 = \frac{-k_1 \zeta_1 + \zeta_2}{2 |\zeta_1|}, \qquad \dot \zeta_2 = -k_2 \operatorname{sgn}(\zeta_1) + \dot d = \frac{(-k_2 + \theta L)\, \zeta_1}{|\zeta_1|},$$

with $\theta = \dot d \operatorname{sgn}(\zeta_1) / L \in [-1, 1]$ (any $\theta$ if $L = 0$). Indeed $|\zeta_1|\, \dot d = \dot d \operatorname{sgn}(\zeta_1)\, \zeta_1 = \theta L \zeta_1$. In matrix form,

$$\dot \zeta = \frac{1}{|\zeta_1|} A(\theta)\, \zeta, \qquad A(\theta) = \begin{bmatrix} -k_1/2 & 1/2 \\ -k_2 + \theta L & 0 \end{bmatrix}. \qquad \square$$

## Lemma 2: the Lyapunov matrix and its derivative

Let

$$P = \begin{bmatrix} 2k_2 + k_1^2/2 & -k_1/2 \\ -k_1/2 & 1 \end{bmatrix}, \qquad Q(\theta) = \begin{bmatrix} k_1 k_2 + k_1^3/2 + \theta L k_1 & -k_1^2/2 - \theta L \\ -k_1^2/2 - \theta L & k_1/2 \end{bmatrix}.$$

(a) $P$ is positive definite: $P_{11} > 0$ and $\det P = 2k_2 + k_1^2/4 > 0$.

(b) $A(\theta)^T P + P A(\theta) = -Q(\theta)$. With $c = -k_2 + \theta L$ and $p = 2k_2 + k_1^2/2$, the product $P A$ has the entries $(PA)_{11} = -k_1 p / 2 - k_1 c / 2$, $(PA)_{12} = p / 2$, $(PA)_{21} = k_1^2 / 4 + c$ and $(PA)_{22} = -k_1 / 4$. Adding the transpose gives the diagonal entries $-k_1 p - k_1 c = -k_1 k_2 - k_1^3/2 - \theta L k_1$ and $-k_1 / 2$, and the off-diagonal entry $p/2 + k_1^2/4 + c = k_1^2/2 + \theta L$. These are the entries of $-Q(\theta)$.

(c) $\det Q(\theta) = \frac{k_1}{2}\left(k_1 k_2 + \frac{k_1^3}{2} + \theta L k_1\right) - \left(\frac{k_1^2}{2} + \theta L\right)^2 = \frac{k_1^2 k_2}{2} - \frac{\theta L k_1^2}{2} - \theta^2 L^2.$

(d) If $k_2 > L + 2L^2 / k_1^2$, then $Q(\theta)$ is positive definite for every $\theta \in [-1, 1]$. Its entry $Q_{22} = k_1 / 2$ is positive. The function $\theta \mapsto \det Q(\theta)$ is a concave quadratic, so on $[-1, 1]$ it is smallest at an endpoint. $\det Q(-1) - \det Q(1) = L k_1^2 \ge 0$, and $\det Q(1) = k_1^2 (k_2 - L) / 2 - L^2 > 0$ exactly when $k_2 > L + 2L^2/k_1^2$. Conversely, if $k_2 \le L + 2L^2/k_1^2$, then $Q(1)$ is not positive definite.

(e) Let $q = \min(\lambda_{\min} Q(1), \lambda_{\min} Q(-1))$. For a fixed unit vector $x$, $\theta \mapsto x^T Q(\theta) x$ is affine, so $\lambda_{\min} Q(\theta) = \min_{\|x\| = 1} x^T Q(\theta) x$ is concave in $\theta$ and its minimum on $[-1, 1]$ is at an endpoint. So $\lambda_{\min} Q(\theta) \ge q$ for every $\theta \in [-1, 1]$, and $q > 0$ under the condition of (d). $\square$

The tests check (b) and (c) exactly in Fraction for 200 random gains, and the identity of Lemma 3 at 200 random points.

## Lemma 3: V decreases away from s = 0

Let $V = \zeta^T P \zeta$ and assume $k_2 > L + 2L^2/k_1^2$. On every open time interval where $s \neq 0$, $V$ is absolutely continuous and, for almost every $t$,

$$\dot V = 2 \zeta^T P \dot \zeta = \frac{1}{|\zeta_1|} \zeta^T (A^T P + P A) \zeta = -\frac{1}{|\zeta_1|} \zeta^T Q(\theta) \zeta \le -\frac{q \|\zeta\|^2}{|\zeta_1|} \le -q \|\zeta\| \le -\frac{q}{\lambda_{\max}(P)^{1/2}} V^{1/2},$$

using $|\zeta_1| \le \|\zeta\|$ and $V \le \lambda_{\max}(P) \|\zeta\|^2$. So $\frac{d}{dt} V^{1/2} \le -c$ with $c = q / (2 \lambda_{\max}(P)^{1/2})$ wherever $V > 0$ and $s \neq 0$. $\square$

## Lemma 4: zeros of s with v nonzero are isolated

Let $s(t^*) = 0$ and $v(t^*) \neq 0$. By the first equation of (1), which holds for every $t$ with a continuous right side, $\dot s(t^*) = v(t^*) \neq 0$, and $\dot s$ is continuous near $t^*$. So $s$ is strictly monotone near $t^*$ and $s(t) \neq 0$ for $0 < |t - t^*| < \rho$ for some $\rho > 0$. $\square$

## Theorem 1: finite-time convergence

Assume $k_2 > L + 2L^2/k_1^2$. Then $(s(t), v(t)) = (0, 0)$ for all $t \ge T$, where

$$T = \frac{2 \lambda_{\max}(P)^{1/2}\, V(0)^{1/2}}{q}.$$

Proof. Fix $\varepsilon > 0$ and an interval $[a, b]$ on which $V \ge \varepsilon$. The zeros of $s$ in $[a, b]$ have $v \neq 0$, because $s = v = 0$ gives $V = 0$. By Lemma 4 each zero is isolated. If there were infinitely many, they would have an accumulation point $\bar t \in [a, b]$, with $s(\bar t) = 0$ by continuity and $v(\bar t) \neq 0$ since $V(\bar t) \ge \varepsilon$; then $\bar t$ would be isolated by Lemma 4, which is a contradiction. So $s$ has finitely many zeros in $[a, b]$. On each of the open intervals between them, Lemma 3 gives $V^{1/2}(t'') - V^{1/2}(t') \le -c (t'' - t')$, and since $V$ is continuous, the inequality holds across the zeros too. So $V^{1/2}(b) \le V^{1/2}(a) - c (b - a)$.

Now let $t_\varepsilon$ be the first time with $V(t) = \varepsilon$ (if $V(0) \le \varepsilon$, put $t_\varepsilon = 0$). On $[0, t_\varepsilon]$, $V \ge \varepsilon$, so $t_\varepsilon \le (V(0)^{1/2} - \varepsilon^{1/2}) / c \le T$. Hence $V$ takes values at most $\varepsilon$ before $T$ for every $\varepsilon > 0$.

It remains to show that $V$ never increases. Let $t_0 < t_1$ and suppose $V(t_1) > V(t_0)$. Let $t_2 = \sup \{ t \in [t_0, t_1] : V(t) \le V(t_0) \}$. By continuity $V(t_2) = V(t_0)$, and $V > V(t_0) \ge 0$ on $(t_2, t_1]$. For each $\delta \in (0, t_1 - t_2)$, $V$ is continuous and positive on $[t_2 + \delta, t_1]$, so it has a positive minimum there, and the first part, with $\varepsilon$ equal to this minimum, gives $V(t_1) \le V(t_2 + \delta)$. Letting $\delta \to 0$ gives $V(t_1) \le V(t_2) = V(t_0)$, a contradiction. So $V$ is non-increasing on $[0, \infty)$. Combined with the first part, $V(t) \le \varepsilon$ for $t \ge T$ and every $\varepsilon > 0$, so $V(t) = 0$ for $t \ge T$. Since $P$ is positive definite, $\zeta = 0$, that is $s = v = 0$. $\square$

At $s = v = 0$ the Filippov set for $\dot v$ is $-k_2 [-1, 1] + \dot d$, which contains $0$ because $|\dot d| \le L < k_2$. So staying at the origin is a valid solution, and by the theorem it is the only one. On the origin $v = 0$, so $w = -d$: the integral state equals minus the disturbance, and the averaged value of $k_2 \Sigma(s)$ is $\dot d$.

## Theorem 2: k_2 >= L is necessary

Let $k_2 < L$ and $d(t) = L t$, so $\dot d = L$. Suppose $s = 0$ on an interval $I$ of positive length. By the first equation of (1), $v = \dot s = 0$ on $I$, so $\dot v = 0$ for almost every $t \in I$. But $\dot v \in -k_2 [-1, 1] + L \subset [L - k_2, L + k_2]$, and $L - k_2 > 0$. This is a contradiction. So no solution stays on $s = 0$ for any $k_1$, and $s = 0$ is not reached in the sense of Theorem 1. $\square$

The test with $k_1 = 2$, $k_2 = 0.5$ and $d = t$ shows $s(10) > 4$. The gap between $k_2 \ge L$ and the sufficient condition $k_2 > L + 2L^2/k_1^2$ comes from the choice of $P$; other Lyapunov functions give other sufficient conditions.

## Sampling

The implementation samples $s$ with period $h$ and integrates $\dot w$ by explicit Euler (line L2). Then exact convergence is replaced by a neighborhood: Levant (1993) shows that $|s| = O(h^2)$ and $|\dot s| = O(h)$ after a finite time. This page does not reprove that result. The tests measure $\max_{t \ge 6} |s|$ between $4.3 h^2$ and $5.3 h^2$ for $h = 0.01, 0.005, 0.0025$ in the page example.
