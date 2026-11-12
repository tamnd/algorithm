---
title: Chaikin corner cutting is knot insertion for the uniform quadratic B-spline, and the polygons converge to it
proves: [correctness, convergence-rate]
status: full
---

We use the pseudocode of the page for a closed polygon $P_0, \dots, P_{m-1}$, with indices modulo $m$. The uniform B-splines are defined by convolution: $N_0$ is the indicator function of $[0, 1)$, and $N_d = N_{d-1} * N_0$, so $N_d$ is a piecewise polynomial of degree $d$ with support $[0, d + 1]$. The quadratic one is

$$N_2(x) = \tfrac12 x^2 \text{ on } [0, 1], \quad \tfrac12(-2x^2 + 6x - 3) \text{ on } [1, 2], \quad \tfrac12 (3 - x)^2 \text{ on } [2, 3],$$

and $0$ elsewhere. The curve of the polygon is $C(x) = \sum_{i \in \mathbb{Z}} P_i N_2(x - i)$, with $P_{i+m} = P_i$, so $C$ has period $m$.

**Lemma 1 (refinement).** $N_d(x) = 2^{-d} \sum_{k=0}^{d+1} \binom{d+1}{k} N_d(2x - k)$ for all $d \ge 0$.

*Proof.* For $d = 0$ this is $N_0(x) = N_0(2x) + N_0(2x - 1)$, which holds because $[0, 1)$ is the union of $[0, \tfrac12)$ and $[\tfrac12, 1)$. Assume $f(x) = \sum_k a_k g(2x - k)$ and $h(x) = \sum_l b_l g'(2x - l)$ with finite sums. Then

$$(f * h)(x) = \sum_{k, l} a_k b_l \int g(2y - k)\, g'(2x - 2y - l)\, dy = \tfrac12 \sum_{k, l} a_k b_l\, (g * g')(2x - k - l),$$

by the change of variables $z = 2y - k$. So the coefficients of a convolution are half the product of the coefficient sequences. With $N_d = N_{d-1} * N_0$ and induction, the coefficients of $N_d$ are $2^{-d}$ times the coefficients of $(1 + z)^{d+1}$. $\square$

**Lemma 2 (one round).** One round of lines L2 to L6 gives the polygon $R_j$, $j = 0, \dots, 2m - 1$, with $R_{2i} = \tfrac34 P_i + \tfrac14 P_{i+1}$ and $R_{2i+1} = \tfrac14 P_i + \tfrac34 P_{i+1}$. Then $C(x) = \sum_{j} R_j N_2(2x - j - 2)$, so $R$ is the control polygon of the same curve on the knots $\tfrac12 \mathbb{Z}$.

*Proof.* Lemma 1 for $d = 2$ has the coefficients $c = (\tfrac14, \tfrac34, \tfrac34, \tfrac14)$. So

$$C(x) = \sum_i P_i \sum_{k=0}^{3} c_k N_2(2x - 2i - k) = \sum_{j} N_2(2x - j) \sum_i c_{j - 2i} P_i.$$

For $j = 2i + 2$ the inner sum is $c_2 P_i + c_0 P_{i+1} = \tfrac34 P_i + \tfrac14 P_{i+1} = R_{2i}$. For $j = 2i + 3$ it is $c_3 P_i + c_1 P_{i+1} = \tfrac14 P_i + \tfrac34 P_{i+1} = R_{2i+1}$. So the coefficient of $N_2(2x - j)$ is $R_{j-2}$. The sequence $R$ has period $2m$, as the loop of line L3 computes it. $\square$

By induction on the round, the polygon after $r$ rounds is a control polygon of the same curve $C$ on the knots $2^{-r} \mathbb{Z}$. So no round changes the curve.

**Lemma 3 (distance to the curve).** Let $\Delta_i = P_{i-1} - 2 P_i + P_{i+1}$ and $D = \max_i |\Delta_i|$. Then every point of $C$ is within $D / 8$ of the polygon, and every point of the polygon is within $D / 8$ of $C$.

*Proof.* On $[i + 2, i + 3]$ only $N_2(x - i)$, $N_2(x - i - 1)$ and $N_2(x - i - 2)$ are nonzero. With the formula of $N_2$, $C(i + 2) = M_i = \tfrac12 (P_i + P_{i+1})$, $C(i + 3) = M_{i+1}$ and $C'(i + 2) = P_{i+1} - P_i$. A quadratic is fixed by these three values, so the span is the quadratic Bézier curve with control points $M_i, P_{i+1}, M_{i+1}$. Write $s \in [0, 1]$ for the local parameter. On $s \le \tfrac12$, compare it with the point $L(s) = M_i + 2s (P_{i+1} - M_i)$ of the polygon edge from $M_i$ to $P_{i+1}$:

$$B(s) - L(s) = s^2 (M_i - 2 P_{i+1} + M_{i+1}) = \tfrac12 s^2 \Delta_{i+1}.$$

So $|B(s) - L(s)| \le \tfrac18 |\Delta_{i+1}| \le D/8$, and the case $s \ge \tfrac12$ is the same by symmetry. The map $s \mapsto L(s)$ covers the two half edges from $M_i$ to $P_{i+1}$ and from $P_{i+1}$ to $M_{i+1}$, and the spans cover the whole curve and the whole polygon. This gives both claims. $\square$

**Lemma 4 (the second differences).** The polygon $R$ of Lemma 2 has $R_{2i} - 2 R_{2i+1} + R_{2i+2} = \tfrac14 (P_i - 2 P_{i+1} + P_{i+2})$ and $R_{2i-1} - 2 R_{2i} + R_{2i+1} = \tfrac14 (P_{i-1} - 2 P_i + P_{i+1})$. So $D$ drops by the factor 4 in each round.

*Proof.* Substitute the formulas of Lemma 2. In the first case the coefficients of $P_i$, $P_{i+1}$ and $P_{i+2}$ are $\tfrac34 - \tfrac12$, $\tfrac14 - \tfrac32 + \tfrac34$ and $\tfrac14$, which are $\tfrac14$, $-\tfrac12$ and $\tfrac14$. The second case is the same with $i - 1$ in place of $i$. $\square$

**Theorem.** After $r$ rounds, the polygon and the uniform quadratic B-spline curve $C$ of the input are within Hausdorff distance $D / (8 \cdot 4^r)$. So the polygons converge to $C$.

*Proof.* By Lemma 2 and induction, the polygon after $r$ rounds is a control polygon of $C$ on the knots $2^{-r} \mathbb{Z}$. Lemma 3 holds for these knots by the change of variable $x \mapsto 2^r x$, which does not change distances in $\mathbb{R}^d$. By Lemma 4 its largest second difference is $D / 4^r$. Lemma 3 then gives the bound. $\blacksquare$

**The open polyline.** For an open polyline $P_0, \dots, P_{n-1}$ the loop of line L3 skips the edge from $P_{n-1}$ to $P_0$. The output is the first $2(n - 1)$ points of the closed output, and each of them depends only on one edge. Lemma 2 and Lemma 4 hold for them. The curve of the new polygon runs from the midpoint of $R_0 R_1$, which is $M_0$, to the midpoint of its last edge, which is $M_{n-2}$, so it is the part of $C$ between $M_0$ and $M_{n-2}$. Lemma 3 covers the polygon from the midpoint of its first edge to the midpoint of its last edge. The two half edges at the ends are outside this part, and their length halves in each round, so the open polygons also converge to this part of $C$.
