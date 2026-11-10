---
title: The Metropolis-Hastings kernel satisfies detailed balance with respect to π
proves: [correctness]
status: full
---

**Setting.** The state space $\mathcal{X}$ has a reference measure $\mu$: the counting measure for a countable space, or Lebesgue measure on $\mathbb{R}^d$. The target $\pi$ has a density $\pi(x)$ with respect to $\mu$, and $\tilde\pi = Z\pi$ for a constant $Z > 0$. For each $x$, $Q(x, \cdot)$ is a probability distribution with density $Q(x, y)$ with respect to $\mu$. Write $S = \{x : \pi(x) > 0\}$ for the support. Define, for $x \in S$ and $y \in \mathcal{X}$,

$$\alpha(x, y) = \begin{cases} \min\Big(1, \dfrac{\pi(y)Q(y, x)}{\pi(x)Q(x, y)}\Big) & \text{if } Q(x, y) > 0, \\ 0 & \text{if } Q(x, y) = 0. \end{cases}$$

The constant $Z$ cancels, so $\alpha$ is the acceptance probability of line L6 of the page: $\Pr(u < r) = \min(1, r)$ for $u$ uniform on $[0, 1)$ and $r \ge 0$.

**Step 1: the kernel.** From $x \in S$, one step (lines L3 to L7) moves to a set $A$ with probability

$$P(x, A) = \int_A Q(x, y)\alpha(x, y)\,\mu(dy) + \rho(x)\,\mathbf{1}[x \in A], \qquad \rho(x) = 1 - \int_{\mathcal{X}} Q(x, y)\alpha(x, y)\,\mu(dy).$$

The first term is a candidate $y \in A$ that is accepted. The second term is a rejection, which keeps $x$; $\rho(x) \in [0, 1]$ because $0 \le \alpha \le 1$ and $Q(x, \cdot)$ integrates to 1. An accepted candidate has $\pi(y) > 0$, since $\alpha(x, y) = 0$ when $\pi(y) = 0$. So the chain stays in $S$.

**Step 2: the off-diagonal part is symmetric.** Let $g(x, y) = \pi(x)Q(x, y)\alpha(x, y)$ for $x, y \in S$. We show $g(x, y) = g(y, x)$. If $Q(x, y) > 0$ and $Q(y, x) > 0$, then

$$g(x, y) = \pi(x)Q(x, y)\min\Big(1, \frac{\pi(y)Q(y, x)}{\pi(x)Q(x, y)}\Big) = \min\big(\pi(x)Q(x, y), \pi(y)Q(y, x)\big),$$

which is symmetric in $x$ and $y$. If $Q(x, y) = 0$, then $g(x, y) = 0$ by the definition of $\alpha$. In the same case $Q(y, x) > 0$ gives $\alpha(y, x) = \min(1, 0) = 0$, and $Q(y, x) = 0$ gives $\alpha(y, x) = 0$ by definition, so $g(y, x) = 0$ too. The case $Q(y, x) = 0$ is the same with $x$ and $y$ exchanged.

**Step 3: detailed balance.** For measurable sets $A, B \subseteq S$,

$$\int_A \pi(x)P(x, B)\,\mu(dx) = \int_A\int_B g(x, y)\,\mu(dy)\,\mu(dx) + \int_{A \cap B}\pi(x)\rho(x)\,\mu(dx).$$

By Step 2 and Tonelli's theorem ($g \ge 0$), the double integral does not change when we exchange the roles of $A$ and $B$. The last term is symmetric in $A$ and $B$. So

$$\int_A \pi(x)P(x, B)\,\mu(dx) = \int_B \pi(y)P(y, A)\,\mu(dy).$$

This is [detailed balance](/detailed-balance/) in its measure form. On a countable space with $A = \{x\}$ and $B = \{y\}$, it reads $\pi(x)P(x, y) = \pi(y)P(y, x)$.

**Step 4: stationarity.** Take $A = S$ in Step 3. Since $P(y, S) = 1$ for $y \in S$ by Step 1,

$$\int_S \pi(x)P(x, B)\,\mu(dx) = \int_B \pi(y)\,\mu(dy) = \pi(B).$$

So if $X_t \sim \pi$, then $X_{t+1} \sim \pi$: $\pi$ is a stationary distribution of $P$. $\blacksquare$

**What the theorem does not say.** Stationarity does not imply that the chain reaches $\pi$ from a given start. On a finite space, if $P$ restricted to $S$ is irreducible and aperiodic, then $P^t(x, \cdot) \to \pi$ for each $x \in S$ (the convergence theorem for finite [ergodic](/ergodicity/) chains, Levin, Peres and Wilmer, Theorem 4.9). An irreducible chain is aperiodic when some state has $\rho(x) > 0$, because that state has a loop of length 1. On a general space, Tierney (1994, Section 3) shows that a $\pi$-irreducible and aperiodic kernel converges to $\pi$ in total variation from $\pi$-almost every start.
