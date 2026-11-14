---
title: The interval projected polyhedron method keeps every root of the system in the box and stops
proves: [correctness]
status: full
---

The input is $m$ polynomials $f_1, \dots, f_m$ in $n$ variables and a box $X_0 = \prod_j [a_j, b_j]$ with rational ends. A *root* is a point $x \in X_0$ with $f_1(x) = \dots = f_m(x) = 0$. Every box $X = \prod_j [\alpha_j, \beta_j]$ of the method has exact rational ends, and its local coordinates are $u_j = (x_j - \alpha_j) / (\beta_j - \alpha_j)$ when $\beta_j > \alpha_j$. Let $d_j$ be the degree of $f_k$ in $x_j$. On $X$, $f_k$ has the tensor product Bernstein form

$$f_k(x) = \sum_I b_I \, B_I(u), \qquad B_I(u) = \prod_{j=1}^{n} B_{i_j, d_j}(u_j), \qquad B_{i, d}(t) = \binom{d}{i} t^i (1 - t)^{d - i},$$

over the multi-indices $I = (i_1, \dots, i_n)$ with $0 \le i_j \le d_j$; see [Bernstein polynomials](/bernstein-polynomials/). The method stores, for each $k$ and $I$, a float interval $[\ell_I, h_I]$. The **invariant** is that $\ell_I \le b_I \le h_I$ for the exact coefficients $b_I$ of $f_k$ on the box the intervals are stored with.

**Claim 1 (three facts on the basis).** For $u \in [0, 1]^n$: $B_I(u) \ge 0$, $\sum_I B_I(u) = 1$, and if $d_j \ge 1$, $\sum_I \tfrac{i_j}{d_j} B_I(u) = u_j$.

*Proof.* Each factor is a product of nonnegative numbers. By the binomial theorem $\sum_{i=0}^{d} B_{i,d}(t) = (t + 1 - t)^d = 1$, and the sum over $I$ is the product of these $n$ sums. For the last fact, $\tfrac{i}{d} \binom{d}{i} = \binom{d - 1}{i - 1}$ for $i \ge 1$, so

$$\sum_{i=0}^{d} \tfrac{i}{d} B_{i,d}(t) = t \sum_{i=1}^{d} \binom{d-1}{i-1} t^{i-1} (1 - t)^{d - i} = t,$$

and the sums over the other indices are $1$. $\square$

**Claim 2 (the hull and the axis).** Let $E$ be a finite set of points $(\tau, \varphi)$ in the plane, and let $C$ be the set made of the $\tau$ of the points with $\varphi = 0$ and of the crossings

$$c_{pq} = \frac{\varphi_p \tau_q - \varphi_q \tau_p}{\varphi_p - \varphi_q}$$

of the segments from a point $p$ with $\varphi_p > 0$ to a point $q$ with $\varphi_q < 0$. If $(\tau, 0)$ is in the convex hull of $E$, then $C$ is not empty and $\min C \le \tau \le \max C$.

*Proof.* Write $(\tau, 0) = \sum_e \lambda_e e$ with $\lambda_e \ge 0$ and $\sum_e \lambda_e = 1$, and split $E$ into $E_+$, $E_0$ and $E_-$ by the sign of $\varphi$. The second coordinate gives $W := \sum_{p \in E_+} \lambda_p \varphi_p = \sum_{q \in E_-} \lambda_q (-\varphi_q)$. If $W = 0$, all the weight is on $E_0$, so $\tau$ is a convex combination of the $\tau$ of the points of $E_0$, which are in $C$. If $W > 0$, put $\mu_{pq} = \lambda_p \lambda_q (\varphi_p - \varphi_q) / W \ge 0$ for $p \in E_+$, $q \in E_-$. Then

$$\sum_{p, q} \mu_{pq} c_{pq} = \frac{1}{W} \sum_{p, q} \lambda_p \lambda_q (\varphi_p \tau_q - \varphi_q \tau_p) = \sum_q \lambda_q \tau_q + \sum_p \lambda_p \tau_p,$$

and in the same way $\sum_{p,q} \mu_{pq} = \sum_{q} \lambda_q + \sum_p \lambda_p$. So $\tau = \sum_{e \in E_0} \lambda_e \tau_e + \sum_{p,q} \mu_{pq} c_{pq}$ with nonnegative weights of sum $1$, a convex combination of elements of $C$. In both cases $C \ne \emptyset$ and $\tau$ lies between $\min C$ and $\max C$. $\square$

**Claim 3 (line L4 keeps every root).** Assume the invariant on a box $X$, and let $x \in X$ be a zero of $f_k$ with local coordinates $u$. Then for every axis $j$ the interval $[s, t]$ that line L4 computes from $f_k$ exists and contains $u_j$.

*Proof.* For each column $i$ of axis $j$ the code takes $m_i = \min \ell_I$ and $M_i = \max h_I$ over the $I$ with $i_j = i$. If $d_j = 0$, the polynomial does not depend on $x_j$, and $0 = f_k(x) = \sum_I B_I(u) b_I$ is a convex combination of the $b_I$ by Claim 1, so $m_0 \le \min b_I \le 0 \le \max b_I \le M_0$, and the code returns $[0, 1] \ni u_j$. If $d_j \ge 1$, Claim 1 gives

$$(u_j, 0) = \big(u_j, f_k(x)\big) = \sum_I B_I(u) \left(\tfrac{i_j}{d_j}, \, b_I\right),$$

a convex combination of the projected control points. By the invariant each point $(i/d_j, b_I)$ lies on the segment from $(i/d_j, m_i)$ to $(i/d_j, M_i)$, so $(u_j, 0)$ is in the convex hull of the set $E$ of these $2(d_j + 1)$ ends. By Claim 2, the set $C$ is not empty and $\min C \le u_j \le \max C$. The code computes $\min C$ and $\max C$ exactly in rational arithmetic, rounds the first down and the second up to floats, and clips to $[0, 1]$, which contains $u_j$. $\square$

So a box that line L5 discards has no root: either some $f_k$ gives no interval on some axis, or the intervals of two equations on one axis are disjoint, and in both cases Claim 3 rules out a root. If the box is kept, every root in it has local coordinates in $\prod_j [s_j, t_j]$, the intersection over $k$.

**Claim 4 (lines L7 and L8 keep the invariant and the roots).** The de Casteljau scheme at a parameter $\tau \in [0, 1]$ along axis $j$ maps the Bernstein coefficients on a box to those on its two parts at the local value $\tau$ of $u_j$; this is the subdivision property of the [de Casteljau algorithm](/de-casteljau-algorithm/), applied to each line of the tensor along axis $j$ (cited, not proved here). The code runs it in [interval arithmetic](/interval-arithmetic/) where each sum and product is computed in round to nearest and then widened by one float step down and up. With round to nearest, the exact value of an operation lies between the two floats next to the rounded value, so each computed interval contains the exact result of the same operation on any numbers in the input intervals, provided that no operation overflows. The value $1 - \tau$ is also enclosed in an interval. By induction over the steps of the scheme, the new intervals contain the exact coefficients on the parts, and the invariant holds.

Line L7 first keeps the part $[0, t_j]$, at the float $t_j$. Then it keeps the part $[r, 1]$ of that, with $r$ the float $s_j / t_j$ rounded down, so that the kept local range is $[r t_j, t_j] \supseteq [s_j, t_j]$. The new ends are computed exactly from $r$ and $t_j$ in rational arithmetic, so the coefficients belong to the stored box and every root of $X$ is in the new box. Line L8 splits at the local value $1/2$ into two closed halves whose union is the box, and each root is in one of them. $\square$

**Claim 5 (termination).** Let $W = \max_j (b_j - a_j)$ and $\varepsilon > 0$. Every path from $X_0$ in the tree of boxes has at most $n (1 + \log_2(W / \varepsilon)) + 1$ steps, and the method stops.

*Proof.* A step that does not discard or output its box has a widest side $j^*$ of width $w \ge \varepsilon$, by line L6. Line L7 only shrinks the sides. If side $j^*$ is then still longer than $w/2$, line L8 halves it; otherwise it is already at most $w / 2$. So each such step at least halves one side of width at least $\varepsilon$. A side of initial width $w_0 \le W$ that has been halved $k$ times in this way had width at most $w_0 / 2^{k-1}$ before the last of them, and at least $\varepsilon$, so $k \le 1 + \log_2(W / \varepsilon)$. Summing over the $n$ sides and adding the last step bounds the path length. Each box has at most two children, so the tree is finite, and the stack is empty after finitely many steps. $\square$

**Conclusion.** By induction over the tree, with Claims 3 and 4 as the step: every root in $X_0$ stays in some box on a path of the tree, and the path ends at line L6, since line L5 never discards a box that holds a root. So every root lies in an output box, every output box passed the test of line L4 and has all sides shorter than $\varepsilon$, and line L10, which only groups boxes, keeps them all.

What is not proved is the converse: an output box need not hold a root, near a root the method can return several boxes, and the number of groups need not be the number of roots. Nor is a rate of convergence proved. The tests measure, for systems with known simple roots, that each group holds exactly one root, and that the boxes of a tangent root form one group. $\blacksquare$
