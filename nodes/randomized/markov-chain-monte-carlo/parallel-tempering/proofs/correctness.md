---
title: The swap move is reversible with respect to the product of the tempered laws, so the cold level has stationary law π
proves: [correctness]
status: full
---

**Setting.** $\mathcal{X}$ is a measurable space with a reference measure $\lambda$ (counting measure on a finite set, or Lebesgue measure on $\mathbb{R}^d$). $\tilde\pi > 0$ is a density with respect to $\lambda$ with $\int\tilde\pi\,d\lambda < \infty$, and $1 = \beta_1 > \dots > \beta_K > 0$. Assume $Z_k = \int\tilde\pi^{\beta_k}\,d\lambda < \infty$ for each $k$, and let $\pi_k = \tilde\pi^{\beta_k}/Z_k$, so $\pi_1 = \pi$. On $\mathcal{X}^K$ with the measure $\lambda^K$, let $\Pi(x) = \prod_{k=1}^K\pi_k(x_k)$.

**Step 1: the local sweep keeps $\Pi$.** Lines L2 and L3 apply, in turn, the kernels $Q_k(x, dy) = P_k(x_k, dy_k)\prod_{j \ne k}\delta_{x_j}(dy_j)$, where $P_k$ keeps $\pi_k$. Let $f \ge 0$ be measurable on $\mathcal{X}^K$. By Fubini,

$$\int\Pi(dx)\,Q_kf(x) = \int\prod_{j \ne k}\pi_j(dx_j)\int\pi_k(dx_k)\int P_k(x_k, dy_k)f(\dots, y_k, \dots) = \int\prod_{j \ne k}\pi_j(dx_j)\int\pi_k(dy_k)f(\dots, y_k, \dots),$$

which is $\int\Pi f$. So each $Q_k$ keeps $\Pi$, and so does their product.

**Step 2: the swap ratio.** Let $\tau_k$ exchange the coordinates $k$ and $k+1$ of $x$. Then $\tau_k\circ\tau_k$ is the identity, and $\tau_k$ maps $\lambda^K$ to itself, because $\lambda^K$ is a product of equal factors. The ratio of line L5 is

$$r_k(x) = \Big(\frac{\tilde\pi(x_{k+1})}{\tilde\pi(x_k)}\Big)^{\beta_k - \beta_{k+1}} = \frac{\tilde\pi(x_{k+1})^{\beta_k}\tilde\pi(x_k)^{\beta_{k+1}}}{\tilde\pi(x_k)^{\beta_k}\tilde\pi(x_{k+1})^{\beta_{k+1}}} = \frac{\Pi(\tau_kx)}{\Pi(x)},$$

where in the last step the factors $Z_k$, $Z_{k+1}$ and $\pi_j(x_j)$ for $j \ne k, k+1$ are the same in the numerator and the denominator. Let $a_k(x) = \min(1, r_k(x))$. Then

$$\Pi(x)a_k(x) = \min\big(\Pi(x), \Pi(\tau_kx)\big) = \Pi(\tau_kx)a_k(\tau_kx). \tag{1}$$

**Step 3: the swap is reversible.** Lines L4 to L7 give the kernel

$$Sf(x) = \frac1{K - 1}\sum_{k=1}^{K-1}\Big(a_k(x)f(\tau_kx) + \big(1 - a_k(x)\big)f(x)\Big).$$

Fix $k$ and measurable $f, g \ge 0$. Substitute $x = \tau_ky$, which keeps $\lambda^K$, and then use (1):

$$\int g(x)a_k(x)f(\tau_kx)\Pi(x)\,\lambda^K(dx) = \int g(\tau_ky)a_k(\tau_ky)\Pi(\tau_ky)f(y)\,\lambda^K(dy) = \int f(y)a_k(y)g(\tau_ky)\Pi(y)\,\lambda^K(dy).$$

So the term with $a_k(x)f(\tau_kx)$ is symmetric in $f$ and $g$, and the term $(1 - a_k(x))f(x)g(x)$ is symmetric in an obvious way. Summing over $k$ gives $\int g\,Sf\,d\Pi = \int f\,Sg\,d\Pi$, which is detailed balance. With $g = 1$ it gives $\int Sf\,d\Pi = \int f\,d\Pi$, so $S$ keeps $\Pi$.

**Step 4: stationarity.** One iteration is the local sweep followed by $S$. By Steps 1 and 3 it keeps $\Pi$. If the joint chain starts with law $\Pi$, then at every time its law is $\Pi$, and the marginal law of the first coordinate is $\pi_1 = \pi$.

**Step 5: a condition for convergence.** Suppose that the local sweep $L$ has the property that for every $x$, the law $L(x, \cdot)$ gives positive mass to every set of positive $\Pi$ measure (this holds when each $P_k(x_k, \cdot)$ has a positive density, as for a Gaussian proposal on $\mathbb{R}^d$ with a positive target, or when each $P_k$ has all entries positive on a finite set). Let $A$ have $\Pi(A) > 0$. By Step 3, $\int\Pi(dy)S(y, A) = \Pi(A) > 0$, so the set $B = \{y : S(y, A) > 0\}$ has $\Pi(B) > 0$. Then

$$(LS)(x, A) = \int L(x, dy)S(y, A) \ge \int_BL(x, dy)S(y, A) > 0,$$

because $L(x, B) > 0$ and the integrand is positive on $B$. So the chain reaches every set of positive measure in one iteration from every start. This makes it $\Pi$-irreducible, and aperiodic, because a cycle of disjoint sets $D_1, \dots, D_m$ with $m \ge 2$ would need $(LS)(x, D_2) = 0$ for $x \in D_2$. By the general theory of Markov chains with a stationary law (as in Tierney 1994), the law of the joint chain then converges to $\Pi$ in total variation from $\Pi$-almost every start, and the law of $x_1$ converges to $\pi$. $\blacksquare$

**Remark.** Nothing in the proof uses the order of the $\beta_k$ or the choice of the local kernels beyond their invariance. The ladder and the kernels decide only the speed of convergence.
