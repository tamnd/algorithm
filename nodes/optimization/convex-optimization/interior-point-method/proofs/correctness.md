---
title: The short-step path-following method stays in N2(0.4) and reduces the gap by a fixed factor
proves: [correctness, termination, time.worst]
status: full
---

We use the notation of the page. The program is $\min c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A \in \mathbb{R}^{m \times n}$ of full row rank $m$. The dual is $\max b^\top y$ subject to $A^\top y + s = c$, $s \ge 0$. For vectors $x, s$ we write $X = \operatorname{diag}(x)$, $S = \operatorname{diag}(s)$, $e = (1, \ldots, 1)$ and $\mu = x^\top s / n$. The neighborhood is

$$\mathcal{N}_2(\theta) = \{(x, y, s) : Ax = b,\ A^\top y + s = c,\ x > 0,\ s > 0,\ \|XSe - \mu e\| \le \theta \mu\}.$$

The method uses $\theta = 0.4$ and $\sigma = 1 - 0.4/\sqrt{n}$. One iteration solves

$$A\,\Delta x = 0, \qquad A^\top \Delta y + \Delta s = 0, \qquad S\,\Delta x + X\,\Delta s = \sigma \mu e - XSe \tag{N}$$

and sets $(x^+, y^+, s^+) = (x + \Delta x, y + \Delta y, s + \Delta s)$.

**Step 0 (the system has one solution, and lines L6 to L8 compute it).** Let $r = \sigma\mu e - XSe$ and $D = XS^{-1}$, a positive diagonal matrix. The third equation of (N) gives $\Delta x = S^{-1} r - D \Delta s$, and the second gives $\Delta s = -A^\top \Delta y$, so $\Delta x = S^{-1} r + D A^\top \Delta y$. The first equation then reads $A D A^\top \Delta y = -A S^{-1} r$. The matrix $A D A^\top$ is positive definite: for $z \ne 0$, $A^\top z \ne 0$ because $A$ has full row rank, so $z^\top A D A^\top z = \sum_j D_{jj} (A^\top z)_j^2 > 0$. So $\Delta y$ is unique, and $\Delta s$ and $\Delta x$ follow. These are lines L6, L7 and L8.

**Lemma 1.** If $u, v \in \mathbb{R}^n$ and $u^\top v \ge 0$, then $\|UVe\| \le 2^{-3/2} \|u + v\|^2$, where $UVe$ is the vector with entries $u_i v_i$.

*Proof.* Let $P = \{i : u_i v_i \ge 0\}$ and $M = \{i : u_i v_i < 0\}$. From $u^\top v \ge 0$ we get $\sum_{i \in M} |u_i v_i| \le \sum_{i \in P} u_i v_i$. For $i \in P$, $u_i v_i \le (u_i + v_i)^2 / 4$, because $(u_i + v_i)^2 - 4 u_i v_i = (u_i - v_i)^2 \ge 0$. So

$$\|UVe\|^2 = \sum_{i \in P} (u_i v_i)^2 + \sum_{i \in M} (u_i v_i)^2 \le \Big(\sum_{i \in P} u_i v_i\Big)^2 + \Big(\sum_{i \in M} |u_i v_i|\Big)^2 \le 2 \Big(\sum_{i \in P} u_i v_i\Big)^2 \le 2 \Big(\frac{\|u+v\|^2}{4}\Big)^2,$$

and the square root gives the claim. $\square$

**Lemma 2.** If $(x, y, s) \in \mathcal{N}_2(\theta)$ and $(\Delta x, \Delta y, \Delta s)$ solves (N), then $\Delta x^\top \Delta s = 0$ and

$$\|\Delta X \Delta S e\| \le \frac{\theta^2 + n(1 - \sigma)^2}{2^{3/2}(1 - \theta)}\, \mu.$$

*Proof.* From (N), $\Delta x^\top \Delta s = -\Delta x^\top A^\top \Delta y = -(A \Delta x)^\top \Delta y = 0$. Let $W = (XS)^{-1/2}$ and multiply the third equation of (N) by $W$. With $u = W S \Delta x$ and $v = W X \Delta s$ we get $u + v = W r$, and $u_i v_i = \Delta x_i \Delta s_i$ because $W_{ii}^2 x_i s_i = 1$. So $u^\top v = \Delta x^\top \Delta s = 0$, and Lemma 1 gives $\|\Delta X \Delta S e\| \le 2^{-3/2} \|W r\|^2 \le 2^{-3/2} \|r\|^2 / \min_i x_i s_i$. Each $x_i s_i \ge \mu - \|XSe - \mu e\| \ge (1 - \theta)\mu$. For $\|r\|^2$, write $r = -(XSe - \mu e) - (1 - \sigma)\mu e$. The cross term is $2(1-\sigma)\mu\, e^\top (XSe - \mu e) = 2(1-\sigma)\mu (x^\top s - n\mu) = 0$, so $\|r\|^2 = \|XSe - \mu e\|^2 + (1 - \sigma)^2 \mu^2 n \le (\theta^2 + n(1-\sigma)^2)\mu^2$. Put the two bounds together. $\square$

**Theorem.** Let $n \ge 1$, $\theta = 0.4$ and $\sigma = 1 - 0.4/\sqrt{n}$. If $(x, y, s) \in \mathcal{N}_2(0.4)$, then $(x^+, y^+, s^+) \in \mathcal{N}_2(0.4)$ and $\mu^+ = \sigma \mu$.

*Proof.* *Feasibility of the equations.* $A x^+ = Ax + A\Delta x = b$ and $A^\top y^+ + s^+ = c + (A^\top \Delta y + \Delta s) = c$.

*The new gap.* $(x^+)^\top s^+ = x^\top s + (s^\top \Delta x + x^\top \Delta s) + \Delta x^\top \Delta s$. The middle term is $e^\top (S \Delta x + X \Delta s) = e^\top r = n\sigma\mu - x^\top s$, and the last term is $0$ by Lemma 2. So $(x^+)^\top s^+ = n \sigma \mu$ and $\mu^+ = \sigma\mu$.

*The new centrality.* Entry $i$ of $X^+ S^+ e$ is $x_i s_i + (s_i \Delta x_i + x_i \Delta s_i) + \Delta x_i \Delta s_i = \sigma\mu + \Delta x_i \Delta s_i$. So $X^+ S^+ e - \mu^+ e = \Delta X \Delta S e$. With $\theta = 0.4$ and $n(1-\sigma)^2 = 0.16$, Lemma 2 gives $\|\Delta X \Delta S e\| \le 0.32 / (2^{3/2} \cdot 0.6)\, \mu < 0.1886\,\mu$. Because $\sigma \ge 0.6$ for each $n \ge 1$, $\theta \mu^+ = 0.4 \sigma \mu \ge 0.24 \mu$. So $\|X^+ S^+ e - \mu^+ e\| \le \theta \mu^+$.

*Positivity.* For $\alpha \in [0, 1]$ let $x(\alpha) = x + \alpha \Delta x$ and $s(\alpha) = s + \alpha \Delta s$. The same expansion gives

$$x_i(\alpha) s_i(\alpha) = (1 - \alpha) x_i s_i + \alpha \sigma \mu + \alpha^2 \Delta x_i \Delta s_i \ge (1-\alpha)(0.6\mu) + \alpha (0.6 \mu) - 0.1886\,\mu > 0,$$

where we used $x_i s_i \ge (1-\theta)\mu = 0.6\mu$, $\sigma \ge 0.6$ and $|\Delta x_i \Delta s_i| \le \|\Delta X \Delta S e\|$. So $x_i(\alpha) s_i(\alpha) \ne 0$ for all $\alpha \in [0, 1]$. The functions $x_i(\alpha)$ and $s_i(\alpha)$ are continuous and positive at $\alpha = 0$, and neither of them is ever $0$, so both are positive at $\alpha = 1$. $\square$

**Corollary (the iteration bound).** Start from $(x^0, y^0, s^0) \in \mathcal{N}_2(0.4)$. By induction on $k$ with the theorem, iterate $k$ is in $\mathcal{N}_2(0.4)$, it is strictly feasible, and $\mu_k = \sigma^k \mu_0$. Its duality gap is

$$c^\top x^k - b^\top y^k = (A^\top y^k + s^k)^\top x^k - (A x^k)^\top y^k = (x^k)^\top s^k = n \mu_k = n \sigma^k \mu_0.$$

The loop of line L2 stops at the first $k$ with $n\mu_k \le \varepsilon$. Because $-\ln(1 - \delta) \ge \delta$ for $\delta \in [0, 1)$, we have $\sigma^k \le e^{-0.4 k/\sqrt{n}}$, so the method stops after at most

$$K = \left\lceil \frac{\ln(n\mu_0/\varepsilon)}{-\ln \sigma} \right\rceil \le \left\lceil \frac{\sqrt{n}}{0.4} \ln\frac{n\mu_0}{\varepsilon} \right\rceil$$

iterations. By weak duality, $b^\top y^k \le f^* \le c^\top x^k$, so the returned $x$ has $c^\top x - f^* \le \varepsilon$ and the returned $y$ has $f^* - b^\top y \le \varepsilon$. $\blacksquare$
