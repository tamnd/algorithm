---
title: Each Morris elementary effect is a uniform draw from the grid differences, so mu and mu* are unbiased
proves: [correctness]
status: full
---

We assume exact arithmetic and exact random numbers. The inputs are scaled to the unit cube. The grid has $p$ levels $G = \{0, \frac{1}{p-1}, \ldots, 1\}$ with $p$ even, and the step is $\Delta = \frac{p}{2(p-1)}$, which is $p/2$ grid cells. Let $G_- = \{0, \frac{1}{p-1}, \ldots, \frac{p/2 - 1}{p-1}\}$, the $p/2$ levels $v$ with $v + \Delta \in G$. For input $i$, the grid differences are the numbers

$$d_i(x) = \frac{f(x + \Delta e_i) - f(x)}{\Delta}, \qquad x_i \in G_-, \quad x_k \in G \ (k \ne i).$$

There are $\frac{p}{2} p^{d-1}$ of them. The method estimates the grid means $\mu_i = \mathrm{mean}_x\, d_i(x)$ and $\mu_i^* = \mathrm{mean}_x\, |d_i(x)|$, and the spread $\sigma_i$ of the $d_i(x)$. These are the screening measures of Morris (for $\mu$ and $\sigma$) and of Campolongo, Cariboni and Saltelli (for $\mu^*$).

One trajectory draws, independently, base values $x^*_k$ uniform on $G_-$ (line L2), fair coins $u_k$ for the direction up or down (line L3) and a uniform random order $\pi$ of the inputs (line L4). The start point has the components $x^*_k$ if $u_k$ is up and $x^*_k + \Delta$ if not. Line L5 moves the inputs in the order $\pi$, each once, by $+\Delta$ if $u_k$ is up and by $-\Delta$ if not.

**Lemma 1 (the trajectory stays on the grid).** Every point of the trajectory is in $G^d$, consecutive points differ in one component by $\pm\Delta$, and each component moves exactly once.

*Proof.* Component $k$ takes only the two values $x^*_k$ and $x^*_k + \Delta$, which are in $G$ because $x^*_k \in G_-$. It starts at one of them and moves once, to the other one. $\square$

**Lemma 2 (one elementary effect is a grid difference).** The elementary effect of input $i$ in line L7 is $d_i(y)$, where $y$ is the point before the move of $i$ with its component $i$ set to $x^*_i$.

*Proof.* If $u_i$ is up, the move goes from $y$ to $y + \Delta e_i$, and the effect is $(f(y + \Delta e_i) - f(y)) / \Delta = d_i(y)$. If not, the move goes from $y + \Delta e_i$ to $y$, and the effect is $(f(y) - f(y + \Delta e_i)) / (-\Delta) = d_i(y)$. $\square$

**Lemma 3 (the lower point is uniform).** The point $y$ of Lemma 2 is uniform on the set $G_- \times G^{d-1}$ (with $G_-$ in component $i$).

*Proof.* Condition on the order $\pi$. Component $i$ of $y$ is $x^*_i$, uniform on $G_-$. For $k \ne i$, let $m_k = 1$ if $k$ moves before $i$ and $m_k = 0$ if not; given $\pi$, $m_k$ is fixed. Component $k$ of $y$ is $x^*_k + \Delta$ if exactly one of "$u_k$ is down" and "$m_k = 1$" holds, and $x^*_k$ if not. So it is $x^*_k + \Delta c_k$, where $c_k$ is the coin $u_k$ flipped when $m_k = 1$. A flipped fair coin is a fair coin, so the $c_k$ are independent fair coins, independent of the $x^*$. Now $x^*_k$ is uniform on $\{0, \ldots, p/2 - 1\} / (p - 1)$ and $\Delta = (p/2)/(p - 1)$, so $x^*_k + \Delta c_k$ is uniform on $\{0, \ldots, p - 1\} / (p - 1) = G$. The components are independent, so $y$ is uniform on the product set. This holds for every $\pi$, so it holds without the condition. $\square$

**Theorem (unbiased screening measures).** With $r$ independent trajectories, the outputs of line L8 satisfy $\mathbb{E}[\widehat{\mu}_i] = \mu_i$ and $\mathbb{E}[\widehat{\mu}^*_i] = \mu^*_i$, and $\widehat{\sigma}_i^2$ (with the divisor $r - 1$) is unbiased for the variance of the $d_i(x)$ over the grid. As $r \to \infty$, all three converge almost surely.

*Proof.* By Lemmas 2 and 3, the effect of input $i$ on one trajectory is $d_i(y)$ with $y$ uniform on its set, so it is a uniform draw from the list of grid differences. The $r$ trajectories are independent, so the $r$ effects of input $i$ are independent draws. The sample mean, the mean of the absolute values and the sample variance of independent draws are unbiased for the mean, the mean absolute value and the variance of the list. The list is finite, so the strong law of large numbers applies. $\blacksquare$

The effects of different inputs on one trajectory are dependent, because they share points. The theorem is about each input alone. The run count is $r(d + 1)$: one start point and one point per move.

**Corollary (a linear model).** If $f(x) = c_0 + \sum_k c_k x_k$, then $d_i(x) = c_i$ for every $x$, so $\widehat{\mu}_i = c_i$, $\widehat{\mu}^*_i = |c_i|$ and $\widehat{\sigma}_i = 0$ for every $r$.

**Corollary (an input that the model ignores).** If $f$ does not depend on $x_i$, every effect of input $i$ is zero, so $\widehat{\mu}^*_i = 0$ exactly.

**What is not proved.** The measures are defined by the grid and the step $\Delta$; they are not the [Sobol indices](/sobol-indices/), and there is no theorem that orders the inputs in the same way. The theorem says that the estimates converge to the grid measures; how many trajectories are enough for a stable ranking is a rule of thumb, not a result. For odd $p$, the step $\Delta$ is $p/2$ grid cells, which is not a whole number, so the moves leave the grid and Lemma 3 fails; the code rejects odd $p$.
