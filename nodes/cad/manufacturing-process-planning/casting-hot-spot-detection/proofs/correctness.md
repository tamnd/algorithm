---
title: HOT-SPOTS computes the exact squared distance to the mold and returns exactly the regional maxima
proves: [correctness]
status: full
---

We use the definitions of the page. The grid has $k$ axes, and a cell is a vector $x$ of $k$ integer indices. $M_0$ is the set of mold cells, which is not empty. For a real number $u$ and a cell index $p$ with a finite value $f(p)$, the parabola of $p$ is $P_p(u) = (u - p)^2 + f(p)$.

**Lemma 1 (two parabolas).** For $p < r$, the difference $P_r(u) - P_p(u) = \bigl(f(r) + r^2\bigr) - \bigl(f(p) + p^2\bigr) - 2u(r - p)$ is strictly decreasing in $u$ and is zero at

$$s(p, r) = \frac{\bigl(f(r) + r^2\bigr) - \bigl(f(p) + p^2\bigr)}{2(r - p)}.$$

So $P_r(u) \le P_p(u)$ if and only if $u \ge s(p, r)$.

*Proof.* Expand both squares: the terms $u^2$ cancel, and what is left is linear in $u$ with the slope $-2(r - p) < 0$. $\square$

**Lemma 2 (the lower envelope).** For a line $f(0), \dots, f(n-1)$ in which some values may be infinite, LOWER-ENVELOPE returns $d(q) = \min_p P_p(q)$ over the $p$ with $f(p)$ finite, and $d(q) = \infty$ for all $q$ if there are none.

*Proof.* The procedure takes the finite points in increasing order and keeps a stack $v_1 < \dots < v_m$ with breakpoints $z_1 = -\infty$ and $z_j = s(v_{j-1}, v_j)$ for $j \ge 2$. Let $F$ be the function equal to $P_{v_j}$ on $[z_j, z_{j+1})$, with $z_{m+1} = \infty$. Let $E$ be the minimum of the parabolas of all points processed so far. While the procedure processes a new point $r$, these hold:

- (I1) $z_1 < z_2 < \dots < z_m$;
- (I2) $F(u) = \min_{j \le m} P_{v_j}(u)$ for all real $u$;
- (I3) $\min\bigl(F(u), P_r(u)\bigr) = \min\bigl(E(u), P_r(u)\bigr)$ for all real $u$.

Before the first pop for $r$, the stack is the result of the earlier steps, so (I1) and (I2) hold by induction and $F = E$, which gives (I3). For the first point, the stack is empty and the procedure pushes it with $z_1 = -\infty$, and all three hold.

*A pop.* Let $m \ge 2$ and $s(v_m, r) \le z_m$. For $u \ge z_m$, Lemma 1 gives $P_r(u) \le P_{v_m}(u) = F(u)$. Let $F^-$ be the function of the stack without $v_m$, in which $P_{v_{m-1}}$ runs from $z_{m-1}$ to $\infty$.

(I2) for $F^-$: on $(-\infty, z_m)$, $F^- = F$, which is the minimum over all $m$ parabolas, so also over the first $m - 1$. On $[z_{m-1}, z_m)$, which is not empty by (I1), $P_{v_{m-1}} = F \le P_{v_i}$ for every $i < m - 1$. By Lemma 1, $P_{v_{m-1}} - P_{v_i}$ is decreasing, so it stays at most 0 for all $u \ge z_m$ as well.

(I3) for $F^-$: on $(-\infty, z_m)$ nothing changes. On $[z_m, \infty)$, $\min(F, P_r) = P_r$, as shown above. Also $P_{v_m} \le P_{v_{m-1}}$ there, by Lemma 1, since $z_m = s(v_{m-1}, v_m)$. So $P_r \le P_{v_m} \le P_{v_{m-1}} = F^-$, and $\min(F^-, P_r) = P_r$ too.

(I1) holds for the shorter stack. So a pop keeps the invariants.

*A push.* The loop stops when $m = 1$ or $s = s(v_m, r) > z_m$, and the procedure pushes $r$ with $z_{m+1} = s$. Then (I1) holds. Let $G$ be the new stack function: $F$ on $(-\infty, s)$ and $P_r$ on $[s, \infty)$. We show that $G = \min(F, P_r)$, which by (I3) is the minimum of all parabolas processed so far, so that (I2) and $G = E$ hold for the next point.

- On $[s, \infty)$: $P_r \le P_{v_m}$ by Lemma 1. Also $s > z_m$, so $F = P_{v_m}$ there, and $G = P_r = \min(F, P_r)$.
- On $(-\infty, s)$: $P_r > P_{v_m}$ by Lemma 1, and $P_{v_m} \ge F$ by (I2). So $\min(F, P_r) = F = G$.

*The read-out.* After the last point, $F = E$ is the lower envelope of all finite parabolas. For an integer $q$, the procedure finds the index $j$ with $z_j < q \le z_{j+1}$, by moving right while $z_{j+1} < q$, and returns $P_{v_j}(q)$. If $q < z_{j+1}$ this is $F(q)$. If $q = z_{j+1}$, the two parabolas $P_{v_j}$ and $P_{v_{j+1}}$ are equal at $q$, so the value is $F(q)$ again.

*Exactness.* Every breakpoint is a fraction of integers with a positive denominator $2(r - p)$. The procedure compares $a/b \le c/e$ as $a e \le c b$ and $a/b < q$ as $a < q b$, with integers only, so no comparison is rounded. If no value is finite, the stack stays empty, and every $d(q)$ is infinite. $\square$

**Lemma 3 (one axis at a time).** After the passes over the axes $1, \dots, a$, every cell $x$ holds

$$f_a(x) = \min \Bigl\{ \sum_{i \le a} (x_i - y_i)^2 \;:\; y \in M_0, \; y_i = x_i \text{ for all } i > a \Bigr\},$$

with the minimum of an empty set equal to $\infty$.

*Proof.* By induction on $a$. For $a = 0$, the set holds only $y = x$ if $x$ is a mold cell and is empty otherwise, so $f_0(x) = 0$ or $\infty$, as set by line L1. For the step, the pass over axis $a$ works on the line of cells that agree with $x$ in all coordinates except the $a$-th. By Lemma 2 it sets

$$f_a(x) = \min_p \Bigl((x_a - p)^2 + f_{a-1}(x \text{ with } x_a \text{ replaced by } p)\Bigr).$$

Put in $f_{a-1}$ from the induction hypothesis. The cells $y$ in the inner minimum have $y_a = p$, and the outer minimum runs over all $p$. So the two minima join into one minimum over the mold cells $y$ with $y_i = x_i$ for $i > a$, of $(x_a - y_a)^2 + \sum_{i < a} (x_i - y_i)^2$. That is the claim for $a$. $\square$

**Theorem 1 (the distance).** After line L4, $D(x) = \min_{y \in M_0} \lVert x - y \rVert^2$ for every cell $x$, and every value is a finite integer.

*Proof.* Lemma 3 with $a = k$ has no constraint left on $y$. $M_0$ is not empty, so the minimum is finite. All values are sums and minima of integers. $\square$

**Theorem 2 (the maxima).** Call a *plateau* a connected set of metal cells with one value $c$ of $D$, under the full neighbourhood, that is maximal with this property. A plateau is a *regional maximum* if every cell outside it that is a neighbour of one of its cells has $D < c$. HOT-SPOTS returns each regional maximum exactly once, with its value, and nothing else, sorted by value from the largest.

*Proof.* A mold cell has $D = 0$, and a metal cell has $D \ge 1$, since its nearest mold cell is a different cell with integer coordinates. So a neighbour with $D = c \ge 1$ is a metal cell. The search at line L5 starts at a metal cell not yet seen and adds every metal neighbour with the same value that is not yet seen. This is a graph search on the graph whose nodes are the metal cells of value $c$ and whose edges join neighbours, so it collects exactly the connected component of the start cell, which is its plateau. Every cell of the plateau is marked seen, so no later search starts in it, and each plateau is found once.

During the search, line L6 looks at every neighbour of every cell of the plateau. A neighbour with $D > c$ sets the flag to false. A neighbour with $D = c$ is in the plateau, by maximality. So the flag stays true if and only if every neighbour outside the plateau has $D < c$, which is the definition of a regional maximum. Line L7 sorts the kept plateaus by their value. $\blacksquare$
