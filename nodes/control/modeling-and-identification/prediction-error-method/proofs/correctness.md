---
title: PEM is a descent method on the prediction error criterion, exact in one step for ARX
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM. Fix the data, the orders and $n_0 = \max(n_a, n_k + n_b - 1, n_c, n_d, n_f)$, and write $M = N - n_0$. The admissible set $\Theta$ is the set of $\theta = (a, b, c, d, f)$ for which $C$ and $F$ are Schur.

**Signals as power series.** Identify a signal $x(0), x(1), \ldots$ that is 0 before time 0 with the formal power series $\sum_k x(k)\, z^k$ in a variable $z$ that stands for $q^{-1}$. A polynomial $P(q) = p_0 + p_1 q^{-1} + \cdots$ acting on $x$ from rest is multiplication by $P(z)$. For a monic $P$, the recursion $P(q)\, x' = x$ from rest, that is $x'(k) = x(k) - \sum_{i \ge 1} p_i x'(k-i)$ with $x'(k) = 0$ for $k < 0$, is multiplication by the power series $1/P(z)$, which exists because $P(0) = 1$. Formal power series form a commutative ring, so all these filters commute and obey the usual rules of algebra. This is exact for finite data: the first $N$ coefficients of a product depend only on the first $N$ coefficients of the factors.

**Lemma 1 (the gradient filters).** For every $\theta$ and every $k$, the vector $\psi(k, \theta)$ computed by L3 equals $-\partial \varepsilon(k, \theta)/\partial \theta$.

*Proof.* In the ring of power series, $w = (B/F)\, u$, $v = A y - w$ and $\varepsilon = (D/C)\, v$. The power series $1/C$ and $1/F$ have coefficients that are polynomials in $c$ and $f$, so each $\varepsilon(k, \theta)$ is a polynomial in $\theta$, and the product and quotient rules hold coefficientwise. Differentiate.

- $\partial A/\partial a_i = z^i$, so $\partial \varepsilon/\partial a_i = (D/C)\, z^i y$, the signal $(D/C)\, y$ delayed by $i$.
- $\partial B/\partial b_j = z^{n_k + j - 1}$, so $\partial w/\partial b_j = z^{n_k + j - 1} u/F$ and $\partial \varepsilon/\partial b_j = -(D/(CF))\, z^{n_k + j - 1} u$.
- $\partial (1/C)/\partial c_i = -z^i/C^2$, so $\partial \varepsilon/\partial c_i = -z^i D v/C^2 = -(1/C)\, z^i \varepsilon$.
- $\partial \varepsilon/\partial d_i = (1/C)\, z^i v$.
- $\partial (1/F)/\partial f_i = -z^i/F^2$, so $\partial w/\partial f_i = -z^i w/F$ and $\partial \varepsilon/\partial f_i = (D/(CF))\, z^i w$.

Negating gives $\psi_{a_i} = -z^i (D/C) y$, $\psi_{b_j} = z^{n_k+j-1} (D/(CF)) u$, $\psi_{c_i} = z^i \varepsilon / C$, $\psi_{d_i} = -z^i v/C$ and $\psi_{f_i} = -z^i (D/(CF)) w$, which are the filtered and delayed signals that L3 forms. $\square$

Let $g(\theta) = \sum_{k=n_0}^{N-1} \psi(k, \theta)\, \varepsilon(k, \theta)$ and $R(\theta) = \sum_{k=n_0}^{N-1} \psi(k, \theta) \psi(k, \theta)^T$, the quantities of L4.

**Lemma 2 (the gradient of the criterion).** $V$ is differentiable on $\mathbb{R}^d$ and $\nabla V(\theta) = -\frac{2}{M}\, g(\theta)$.

*Proof.* $V = \frac{1}{M} \sum_k \varepsilon(k, \theta)^2$ is a polynomial in $\theta$ by the proof of Lemma 1, and $\nabla V = \frac{2}{M} \sum_k \varepsilon\, \partial\varepsilon/\partial\theta = -\frac{2}{M} \sum_k \varepsilon\, \psi$. $\square$

**Lemma 3 (descent).** Let $\theta \in \Theta$, let $R = R(\theta)$ be nonsingular and let $\delta = R^{-1} g(\theta)$. If $g(\theta) \ne 0$, there is $\bar\mu > 0$ such that $\theta + \mu\delta \in \Theta$ and $V(\theta + \mu\delta) < V(\theta)$ for all $0 < \mu \le \bar\mu$.

*Proof.* $R$ is a sum of matrices $\psi\psi^T$, so it is positive semidefinite, and being nonsingular it is positive definite; so is $R^{-1}$. By Lemma 2, $\nabla V(\theta)^T \delta = -\frac{2}{M}\, g^T R^{-1} g < 0$. Since $V$ is differentiable, $V(\theta + \mu\delta) = V(\theta) + \mu \nabla V(\theta)^T \delta + o(\mu)$, which is below $V(\theta)$ for all small $\mu > 0$. The roots of a polynomial depend continuously on its coefficients, so the set where $C$ and $F$ are Schur is open, and $\theta + \mu\delta \in \Theta$ for all small $\mu$. Take $\bar\mu$ as the smaller of the two bounds. $\square$

**Lemma 4 (one step for affine errors).** Suppose $\varepsilon(k, \theta) = y(k) - \varphi(k)^T \theta$ for fixed vectors $\varphi(k)$, as in the ARX case ($n_c = n_d = n_f = 0$), and let $R = \sum \varphi \varphi^T$ be nonsingular. Then from any $\theta$, $\theta + \delta$ is the least squares solution $\theta^* = R^{-1} \sum \varphi(k)\, y(k)$.

*Proof.* Here $\psi(k) = \varphi(k)$ for every $\theta$, so $R(\theta) = R$ and $g(\theta) = \sum \varphi\, (y - \varphi^T \theta) = R \theta^* - R \theta$. Hence $\delta = \theta^* - \theta$ and $\theta + \delta = \theta^*$. $\square$

**Theorem.** Suppose the start $\theta_0$ is admissible and every matrix $R$ met at L5 is nonsingular. Then:

1. at the start of each pass of L2, $\theta \in \Theta$, and the values of $V$ at the start of the passes strictly decrease;
2. the returned $\theta$ is admissible and $V(\theta) \le V(\theta_0)$;
3. if the search ends because L7 accepts no step, then $g(\theta) = 0$, so $\theta$ is a stationary point of $V$, or no $\mu \in \{1, \frac12, \ldots, 2^{-39}\}$ gives an admissible point with a lower $V$;
4. in the ARX case, if $\theta_0 \ne \theta^*$, the first pass accepts $\mu = 1$ and moves to $\theta^*$, the unique minimizer of $V$.

*Proof.* (1) By induction on the passes. Initially $\theta = \theta_0 \in \Theta$. A pass changes $\theta$ only at L8, and only to a point $\theta + \mu\delta$ that the test of L7 has found admissible with $V(\theta + \mu\delta) < V(\theta)$. So the new $\theta$ is admissible and its $V$ is strictly smaller. (2) follows from (1) because the returned $\theta$ is the last value of the induction, and the loop ends after a finite number of passes. (3) If L7 rejects all 40 values of $\mu$, then by the test in L7 none of them gives an admissible point with lower $V$. If $g(\theta) \ne 0$, Lemma 3 guarantees such points for all small $\mu$, so this can happen only when all the tested $\mu$ are larger than $\bar\mu$; otherwise $g(\theta) = 0$ and $\nabla V(\theta) = 0$ by Lemma 2. (4) In the ARX case $\Theta = \mathbb{R}^d$, since there is no $C$ or $F$. By Lemma 4 the step with $\mu = 1$ reaches $\theta^*$, the unique minimizer of the convex quadratic $V$ when $R$ is nonsingular, so $V(\theta^*) < V(\theta_0)$ when $\theta_0 \ne \theta^*$, and L7 accepts $\mu = 1$ at once. $\blacksquare$
