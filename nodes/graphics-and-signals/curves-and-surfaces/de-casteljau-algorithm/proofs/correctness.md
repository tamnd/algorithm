---
title: The de Casteljau triangle gives the curve point, the tangent, the two halves and a small rounding error
proves: [correctness]
status: full
---

We use the pseudocode of the page. The control points are $P_0, \dots, P_n$ in $\mathbb{R}^d$, the parameter is a real $t$, and $B(t) = \sum_{i=0}^n P_i B_i^n(t)$ with $B_i^n(t) = \binom{n}{i} t^i (1 - t)^{n-i}$ and $B_i^n = 0$ for $i < 0$ or $i > n$. The points of the triangle are $b_i^0 = P_i$ and $b_i^r = (1 - t) b_i^{r-1} + t b_{i+1}^{r-1}$.

**Lemma 0 (the in-place loop).** After round $r$ of line L3, the array entry $b_i$ holds $b_i^r$ for $0 \le i \le n - r$.

*Proof.* Induction on $r$. Before round 1, line L1 gives $b_i = b_i^0$. In round $r$, line L4 visits $i = 0, 1, \dots, n - r$ in this order. When line L5 writes $b_i$, the entries $b_i$ and $b_{i+1}$ have not been written in this round (index $i + 1 > i$, and $b_i$ is written only now), so they hold $b_i^{r-1}$ and $b_{i+1}^{r-1}$ by the induction hypothesis. So line L5 stores $b_i^r$. $\square$

So line L6 stores $\mathrm{left}_r = b_0^r$ and $\mathrm{right}_{n-r} = b_{n-r}^r$, and with line L2, $\mathrm{left} = (b_0^0, \dots, b_0^n)$ and $\mathrm{right} = (b_0^n, b_1^{n-1}, \dots, b_n^0)$.

**Lemma 1 (the points of the triangle).** For all real $t$, $0 \le r \le n$ and $0 \le i \le n - r$,
$$b_i^r = \sum_{j=0}^{r} P_{i+j} B_j^r(t).$$

*Proof.* Induction on $r$. For $r = 0$ both sides are $P_i$. For $r \ge 1$, by the definition and the hypothesis,
$$b_i^r = (1 - t) \sum_{j=0}^{r-1} P_{i+j} B_j^{r-1}(t) + t \sum_{j=1}^{r} P_{i+j} B_{j-1}^{r-1}(t) = \sum_{j=0}^{r} P_{i+j}\big((1 - t) B_j^{r-1}(t) + t B_{j-1}^{r-1}(t)\big),$$
where we used $B_r^{r-1} = 0$ and $B_{-1}^{r-1} = 0$ to extend both sums to $0 \le j \le r$. By Pascal's rule $\binom{r}{j} = \binom{r-1}{j} + \binom{r-1}{j-1}$, the bracket is $B_j^r(t)$. $\square$

**Theorem 1 (the point).** Line L7 returns $b_0^n = B(t)$.

*Proof.* Lemma 1 with $r = n$ and $i = 0$. $\square$

**Lemma 2 (a product identity).** For all real $t, u$ and $0 \le k \le n$, $\sum_{j=k}^{n} B_j^n(u) B_k^j(t) = B_k^n(tu)$.

*Proof.* We use $\binom{n}{j}\binom{j}{k} = \binom{n}{k}\binom{n-k}{j-k}$, which holds because both sides count the ways to choose a set of size $j$ and a subset of it of size $k$ from $n$ items. Put $m = j - k$. Then
$$\sum_{j=k}^n \binom{n}{j} u^j (1-u)^{n-j} \binom{j}{k} t^k (1-t)^{j-k} = \binom{n}{k} (tu)^k \sum_{m=0}^{n-k} \binom{n-k}{m} \big(u(1-t)\big)^m (1-u)^{n-k-m}.$$
By the binomial theorem the last sum is $\big(u(1 - t) + 1 - u\big)^{n-k} = (1 - tu)^{n-k}$. $\square$

**Theorem 2 (the left half).** The Bézier curve $L$ with the control points $\mathrm{left}_j = b_0^j$ satisfies $L(u) = B(tu)$ for all real $u$. So for $t \in (0, 1]$ it is the part of the curve on $[0, t]$, reparametrized to $[0, 1]$.

*Proof.* By Lemma 1, $b_0^j = \sum_{k=0}^{j} P_k B_k^j(t)$. So
$$L(u) = \sum_{j=0}^n B_j^n(u) \sum_{k=0}^{j} P_k B_k^j(t) = \sum_{k=0}^n P_k \sum_{j=k}^n B_j^n(u) B_k^j(t) = \sum_{k=0}^n P_k B_k^n(tu) = B(tu),$$
by Lemma 2. $\square$

**Theorem 3 (the right half).** The Bézier curve $R$ with the control points $\mathrm{right}_k = b_k^{n-k}$, $k = 0, \dots, n$, satisfies $R(v) = B(t + (1 - t) v)$ for all real $v$.

*Proof.* Let $P'_i = P_{n-i}$, with curve $B'(s) = \sum_i P_{n-i} B_i^n(s) = \sum_i P_i B_{n-i}^n(s) = B(1 - s)$, by the symmetry $B_{n-i}^n(s) = B_i^n(1 - s)$. Build the triangle $b'$ of $P'$ with the parameter $t' = 1 - t$. By induction on $r$, $b'^r_i = b_{n-r-i}^r$: this holds for $r = 0$, and
$$b'^r_i = t\, b'^{r-1}_i + (1 - t)\, b'^{r-1}_{i+1} = t\, b^{r-1}_{n-r+1-i} + (1 - t)\, b^{r-1}_{n-r-i} = b^r_{n-r-i}.$$
So the left edge of $b'$ is $b'^j_0 = b^j_{n-j}$. By Theorem 2 for $P'$ and $t'$, the curve with control points $b^j_{n-j}$, $j = 0, \dots, n$, is $u \mapsto B'(t' u) = B(1 - (1 - t) u)$. The polygon $\mathrm{right}$ is this polygon in the opposite order, so by the same symmetry $R(v)$ is this curve at $u = 1 - v$, which is $B(1 - (1 - t)(1 - v)) = B(t + (1 - t) v)$. $\square$

**Theorem 4 (the tangent).** For $n \ge 1$, $B'(t) = n\,(b_1^{n-1} - b_0^{n-1})$.

*Proof.* By the derivative rule of the basis, $\frac{d}{dt} B_i^n = n (B_{i-1}^{n-1} - B_i^{n-1})$. So $B'(t) = n \sum_{i} P_i B_{i-1}^{n-1}(t) - n \sum_i P_i B_i^{n-1}(t) = n \sum_{j=0}^{n-1} P_{j+1} B_j^{n-1}(t) - n \sum_{j=0}^{n-1} P_j B_j^{n-1}(t)$. By Lemma 1 with $r = n - 1$, the two sums are $b_1^{n-1}$ and $b_0^{n-1}$. $\square$

**Theorem 5 (convexity).** For $t \in [0, 1]$, each $b_i^r$ is a convex combination of $P_i, \dots, P_{i+r}$.

*Proof.* In Lemma 1 the weights $B_j^r(t)$ are nonnegative for $t \in [0, 1]$, and they sum to $(t + 1 - t)^r = 1$. $\square$

**Theorem 6 (rounding error).** Use floating point arithmetic in the standard model: for each operation, $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$. Let $t \in [0, 1]$ and the coordinates of the $P_i$ be floating point numbers, and let $3 n u < 1$. Let $\hat s = \mathrm{fl}(1 - t)$. Then for each coordinate, the computed value $\hat b$ of $b_0^n$ satisfies
$$|\hat b - B(t)| \le \gamma_{3n} \sum_{i=0}^n |P_i| B_i^n(t) \le \gamma_{3n} \max_i |P_i|, \qquad \gamma_k = \frac{k u}{1 - k u}.$$

*Proof.* Fix one coordinate. One step of line L5 computes $\mathrm{fl}(\mathrm{fl}(\hat s\, x) + \mathrm{fl}(t\, y))$ from the computed values $x = \hat b_i^{r-1}$ and $y = \hat b_{i+1}^{r-1}$. With $\hat s = (1 - t)(1 + \delta_0)$, this is
$$(1 - t)\, x\, (1 + \delta_0)(1 + \delta_1)(1 + \delta_3) + t\, y\, (1 + \delta_2)(1 + \delta_3),$$
with $|\delta_k| \le u$. So each step multiplies the value from the left by $(1 - t)$ and at most three factors $1 + \delta$, and the value from the right by $t$ and at most two such factors.

Unroll the triangle. A path from the apex $b_0^n$ down to $P_k$ makes $n$ steps, $k$ of them to the right and $n - k$ to the left, and there are $\binom{n}{k}$ such paths. By induction on $r$, the computed value is
$$\hat b = \sum_{k=0}^n P_k \sum_{\pi \text{ ends at } k} (1 - t)^{n-k} t^k \prod_{\text{factors on } \pi} (1 + \delta),$$
where each path $\pi$ carries at most $3n$ factors $1 + \delta$. (The $\delta$ of different paths differ, because the paths share some operations and not others, but each one is bounded by $u$.) By Lemma 3.1 of Higham, a product of at most $3n$ factors $1 + \delta$ with $|\delta| \le u$ is $1 + \theta$ with $|\theta| \le \gamma_{3n}$ when $3 n u < 1$. So
$$\hat b - B(t) = \sum_{k=0}^n P_k \sum_{\pi \text{ ends at } k} (1 - t)^{n-k} t^k\, \theta_\pi,$$
and, because $(1 - t)^{n-k} t^k \ge 0$ for $t \in [0, 1]$,
$$|\hat b - B(t)| \le \gamma_{3n} \sum_{k=0}^n |P_k| \binom{n}{k} (1 - t)^{n-k} t^k = \gamma_{3n} \sum_k |P_k| B_k^n(t).$$
The last bound follows from $\sum_k B_k^n(t) = 1$. $\blacksquare$

When $1 - t$ is exact, for example for $t \in [1/2, 1]$ by Sterbenz's lemma, the factor $1 + \delta_0$ is 1 and the same proof gives $\gamma_{2n}$.
