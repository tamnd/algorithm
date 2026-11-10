---
title: The ratio of a uniform point in the region C_h has density proportional to h
proves: [correctness, time.expected]
status: full
---

Let $h \ge 0$ be a measurable function on $\mathbb{R}$ with $0 < \int h < \infty$. Let

$$C_h = \{(u, v) : 0 < u \le \sqrt{h(v/u)}\}.$$

Suppose $a = \sup_x \sqrt{h(x)}$, $b_- = \inf_x x\sqrt{h(x)}$ and $b_+ = \sup_x x \sqrt{h(x)}$ are finite. Lines L1 to L4 draw $U$ uniform on $(0, a]$ and $V$ uniform on $[b_-, b_+]$, independent, put $X = V/U$, and accept when $U^2 \le h(X)$, that is, when $(U, V) \in C_h$.

**Lemma 1 (change of variables).** $C_h$ has area $\frac{1}{2}\int h$. If $(U, V)$ is uniform on $C_h$, then $X = V/U$ has density $h(x)/\int h$.

*Proof.* The map $\Psi(u, x) = (u, ux)$ is a bijection from $(0, \infty) \times \mathbb{R}$ onto $(0, \infty) \times \mathbb{R}$, with inverse $(u, v) \mapsto (u, v/u)$. Its Jacobian matrix is $\begin{pmatrix} 1 & 0 \\ x & u \end{pmatrix}$, with determinant $u > 0$. So, by the [change of variables](/change-of-variables/) formula, $du\,dv = u\,du\,dx$. The point $(u, v)$ is in $C_h$ exactly when $x = v/u$ satisfies $0 < u \le \sqrt{h(x)}$. Hence, for a measurable set $A$,

$$\operatorname{area}\{(u, v) \in C_h : v/u \in A\} = \int_A \int_0^{\sqrt{h(x)}} u\,du\,dx = \int_A \frac{h(x)}{2}\,dx.$$

With $A = \mathbb{R}$ the area of $C_h$ is $\frac{1}{2}\int h$. For $(U, V)$ uniform on $C_h$, $\Pr[V/U \in A] = \int_A h / \int h$. $\square$

**Lemma 2 (the box).** $C_h \subseteq (0, a] \times [b_-, b_+]$.

*Proof.* Take $(u, v) \in C_h$ and put $x = v/u$. Then $0 < u \le \sqrt{h(x)} \le a$. Also $v = xu$. If $x \ge 0$, then $0 \le v \le x\sqrt{h(x)} \le b_+$, and $b_- \le 0$ since $0 \cdot \sqrt{h(0)} = 0$. If $x < 0$, then $0 > v \ge x\sqrt{h(x)} \ge b_-$, and $b_+ \ge 0$. In both cases $b_- \le v \le b_+$. $\square$

**Theorem.** The algorithm returns $X$ with density $h/\int h$. The number of tries is geometric with success probability

$$p = \frac{\int h}{2a(b_+ - b_-)},$$

so the mean number of tries is $1/p$.

*Proof.* Each try gives $(U, V)$ uniform on the box $Q = (0, a] \times [b_-, b_+]$, of area $a(b_+ - b_-)$, independent of the other tries. By Lemma 2 and Lemma 1, a try is accepted with probability $\operatorname{area}(C_h)/\operatorname{area}(Q) = p$. For a measurable set $E \subseteq C_h$, a try is accepted with $(U, V) \in E$ with probability $\operatorname{area}(E)/\operatorname{area}(Q)$. Summing over the index $k$ of the first accepted try,

$$\Pr[(U, V)_{\text{accepted}} \in E] = \sum_{k \ge 1} (1 - p)^{k-1} \frac{\operatorname{area}(E)}{\operatorname{area}(Q)} = \frac{\operatorname{area}(E)}{p \cdot \operatorname{area}(Q)} = \frac{\operatorname{area}(E)}{\operatorname{area}(C_h)}.$$

So the accepted point is uniform on $C_h$. By Lemma 1, $X = V/U$ has density $h/\int h$. The tries are independent with the same success probability $p$, so their number is geometric with mean $1/p$. $\blacksquare$

**Examples of $p$.** For the normal, $h(x) = e^{-x^2/2}$ has $a = 1$ and $b_\pm = \pm\sqrt{2/e}$ (the maximum of $x e^{-x^2/4}$ is at $x = \sqrt{2}$), and $\int h = \sqrt{2\pi}$, so $p = \sqrt{2\pi}/(4\sqrt{2/e}) = \sqrt{\pi e}/4 \approx 0.7306$. For the Cauchy density, $h(x) = 1/(1 + x^2)$ gives $C_h = \{u^2 + v^2 \le 1, u > 0\}$, a half disk, and $p = \pi/4$. For the exponential density, $h(x) = e^{-x}$ on $x \ge 0$ gives $a = 1$, $b_- = 0$, $b_+ = 2/e$, and $p = e/4 \approx 0.6796$.

**Floating point.** The proof needs exact uniform reals, an exact ratio $V/U$ and an exact test. In floating point $U \ge 2^{-53} a$, so $|X| \le 2^{53} \max(|b_-|, b_+)/a$, and the values of $X$ lie on a finite set. The theorem holds only in exact arithmetic.
