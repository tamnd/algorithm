---
title: On average, extremum seeking is a gradient flow, and for a fast dither the loop converges to a small neighborhood of the optimum
proves: [correctness]
status: full
---

Notation is that of the page. The map is $J$, the dither is $a_i\sin\omega_i t$, the washout is $\eta' = h(y - \eta)$, and the law is $\hat\theta_i' = -k_i(y - \eta)\sin\omega_i t$ with $y = J(\hat\theta + d(t))$. We first treat one parameter, $n = 1$, with $a = a_1$, $\omega = \omega_1$, $k = k_1$.

**Claim 1 (demodulation identity).** Let $s = \sin\tau$ and let $\langle\cdot\rangle$ be the mean over $\tau \in [0, 2\pi]$. For every constant $c$ and every $J$ with five continuous derivatives,
$$M(\theta) := \langle (J(\theta + a s) - c)\, s\rangle = \frac{a}{2}J'(\theta) + \frac{a^3}{16}J'''(\theta) + O(a^5).$$
If $J$ is a polynomial of degree at most 2, then $M(\theta) = (a/2)J'(\theta)$ exactly.

*Proof.* $\langle s\rangle = 0$, so the constant $c$ does not contribute. By Taylor's theorem, $J(\theta + a s) = \sum_{m=0}^{4} J^{(m)}(\theta)\,a^m s^m/m! + O(a^5)$, uniformly in $s \in [-1, 1]$. The means of the odd powers of $s$ are zero, and $\langle s^2\rangle = 1/2$, $\langle s^4\rangle = 3/8$. So $\langle J(\theta + as)\,s\rangle = J'(\theta)\,a\langle s^2\rangle + J'''(\theta)\,(a^3/6)\langle s^4\rangle + O(a^5) = (a/2)J' + (a^3/16)J''' + O(a^5)$. For a quadratic $J$ the Taylor series stops at $m = 2$ with no remainder, and the term with $m = 2$ multiplies $\langle s^3\rangle = 0$. $\square$

For $J = \theta^4$ the series is finite and gives exactly $M = 2a\theta^3 + (3/2)a^3\theta$, which the tests check by a rectangle rule that is exact for these trigonometric polynomials.

**Claim 2 (the averaged system).** Put $\tau = \omega t$ and $\epsilon = 1/\omega$. Then the loop is
$$\frac{d\hat\theta}{d\tau} = -\epsilon k\,(J(\hat\theta + a\sin\tau) - \eta)\sin\tau,\qquad \frac{d\eta}{d\tau} = \epsilon h\,(J(\hat\theta + a\sin\tau) - \eta),$$
which is $\epsilon f(\tau, z)$ with $f$ of period $2\pi$ in $\tau$. Its average, with $\eta$ and $\hat\theta$ frozen over one period, is
$$\frac{d\bar\theta}{d\tau} = -\epsilon k\,M(\bar\theta),\qquad \frac{d\bar\eta}{d\tau} = \epsilon h\,(\bar J(\bar\theta) - \bar\eta),\qquad \bar J(\theta) = \langle J(\theta + a s)\rangle.$$

*Proof.* $\langle\eta\sin\tau\rangle = \eta\langle s\rangle = 0$ for a frozen $\eta$, so the first equation is $-\epsilon k\,M$ by Claim 1 with $c = \eta$. The second follows from the definition of $\bar J$. $\square$

The averaged system is triangular: $\bar\theta$ does not depend on $\bar\eta$. For $J(\theta) = c(\theta - \theta^*)^2 + J^*$ with $c > 0$, Claim 1 gives $M(\theta) = a c(\theta - \theta^*)$, so in the time $t$, $\bar\theta(t) = \theta^* + (\theta(0) - \theta^*)e^{-kac\,t}$. In the example of the page, $c = 1$, $\theta^* = 2$, $\theta(0) = 0$, which gives $\bar\theta(t) = 2 - 2e^{-kat}$. The equilibrium of the averaged system is $\bar\theta = \theta^*$ and $\bar\eta = \bar J(\theta^*) = J^* + ca^2/2$. Its Jacobian, in the time $\tau$, is lower triangular with the eigenvalues $-\epsilon kac$ and $-\epsilon h$, both negative for $k > 0$ and $h > 0$, so the equilibrium is exponentially stable (in the sense of Lyapunov, with an exponential rate), and since the averaged system is linear in this case, from every initial state.

For a general $J$ with a nondegenerate minimum, $M(\theta) = 0$ has by Claim 1 and the implicit function theorem a root $\theta_a = \theta^* - (a^2/8)\,J'''(\theta^*)/J''(\theta^*) + O(a^4)$ for small $a$, and $M'(\theta_a) = (a/2)J''(\theta^*) + O(a^3) > 0$, so the averaged equilibrium is exponentially stable and has a bias of order $a^2$.

**Claim 3 (the real loop).** Let the averaged system have an exponentially stable equilibrium $\bar z$ (Claim 2), and let $f$ be continuously differentiable with bounded derivatives on a neighborhood. Then there is $\omega_0$ such that, for every $\omega > \omega_0$, the loop has a unique periodic solution of period $2\pi/\omega$ in an $O(1/\omega)$ neighborhood of $\bar z$, this solution is exponentially attractive, and every solution that starts close enough to $\bar z$ stays within $O(1/\omega)$ of the solution of the averaged system for all $t \ge 0$.

*Proof.* This is the averaging theorem for periodic systems (Khalil, Nonlinear Systems, Section 10.4, Theorem 10.4) applied to Claim 2 with $\epsilon = 1/\omega$. The theorem needs $f$ periodic in $\tau$ and continuously differentiable with bounded derivatives in $z$ on compact sets, which holds when $J$ is twice continuously differentiable. $\square$

**Consequence.** Combining Claims 2 and 3, $\hat\theta(t) = \hat\theta$ of the periodic solution plus a decaying term, and the periodic solution is within $O(1/\omega)$ of $\theta_a$, which is within $O(a^2)$ of $\theta^*$. So $\limsup_{t\to\infty}|\hat\theta(t) - \theta^*| = O(1/\omega + a^2)$, and the output stays within $O(a^2 + 1/\omega)$ of $J^*$; the dither alone raises the mean of $y$ by $\bar J(\theta^*) - J^* = a^2J''(\theta^*)/4 + O(a^4)$.

**Several parameters.** For $n > 1$ with frequencies $\omega_i = \nu_i\omega$, $\nu_i$ distinct positive integers, the vector field is periodic with period $2\pi$ in $\tau$. For a quadratic $J$, the mean of $J(\theta + \sum_j a_j\sin\nu_j\tau)\sin\nu_i\tau$ has three kinds of terms: the linear term gives $(a_i/2)\,\partial_iJ$, because $\langle\sin\nu_j\tau\sin\nu_i\tau\rangle = \delta_{ij}/2$; the quadratic terms are products $\sin\nu_j\tau\,\sin\nu_l\tau\,\sin\nu_i\tau$, which are sums of products of a cosine and a sine with integer frequencies, and their mean is zero; and the constant terms give zero. So the averaged law is $\bar\theta_i' = -k_i(a_i/2)\,\partial_iJ(\bar\theta)$, the gradient flow with the diagonal gain $\mathrm{diag}(k_ia_i/2)$, and Claim 3 applies in the same way. In the example of the page, $\nu = (5, 7)$ with $\omega = 10$, and the rates are $k_1 a_1\cdot 1 = 0.2$ and $k_2 a_2\cdot 2 = 0.4$.

The tests check Claim 1 exactly for random quadratic data and for $\theta^4$, compare the simulated loop with the averaged solution, and compare the limit for $J = e^\theta - 2\theta$ with a brute force grid search for the minimizer $\ln 2$.
