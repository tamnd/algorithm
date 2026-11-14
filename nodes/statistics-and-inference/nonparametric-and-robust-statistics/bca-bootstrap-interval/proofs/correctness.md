---
title: The BCa interval computes Efron's adjusted percentiles and is exact in his transformation model
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. $G$ is the bootstrap distribution function of $\hat\theta^*$, $\hat G_b$ the empirical distribution function of the $b$ replicates, $\Phi$ the standard normal distribution function and $z_p = \Phi^{-1}(p)$. For any distribution function $K$, $K^{-1}(p) = \inf\{t : K(t) \ge p\}$.

This file proves what the algorithm computes, two invariance facts, and exact coverage in an idealized model. It does not prove a coverage level for a general $F$; that coverage is measured on the page.

**Claim 1 (the algorithm computes the formulas).** Line L6 sets $z_0 = \Phi^{-1}(\hat G_b(\hat\theta^-))$, where $\hat G_b(\hat\theta^-) = c/b$ is the fraction of replicates below $\hat\theta$. Line L9 returns $[\hat G_b^{-1}(\alpha_1), \hat G_b^{-1}(\alpha_2)]$. If $z_0 = 0$ and $a = 0$, then $\alpha_1 = \alpha/2$ and $\alpha_2 = 1 - \alpha/2$, and the result is the percentile interval computed from the same replicates.

*Proof.* The first statement is the definition of $c$. For the second, $\alpha_1, \alpha_2 \in (0, 1)$ because they are values of $\Phi$, and the quantile rule of the percentile interval (its Claim 1) shows that $\theta^*_{(\lceil b p \rceil)} = \hat G_b^{-1}(p)$ for $0 < p < 1$. For the third, put $z_0 = a = 0$ in line L8: $\alpha_1 = \Phi(z_{\alpha/2}) = \alpha/2$ and $\alpha_2 = \Phi(z_{1-\alpha/2}) = 1 - \alpha/2$. $\square$

**Claim 2 (z0 is invariant).** Let $g$ be strictly increasing on a set that contains every value of $s$. If the algorithm runs on the statistic $g \circ s$ with the same random numbers, line L6 gives the same $z_0$.

*Proof.* Lines L2 to L4 draw the indices without looking at the statistic, so the replicates of the second run are $g(\theta^*_j)$, and its estimate is $g(\hat\theta)$. Since $g$ is strictly increasing, $g(\theta^*_j) < g(\hat\theta)$ exactly when $\theta^*_j < \hat\theta$, so $c$ is the same. $\square$

**Claim 3 (transformation respecting for a fixed a).** Under the conditions of Claim 2, and with the same fixed value of $a$ in both runs, if the first run returns $[L, U]$ the second returns $[g(L), g(U)]$.

*Proof.* By Claim 2, $z_0$ is the same, and $a$ and $\alpha$ are the same, so line L8 gives the same $\alpha_1$ and $\alpha_2$, and line L9 uses the same ranks $\lceil b\alpha_1 \rceil$ and $\lceil b\alpha_2 \rceil$. A strictly increasing $g$ keeps the order of the replicates, so the replicate of each rank in the second run is $g$ of the replicate of that rank in the first run. $\square$

The jackknife value of line L7 is a function of the leave-one-out estimates $\hat\theta_{(i)}$, and $g$ changes their spacings: $g(\hat\theta_{(\cdot)})$ is not the mean of the $g(\hat\theta_{(i)})$, and the skewness of the differences changes. So the full algorithm respects transformations only approximately. On the page, $a$ is $0.0784$ for the mean and $0.0875$ for the log of the mean. The tests check both facts: exact equality with a fixed $a$, and a different jackknife $a$ after the logarithm.

**Claim 4 (exact coverage in the transformation model).** Suppose there are numbers $z_0$ and $a$ and a strictly increasing bijection $\phi$ from the parameter range onto $\mathbb{R}$ such that, with $\psi = \phi(\theta)$, $\hat\psi = \phi(\hat\theta)$ and $Z$ standard normal,

$$\hat\psi = \psi + (1 + a\psi)(Z - z_0), \qquad 1 + a\psi > 0,$$

and the bootstrap follows the same model with $\hat\psi$ in place of $\psi$: $\phi(\hat\theta^*) = \hat\psi + (1 + a\hat\psi)(Z^* - z_0)$ with $Z^*$ standard normal under $P^*$. Let $E$ be the event $1 + a(Z - z_0) > 0$, and suppose $1 - a(z_0 + z) > 0$ for $z = z_{\alpha/2}$ and $z = z_{1-\alpha/2}$. Then on $E$ the ideal interval $[G^{-1}(\alpha_1), G^{-1}(\alpha_2)]$ is defined, and

$$\bigl\lvert P\bigl(G^{-1}(\alpha_1) \le \theta \le G^{-1}(\alpha_2)\bigr) - (1 - \alpha) \bigr\rvert \le P(E^c).$$

If $a = 0$, $E$ is the whole space and the coverage is exactly $1 - \alpha$.

*Proof.* From the model, $1 + a\hat\psi = (1 + a\psi) + a(1 + a\psi)(Z - z_0) = (1 + a\psi)\bigl(1 + a(Z - z_0)\bigr)$, which is positive exactly on $E$. On $E$ the bootstrap law is

$$G(t) = P^*\bigl(\phi(\hat\theta^*) \le \phi(t)\bigr) = \Phi\Bigl(\frac{\phi(t) - \hat\psi}{1 + a\hat\psi} + z_0\Bigr),$$

which is continuous and strictly increasing with range $(0, 1)$. In particular $G(\hat\theta) = \Phi(z_0)$, so the ideal value of line L6 is the true $z_0$.

Fix $z \in \{z_{\alpha/2}, z_{1-\alpha/2}\}$, let $w = z_0 + z$ and $p = \Phi(z_0 + w/(1 - a w))$, which is $\alpha_1$ or $\alpha_2$. Solving $G(t) = p$ gives the endpoint $t_z = G^{-1}(p)$ with

$$\phi(t_z) = \hat\psi + (1 + a\hat\psi)\frac{w}{1 - a w}, \qquad 1 + a\phi(t_z) = \frac{1 + a\hat\psi}{1 - a w} = \frac{(1 + a\psi)\bigl(1 + a(Z - z_0)\bigr)}{1 - a w}.$$

Now compare $\theta$ with $t_z$, which is the same as comparing $\psi$ with $\phi(t_z)$.

- If $a > 0$: $\psi \le \phi(t_z)$ is the same as $1 + a\psi \le 1 + a\phi(t_z)$. Divide by $1 + a\psi > 0$ and multiply by $1 - a w > 0$: this is $1 - a w \le 1 + a(Z - z_0)$, that is $-a z \le a Z$, that is $Z \ge -z$.
- If $a < 0$: $\psi \le \phi(t_z)$ is the same as $1 + a\psi \ge 1 + a\phi(t_z)$, which by the same steps is $-a z \ge a Z$, that is again $Z \ge -z$.
- If $a = 0$: $\phi(t_z) = \hat\psi + w = \psi + Z - z_0 + z_0 + z$, so $\psi \le \phi(t_z)$ is $Z \ge -z$.

So on $E$, $\theta \le G^{-1}(\alpha_2)$ exactly when $Z \ge -z_{1-\alpha/2} = z_{\alpha/2}$, and $\theta \ge G^{-1}(\alpha_1)$ exactly when $Z \le -z_{\alpha/2} = z_{1-\alpha/2}$. The coverage event therefore agrees on $E$ with the event $z_{\alpha/2} \le Z \le z_{1-\alpha/2}$, which has probability $1 - \alpha$. Two events that agree on $E$ differ in probability by at most $P(E^c)$. $\square$

For $a > 0$, $P(E^c) = \Phi(z_0 - 1/a)$, and for $a < 0$ it is $\Phi(-z_0 - 1/\lvert a \rvert)$; both are at most $\Phi(\lvert z_0 \rvert - 1/\lvert a \rvert)$. With the values of the page, $z_0 = 0.109$ and $a = 0.0784$, this is $\Phi(-12.6)$, which is below $10^{-35}$. The model needs the exception because a normal $Z$ is unbounded while $1 + a\hat\psi$ must stay positive.

The method does not need to know $\phi$; it uses only $G$, $z_0$ and $a$. The two inputs are the two departures from Claim 4 of the percentile interval: $z_0$ allows a median bias on the normalized scale, and $a$ lets the standard deviation $1 + a\psi$ change with the parameter.

**What is not proved.** For a real $F$, the transformation model holds only approximately, the jackknife value of $a$ is an estimate, and the bootstrap law is discrete. Efron (1987) and Hall (1988) show under smoothness conditions that the one-sided coverage error is $O(n^{-1})$. This file does not reproduce those expansions. The coverages on the page come from a simulation with stated seeds, with a Monte Carlo standard error of about $0.007$.

**Cost.** Lines L2 to L4 cost $\Theta(b \cdot (n + C_s(n)))$, where $C_s(n)$ is the cost of $s$. Line L5 sorts and counts in $\Theta(b \log b)$. Line L7 evaluates $s$ on $n$ samples of size $n - 1$, which costs $\Theta(n\, C_s(n - 1))$, that is $\Theta(n^2)$ for a linear-time statistic. Lines L6, L8 and L9 take constant time. The extra space is $\Theta(b + n)$.
