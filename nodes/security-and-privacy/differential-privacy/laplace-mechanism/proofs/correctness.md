---
title: The Laplace mechanism samples the right noise, is epsilon-DP, and is accurate
proves: [correctness]
status: full
---

We work in the real RAM. Fix a neighbor relation $\sim$, a query $f$ with values in $\mathbb R^k$, a number $\Delta \ge \Delta_1 f = \max_{x \sim x'} \lVert f(x) - f(x') \rVert_1$, and $\varepsilon > 0$. Let $b = \Delta / \varepsilon$ (line L1). We write $p_b(z) = \frac{1}{2b} e^{-|z|/b}$ for the density of $\mathrm{Lap}(b)$ and $F_b$ for its distribution function.

**Lemma 1 (the sampler).** If $u$ is uniform on $(-1/2, 1/2)$, then $z = -b\,\mathrm{sgn}(u) \ln(1 - 2|u|)$ of line L5 has the distribution $\mathrm{Lap}(b)$.

*Proof.* Let $w = u + 1/2$, which is uniform on $(0, 1)$. We show that $z = F_b^{-1}(w)$. If $w < 1/2$, then $u < 0$ and $z = b \ln(1 - 2|u|) = b \ln(2w)$. This is negative, and $F_b(z) = \frac12 e^{z/b} = \frac12 \cdot 2w = w$. If $w \ge 1/2$, then $u \ge 0$ and $z = -b \ln(1 - 2u) = -b \ln(2 - 2w) \ge 0$, and $F_b(z) = 1 - \frac12 e^{-z/b} = 1 - (1 - w) = w$. ($u = 0$ gives $z = 0$ with either sign.) $F_b$ is continuous and strictly increasing, so $\Pr[z \le t] = \Pr[w \le F_b(t)] = F_b(t)$ for every $t$. $\square$

So, by Lemma 1 and because each pass of line L3 draws a fresh $u$, the output of line L7 is $y = f(x) + Z$ with $Z = (Z_1, \ldots, Z_k)$ and $Z_i$ independent $\mathrm{Lap}(b)$. Its density at $y \in \mathbb R^k$ is

$$p_x(y) = \prod_{i=1}^{k} \frac{1}{2b} \exp\Big(-\frac{|y_i - f(x)_i|}{b}\Big).$$

**Theorem 1 (privacy).** For all $x \sim x'$ and every measurable set $S \subseteq \mathbb R^k$, $\Pr[M(x) \in S] \le e^{\varepsilon} \Pr[M(x') \in S]$, where $M$ is LAPLACE-MECHANISM with the parameters above.

*Proof.* Fix $x \sim x'$ and $y \in \mathbb R^k$. For each $i$, the triangle inequality gives $|y_i - f(x')_i| - |y_i - f(x)_i| \le |f(x)_i - f(x')_i|$. So

$$\frac{p_x(y)}{p_{x'}(y)} = \exp\Big(\frac{1}{b} \sum_{i=1}^{k} \big(|y_i - f(x')_i| - |y_i - f(x)_i|\big)\Big) \le \exp\Big(\frac{\lVert f(x) - f(x') \rVert_1}{b}\Big) \le \exp\Big(\frac{\Delta_1 f}{\Delta / \varepsilon}\Big) \le e^{\varepsilon}.$$

The last step uses $\Delta \ge \Delta_1 f$. Both densities are positive everywhere, so $p_x(y) \le e^{\varepsilon} p_{x'}(y)$ for all $y$. The integral over $S$ gives

$$\Pr[M(x) \in S] = \int_S p_x(y)\,dy \le e^{\varepsilon} \int_S p_{x'}(y)\,dy = e^{\varepsilon} \Pr[M(x') \in S].$$

The relation $\sim$ is symmetric, so the same holds with $x$ and $x'$ swapped. $\square$

**Theorem 2 (accuracy).** For $0 < \beta < 1$, $\Pr\big[\max_i |y_i - f(x)_i| > b \ln(k/\beta)\big] \le \beta$.

*Proof.* For $t \ge 0$, $\Pr[|Z_i| > t] = 2 \int_t^\infty \frac{1}{2b} e^{-z/b}\,dz = e^{-t/b}$. Take $t = b \ln(k/\beta)$, so that $e^{-t/b} = \beta / k$. The union bound over the $k$ coordinates gives $\Pr[\exists i : |Z_i| > t] \le k \cdot \beta / k = \beta$. Since $y_i - f(x)_i = Z_i$, this is the claim. $\square$

**Termination.** The loop of line L3 runs $k$ times. Line L4 draws again only on the event $u = -1/2$, which has probability 0 in the real RAM, so each pass ends with probability 1.

Lemma 1, Theorem 1 and Theorem 2 together show that the output has the stated distribution, is $\varepsilon$-differentially private under the relation for which $\Delta \ge \Delta_1 f$, and has error at most $(\Delta/\varepsilon) \ln(k/\beta)$ in every coordinate with probability at least $1 - \beta$. $\blacksquare$
