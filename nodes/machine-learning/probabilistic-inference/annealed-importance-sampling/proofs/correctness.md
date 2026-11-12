---
title: Annealed importance sampling gives an unbiased estimate of Z_T / Z_0
proves: [correctness]
status: full
---

The proof is for a finite or countable state space $\mathcal{X}$, with sums. For a general space, replace each sum by an integral against the base measure; the steps are the same.

**Setting.** The unnormalized densities are $f_0, \ldots, f_T \ge 0$ on $\mathcal{X}$, with $Z_j = \sum_x f_j(x)$ and $0 < Z_j < \infty$, and $p_j = f_j / Z_j$. The kernel $K_j(x, y)$ of line L6 is a Markov kernel that leaves $p_j$ invariant:
$$\sum_x f_j(x) K_j(x, y) = f_j(y) \quad \text{for every } y. \tag{1}$$
The support condition is: $f_{j-1}(x) > 0$ wherever $f_j(x) > 0$, for $j = 1, \ldots, T$.

Number the states of one run as in lines L2 to L6. The state $x_0$ is drawn from $p_0$ at line L2. At step $j$, line L5 multiplies the weight by $f_j(x_{j-1}) / f_{j-1}(x_{j-1})$, and line L6 draws $x_j$ from $K_j(x_{j-1}, \cdot)$. So the weight after step $j$ is
$$w_j = w_{j-1} \cdot \frac{f_j(x_{j-1})}{f_{j-1}(x_{j-1})}, \qquad w_0 = 1,$$
with the convention that $w_j = 0$ when $w_{j-1} = 0$, without evaluating the ratio. In log form, a weight of $-\infty$ stays $-\infty$. Lemma 1 shows that the ratio is defined whenever $w_{j-1} > 0$.

**Lemma 1 (the weighted state).** For $j = 0, \ldots, T$ and every $y$,
$$m_j(y) := \mathbb{E}\big[w_j \, [x_j = y]\big] = \frac{f_j(y)}{Z_0}.$$
Consequently, $w_j > 0$ implies $f_j(x_j) > 0$, almost surely.

*Proof.* The consequence follows from the formula: if $f_j(y) = 0$, then $\mathbb{E}[w_j [x_j = y]] = 0$, and $w_j \ge 0$, so $w_j [x_j = y] = 0$ almost surely.

The formula is proved by induction on $j$. For $j = 0$, $w_0 = 1$ and $x_0 \sim p_0$, so $m_0(y) = f_0(y) / Z_0$.

Assume the formula for $j - 1$. Let $A = \{x : f_{j-1}(x) > 0\}$. By the consequence for $j - 1$, a run with $w_{j-1} > 0$ has $x_{j-1} \in A$, where the ratio $r(x) = f_j(x) / f_{j-1}(x)$ is defined, and a run with $w_{j-1} = 0$ has $w_j = 0$. Given $x_{j-1}$, the state $x_j$ is drawn from $K_j(x_{j-1}, \cdot)$ independently of $w_{j-1}$. So
$$m_j(y) = \sum_{x \in A} \mathbb{E}\big[w_{j-1} [x_{j-1} = x]\big] \, r(x) \, K_j(x, y) = \sum_{x \in A} \frac{f_{j-1}(x)}{Z_0} \cdot \frac{f_j(x)}{f_{j-1}(x)} \, K_j(x, y) = \frac{1}{Z_0} \sum_{x \in A} f_j(x) K_j(x, y).$$
By the support condition, every $x \notin A$ has $f_j(x) = 0$, so the last sum equals the sum over all $x$. By (1),
$$m_j(y) = \frac{1}{Z_0} \sum_x f_j(x) K_j(x, y) = \frac{f_j(y)}{Z_0}. \qquad \square$$

Without the support condition, the states with $f_{j-1}(x) = 0 < f_j(x)$ are never reached with positive weight, so $m_j(y) \le f_j(y) / Z_0$ only, and $\mathbb{E}[w_T]$ can be smaller than $Z_T / Z_0$.

**Theorem 1 (unbiased estimate of the ratio).** For one run, $\mathbb{E}[w_T] = Z_T / Z_0$. For $s$ independent runs and every $s \ge 1$,
$$\mathbb{E}\Big[\frac{Z_0}{s} \sum_{r=1}^{s} w^{(r)}\Big] = Z_T.$$

*Proof.* Sum Lemma 1 over $y$ for $j = T$: $\mathbb{E}[w_T] = \sum_y f_T(y) / Z_0 = Z_T / Z_0$. The runs are identically distributed, and the expectation is linear. $\square$

**Theorem 2 (weighted expectations).** For a function $h$ with $\mathbb{E}_{p_T}|h| < \infty$, $\mathbb{E}[w_T \, h(x_T)] = (Z_T / Z_0) \, \mathbb{E}_{p_T}[h]$. The self-normalized estimate
$$\hat\mu_s = \frac{\sum_r w^{(r)} h(x^{(r)}_T)}{\sum_r w^{(r)}}$$
converges almost surely to $\mathbb{E}_{p_T}[h]$ as $s \to \infty$.

*Proof.* By Lemma 1, $\mathbb{E}[w_T h(x_T)] = \sum_y h(y) f_T(y) / Z_0 = (Z_T / Z_0) \sum_y h(y) p_T(y)$; the sum converges absolutely because $\mathbb{E}_{p_T}|h| < \infty$. The numerator and the denominator of $\hat\mu_s$, each divided by $s$, are averages of i.i.d. terms with finite means $(Z_T / Z_0) \mathbb{E}_{p_T}[h]$ and $Z_T / Z_0 > 0$. By the strong law of large numbers, both converge almost surely, and so does their ratio. $\square$

The ratio estimate $\hat\mu_s$ is biased for finite $s$, as for every self-normalized importance sampler.

**Theorem 3 (the log estimate is a stochastic lower bound).** Let $\hat Z = (Z_0 / s) \sum_r w^{(r)}$. Then $\mathbb{E}[\log \hat Z] \le \log Z_T$, and for every $b > 0$,
$$P\big(\log \hat Z > \log Z_T + b\big) \le e^{-b}.$$

*Proof.* The logarithm is concave, so by Jensen's inequality and Theorem 1, $\mathbb{E}[\log \hat Z] \le \log \mathbb{E}[\hat Z] = \log Z_T$. For the tail, $\hat Z \ge 0$ and $\mathbb{E}[\hat Z] = Z_T$, so Markov's inequality gives $P(\hat Z > e^{b} Z_T) \le e^{-b}$. $\square$

**Remarks.**

1. The kernels need only the invariance (1). They do not need to be reversible, and they do not need to mix. With $K_j(x, y) = [x = y]$, which leaves every distribution invariant, the weight telescopes to $f_T(x_0) / f_0(x_0)$, and the method is plain importance sampling with the proposal $p_0$.
2. The final state $x_T$ alone is not a draw from $p_T$. Only the weighted pair $(w_T, x_T)$ has the property of Theorem 2.
3. The proof shows where the order of lines L5 and L6 matters. The weight factor at step $j$ is evaluated at the state *before* the kernel $K_j$ moves it. If the kernel $K_j$ came first and the ratio were taken at its output, $m_j(y)$ would be $\sum_x (f_{j-1}(x) / Z_0) K_j(x, y) \cdot f_j(y) / f_{j-1}(y)$, which is not $f_j(y) / Z_0$ in general, because $K_j$ leaves $p_j$ invariant and not $p_{j-1}$. The other correct order uses $K_{j-1}$ first and then the ratio, which is the same algorithm with the indices shifted.
