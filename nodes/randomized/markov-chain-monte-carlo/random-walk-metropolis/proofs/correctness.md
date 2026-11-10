---
title: Random-walk Metropolis is reversible with respect to π, and its acceptance rate on N(0, 1) is (2/π) arctan(2/σ)
proves: [correctness]
status: full
---

**Setting.** The target $\pi$ has a density on $\mathbb{R}^d$ with respect to Lebesgue measure, and $\tilde\pi = Z\pi$ is the function that the algorithm evaluates. The increment $Z$ has a density $g$ with $g(z) = g(-z)$, so the proposal density from $x$ is $Q(x, y) = \sigma^{-d}g((y - x)/\sigma)$. Write $\alpha(x, y) = \min(1, \pi(y)/\pi(x))$ for $\pi(x) > 0$. As on the [Metropolis-Hastings](/metropolis-hastings/) page, the chain starts at $\pi(x_0) > 0$ and stays in $\{\pi > 0\}$, because a move to $y$ needs $u < \pi(y)/\pi(x)$, which is false when $\pi(y) = 0$.

**Step 1: the proposal is symmetric.** $Q(y, x) = \sigma^{-d}g((x - y)/\sigma) = \sigma^{-d}g(-(y - x)/\sigma) = \sigma^{-d}g((y - x)/\sigma) = Q(x, y)$.

**Step 2: the test of line L6 is the Metropolis-Hastings test.** By Step 1, the Metropolis-Hastings ratio is $r(x, y) = \pi(y)Q(y, x)/(\pi(x)Q(x, y)) = \pi(y)/\pi(x) = \tilde\pi(y)/\tilde\pi(x)$, since $Z$ cancels. Line L6 accepts when $u < r$ with $u$ uniform on $[0, 1)$, which has probability $\min(1, r)$.

**Step 3: detailed balance.** The kernel is $P(x, dy) = Q(x, y)\alpha(x, y)\,dy + \rho(x)\delta_x(dy)$, where $\rho(x) = 1 - \int Q(x, y)\alpha(x, y)\,dy$ is the probability of a rejection. For $x \ne y$ with $\pi(x), \pi(y) > 0$,

$$\pi(x)Q(x, y)\alpha(x, y) = Q(x, y)\min(\pi(x), \pi(y)) = Q(y, x)\min(\pi(y), \pi(x)) = \pi(y)Q(y, x)\alpha(y, x),$$

by Step 1. If $\pi(y) = 0$, both sides are 0. So the measure $\pi(dx)P(x, dy)$ is symmetric in $(x, y)$ on the part off the diagonal, and the part on the diagonal, $\pi(x)\rho(x)\delta_x(dy)$, is symmetric by itself. Integrate over $x$ in $\mathbb{R}^d$ and $y$ in a Borel set $A$: $\int\pi(dx)P(x, A) = \int_A\pi(dy)P(y, \mathbb{R}^d) = \pi(A)$. So $\pi$ is stationary. This is the [detailed balance](/detailed-balance/) argument of the general proof, with the Hastings factor equal to 1.

**Step 4: the acceptance rate in stationarity.** Let $X \sim \pi$ and $Y = X + \sigma Z$, and assume that $\Pr(\pi(Y) = \pi(X)) = 0$. The mean acceptance rate is $\bar\alpha = E[\min(1, r(X, Y))]$. Split it as $E[\mathbf{1}\{r \ge 1\}] + E[r\,\mathbf{1}\{r < 1\}]$. The second term is

$$\iint \pi(x)Q(x, y)\frac{\pi(y)}{\pi(x)}\mathbf{1}\{\pi(y) < \pi(x)\}\,dx\,dy = \iint \pi(y)Q(y, x)\mathbf{1}\{\pi(y) < \pi(x)\}\,dx\,dy,$$

by Step 1. Rename $y$ as $x$ and $x$ as $y$: this is $\Pr(\pi(X) < \pi(Y))$. So $\bar\alpha = 2\Pr(\pi(Y) > \pi(X))$.

Now take $d = 1$, $\pi = \mathcal{N}(0, 1)$ and $Z \sim \mathcal{N}(0, 1)$. Then $\pi(Y) > \pi(X)$ exactly when $Y^2 < X^2$, that is, when $(Y - X)(Y + X) < 0$, that is, when $UV < 0$ with $U = \sigma Z$ and $V = 2X + \sigma Z$. The pair $(U, V)$ is Gaussian with mean 0, $\operatorname{Var}U = \sigma^2$, $\operatorname{Var}V = 4 + \sigma^2$ and $\operatorname{Cov}(U, V) = \sigma^2$, so its correlation is $\rho = \sigma/\sqrt{4 + \sigma^2}$. For a centered Gaussian pair with correlation $\rho$, $\Pr(UV < 0) = \arccos(\rho)/\pi$. To see this, let $W$ be a standard Gaussian vector in $\mathbb{R}^2$, $e_1 = (1, 0)$ and $e_2 = (\rho, \sqrt{1 - \rho^2})$. Then $(\langle W, e_1\rangle, \langle W, e_2\rangle)$ has the law of $(U/\operatorname{sd}U, V/\operatorname{sd}V)$. The direction of $W$ is uniform on the circle, and the two inner products have opposite signs exactly when the line through 0 perpendicular to $W$ separates $e_1$ from $e_2$. The angle between $e_1$ and $e_2$ is $\arccos\rho$, so this has probability $2\arccos(\rho)/(2\pi)$. Since $\cos\theta = \sigma/\sqrt{4 + \sigma^2}$ means $\tan\theta = 2/\sigma$ for $\theta \in (0, \pi/2)$,

$$\bar\alpha(\sigma) = \frac{2}{\pi}\arccos\frac{\sigma}{\sqrt{4 + \sigma^2}} = \frac{2}{\pi}\arctan\frac{2}{\sigma}. \qquad \blacksquare$$

**Remarks.** The formula gives $\bar\alpha \to 1$ as $\sigma \to 0$ and $\bar\alpha \approx 4/(\pi\sigma)$ as $\sigma \to \infty$. Stationarity does not give convergence. If $\pi$ is positive and continuous and $g$ is positive near 0, the chain is $\pi$-irreducible and aperiodic, so it converges in total variation from $\pi$-almost every start by the general theory (Tierney 1994). The rate of convergence depends on the tails of $\pi$, as the main page says.
