---
title: The independence sampler leaves π invariant, and a bounded weight w ≤ M gives total variation distance at most (1 − 1/M)^t
proves: [correctness]
status: full
---

**Setting.** Let $\pi$ and $q$ be densities with respect to a common measure $dy$ on a space $\mathcal{X}$ (Lebesgue measure, or counting measure on a finite set). Let $S = \{\pi > 0\}$, and assume $q > 0$ on $S$. Let $w = \pi/q$ on $S$. The chain starts in $S$. Line L6 accepts $y$ with probability $\alpha(x, y) = \min(1, w(y)/w(x))$, which is 0 when $\pi(y) = 0$, so the chain stays in $S$. The kernel is

$$P(x, dy) = q(y)\alpha(x, y)\,dy + \rho(x)\delta_x(dy), \qquad \rho(x) = 1 - \int q(y)\alpha(x, y)\,dy.$$

**Step 1: detailed balance.** This is Metropolis-Hastings with $Q(x, y) = q(y)$. For $x, y \in S$,

$$\pi(x)q(y)\alpha(x, y) = \min\big(\pi(x)q(y), \pi(x)q(y)\tfrac{w(y)}{w(x)}\big) = \min\big(\pi(x)q(y), \pi(y)q(x)\big),$$

since $\pi(x)q(y)w(y)/w(x) = q(x)q(y)w(y) = \pi(y)q(x)$. The right side is symmetric in $x$ and $y$. With the symmetric rejection part $\pi(x)\rho(x)\delta_x(dy)$, the measure $\pi(dx)P(x, dy)$ is symmetric, so $\int\pi(dx)P(x, A) = \pi(A)$ for each measurable $A$. So $\pi$ is stationary.

**Step 2: minorization.** Assume $w(x) \le M$ for every $x \in S$. Then $M \ge 1$, because $1 = \int_S\pi = \int_S wq \le M$. For $x, y \in S$, $q(y) = \pi(y)/w(y) \ge \pi(y)/M$ and $\pi(y)/w(x) \ge \pi(y)/M$, so

$$q(y)\alpha(x, y) = \min\Big(q(y), \frac{\pi(y)}{w(x)}\Big) \ge \frac{\pi(y)}{M}.$$

So $P(x, A) \ge \pi(A)/M$ for every $x \in S$ and every measurable $A$.

**Step 3: contraction.** If $M = 1$, Step 2 gives $P(x, A) \ge \pi(A)$ for every $A$ and also for its complement, so $P(x, \cdot) = \pi$, and the claim holds for $t \ge 1$. Let $M > 1$ and $\varepsilon = 1/M$. By Step 2, $R(x, A) = (P(x, A) - \varepsilon\pi(A))/(1 - \varepsilon)$ is a probability kernel on $S$, and $P(x, \cdot) = \varepsilon\pi + (1 - \varepsilon)R(x, \cdot)$. For a probability measure $\mu$ on $S$, $\mu P - \pi = \mu P - \pi P$ by Step 1, and

$$\mu P - \pi P = \varepsilon(\mu(S) - \pi(S))\pi + (1 - \varepsilon)(\mu - \pi)R = (1 - \varepsilon)(\mu - \pi)R.$$

A probability kernel does not increase total variation: for a signed measure $\nu$ with $\nu(S) = 0$, $|\nu R(A)| = |\int R(x, A)\,\nu(dx)| \le \sup_B\nu(B) = \|\nu\|_{TV}$, because $0 \le R(x, A) \le 1$. So $\|\mu P - \pi\|_{TV} \le (1 - \varepsilon)\|\mu - \pi\|_{TV}$.

**Step 4: the bound.** Apply Step 3 $t$ times with $\mu = \delta_xP^{s}$ for $s = t - 1, \ldots, 0$, and use $\|\delta_x - \pi\|_{TV} \le 1$:

$$\|P^t(x, \cdot) - \pi\|_{TV} \le (1 - 1/M)^t. \qquad \blacksquare$$

**Remarks.** The bound is sharp in the example on the page, where the second eigenvalue is $1 - 1/M = 1/2$. Step 2 says that one step is a draw from $\pi$ with probability $1/M$ and a draw from $R$ otherwise. So two copies of the chain can be coupled to meet with probability $1/M$ at each step, which is the [coupling](/coupling-method/) form of the same proof. The converse, that an unbounded $w$ rules out a geometric rate, is the harder half of the theorem of Mengersen and Tweedie (1996) and is not proved here.
