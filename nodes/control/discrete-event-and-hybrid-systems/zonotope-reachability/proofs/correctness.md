---
title: Each zonotope Q_i contains every state reachable in the time interval [i r, (i+1) r]
proves: [correctness, termination]
status: full
---

**Setting.** The system is $x'(t) = A x(t) + u(t)$ with $x(t) \in \mathbb{R}^n$, $x(0) \in X_0$ and a measurable input with $\|u(t)\|_\infty \le \mu$ for all $t$. Here $\|\cdot\|$ is the infinity norm on $\mathbb{R}^n$ and the induced norm (the largest absolute row sum) on matrices. $X_0 = \langle c, g_1, \ldots, g_p \rangle = \{c + \sum_j a_j g_j : |a_j| \le 1\}$ is a zonotope. $B(\rho) = \{x : \|x\| \le \rho\}$ is the box $\langle 0, \rho e_1, \ldots, \rho e_n \rangle$. For a time interval $I$, $\mathcal{R}(I)$ is the set of all $x(t)$ with $t \in I$, over all initial states and inputs. Let $\Phi = e^{rA}$, $a = \|A\|$, $s = \max_{x \in X_0} \|x\|$, $\alpha = (e^{ra} - 1 - ra) s$ and $\beta = (e^{ra} - 1)\mu / a$ (and $\beta = r\mu$ if $a = 0$). These are lines L1 and L2.

**Lemma 1 (operations).** For zonotopes $Z = \langle c, g_1, \ldots, g_p \rangle$ and $Z' = \langle c', h_1, \ldots, h_q \rangle$ and a matrix $M$: $MZ = \langle Mc, Mg_1, \ldots, Mg_p \rangle$ and $Z \oplus Z' = \langle c + c', g_1, \ldots, g_p, h_1, \ldots, h_q \rangle$. Also $\max_{x \in Z} \|x\| = \max_i (|c_i| + \sum_j |g_{j,i}|)$.

*Proof.* $M(c + \sum a_j g_j) = Mc + \sum a_j M g_j$, and a sum of two points of $Z$ and $Z'$ is $c + c' + \sum a_j g_j + \sum b_k h_k$ with free coefficients in $[-1, 1]$. For the norm, coordinate $i$ of a point of $Z$ is at most $|c_i| + \sum_j |g_{j,i}|$ in absolute value, and the signs $a_j = \operatorname{sign}(c_i) \operatorname{sign}(g_{j,i})$ reach this bound. $\blacksquare$

**Lemma 2 (hull, line L3).** The zonotope $P_0$ with center $(c + \Phi c)/2$ and generators $(g_j + \Phi g_j)/2$, $(c - \Phi c)/2$ and $(g_j - \Phi g_j)/2$ contains the convex hull of $X_0 \cup \Phi X_0$.

*Proof.* Both sets are convex, so a point of the hull is $y = \lambda z + (1 - \lambda) \Phi z'$ with $z = c + \sum a_j g_j$, $z' = c + \sum b_j g_j$ in $X_0$ and $\lambda \in [0, 1]$. Write

$$y = \frac{c + \Phi c}{2} + (2\lambda - 1)\frac{c - \Phi c}{2} + \sum_j \left( \xi_j \frac{g_j + \Phi g_j}{2} + \eta_j \frac{g_j - \Phi g_j}{2} \right)$$

with $\xi_j = \lambda a_j + (1 - \lambda) b_j$ and $\eta_j = \lambda a_j - (1 - \lambda) b_j$. Expanding the right side gives back $\lambda c + (1 - \lambda)\Phi c + \sum_j (\lambda a_j g_j + (1 - \lambda) b_j \Phi g_j) = y$. Each coefficient is in $[-1, 1]$: $|2\lambda - 1| \le 1$, and $|\xi_j|, |\eta_j| \le \lambda |a_j| + (1 - \lambda)|b_j| \le 1$. $\blacksquare$

**Lemma 3 (first interval, line L4).** $\mathcal{R}([0, r]) \subseteq Q_0 = P_0 \oplus B(\alpha + \beta)$.

*Proof.* Take $x_0 \in X_0$, an input $u$ and $t \in [0, r]$. By the variation of constants formula, $x(t) = e^{tA} x_0 + \int_0^t e^{(t - \tau)A} u(\tau)\, d\tau$. Compare the first term with the point $y = x_0 + \frac{t}{r}(\Phi x_0 - x_0)$, which lies on the segment from $x_0$ to $\Phi x_0$, so in $P_0$ by Lemma 2. From the power series,

$$e^{tA} x_0 - y = \sum_{k \ge 2} \frac{t^k - t r^{k-1}}{k!} A^k x_0.$$

For $0 \le t \le r$, $0 \le t r^{k-1} - t^k \le r^k$, so $\|e^{tA} x_0 - y\| \le \sum_{k \ge 2} \frac{r^k a^k}{k!} \|x_0\| = (e^{ra} - 1 - ra)\|x_0\| \le \alpha$. For the second term, $\|e^{\sigma A}\| \le e^{\sigma a}$ gives $\left\|\int_0^t e^{(t - \tau)A} u(\tau)\, d\tau\right\| \le \mu \int_0^t e^{\sigma a}\, d\sigma = \mu (e^{ta} - 1)/a \le \beta$ (and $\le r\mu$ if $a = 0$). So $x(t) = y + (e^{tA}x_0 - y) + \int \ldots \in P_0 \oplus B(\alpha) \oplus B(\beta) = P_0 \oplus B(\alpha + \beta)$, as $B(\alpha) \oplus B(\beta) = B(\alpha + \beta)$ for boxes. $\blacksquare$

**Lemma 4 (one more step, line L6).** If $\mathcal{R}([ir, (i+1)r]) \subseteq Q_i$, then $\mathcal{R}([(i+1)r, (i+2)r]) \subseteq \Phi Q_i \oplus B(\beta)$.

*Proof.* A state at time $t + r$ with $t \in [ir, (i+1)r]$ is $x(t + r) = \Phi x(t) + \int_t^{t + r} e^{(t + r - \tau)A} u(\tau)\, d\tau$. Here $x(t) \in Q_i$, and the integral has norm at most $\beta$, as in Lemma 3. $\blacksquare$

**Lemma 5 (reduction, line L7).** Split the generators of $Z = \langle c, G \rangle$ into $K$ and $L$, and let $D$ be the diagonal matrix with $D_{ii} = \sum_{h \in L} |h_i|$. Then $Z \subseteq \langle c, K, D e_1, \ldots, D e_n \rangle$.

*Proof.* $\sum_{h \in L} b_h h$ with $|b_h| \le 1$ has coordinate $i$ at most $D_{ii}$ in absolute value, so it is $\sum_i d_i D_{ii} e_i$ with $|d_i| \le 1$. $\blacksquare$

**Theorem.** For $i = 0, \ldots, N - 1$, the zonotope $Q_i$ returned at line L9 contains $\mathcal{R}([ir, (i+1)r])$, with or without the reduction of line L7.

*Proof.* By induction on $i$. Lemma 3 gives the case $i = 0$, and Lemma 5 keeps it after a reduction. Lemma 4 gives the step from $i$ to $i + 1$, and Lemma 5 again keeps it after a reduction, because a superset of a superset is a superset. Lemma 1 shows that the zonotopes built by lines L3, L4 and L6 are exactly the sets in Lemmas 2 to 4. $\blacksquare$

**What is not proved.** The theorem gives containment only. The sets $Q_i$ are larger than the reach sets by terms of order $\alpha$ and by the reduction, and the gap does not go to zero with $i$ unless $\Phi$ is a contraction. As $r \to 0$, $\alpha = O(r^2)$ and $\beta = r\mu + O(r^2)$.

**Termination and cost.** The loop of line L5 runs $N - 1$ times. If $X_0$ has $p$ generators, $Q_0$ has $2p + 1 + n$ generators and each step adds $n$. A step multiplies each generator by $\Phi$ in $O(n^2)$ operations. With the reduction to at most $m$ generators, a step costs $O(n^2 m)$ for the product and $O(m \log m)$ for the sort; $\Phi$ costs $O(n^3)$ once. $\blacksquare$
