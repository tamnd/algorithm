---
title: Doubling and d averagings refine the uniform B-spline of degree d, and the polygons converge to it
proves: [correctness, convergence-rate]
status: full
---

We use the pseudocode of the page for a closed polygon $P_0, \dots, P_{m-1}$ with indices modulo $m$, and a degree $d \ge 0$. The uniform B-splines are $N_0 = $ the indicator function of $[0, 1)$ and $N_d = N_{d-1} * N_0$. So $N_d$ has support $[0, d + 1]$, it is a piecewise polynomial of degree $d$ with $C^{d-1}$ joins at the integers, and $\sum_{i} N_d(x - i) = 1$. The curve is $C(x) = \sum_{i \in \mathbb{Z}} P_i N_d(x - i)$.

**Lemma 1 (refinement).** $N_d(x) = 2^{-d} \sum_{k=0}^{d+1} \binom{d+1}{k} N_d(2x - k)$.

*Proof.* For $d = 0$ it says $N_0(x) = N_0(2x) + N_0(2x - 1)$. If $f(x) = \sum_k a_k g(2x - k)$ and $h(x) = \sum_l b_l g'(2x - l)$, the change of variables $z = 2y - k$ in the convolution integral gives $(f * h)(x) = \tfrac12 \sum_{k, l} a_k b_l (g * g')(2x - k - l)$. So the coefficient sequence of $N_d$ is $2^{-d}$ times that of $(1 + z)^{d+1}$, by induction on $d$. $\square$

**Lemma 2 (the loop).** After line L2 and $s$ passes of line L4, point $j$ is

$$A^s_j = 2^{-s} \sum_{i} \binom{s+1}{2i - j + 1} P_i.$$

*Proof.* Line L2 gives $A^0_j = P_{\lfloor j/2 \rfloor}$. The coefficient of $P_i$ is $1$ when $2i - j + 1 \in \{0, 1\}$ and $0$ otherwise, which is $\binom{1}{2i - j + 1}$. Line L4 replaces $A_j$ by $\tfrac12 (A_j + A_{j+1})$, using only old values. With the claim for $s$, the coefficient of $P_i$ in $A^{s+1}_j$ is $2^{-s-1} \big( \binom{s+1}{2i - j + 1} + \binom{s+1}{2i - j} \big) = 2^{-s-1} \binom{s+2}{2i - j + 1}$ by Pascal's rule. $\square$

**Theorem 1 (one round).** Let $R_j = A^d_j$ be the output of one round. Then $C(x) = \sum_{j} R_j N_d(2x - j - d)$. So $R$ is the control polygon of the same curve on the knots $\tfrac12 \mathbb{Z}$, and point $j$ belongs to the basis function with first knot $(j + d)/2$.

*Proof.* By Lemma 1,

$$C(x) = \sum_i P_i\, 2^{-d} \sum_k \binom{d+1}{k} N_d(2x - 2i - k) = \sum_l N_d(2x - l)\, 2^{-d} \sum_i \binom{d+1}{l - 2i} P_i.$$

With $l = j + d$ and the symmetry $\binom{d+1}{l - 2i} = \binom{d+1}{d + 1 - l + 2i} = \binom{d+1}{2i - j + 1}$, the inner sum is $R_j$ by Lemma 2. The sequence $R$ has period $2m$, and line L4 computes it with the indices modulo the new length. $\blacksquare$

By induction, after $r$ rounds the polygon is a control polygon of $C$ on the knots $2^{-r} \mathbb{Z}$, and point $j$ belongs to the basis function with first knot $(j + d(2^r - 1)) / 2^r$. No round changes the curve.

**Lemma 3 (second differences).** Let $D(P) = \max_i |P_{i-1} - 2 P_i + P_{i+1}|$. If $d \ge 2$, then $D(R) \le D(P) / 4$.

*Proof.* Write $P(z) = \sum_i P_i z^i$ as a formal series, and similarly for $R$. Theorem 1 says $R(z) = a(z) P(z^2)$ up to a shift of the index, with $a(z) = 2^{-d} (1 + z)^{d+1}$. The second difference has the series $(1 - z)^2 R(z) = \frac{a(z)}{(1 + z)^2} (1 - z^2)^2 P(z^2)$. So each second difference of $R$ is a combination of second differences of $P$ with the coefficients of $b(z) = 2^{-d} (1 + z)^{d-1}$, and each new value uses only the coefficients of one parity. The coefficients are at least $0$, and the coefficients of even index and of odd index of $(1 + z)^{d-1}$ each sum to $2^{d-2}$ when $d \ge 2$. So each second difference of $R$ has length at most $2^{-d} 2^{d-2} D(P) = D(P)/4$. $\square$

**Lemma 4 (distance to the polygon).** Let $d \ge 1$, put $g_i = i + (d + 1)/2$, and let $L$ be the polygon parametrized so that $L(g_i) = P_i$ and $L$ is linear between. Then $|C(x) - L(x)| \le c_d D(P)$ for all $x$, with $c_d = (d + 1)(d + 3)/8$.

*Proof.* The uniform B-splines reproduce linear functions with these abscissae: $\sum_i g_i N_d(x - i) = x$. To see it, put $S_d(x) = \sum_i (x - i) N_d(x - i)$. Then $S_0(x) = x - \lfloor x \rfloor$, which has period 1 and mean $\tfrac12$. From $N_d(y) = \int_0^1 N_{d-1}(y - t)\, dt$ and $\sum_i N_{d-1}(y - i) = 1$,

$$S_d(x) = \int_0^1 \sum_i \big( (x - t - i) + t \big) N_{d-1}(x - t - i)\, dt = \int_0^1 S_{d-1}(x - t)\, dt + \tfrac12.$$

So $S_1 = \tfrac12 + \tfrac12 = 1$, and by induction $S_d = (d + 1)/2$ for $d \ge 1$, which is the claim. Fix $x$ and the index $i_0$ with $g_{i_0} \le x < g_{i_0 + 1}$, and let $\ell$ be the linear map that agrees with $L$ on $[g_{i_0}, g_{i_0+1}]$. Since the weights $N_d(x - i)$ are at least 0 and sum to 1, and reproduce $\ell$,

$$C(x) - L(x) = \sum_i \big( P_i - \ell(g_i) \big) N_d(x - i).$$

Only $i$ with $x - d - 1 < i \le x$ appear, so $|g_i - x| < (d + 1)/2$. For $i \ge i_0 + 2$, put $k = i - i_0 - 1 < (d + 1)/2$. The slope of $L$ changes at each $g_t$ by $\Delta_t = P_{t-1} - 2P_t + P_{t+1}$, so $P_i - \ell(g_i) = \sum_{t = i_0 + 1}^{i - 1} (i - t) \Delta_t$, and its length is at most $D(P)\, k (k + 1)/2 < D(P) (d + 1)(d + 3) / 8$. The case $i \le i_0 - 1$ is the same, and $P_i = \ell(g_i)$ for $i = i_0, i_0 + 1$. $\square$

**Theorem 2 (convergence).** For $d \ge 2$, after $r$ rounds the polygon and the curve $C$ are within Hausdorff distance $c_d D(P) / 4^r$. For $d = 1$ the polygon is the curve.

*Proof.* After $r$ rounds the polygon is a control polygon of $C$ on the knots $2^{-r} \mathbb{Z}$. Lemma 4 applies after the change of parameter $x \mapsto 2^r x$, which does not change lengths in $\mathbb{R}^d$, and Lemma 3 gives $D \le D(P)/4^r$. The map $L$ is onto the polygon and $C$ is onto the curve, so the bound holds in both directions. For $d = 1$, $N_1$ is the hat function, and $C = L$. $\blacksquare$

**The open polyline.** For an open polyline line L4 drops the last point in each pass, so one round maps $n$ points to $2n - d$. Each output point is the same combination of $d + 1$ consecutive doubled points as in the closed case, so the output is the first $2n - d$ points of the closed output, and Theorem 1 holds for it on the part of the parameter line where all its basis functions come from the input.
