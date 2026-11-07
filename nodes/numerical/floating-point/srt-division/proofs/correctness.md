---
title: Radix-4 SRT division returns the exact quotient and remainder
proves: [correctness]
status: full
---

**Setting.** $x, d \in [1/2, 1)$, radix 4, digits $q_j \in \{-2, \ldots, 2\}$, $\rho = 2/3$. Write $y_j = 4 w_{j-1}$. The divisor estimate $\hat d = \lfloor 16 d \rfloor / 16$ and the remainder estimate $\hat y_j = \lfloor 8 y_j \rfloor / 8$ satisfy $\hat d \le d < \hat d + 1/16$ and $\hat y_j \le y_j < \hat y_j + 1/8$. A *cell* is the set $C(\hat d, \hat y) = \{(y, d) : \hat d \le d < \hat d + \tfrac{1}{16},\ \hat y \le y < \hat y + \tfrac18,\ |y| \le 4\rho d\}$.

**Table condition (T).** For every nonempty cell the table digit $k$ satisfies, for all $(y, d)$ in the cell, $y \ge (k - \rho)d$ unless $k = -2$, and $y \le (k + \rho)d$ unless $k = 2$. The implementation checks (T) by evaluating the two linear functions at the corners of each cell in exact rationals; a linear function on a box attains its extremes at corners, and the strict upper edges only make the check conservative.

**Lemma 1 (invariant).** Under (T), $|w_j| \le \rho d$ for $j = 0, \ldots, n$.

*Proof.* $w_0 = x/4 < 1/4$, and $\rho d \ge \tfrac23 \cdot \tfrac12 = \tfrac13$. Suppose $|w_{j-1}| \le \rho d$. Then $|y_j| \le 4\rho d$, so $(y_j, d)$ lies in the cell $C(\hat d, \hat y_j)$, which is therefore nonempty, and the digit $k = q_j$ read from the table satisfies (T) at $(y_j, d)$. If $k \ne -2$ then $w_j = y_j - kd \ge -\rho d$; if $k = -2$ then $w_j = y_j + 2d \ge -4\rho d + 2d = -\tfrac23 d = -\rho d$. Symmetrically $w_j \le \rho d$, using $y_j \le 4\rho d$ when $k = 2$: $w_j \le \tfrac83 d - 2d = \rho d$. $\square$

**Lemma 2 (series).** $\dfrac{x}{4d} = \sum_{j=1}^{n} q_j 4^{-j} + \dfrac{w_n}{4^n d}$.

*Proof.* From $w_j = 4w_{j-1} - q_j d$, dividing by $4^j d$ gives $\dfrac{w_{j-1}}{4^{j-1} d} = q_j 4^{-j} + \dfrac{w_j}{4^j d}$. Summing from $j = 1$ to $n$ telescopes to the claim, since $w_0/d = x/(4d)$. $\square$

**Theorem.** After line L7, $Q = \lfloor x\,4^{n-1}/d \rfloor$ and $0 \le w < d$, with $\frac{x}{4d} = Q 4^{-n} + w 4^{-n}/d$.

*Proof.* Line L6 accumulates $Q = \sum_{j=1}^n q_j 4^{n-j}$, an integer. By Lemma 2, $x 4^{n-1}/d = Q + w_n/d$, and by Lemma 1, $w_n/d \in [-\tfrac23, \tfrac23]$. If $w_n \ge 0$ then $w_n/d \in [0, 1)$ and $Q$ is the floor. If $w_n < 0$, line L7 replaces $(Q, w_n)$ by $(Q - 1, w_n + d)$, which keeps $Q + w/d$ unchanged and puts $w/d \in [\tfrac13, 1)$; again $Q$ is the floor. $\square$

**Corollary (correct rounding).** Let $a = m_a 2^{e_a}$, $b = m_b 2^{e_b}$ with $m_a, m_b \in [1/2, 1)$ binary64 significands, $n = 28$, and suppose $a/b$ is a normal number. Then $Q = \lfloor (m_a/m_b) 2^{54} \rfloor$ lies in $[2^{53}, 2^{55})$, and $m_a/m_b = (Q + \theta) 2^{-54}$ with $\theta \in [0, 1)$ and $\theta = 0$ iff $w = 0$. Let $Q = K 2^{s} + R$ with $0 \le R < 2^s$ and $K$ of exactly 53 bits ($s \in \{1, 2\}$). The exact value lies in $(K + (R + \theta) 2^{-s}) 2^{s - 54}$, and round to nearest, ties to even, picks $K + 1$ iff $(R + \theta) 2^{-s} > 1/2$, or $= 1/2$ and $K$ is odd. Since $R$ is an integer and $\theta \in [0, 1)$, $(R + \theta)2^{-s} > 1/2$ iff $R > 2^{s-1}$, or $R = 2^{s-1}$ and $\theta > 0$; and $= 1/2$ iff $R = 2^{s-1}$ and $\theta = 0$. This is exactly the test in `srt_float_divide`, and the scaling by $2^{e_a - e_b}$ is exact for a normal result. $\square$
