---
title: Every fixed point of AMP with soft thresholding solves a LASSO problem, and the Onsager coefficient is the average derivative of the threshold function
proves: [correctness]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix and $y \in \mathbb{R}^m$. The soft threshold function is $\eta(v; \theta) = \operatorname{sign}(v)\max(|v| - \theta, 0)$ for $\theta > 0$, applied entry by entry to vectors. AMP starts from $x^0 = 0$, $z^0 = y$ and repeats, for $t = 0, 1, 2, \dots$,

$$x^{t+1} = \eta(x^t + A^Tz^t; \theta_t),\qquad z^{t+1} = y - Ax^{t+1} + \frac{\|x^{t+1}\|_0}{m}\,z^t.$$

The threshold is either a fixed $\theta$ or $\theta_t = \alpha\tau_t$ with $\tau_t = \|z^t\|/\sqrt m$.

This page proves two facts that hold for every matrix: the form of the correction term, and the fact that fixed points are LASSO solutions. The statement that the iterates follow state evolution is a theorem of Bayati and Montanari (2011) for Gaussian matrices in the large system limit; it is stated at the end and cited, not proved.

## Part 1: the correction term

Donoho, Maleki and Montanari (2009) write the correction as $\frac1\delta z^t\langle\eta'(x^t + A^Tz^t; \theta_t)\rangle$, with $\delta = m/n$ and $\langle v\rangle = \frac1n\sum_i v_i$.

**Lemma 1.** For $|v| \ne \theta$, $\eta'(v; \theta) = 1$ if $|v| > \theta$ and $0$ if $|v| < \theta$. Hence, with $u = x^t + A^Tz^t$ and no entry with $|u_i| = \theta_t$,

$$\frac1\delta\langle\eta'(u; \theta_t)\rangle = \frac nm\cdot\frac{\#\{i : |u_i| > \theta_t\}}{n} = \frac{\|x^{t+1}\|_0}{m}.$$

*Proof.* On $v > \theta$ the function is $v - \theta$, on $v < -\theta$ it is $v + \theta$, and on $|v| < \theta$ it is 0. The entries with $|u_i| > \theta_t$ are exactly the nonzero entries of $x^{t+1} = \eta(u; \theta_t)$. $\square$

An entry with $|u_i| = \theta_t$ exactly gives $x^{t+1}_i = 0$, and counting it as 0 is the convention used by the implementation.

## Part 2: fixed points are LASSO solutions

**Lemma 2.** For $\theta > 0$ and real numbers $x$, $g$: $x = \eta(x + g; \theta)$ if and only if $g = \theta\operatorname{sign}(x)$ when $x \ne 0$, and $|g| \le \theta$ when $x = 0$. In other words, $g \in \theta\,\partial|x|$.

*Proof.* Let $x \ne 0$ and $x = \eta(x + g; \theta)$. A nonzero output has the sign of the input and magnitude $|x + g| - \theta$, so $x + g = x + \theta\operatorname{sign}(x)$ and $g = \theta\operatorname{sign}(x)$. Conversely, if $g = \theta\operatorname{sign}(x)$, then $|x + g| = |x| + \theta > \theta$ and $\eta(x + g; \theta) = x + g - \theta\operatorname{sign}(x) = x$. Let $x = 0$. Then $0 = \eta(g; \theta)$ holds if and only if $|g| \le \theta$. $\square$

**Theorem.** Let $(x, z)$ be a fixed point of the iteration with a fixed threshold $\theta > 0$, that is $x = \eta(x + A^Tz; \theta)$ and $z = y - Ax + \frac km z$ with $k = \|x\|_0$. If $k < m$, then $x$ minimizes

$$F(w) = \tfrac12\|y - Aw\|^2 + \lambda\|w\|_1,\qquad \lambda = \theta\left(1 - \frac km\right).$$

The same holds for the adaptive rule $\theta_t = \alpha\tau_t$: at a fixed point $z$ does not change, so $\tau_t$ and $\theta_t$ are constant, and the theorem applies with $\theta = \alpha\|z\|/\sqrt m$.

*Proof.* The second equation gives $(1 - k/m)z = y - Ax$. Since $k < m$, the factor is positive and $A^Tz = A^T(y - Ax)/(1 - k/m)$. By Lemma 2 applied to each entry, the first equation says that $(A^Tz)_i \in \theta\,\partial|x_i|$ for all $i$. Multiply by $1 - k/m > 0$:

$$A^T(y - Ax) \in \lambda\,\partial\|x\|_1.$$

This is the condition $0 \in A^T(Ax - y) + \lambda\,\partial\|x\|_1 = \partial F(x)$. $F$ is convex, so a point where $0$ is a subgradient is a global minimizer. $\square$

If $k \ge m$, the factor $1 - k/m$ is zero or negative, and the fixed point equation for $z$ either forces $y = Ax$ or gives a negative weight, which is not a LASSO problem. In practice the iteration with a small fixed threshold then diverges: the correction coefficient $k/m$ reaches 1 and $z$ grows. The adaptive rule avoids this because $\theta_t$ grows with $\|z^t\|$.

The theorem does not say that AMP converges. For a general matrix it can diverge. It says that whenever the iteration stops at a fixed point, the result is a LASSO solution, with a weight $\lambda$ that the user does not choose directly. Donoho, Maleki and Montanari (2009) give this correspondence, and the test file checks it against an independent coordinate descent solver.

## Part 3: state evolution (cited)

Let $A$ have i.i.d. $N(0, 1/m)$ entries, $y = Ax + w$ with noise of variance $\sigma^2$ per entry, and let $n \to \infty$ with $m/n \to \delta$ while the empirical distribution of the entries of $x$ converges to the law of a random variable $X$ (with the moment conditions of the theorem). Define $\tau_0^2 = \sigma^2 + E[X^2]/\delta$ and

$$\tau_{t+1}^2 = \sigma^2 + \frac1\delta E\big[(\eta(X + \tau_tZ; \theta_t) - X)^2\big],\qquad Z \sim N(0, 1) \text{ independent of } X.$$

Bayati and Montanari (2011) prove that for each fixed $t$, and for every pseudo-Lipschitz function $\psi$, $\frac1n\sum_i\psi(x^{t+1}_i, x_i) \to E[\psi(\eta(X + \tau_tZ; \theta_t), X)]$ almost surely. With $\psi(a, b) = (a - b)^2$ this says that the mean squared error of $x^{t+1}$ is the state evolution prediction. The proof uses a conditioning technique for Gaussian matrices and needs the Onsager term: without it, the effective noise in $x^t + A^Tz^t$ is not Gaussian with the predicted variance, and the prediction fails. The statement is for a fixed number of iterations as $n \to \infty$ and for Gaussian matrices; it is not a statement about one finite matrix.
