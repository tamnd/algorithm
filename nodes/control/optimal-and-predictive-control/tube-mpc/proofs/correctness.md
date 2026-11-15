---
title: The error set is robustly invariant, so the tube controller meets the constraints for every disturbance, stays feasible, and drives the state to the error set
proves: [correctness]
status: full
---

**Setting.** The plant is $x^+ = A x + B u + w$ with $w \in W$, where $W = \{\sum_j \xi_j g_j : |\xi_j| \le 1\}$ is a zonotope whose generators $g_j$ span $\mathbb{R}^n$. The gain $K$ makes $A_K = A + B K$ Schur. The constraints are polyhedra $X = \{x : a^T x \le b \text{ for each row}\}$ and $U = \{u : a^T u \le b\}$. For a set $S$ and a vector $a$, the support function is $h_S(a) = \max_{s \in S} a^T s$. For zonotopes, $h_S(a) = \sum_j |a^T g_j|$, $h_{S_1 \oplus S_2} = h_{S_1} + h_{S_2}$, $h_{\lambda S} = \lambda h_S$ for $\lambda \ge 0$, and $h_{M S}(a) = h_S(M^T a)$.

## Part 1: the facet rows of a zonotope

**Lemma 1.** Let $Z$ be a zonotope in $\mathbb{R}^n$ whose generators span $\mathbb{R}^n$. The rows $(c, h_Z(c))$ and $(-c, h_Z(c))$, where $c$ runs over the nonzero cofactor vectors of the $(n-1)$-subsets of generators, describe $Z$ exactly. For $n = 1$, $Z = [-h_Z(1), h_Z(1)]$.

*Proof.* Each row is valid for $Z$, since $c^T z \le h_Z(c)$ on $Z$ by the definition of $h_Z$. So $Z$ lies in the intersection. $Z$ is a full-dimensional polytope, so it equals the intersection of the halfspaces of its facets. Let $F$ be a facet with outer normal $d$. The points of $Z$ that maximize $d^T z$ are $\sum_{d^T g_j \ne 0} \mathrm{sign}(d^T g_j) g_j + \{\sum_{d^T g_j = 0} \xi_j g_j : |\xi_j| \le 1\}$. This set has dimension $n - 1$, so the generators with $d^T g_j = 0$ span the $(n-1)$-dimensional subspace $d^\perp$. Choose $n - 1$ linearly independent ones. Their cofactor vector $c$ (the generalized cross product) is nonzero and orthogonal to all of them, so $c$ is parallel to $d$, and one of $\pm c$ is a positive multiple of $d$. The row for that sign is the facet inequality of $F$, scaled. Hence the rows cut out exactly $Z$. $\square$

## Part 2: the error set

**Lemma 2 (Raković, Kerrigan, Kouramas and Mayne 2005).** Let $s \ge 1$ and $\alpha \in [0, 1)$ satisfy $A_K^s W \subseteq \alpha W$, and let $Z = (1 - \alpha)^{-1} \bigoplus_{i=0}^{s-1} A_K^i W$. Then $A_K Z \oplus W \subseteq Z$, and $Z$ contains $\bigoplus_{i=0}^{t-1} A_K^i W$ for every $t$.

*Proof.* Write $F_s = \bigoplus_{i<s} A_K^i W$. Then

$$A_K Z \oplus W = (1 - \alpha)^{-1} \bigoplus_{i=1}^{s} A_K^i W \oplus W \subseteq (1 - \alpha)^{-1} \Big(\bigoplus_{i=1}^{s-1} A_K^i W \oplus \alpha W\Big) \oplus W = (1 - \alpha)^{-1} \bigoplus_{i=1}^{s-1} A_K^i W \oplus (1 - \alpha)^{-1} W = Z,$$

where the middle step uses $\frac{\alpha}{1 - \alpha} W \oplus W = \frac{1}{1 - \alpha} W$, which holds because $W$ is convex. For the second claim, $0 \in W$ gives $0 \in Z$, and applying $e \mapsto A_K e + w$ $t$ times from $0$ reaches every point of $\bigoplus_{i<t} A_K^i W$ and stays in $Z$ by the first claim. $\square$

**The test in line L1.** $W$ is symmetric with $0$ in its interior, so by Lemma 1 it is $\{w : c^T w \le b_c\}$ with all $b_c > 0$. Then $A_K^s W \subseteq \alpha W$ if and only if $h_{A_K^s W}(c) \le \alpha b_c$ for every row, and the least such $\alpha$ is $\max_c h_{A_K^s W}(c) / b_c$, which `rpi_outer` computes. Since $A_K$ is Schur, $A_K^s \to 0$, so this $\alpha$ tends to 0, and the loop stops for any `alpha_max` $> 0$ (and also for `alpha_max` $= 0$ when $A_K$ is nilpotent). The returned generators are those of $Z$.

## Part 3: the tube

Let $\bar X$ and $\bar U$ be the rows of $X$ and $U$ with $b$ replaced by $b - h_Z(a)$ and $b - h_Z(K^T a)$ (line L2); these are $X \ominus Z$ and $U \ominus K Z$.

**Lemma 3.** If $x - z \in Z$, $u = v + K (x - z)$, $z^+ = A z + B v$ and $x^+ = A x + B u + w$ with $w \in W$, then $x^+ - z^+ \in Z$. If moreover $z \in \bar X$ and $v \in \bar U$, then $x \in X$ and $u \in U$.

*Proof.* $x^+ - z^+ = A (x - z) + B K (x - z) + w = A_K (x - z) + w \in A_K Z \oplus W \subseteq Z$ by Lemma 2. For a row $a$ of $X$, $a^T x = a^T z + a^T (x - z) \le (b - h_Z(a)) + h_Z(a) = b$. For a row of $U$, $a^T u = a^T v + (K^T a)^T (x - z) \le (b - h_Z(K^T a)) + h_Z(K^T a) = b$. $\square$

## Part 4: the nominal LP

From the measured state $x$, `tube_mpc` solves

$$V(x) = \min_{z_0, v_0, \dots, v_{N-1}} \sum_{k=0}^{N-1} \left(\|Q z_k\|_1 + \|R v_k\|_1\right)$$

subject to $x - z_0 \in Z$ (the rows of Lemma 1), $z_{k+1} = A z_k + B v_k$, $z_k \in \bar X$ and $v_k \in \bar U$ for $k < N$, and $z_N = 0$. The states $z_k$ are affine in $(z_0, v)$ and are substituted. Each $|\cdot|$ is an epigraph variable $\sigma \ge 0$ with $\sigma \ge \pm(\cdot)$; for fixed $(z_0, v)$ the least feasible sum of the epigraph variables is the cost, so the LP value is $V(x)$. The LP is solved by the two-phase simplex method with Bland's rule, which ends after finitely many pivots and is exact for rational data and `tol = 0`; the cost is a sum of nonnegative variables, so it is bounded below and never unbounded.

Write $\ell(z, v) = \|Q z\|_1 + \|R v\|_1$ and assume $0 \in \bar X$ and $0 \in \bar U$ (the tightened bounds are nonnegative).

**Theorem.** If the LP is feasible at $x_0$, then for every disturbance sequence in $W$:

1. the LP is feasible at every sample;
2. $x_k \in X$ and $u_k \in U$ for all $k$;
3. $V(x_{k+1}) \le V(x_k) - \ell(z_0^*(x_k), v_0^*(x_k))$;
4. if $Q$ has full column rank, then $z_0^*(x_k) \to 0$ and the distance from $x_k$ to $Z$ tends to 0.

*Proof.* Let $(z_0^*, v_0^*, \dots, v_{N-1}^*)$ be optimal at $x$, with states $z_k^*$ and $z_N^* = 0$. The applied input is $u = v_0^* + K (x - z_0^*)$ (line L6). Consider at $x^+$ the candidate $z_0' = z_1^*$ and $v' = (v_1^*, \dots, v_{N-1}^*, 0)$. Its states are $z_k' = z_{k+1}^*$ for $k < N$ and $z_N' = A z_N^* + B \cdot 0 = 0$.

- $x^+ - z_0' = x^+ - z_1^* \in Z$ by Lemma 3 with $z = z_0^*$, $v = v_0^*$.
- $z_k' = z_{k+1}^* \in \bar X$ for $k \le N - 2$, and $z_{N-1}' = z_N^* = 0 \in \bar X$.
- $v_k' = v_{k+1}^* \in \bar U$ for $k \le N - 2$, and $v_{N-1}' = 0 \in \bar U$.

So the candidate is feasible, which proves (1) by induction, and its cost is $V(x) - \ell(z_0^*, v_0^*) + \ell(0, 0) = V(x) - \ell(z_0^*, v_0^*)$, which proves (3). Lemma 3 with $z = z_0^* \in \bar X$ and $v = v_0^* \in \bar U$ gives (2). Summing (3) gives $\sum_k \ell(z_0^*(x_k), v_0^*(x_k)) \le V(x_0) < \infty$, so $\ell(z_0^*(x_k), \cdot) \to 0$. If $Q$ has full column rank, $\|Q z\|_1 \ge \mu \|z\|$ for some $\mu > 0$, so $z_0^*(x_k) \to 0$. Since $x_k \in z_0^*(x_k) \oplus Z$, the distance from $x_k$ to $Z$ is at most $\|z_0^*(x_k)\|$, which tends to 0. $\square$

## Part 5: what the code computes

- **Line L1** is `rpi_outer`, the test and the set of Part 2.
- **Line L2** is `tighten`, the sets $\bar X$ and $\bar U$ of Part 3.
- **Line L3** is the loop over the samples in `closed_loop`.
- **Line L4** writes the rows of Part 4: $x - z_0 \in Z$ by the rows of Lemma 1, the tightened state and input rows, the equality $z_N = 0$, and the epigraph rows.
- **Line L5** solves the LP.
- **Line L6** applies $u = v_0^* + K (x - z_0^*)$ and updates the plant.
