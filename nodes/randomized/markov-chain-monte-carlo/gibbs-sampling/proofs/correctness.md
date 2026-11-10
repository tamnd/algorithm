---
title: Each Gibbs update is reversible with respect to π, so both scans leave π invariant
proves: [correctness]
status: full
---

**Setting.** The space is $\mathcal{X} = D_1 \times \cdots \times D_d$ with finite sets $D_i$, and $\pi$ is a distribution on $\mathcal{X}$. For a state $x$ and an index $i$, write $x_{-i} = (x_j)_{j \ne i}$ and $\pi_{-i}(x_{-i}) = \sum_{v \in D_i}\pi(x_1, \ldots, x_{i-1}, v, x_{i+1}, \ldots, x_d)$ for the marginal of $x_{-i}$. The update of coordinate $i$ (lines L6 and L7) is defined at states with $\pi_{-i}(x_{-i}) > 0$, which holds along the chain because the chain starts at $\pi(x^{(0)}) > 0$ and Step 1 below shows that it stays in $\{\pi > 0\}$. Its kernel is

$$K_i(x, y) = \begin{cases} \dfrac{\pi(y)}{\pi_{-i}(x_{-i})} & \text{if } y_{-i} = x_{-i}, \\ 0 & \text{otherwise.} \end{cases}$$

This is the distribution of line L6: the new value $v = y_i$ has probability $\tilde\pi(y)/\sum_{v'}\tilde\pi(\ldots, v', \ldots)$, and the constant $Z$ cancels.

**Step 1: the chain stays in the support.** $K_i(x, y) > 0$ implies $\pi(y) > 0$. So if $\pi(x) > 0$, then each state reached has positive probability, and its marginals $\pi_{-j}$ are positive for each $j$.

**Step 2: each $K_i$ is reversible.** Let $x, y$ be states with $\pi(x) > 0$ and $\pi(y) > 0$. If $y_{-i} \ne x_{-i}$, then $K_i(x, y) = K_i(y, x) = 0$. If $y_{-i} = x_{-i}$, then $\pi_{-i}(x_{-i}) = \pi_{-i}(y_{-i})$, and

$$\pi(x)K_i(x, y) = \frac{\pi(x)\pi(y)}{\pi_{-i}(x_{-i})} = \frac{\pi(y)\pi(x)}{\pi_{-i}(y_{-i})} = \pi(y)K_i(y, x).$$

If $\pi(x) = 0$, the left side is 0, and $K_i(y, x) = 0$ by the formula, so both sides are 0. So $\pi(x)K_i(x, y) = \pi(y)K_i(y, x)$ for all $x, y$: this is [detailed balance](/detailed-balance/).

**Step 2 as a Metropolis-Hastings step.** Take the proposal $Q(x, y) = K_i(x, y)$. For $Q(x, y) > 0$, the Metropolis-Hastings ratio is

$$r = \frac{\pi(y)Q(y, x)}{\pi(x)Q(x, y)} = \frac{\pi(y)\,\pi(x)/\pi_{-i}(y_{-i})}{\pi(x)\,\pi(y)/\pi_{-i}(x_{-i})} = 1,$$

so the [acceptance probability](/acceptance-probability/) is $\min(1, 1) = 1$ and the Metropolis-Hastings kernel equals $K_i$. The general proof on the [Metropolis-Hastings](/metropolis-hastings/) page then gives Step 2 again.

**Step 3: invariance.** Sum the identity of Step 2 over $x$: $\sum_x \pi(x)K_i(x, y) = \pi(y)\sum_x K_i(y, x) = \pi(y)$. So $\pi K_i = \pi$ for each $i$.

**Step 4: the random scan.** One random-scan step has kernel $K = \frac1d\sum_{i=1}^{d} K_i$. It is a convex combination of kernels that each satisfy detailed balance with respect to $\pi$, so $\pi(x)K(x, y) = \frac1d\sum_i\pi(x)K_i(x, y) = \frac1d\sum_i\pi(y)K_i(y, x) = \pi(y)K(y, x)$. So $K$ is reversible, and $\pi K = \pi$.

**Step 5: the systematic scan.** One sweep has kernel $K_{\mathrm{sys}} = K_1K_2\cdots K_d$, the product in the order of line L3. By Step 3 and induction on $j$, $\pi K_1 \cdots K_j = \pi$ for $j = 1, \ldots, d$. So $\pi K_{\mathrm{sys}} = \pi$. $\blacksquare$

**Remarks.** The product of reversible kernels need not be reversible: the example on the page has $\pi(00)K_{\mathrm{sys}}(00, 01) = 4/75 \ne 1/50 = \pi(01)K_{\mathrm{sys}}(01, 00)$. The palindromic sweep $K_1 \cdots K_d K_d \cdots K_1$ is reversible, because in $L^2(\pi)$ each $K_i$ is self-adjoint, and the adjoint of a product is the product of the adjoints in reverse order. Invariance does not give convergence. If $\pi(x) > 0$ for all $x \in \mathcal{X}$, then $K_i(x, y) > 0$ whenever $y$ differs from $x$ only in coordinate $i$, so any state reaches any other by changing one coordinate at a time, and $K_i(x, x) > 0$ makes the chain aperiodic. Then both scans converge to $\pi$ from every start by the convergence theorem for finite [ergodic](/ergodicity/) chains.
