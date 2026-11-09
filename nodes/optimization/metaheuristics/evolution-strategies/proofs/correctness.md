---
title: The (1+1)-ES is elitist, its step size counts successes, it is invariant, and one bit per step gives a lower bound
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $x_t$ and $\sigma_t$ for the values of $x$ and $\sigma$ after step $t$, with $x_0$ and $\sigma_0$ the start values, and $y_t = x_{t-1} + \sigma_{t-1} z_t$ for the point made in line L3 of step $t$, where $z_1, z_2, \dots$ are independent $\mathcal{N}(0, I)$ vectors.

**Claim 1 (elitism).** For every $t$, $f(x_t) \le f(x_{t-1})$ and $f(x_t) = \min\{f(x_0), f(y_1), \dots, f(y_t)\}$.

*Proof.* If step $t$ succeeds, line L5 sets $x_t = y_t$ with $f(y_t) \le f(x_{t-1})$. Otherwise $x_t = x_{t-1}$. In both cases $f(x_t) \le f(x_{t-1})$. For the second statement use induction on $t$, with $t = 0$ clear. If step $t$ succeeds, $f(x_t) = f(y_t) \le f(x_{t-1})$, which by induction is the minimum of the earlier values, so $f(x_t)$ is the new minimum. If it fails, $f(y_t) > f(x_{t-1}) = f(x_t)$, so the minimum does not change. $\square$

**Claim 2 (the step size).** If $S$ of the steps $1, \dots, K$ succeed, then $\sigma_K = \sigma_0 \exp\bigl((S - (K - S)/4)/D\bigr)$. In particular, $\sigma_K = \sigma_0$ if and only if $S = K/5$.

*Proof.* Each step changes $\sigma$ only in line L6 or L7, so $\ln \sigma$ increases by $1/D$ in each of the $S$ successful steps and decreases by $1/(4D)$ in each of the $K - S$ others. Summing gives $\ln \sigma_K = \ln \sigma_0 + S/D - (K - S)/(4D)$. The exponent is 0 exactly when $4S = K - S$, that is, $S = K/5$. $\square$

**Claim 3 (invariance).** Fix the vectors $z_1, z_2, \dots$.

1. Let $g$ be strictly increasing. The runs on $f$ and on $g \circ f$ from the same $x_0, \sigma_0$ give the same $x_t$ and $\sigma_t$ for all $t$.
2. Let $c \in \mathbb{R}^n$. The run on $f_c(x) = f(x - c)$ from $x_0 + c$ gives $x_t + c$ and $\sigma_t$.
3. Let $a > 0$. The run on $f_a(x) = f(x/a)$ from $a x_0$ with $a \sigma_0$ gives $a x_t$ and $a \sigma_t$.
4. Let $Q$ be orthogonal. The run on $f_Q(x) = f(Q^\top x)$ from $Q x_0$, with the vectors $Q z_t$, gives $Q x_t$ and $\sigma_t$. Since $Q z_t$ is again $\mathcal{N}(0, I)$, the run on $f_Q$ with fresh random vectors has the same distribution as $Q$ times the run on $f$.

*Proof.* In each case we show by induction on $t$ that the two runs have related states, and that the test in line L4 has the same outcome. For 1, $g(f(y)) \le g(f(x))$ holds if and only if $f(y) \le f(x)$, because $g$ is strictly increasing, so the same steps succeed and the states are equal. For 2, if the state of the second run is $(x_{t-1} + c, \sigma_{t-1})$, its new point is $x_{t-1} + c + \sigma_{t-1} z_t = y_t + c$, and $f_c(y_t + c) = f(y_t)$ and $f_c(x_{t-1} + c) = f(x_{t-1})$, so the test has the same outcome and the next state is $(x_t + c, \sigma_t)$. For 3, the new point is $a x_{t-1} + a \sigma_{t-1} z_t = a y_t$, and $f_a(a y_t) = f(y_t)$, so the same holds, and $\sigma$ is multiplied by the same factor in both runs. For 4, the new point is $Q x_{t-1} + \sigma_{t-1} Q z_t = Q y_t$, and $f_Q(Q y_t) = f(y_t)$ since $Q^\top Q = I$. A vector $Q z$ with $z \sim \mathcal{N}(0, I)$ has the covariance $Q Q^\top = I$, so it is again $\mathcal{N}(0, I)$, and independent vectors stay independent. $\square$

**Claim 4 (one bit per step).** Let $x^*$ be uniform in the unit ball $B$ of $\mathbb{R}^n$ and $f(x) = \lVert x - x^* \rVert^2$. Consider any method whose point after $k$ steps is a function of its own random numbers $\omega$, which are independent of $x^*$, and of $k$ bits $b_1, \dots, b_k$, where $b_t$ is the outcome of one comparison of two values of $f$. This includes the (1+1)-ES, where $\omega = (z_1, z_2, \dots)$ and $b_t$ is the outcome of line L4. If $P(\lVert x_k - x^* \rVert \le \varepsilon) \ge 1/2$ with $0 < \varepsilon < 1$, then $k \ge n \log_2(1/\varepsilon) - 1$.

*Proof.* Fix $\omega$. Then $x_k$ is a function of $(b_1, \dots, b_k)$, so it takes at most $2^k$ values $p_1, \dots, p_{2^k}$, which do not depend on $x^*$. The event $\lVert x_k - x^* \rVert \le \varepsilon$ implies that $x^*$ is in one of the balls of radius $\varepsilon$ around $p_1, \dots, p_{2^k}$. Each such ball has the volume $\varepsilon^n \operatorname{vol}(B)$, so for uniform $x^*$ its probability is at most $\varepsilon^n$. By the union bound, the probability given $\omega$ is at most $2^k \varepsilon^n$. Since $\omega$ is independent of $x^*$, the same bound holds after averaging over $\omega$. So $1/2 \le 2^k \varepsilon^n$, and taking $\log_2$ gives $k \ge n \log_2(1/\varepsilon) - 1$. $\square$

So halving the distance $b$ times needs at least about $b n$ steps, and the $\Theta(n)$ steps per halving in the theorem of Jägersküpper are optimal up to a constant factor among such methods.

**Claim 5 (fixed step size).** Change the method so that $\sigma = \sigma_0$ at every step. Let $f$ be continuous, let $f^* = \min f$ be attained, and let $L = \{x : f(x) \le f(x_0)\}$ be bounded. Then for every $\varepsilon > 0$ there is $p > 0$ with $P(f(x_K) \ge f^* + \varepsilon) \le (1 - p)^K$ for all $K$.

*Proof.* Let $A = \{y : f(y) < f^* + \varepsilon\}$. It is open, because $f$ is continuous, and not empty, because it contains a minimizer, so it contains a ball $U$ of some radius $r > 0$. By Claim 1, every $x_t$ is in $L$, which is bounded, say within the distance $R$ of the center of $U$. For $x \in L$, the density of $x + \sigma_0 \mathcal{N}(0, I)$ at any point of $U$ is at least $(2\pi \sigma_0^2)^{-n/2} e^{-(R + r)^2/(2 \sigma_0^2)}$, so $P(y \in U) \ge p$ for the positive number $p$ that is this density times the volume of $U$. If $y_t \in A$ then $f(y_t) < f^* + \varepsilon \le f(x_{t-1})$ unless $x_{t-1}$ is already in $A$, so step $t$ succeeds and $x_t \in A$, and by Claim 1, $x$ stays in $A$ after that. So the event $f(x_K) \ge f^* + \varepsilon$ requires $y_t \notin U$ at each step $t$ before $x$ enters $A$. Given the past, each such step misses $U$ with probability at most $1 - p$, which gives the bound. $\square$

The number $p$ can be extremely small, so Claim 5 does not give a useful running time. With the 1/5 rule $\sigma_t$ is not bounded below, the density bound fails, and Claim 5 does not apply.
