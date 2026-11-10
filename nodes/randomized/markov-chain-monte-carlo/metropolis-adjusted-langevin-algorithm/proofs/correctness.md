---
title: MALA is reversible with respect to π, and the unadjusted chain on N(0, 1) has stationary variance 1/(1 − h/4)
proves: [correctness]
status: full
---

**Setting.** $\pi$ has a positive density on $\mathbb{R}^d$ with $\nabla\log\pi$ continuous, $\tilde\pi = Z\pi$, $\mu(x) = x + \frac h2\nabla\log\pi(x)$ and $q(y \mid x) = (2\pi h)^{-d/2}\exp(-|y - \mu(x)|^2/(2h))$. Let $\alpha(x, y) = \min(1, r(x, y))$ with $r(x, y) = \pi(y)q(x \mid y)/(\pi(x)q(y \mid x))$.

**Step 1: the proposal.** Line L4 sets $y = \mu(x) + \sqrt h\,Z$ with $Z \sim \mathcal{N}(0, I_d)$, so given $x$ the law of $y$ is $\mathcal{N}(\mu(x), hI_d)$, with density $q(y \mid x)$. It is positive for all $x, y$.

**Step 2: the test is the Metropolis-Hastings test.** In line L5 the factor $(2\pi h)^{-d/2}$ appears in both $q(x \mid y)$ and $q(y \mid x)$, and $Z$ appears in $\tilde\pi(y)$ and $\tilde\pi(x)$, so both cancel, and line L5 computes $r(x, y)$. Line L7 accepts with probability $\Pr(u < r) = \min(1, r) = \alpha(x, y)$.

**Step 3: detailed balance.** The kernel is $P(x, dy) = q(y \mid x)\alpha(x, y)\,dy + \rho(x)\delta_x(dy)$, where $\rho(x)$ is the probability of a rejection. For $x \ne y$,

$$\pi(x)q(y \mid x)\alpha(x, y) = \min\big(\pi(x)q(y \mid x),\ \pi(y)q(x \mid y)\big),$$

which is symmetric in $x$ and $y$. So $\pi(dx)P(x, dy)$ is a symmetric measure off the diagonal, and its diagonal part $\pi(x)\rho(x)\delta_x(dy)$ is symmetric by itself. For Borel sets $A$ and $B$ this gives $\int_A\pi(x)P(x, B)\,dx = \int_B\pi(y)P(y, A)\,dy$, and taking $A = \mathbb{R}^d$ gives $\int\pi(x)P(x, B)\,dx = \pi(B)$. So $\pi$ is stationary.

**Step 4: irreducibility and aperiodicity.** Let $B$ have $\pi(B) > 0$, so $B$ has positive Lebesgue measure. For every $x$, the function $y \mapsto q(y \mid x)\alpha(x, y)$ is positive, because $q > 0$ and $\pi > 0$ make $r(x, y) > 0$. So $P(x, B) \ge \int_Bq(y \mid x)\alpha(x, y)\,dy > 0$: the chain is $\pi$-irreducible in one step. The same bound for a set $B$ containing $x$ shows that there is no cycle of disjoint sets, so it is aperiodic. By the general theory of Markov chains on general state spaces (as in Tierney 1994), a $\pi$-irreducible aperiodic chain with stationary law $\pi$ converges to $\pi$ in total variation from $\pi$-almost every start. $\blacksquare$

**Step 5: the unadjusted chain is biased.** Without lines L5 to L7, on $\pi = \mathcal{N}(0, 1)$ the chain is $X_{t+1} = (1 - h/2)X_t + \sqrt h\,Z_t$ with $Z_t$ independent standard normals. Let $a = 1 - h/2$. If $0 < h < 4$, then $|a| < 1$, and a stationary law $\mathcal{N}(0, s^2)$ must satisfy $s^2 = a^2s^2 + h$, so

$$s^2 = \frac{h}{1 - a^2} = \frac{h}{h - h^2/4} = \frac{1}{1 - h/4} > 1.$$

It is the only stationary law, because $X_t = a^tX_0 + \sqrt h\sum_{k<t}a^kZ_{t-1-k}$ converges in law to $\mathcal{N}(0, s^2)$ from every start. If $h \ge 4$, then $|a| \ge 1$ and $\operatorname{Var}X_t \ge th \to \infty$, so there is no stationary law at all. With the test of Steps 2 and 3, the stationary law is exactly $\mathcal{N}(0, 1)$ for every $h$.

**Remark.** Detailed balance uses only that $q(y \mid x)$ is a positive density, not that it approximates the Langevin diffusion. The quality of the approximation decides only the acceptance rate, and so the step size $h \propto d^{-1/3}$ of the scaling result on the main page.
