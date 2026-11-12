---
title: Mean field raises a lower bound on log Z and stops
proves: [correctness]
status: full
---

We use the model, the objective $L$ and the pseudocode of the page. The spins are $s_i \in \{-1, +1\}$, the unnormalized model is $\tilde p(s) = \exp(\sum_i h_i s_i + \sum_{(i,j) \in E} J_{ij} s_i s_j)$, $Z = \sum_s \tilde p(s)$ and $p = \tilde p / Z$. For $m \in [-1, 1]^n$, $q_m$ is the product distribution with $q_m(s_i = \pm 1) = (1 \pm m_i)/2$.

**Lemma 1 (the objective).** $L(m) = \mathbb{E}_{q_m}[\log \tilde p(s)] + H(q_m)$, and $\log Z = L(m) + \mathrm{KL}(q_m \,\|\, p)$. So $L(m) \le \log Z$.

*Proof.* Under $q_m$ the spins are independent with $\mathbb{E}[s_i] = m_i$, so $\mathbb{E}_{q_m}[s_i s_j] = m_i m_j$ for $i \ne j$, and $\mathbb{E}_{q_m}[\log \tilde p] = \sum_i h_i m_i + \sum_{(i,j)} J_{ij} m_i m_j$. The entropy of a product distribution is the sum of the entropies of its factors, which is $\sum_i H_b(m_i)$. This proves the first equation. For the second, $\mathrm{KL}(q_m \,\|\, p) = \sum_s q_m(s) [\log q_m(s) - \log \tilde p(s) + \log Z] = -H(q_m) - \mathbb{E}_{q_m}[\log \tilde p] + \log Z$. The KL divergence is at least 0 (Gibbs' inequality), which gives the bound. $\square$

**Lemma 2 (one coordinate).** Fix all coordinates except $m_i$, and let $\phi_i = h_i + \sum_{j \in N(i)} J_{ij} m_j$. Then $g(x) = L(m_1, \ldots, m_{i-1}, x, m_{i+1}, \ldots, m_n)$ on $[-1, 1]$ has the unique maximizer $x^* = \tanh \phi_i$, and $g(x^*) - g(x) \ge \frac12 (x^* - x)^2$ for every $x \in [-1, 1]$.

*Proof.* The variable $x$ appears in the terms $h_i x$, $J_{ij} x m_j$ for $j \in N(i)$, and $H_b(x)$; there are no self-loops, so no term is quadratic in $x$. So $g(x) = \phi_i x + H_b(x) + c$, where $c$ does not depend on $x$. On $(-1, 1)$, $H_b'(x) = -\frac12 \log \frac{1+x}{2} + \frac12 \log \frac{1-x}{2} = -\operatorname{artanh}(x)$ and $H_b''(x) = -1/(1 - x^2) \le -1$. So $g'(x) = \phi_i - \operatorname{artanh}(x)$, which is strictly decreasing, tends to $+\infty$ at $x \to -1$ and to $-\infty$ at $x \to 1$, and is 0 only at $x^* = \tanh \phi_i \in (-1, 1)$. Hence $x^*$ is the unique maximizer on $[-1, 1]$ ($g$ is continuous at the end points, and $g$ increases on $[-1, x^*]$ and decreases on $[x^*, 1]$). For the quadratic gap, Taylor's theorem with $g'(x^*) = 0$ gives, for $x \in (-1, 1)$, $g(x) = g(x^*) + \frac12 g''(\xi)(x - x^*)^2$ for some $\xi$ between $x$ and $x^*$, and $g''(\xi) \le -1$. The end points follow by continuity. $\square$

**Theorem.** Run MEAN-FIELD from any $m^{(0)} \in [-1, 1]^n$ with $\varepsilon > 0$ and $T = \infty$. Then:

1. after each execution of line L5, $L(m)$ does not decrease, and $L(m) \le \log Z$ at all times;
2. the loop stops after at most $1 + 2(\log Z - L(m^{(0)}))/\varepsilon^2$ sweeps;
3. the returned $m$ satisfies $|m_i - \tanh \phi_i(m)| \le \varepsilon \sum_{j \in N(i)} |J_{ij}|$ for each $i$; so as $\varepsilon \to 0$, every limit point of the returned vectors is a fixed point of $m_i = \tanh \phi_i$ for all $i$.

*Proof.* (1) Line L4 computes $x^* = \tanh \phi_i$ with the current values of the other coordinates, and line L5 sets $m_i = x^*$. By Lemma 2 this does not lower $L$, and it raises $L$ by at least $\frac12 \delta_i^2$, where $\delta_i$ is the size of the move. Lemma 1 gives the upper bound.

(2) Let $U$ be the number of single updates with a move of at least $\varepsilon$. Each raises $L$ by at least $\varepsilon^2/2$, no update lowers $L$, and $L$ stays between $L(m^{(0)})$ and $\log Z$. So $U \varepsilon^2 / 2 \le \log Z - L(m^{(0)})$. A sweep that does not stop at line L6 has $\delta \ge \varepsilon$, so it holds at least one such update. Hence at most $U$ sweeps do not stop, and the next one stops.

(3) In the last sweep every move was below $\varepsilon$. Let $m$ be the vector at the end, and consider coordinate $i$. After its update in the last sweep, $m_i = \tanh \phi_i$ for the values that its neighbors had at that time, and each neighbor moved afterwards by less than $\varepsilon$. Since $\tanh$ is 1-Lipschitz, $|m_i - \tanh \phi_i(m)| \le \sum_{j \in N(i)} |J_{ij}| \varepsilon$. As $\varepsilon \to 0$ this tends to 0, and by continuity every limit point is a fixed point. $\blacksquare$

**Remark (no global optimality).** $L$ is not concave in $m$. In the two-spin model with $h = 0$ and $J_{12} = 2$, the points $m = (0, 0)$ and $m = \pm(0.9575, 0.9575)$ are all fixed points, with $L = 2 \log 2$ at the first and $L \approx 2.0393$ at the others. So a fixed point need not be a global maximum, and the algorithm can stay at $(0, 0)$ if it starts there.
