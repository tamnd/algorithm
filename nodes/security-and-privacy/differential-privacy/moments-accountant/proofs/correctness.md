---
title: The moments accountant gives a valid (epsilon, delta) bound for the subsampled Gaussian
proves: [correctness]
status: full
---

We work in the real RAM. One step of the mechanism, with the outputs of the earlier steps fixed, is as follows. Each record of the dataset is kept independently with probability $q$; this gives the batch $B$. Each record $i$ has a vector $g_i \in \mathbb R^d$ with $\lVert g_i \rVert_2 \le 1$, which may depend on the earlier outputs. The step releases $s_B + N(0, \sigma^2 I_d)$, where $s_B = \sum_{i \in B} g_i$. Neighbors are add/remove: $x' = x \cup \{r\}$.

For distributions $P, Q$ with positive densities $p, q$ and $\lambda > 0$, write

$$c_\lambda(P\|Q) = \ln \int p^{\lambda + 1}q^{-\lambda} = \ln E_{Y \sim P}\left[e^{\lambda \ell(Y)}\right], \qquad \ell = \ln\frac{p}{q}.$$

Let $\varphi_c$ be the density of $N(c, \sigma^2)$ on $\mathbb R$, and for $a = \lambda + 1$ and $c \ge 0$ let

$$A_a(c) = \sum_{k=0}^{a}\binom{a}{k}(1-q)^{a-k}q^k e^{(k^2 - k)c^2/(2\sigma^2)}.$$

So $A_a = A_a(1)$ is the sum of the page.

**Lemma 1 (Gaussian moments).** For every integer $k \ge 0$ and $c \ge 0$, $\int \varphi_0 (\varphi_c/\varphi_0)^k = e^{(k^2 - k)c^2/(2\sigma^2)}$. Hence $\int ((1-q)\varphi_0 + q\varphi_c)^a\varphi_0^{1-a} = A_a(c)$.

*Proof.* $\varphi_c(z)/\varphi_0(z) = \exp((2cz - c^2)/(2\sigma^2))$. For $Z \sim N(0, \sigma^2)$, $E[e^{tZ}] = e^{t^2\sigma^2/2}$. With $t = kc/\sigma^2$,
$$E\left[(\varphi_c/\varphi_0)^k(Z)\right] = e^{-kc^2/(2\sigma^2)}e^{k^2c^2/(2\sigma^2)}.$$
For the second claim write the integrand as $\varphi_0 \cdot (1 - q + qR)^a$ with $R = \varphi_c/\varphi_0$, expand by the binomial theorem, and apply the first claim to each term. $\square$

**Lemma 2 (lines L2 to L4).** For each $\lambda$, the value $\alpha$ of line L4 equals $\ln A_{\lambda + 1}$.

*Proof.* Line L2 sets $a = \lambda + 1$. Each term of $A_a$ with a non-zero coefficient is positive, and line L3 computes its log $t_k$; the terms that are 0 (the cases $q = 0$, $k > 0$ and $q = 1$, $k < a$) are left out and do not change the sum. At least one term remains. With $M = \max_k t_k$, line L4 returns $M + \ln\sum_k e^{t_k - M} = \ln\sum_k e^{t_k} = \ln A_a$. $\square$

**Lemma 3 (one step, larger dataset first).** Fix the earlier outputs. Let $P$ and $P'$ be the laws of the step on $x$ and on $x' = x \cup \{r\}$. Then $c_\lambda(P'\|P) \le \ln A_{\lambda + 1}$ for every integer $\lambda \ge 1$.

*Proof.* Let $a = \lambda + 1$, and let $p_B$ be the density of $N(s_B, \sigma^2 I)$. A Poisson sample of $x'$ is $B$, or $B \cup \{r\}$ with probability $q$, independently of $B$. So
$$p = E_B[p_B], \qquad p' = E_B[p'_B], \qquad p'_B = (1 - q)p_B + q\,p_{B}(\cdot - g_r).$$
The map $(u, v) \mapsto u^a v^{1-a} = v(u/v)^a$ on $(0, \infty)^2$ is the perspective of the convex function $u \mapsto u^a$, so it is jointly convex. $B$ takes finitely many values, so Jensen's inequality at each point $y$ gives $p'(y)^a p(y)^{1-a} \le E_B[p'_B(y)^a p_B(y)^{1-a}]$. Integrate over $y$ and swap the integral and the finite average:
$$\int p'^a p^{1-a} \le E_B \int (p'_B)^a p_B^{1-a}.$$
Fix $B$. Translate by $s_B$ and rotate so that $g_r = c\,e_1$ with $c = \lVert g_r \rVert_2 \le 1$. Both densities are products of the same factor in coordinates $2, \ldots, d$, which integrates to 1, and of $(1-q)\varphi_0 + q\varphi_c$ and $\varphi_0$ in coordinate 1. By Lemma 1 the inner integral is $A_a(c)$. Every exponent $(k^2 - k)c^2/(2\sigma^2)$ is non-negative and grows with $c$, so $A_a(c) \le A_a(1) = A_a$. Hence $\int p'^a p^{1-a} \le A_a$, and $c_\lambda(P'\|P) = \ln\int p'^a p^{1-a} \le \ln A_a$. $\square$

**Lemma 4 (one step, smaller dataset first).** With the notation of Lemma 3, $c_\lambda(P\|P') \le \ln A_{\lambda + 1}$ for every integer $\lambda \ge 1$.

*Proof.* The joint convexity step of Lemma 3, with the roles of the two arguments swapped, reduces the claim to $B_a(c) \le A_a(1)$, where $B_a(c) = \int \varphi_0^a((1-q)\varphi_0 + q\varphi_c)^{1-a}$ and $c \le 1$. If $c = 0$, then $B_a(0) = 1 \le A_a(1)$. For $c > 0$, the pair with shift $c$ and noise $\sigma$ is the pair with shift 1 and noise $\sigma/c$ after a scaling of the axis, and scaling does not change these integrals. Mironov, Talwar and Zhang (arXiv 1908.10530, Section 3.1 with Theorem 4) prove $B_a \le A_a$ for shift 1 and every noise level. So $B_a(c) \le A_a(c) \le A_a(1)$ by the monotonicity in Lemma 3. This is the one step that we cite and do not prove here. $\square$

**Lemma 5 (adaptive composition).** Let $Y = (Y_1, \ldots, Y_T)$ be the outputs of $T$ steps on a dataset with law $P$, and on its neighbor with law $Q$. If, for each $t$ and each fixed prefix $y_{<t}$, the conditional laws satisfy $c_\lambda(P_t(\cdot \mid y_{<t})\|Q_t(\cdot \mid y_{<t})) \le \alpha$, then $c_\lambda(P\|Q) \le T\alpha$.

*Proof.* The privacy loss of the whole output is $\ell(y) = \sum_t \ell_t(y_t \mid y_{<t})$, the sum of the conditional privacy losses, because the densities factor as products of the conditional densities. Then
$$E_P\left[e^{\lambda\ell(Y)}\right] = E_P\left[e^{\lambda\sum_{t < T}\ell_t}\,E_P\left[e^{\lambda\ell_T} \mid Y_{<T}\right]\right] \le e^{\alpha}E_P\left[e^{\lambda\sum_{t < T}\ell_t}\right],$$
and induction on $T$ gives $e^{T\alpha}$. $\square$

**Lemma 6 (tail bound to DP).** Let $L = \ell(Y)$ with $Y \sim P$. If $\Pr[L > \varepsilon] \le \delta$, then $P(S) \le e^{\varepsilon}Q(S) + \delta$ for every event $S$.

*Proof.* On the set $\{\ell \le \varepsilon\}$ we have $p \le e^{\varepsilon}q$. So $P(S) = P(S \cap \{\ell \le \varepsilon\}) + P(S \cap \{\ell > \varepsilon\}) \le e^{\varepsilon}Q(S) + \delta$. $\square$

**Theorem.** The output $\varepsilon^*$ of MOMENTS-ACCOUNTANT$(q, \sigma, T, \delta, m)$ makes the $T$ composed steps $(\varepsilon^*, \delta)$-DP under add/remove neighbors.

*Proof.* Fix neighbors and either order of the pair, and fix $\lambda \in \{1, \ldots, m\}$. Let $\alpha = \ln A_{\lambda + 1}$, the value of line L4 by Lemma 2. Lemmas 3 and 4 bound the conditional log moment of each step by $\alpha$ in both orders and for every prefix, so Lemma 5 gives $E[e^{\lambda L}] \le e^{T\alpha}$ for the privacy loss $L$ of the $T$ outputs. With $\varepsilon_\lambda = (T\alpha + \ln(1/\delta))/\lambda$ of line L5, Markov's inequality gives
$$\Pr[L > \varepsilon_\lambda] = \Pr\left[e^{\lambda L} > e^{\lambda\varepsilon_\lambda}\right] \le e^{T\alpha - \lambda\varepsilon_\lambda} = e^{-\ln(1/\delta)} = \delta.$$
By Lemma 6, the composition is $(\varepsilon_\lambda, \delta)$-DP for this ordered pair, and so for all of them. Lines L6 and L7 return the smallest $\varepsilon_\lambda$ over $\lambda \le m$, which is one of these valid values. The loop of line L1 runs $m$ times, and the inner work is $O(\lambda)$, so the procedure stops. $\blacksquare$
