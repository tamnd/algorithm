---
title: Klein's sampler outputs lattice points close to the discrete Gaussian
proves: [correctness]
status: full
---

Let $B = (b_1, \dots, b_n)$ be a basis of a full-rank lattice $\Lambda \subset \mathbb{R}^n$, with Gram-Schmidt vectors $\tilde b_i$, so that $\langle b_j, \tilde b_i \rangle = 0$ for $j < i$ and $\langle b_i, \tilde b_i \rangle = \|\tilde b_i\|^2$. Let $s_i = s / \|\tilde b_i\|$. In this proof the one-dimensional sampler of line L9 is assumed to be exact, that is, to return $z$ with probability $\rho_{s_i, c_i}(z) / \rho_{s_i, c_i}(\mathbb{Z})$; the remark at the end treats the tail cut of the code.

**Lemma 1 (the output is a lattice point, and each point has one path).** Line L11 returns $v = \sum_i z_i b_i$ with integers $z_i$. Conversely, each $v \in \Lambda$ arises from exactly one sequence $(z_n, \dots, z_1)$.

*Proof.* Line L10 adds $z_i b_i$ to $v$, which starts at $0$ in line L6. Since $B$ is a basis, the coefficients of $v$ in $B$ are unique. $\square$

**Lemma 2 (the exponents add up).** Let $c^{(n)} = c$ and $c^{(i-1)} = c^{(i)} - z_i b_i$, so that line L8 computes $c_i = \langle c^{(i)}, \tilde b_i \rangle / \|\tilde b_i\|^2$. Then
$$\prod_{i=1}^n \rho_{s_i, c_i}(z_i) = \rho_{s, c}(v).$$

*Proof.* Write $c - v = \sum_j \alpha_j \tilde b_j$; this is possible since the $\tilde b_j$ form an orthogonal basis of $\mathbb{R}^n$. Then $\|c - v\|^2 = \sum_j \alpha_j^2 \|\tilde b_j\|^2$. Also $c - v = c^{(i)} - \sum_{j \le i} z_j b_j$, so
$$\alpha_i = \frac{\langle c - v, \tilde b_i \rangle}{\|\tilde b_i\|^2} = \frac{\langle c^{(i)}, \tilde b_i \rangle - z_i \|\tilde b_i\|^2}{\|\tilde b_i\|^2} = c_i - z_i,$$
using $\langle b_j, \tilde b_i \rangle = 0$ for $j < i$. Hence $\prod_i \exp(-\pi (z_i - c_i)^2 / s_i^2) = \exp(-\pi \sum_i (z_i - c_i)^2 \|\tilde b_i\|^2 / s^2) = \exp(-\pi \|v - c\|^2 / s^2)$. $\square$

**Lemma 3 (one-dimensional normalizers).** If $t \ge \eta_\varepsilon(\mathbb{Z})$, then for every $c \in \mathbb{R}$, $\rho_{t, c}(\mathbb{Z}) \in [1 - \varepsilon, 1 + \varepsilon] \cdot t$.

*Proof.* By the Poisson summation formula, $\rho_{t,c}(\mathbb{Z}) = \sum_{x \in \mathbb{Z}} \rho_t(x - c) = t \sum_{y \in \mathbb{Z}} \rho_{1/t}(y) e^{2 \pi i y c}$, since the Fourier transform of $\rho_t$ is $t \rho_{1/t}$ and $\mathbb{Z}^* = \mathbb{Z}$. The term $y = 0$ is $1$, and the other terms have total absolute value at most $\rho_{1/t}(\mathbb{Z} \setminus \{0\}) \le \varepsilon$ by the definition of $\eta_\varepsilon(\mathbb{Z})$. $\square$

**Theorem.** If $s \ge \|\tilde B\| \cdot \eta_\varepsilon(\mathbb{Z})$ for some $\varepsilon \in (0, 1)$, then for every $v \in \Lambda$ the probability $P(v)$ that Klein's algorithm returns $v$ satisfies
$$\left(\frac{1 - \varepsilon}{1 + \varepsilon}\right)^n \le \frac{P(v)}{D_{\Lambda, s, c}(v)} \le \left(\frac{1 + \varepsilon}{1 - \varepsilon}\right)^n.$$

*Proof.* By Lemma 1, $P(v)$ is the probability of the unique path to $v$, which is $\prod_i \rho_{s_i, c_i}(z_i) / \rho_{s_i, c_i}(\mathbb{Z})$. Each $s_i = s / \|\tilde b_i\| \ge \eta_\varepsilon(\mathbb{Z})$, so by Lemma 3 each denominator lies in $[1 - \varepsilon, 1 + \varepsilon] \cdot s_i$. With Lemma 2, $P(v) = K(v) \rho_{s,c}(v)$ where $K(v) \in [(1 + \varepsilon)^{-n}, (1 - \varepsilon)^{-n}] \cdot K_0$ and $K_0 = \prod_i s_i^{-1}$ does not depend on $v$. Summing over $\Lambda$, $1 = \sum_v P(v)$, so $\rho_{s,c}(\Lambda) K_0 \in [(1 - \varepsilon)^n, (1 + \varepsilon)^n]$. Dividing $P(v) = K(v) \rho_{s,c}(v)$ by $D_{\Lambda,s,c}(v) = \rho_{s,c}(v) / \rho_{s,c}(\Lambda)$ gives $P(v) / D(v) = K(v) \rho_{s,c}(\Lambda)$, which lies in the stated interval. $\blacksquare$

**The integer samplers.** The rejection loop of lines L3 and L4 returns $x$ in the window $I = [c - \tau\sigma, c + \tau\sigma] \cap \mathbb{Z}$ with probability proportional to $\rho_{s,c}(x)$: each trial picks $x$ uniformly in $I$ and accepts with probability $\rho_{s,c}(x) \le 1$, so the accepted value has probability $\rho_{s,c}(x) / \rho_{s,c}(I)$. The CDT of lines L1 and L2 returns $x_i$ exactly when $T[i-1] < u \le T[i]$, an event of probability $T[i] - T[i-1] = \rho_s(x_i) / \rho_s(I)$. So both sample the discrete Gaussian restricted to the window, up to the floating point error of the code.

**Remark (the tail cut).** Restricting to the window changes the distribution by a statistical distance of at most the Gaussian mass outside it, which is below $2 e^{-\tau^2/2}$ times a small factor; for $\tau = 12$ this is about $2^{-100}$ per step. So the code's output is within statistical distance about $n 2^{-100}$ of the distribution of the theorem.
