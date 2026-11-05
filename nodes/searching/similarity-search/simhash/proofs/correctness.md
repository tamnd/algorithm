---
title: SimHash bits are random hyperplane bits, and their Hamming distance concentrates around θ/π
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. A document is a finite set $F$ of features with weights $w(f) > 0$, viewed as the vector $x$ with $x_f = w(f)$ on $F$ and $x_f = 0$ on the other features.

**Lemma 1 (the counters).** For the $\pm 1$ version, after the loop of line L2, $V[i] = \sum_{f \in F} w(f)\,\sigma_i(f)$, where $\sigma_i(f) = +1$ if bit $i$ of $H(f)$ is 1 and $-1$ otherwise. For the Gaussian variant, $V[i] = \sum_{f \in F} w(f)\, g_i(f)$.

*Proof.* Line L1 sets $V[i] = 0$. Line L5, executed once for each pair $(f, i)$, adds $w(f)\sigma_i(f)$ to $V[i]$ and changes no other counter. Addition is commutative, so after all features $V[i]$ is the sum. The Gaussian variant is the same with $g_i(f)$. $\square$

So bit $i$ of the fingerprint is $1$ exactly when $x \cdot \sigma_i > 0$ (or $x \cdot g_i > 0$), where $\sigma_i = (\sigma_i(f))_f$. For two documents $x$ and $y$, only the features in $G = F_x \cup F_y$ matter, so we work in $\mathbb{R}^G$.

**Theorem 1 (Gaussian variant).** Assume that the values $g_i(f)$, for $f \in G$ and $1 \le i \le b$, are independent $N(0, 1)$. Let $\theta$ be the angle between $x$ and $y$ in $\mathbb{R}^G$, and let $X_i = 1$ if bit $i$ of the two fingerprints differs. Then the $X_i$ are independent, $\Pr[X_i = 1] = \theta/\pi$, and the Hamming distance $D = \sum_i X_i$ satisfies $\mathbb{E}[D] = b\theta/\pi$ and $\Pr[|D/b - \theta/\pi| \ge \varepsilon] \le 2e^{-2b\varepsilon^2}$ for every $\varepsilon > 0$.

*Proof.* Fix $i$. The vector $g_i = (g_i(f))_{f \in G}$ has independent $N(0,1)$ coordinates. By Lemma 1 of the proof on the [random hyperplane LSH](/random-hyperplane-lsh/) page, the events $g_i \cdot x \ge 0$ and $g_i \cdot y \ge 0$ disagree with probability $\theta/\pi$. Line L6 uses $> 0$ instead of $\ge 0$; the two rules differ only when $g_i \cdot x = 0$ or $g_i \cdot y = 0$, and each is a linear form with a nonzero coefficient vector in Gaussian variables, which is $0$ with probability $0$. So $\Pr[X_i = 1] = \theta/\pi$. The variable $X_i$ is a function of $g_i$ alone, and the vectors $g_1, \ldots, g_b$ are independent, so the $X_i$ are independent. Linearity of expectation gives $\mathbb{E}[D] = b\theta/\pi$. The $X_i$ take values in $[0, 1]$, so Hoeffding's inequality gives $\Pr[|D - \mathbb{E}D| \ge b\varepsilon] \le 2\exp(-2(b\varepsilon)^2/b) = 2e^{-2b\varepsilon^2}$. $\square$

**Theorem 2 ($\pm 1$ version).** Assume that the bits of $H(f)$, for $f \in G$ and all positions, are independent fair coins. Then the $X_i$ are independent and identically distributed with some probability $\delta(x, y) = \Pr[X_i = 1]$ that does not depend on $i$, $\mathbb{E}[D] = b\,\delta$, and $\Pr[|D/b - \delta| \ge \varepsilon] \le 2e^{-2b\varepsilon^2}$. In general $\delta(x, y) \ne \theta/\pi$.

*Proof.* $X_i$ is the same function of the vector $\sigma_i = (\sigma_i(f))_{f \in G}$ for every $i$, and $\sigma_1, \ldots, \sigma_b$ are independent and identically distributed, uniform on $\{-1, +1\}^G$. So the $X_i$ are independent with a common mean $\delta$, and the expectation and the Hoeffding bound follow as in Theorem 1. For the last claim take $G = \{1, 2, 3\}$, $x = (1, 0, 0)$ and $y = (1, 1, 1)$. Bit $i$ of $x$ is 1 when $\sigma_i(1) = +1$; bit $i$ of $y$ is 1 when $\sigma_i(1) + \sigma_i(2) + \sigma_i(3) > 0$, that is, when at least two of the three signs are $+1$. The two bits disagree exactly when $\sigma_i(2)$ and $\sigma_i(3)$ are both opposite to $\sigma_i(1)$, which has probability $1/4$. So $\delta = 1/4$, while $\theta/\pi = \arccos(1/\sqrt{3})/\pi \approx 0.3041$. $\blacksquare$
