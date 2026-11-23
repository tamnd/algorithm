---
title: DP-SGD with Poisson sampling is (epsilon, delta)-DP with the epsilon of the Renyi accountant
proves: [correctness]
status: partial
---

The neighbor relation is add/remove: $D' = D \cup \{x\}$ for one example $x$. One step of DP-SGD (lines L3 to L7) maps the current parameter $\theta$ to a new one. The released output is the sequence of parameters. Write $s = \sigma C$, $\mathcal N_\mu = \mathcal N(\mu, s^2 I)$ in $\mathbb R^d$, and, for $\alpha > 1$, the Renyi divergence

$$D_\alpha(P \,\|\, Q) = \frac{1}{\alpha - 1} \ln \int p(z)^\alpha q(z)^{1 - \alpha}\, dz.$$

A mechanism is $(\alpha, \rho)$-RDP when $D_\alpha(M(D) \,\|\, M(D')) \le \rho$ for both orders of every pair of neighbors.

The proof is complete except for Lemma 4, which is quoted from Mironov, Talwar and Zhang (2019, Section 3.1, Theorem 5). The status is partial for that reason.

**Lemma 1 (clipping).** For every $g \in \mathbb R^d$, the vector $\bar g = g/\max(1, \|g\|/C)$ of line L5 has $\|\bar g\| \le C$, and $\bar g = g$ when $\|g\| \le C$.

*Proof.* If $\|g\| \le C$ the divisor is 1. Otherwise the divisor is $\|g\|/C$ and $\|\bar g\| = C$. $\square$

**Lemma 2 (the Gaussian at a shift).** For $\mu_0 = \mathcal N(0, \sigma^2)$ and $\mu_1 = \mathcal N(r, \sigma^2)$ on $\mathbb R$ and every integer $k \ge 0$, $\mathbb E_{z \sim \mu_0}[(\mu_1(z)/\mu_0(z))^k] = \exp\big(k(k - 1) r^2/(2\sigma^2)\big)$.

*Proof.* The ratio is $\exp((2rz - r^2)/(2\sigma^2))$. For $z \sim \mathcal N(0, \sigma^2)$, $\mathbb E[e^{tz}] = e^{t^2\sigma^2/2}$. With $t = kr/\sigma^2$ this gives $\exp(k^2 r^2/(2\sigma^2) - k r^2/(2\sigma^2))$. $\square$

**Lemma 3 (one step, from $D'$ to $D$).** Fix $\theta$ and an integer $\alpha \ge 2$, and let $P$ and $P'$ be the laws of the noisy sum $G$ of line L6 on $D$ and on $D'$. Then $\int p'^\alpha p^{1 - \alpha} \le A_\alpha$, where

$$A_\alpha = \sum_{k=0}^{\alpha} \binom{\alpha}{k} (1 - q)^{\alpha - k} q^k \exp\!\left(\frac{k^2 - k}{2\sigma^2}\right).$$

*Proof.* Line L3 draws a Poisson sample. On $D'$ it is a sample $T$ of $D$, plus $x$ with probability $q$, independently. Let $S_T$ be the sum of the clipped gradients of $T$ and $v$ the clipped gradient of $x$, so $\|v\| \le C$ by Lemma 1. Then

$$P = \mathbb E_T\big[\mathcal N_{S_T}\big], \qquad P' = \mathbb E_T\big[(1 - q)\mathcal N_{S_T} + q\,\mathcal N_{S_T + v}\big].$$

The map $(a, b) \mapsto a^\alpha b^{1 - \alpha}$ on $a \ge 0$, $b > 0$ is the perspective $b\,\phi(a/b)$ of the convex function $\phi(u) = u^\alpha$, so it is jointly convex. By Jensen's inequality over $T$, pointwise in $z$, and then by Fubini,

$$\int p'^\alpha p^{1 - \alpha} \le \mathbb E_T \int \big((1 - q)\mathcal N_{S_T} + q\,\mathcal N_{S_T + v}\big)^\alpha \mathcal N_{S_T}^{1 - \alpha}.$$

Each inner integral does not change under the shift by $-S_T$ and under a rotation that maps $v$ to $(\|v\|, 0, \ldots, 0)$. After that, the coordinates other than the first have the same law under both terms and integrate to 1. Divide the first coordinate by $C$; this changes the variance to $\sigma^2$ and the shift to $r = \|v\|/C \le 1$, and it does not change the integral. Expanding the $\alpha$-th power by the binomial theorem and using Lemma 2 gives

$$\sum_{k=0}^{\alpha} \binom{\alpha}{k}(1 - q)^{\alpha - k} q^k \exp\!\left(\frac{(k^2 - k) r^2}{2\sigma^2}\right) \le A_\alpha,$$

because $k^2 - k \ge 0$ and $r \le 1$. $\square$

**Lemma 4 (the other order; Mironov, Talwar and Zhang, Theorem 5).** With $\mu_0 = \mathcal N(0, \sigma^2)$ and $\mu = (1 - q)\mu_0 + q\,\mathcal N(r, \sigma^2)$, $B_\alpha = \mathbb E_{\mu}[(\mu_0/\mu)^{\alpha}] \le A_\alpha = \mathbb E_{\mu_0}[(\mu/\mu_0)^{\alpha}]$ for every integer $\alpha \ge 2$.

The same convexity and reduction steps as in Lemma 3 bound $\int p^\alpha p'^{1 - \alpha}$ by $B_\alpha$ at a shift $r = \|v\|/C$. By Lemma 4, this is at most $A_\alpha$ at the same $r$, and the binomial form shows that $A_\alpha$ grows with $r$, so it is at most $A_\alpha$ at $r = 1$.

**Theorem 1 (one step).** For every integer $\alpha \ge 2$ and every fixed $\theta$, one step is $(\alpha, \rho_\alpha)$-RDP with $\rho_\alpha = \ln(A_\alpha)/(\alpha - 1)$, the value of `rdp_sampled_gaussian`. For $q = 1$, $\rho_\alpha = \alpha/(2\sigma^2)$.

*Proof.* Lemmas 3 and 4 bound both orders. Line L7 is a fixed function of $G$ and $\theta$, and the Renyi divergence does not grow under a fixed function (the data-processing inequality), so the bound holds for the new $\theta$. For $q = 1$, only the term $k = \alpha$ is left, and it is $\exp((\alpha^2 - \alpha)/(2\sigma^2))$. $\square$

**Theorem 2 (T steps).** The sequence $\theta_1, \ldots, \theta_T$ is $(\alpha, T\rho_\alpha)$-RDP.

*Proof.* By induction on $T$. Let $Y$ be the first $T - 1$ outputs and $Z$ the last, with densities $p(y)p(z \mid y)$ on $D$ and $p'(y)p'(z \mid y)$ on $D'$. For each $y$, Theorem 1 at $\theta = \theta_{T-1}(y)$ gives $\int p(z \mid y)^\alpha p'(z \mid y)^{1 - \alpha} dz \le e^{(\alpha - 1)\rho_\alpha}$. So

$$\int\!\!\int (p(y)p(z \mid y))^\alpha (p'(y)p'(z \mid y))^{1 - \alpha} \le e^{(\alpha - 1)\rho_\alpha} \int p(y)^\alpha p'(y)^{1 - \alpha} \le e^{(\alpha - 1)T\rho_\alpha},$$

by the induction hypothesis. The other order is the same. $\square$

**Theorem 3 (conversion; Mironov 2017).** If a mechanism is $(\alpha, \rho)$-RDP, then for every $\delta \in (0, 1)$ it is $(\rho + \ln(1/\delta)/(\alpha - 1), \delta)$-DP. So DP-SGD is $(\varepsilon, \delta)$-DP under add/remove for the $\varepsilon$ that `epsilon_for` returns, which is the smallest such value over the listed orders.

*Proof.* Let $P$, $Q$ be the output laws on two neighbors, $\varepsilon = \rho + \ln(1/\delta)/(\alpha - 1)$, and $L = \{z : p(z) > e^{\varepsilon} q(z)\}$. For every event $S$, $P(S) \le e^{\varepsilon} Q(S) + P(L)$. On $L$, $(p/q)^{\alpha - 1} > e^{(\alpha - 1)\varepsilon}$, so by Markov's inequality

$$P(L) \le e^{-(\alpha - 1)\varepsilon}\, \mathbb E_P\big[(p/q)^{\alpha - 1}\big] = e^{-(\alpha - 1)\varepsilon} e^{(\alpha - 1)\rho} = \delta.$$

The other order is the same. Each order of the list gives a valid $\varepsilon$, so the smallest one is valid. $\square$

Theorems 1 to 3 give the privacy claim of the code for the step count, rate, noise and $\delta$ passed to `epsilon_for`. They do not say anything about the accuracy of the model, which is measured, not proved. They need the real-valued Gaussian noise and the exact Poisson sampling of the analysis; the floats and the seeded generator of the code do not give this, so the code is a model of the algorithm and not a safe deployment. $\blacksquare$
