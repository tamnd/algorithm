---
title: The RoI pooling bins cover the box with nonempty, nearly disjoint ranges, the forward pass is the bin maximum, and the backward pass is its gradient
proves: [correctness]
status: full
---

Fix a box with $h \ge 1$ rows starting at row $r_1$ and an output height $H \ge 1$. For $0 \le p < H$ let $a_p = \lfloor p h / H \rfloor$ and $e_p = \lceil (p + 1) h / H \rceil$, so line L4 gives the rows $[r_1 + a_p, r_1 + e_p)$ before the clipping. The columns behave the same way with $w$ and $W$.

**Claim 1 (the bins).** Before the clipping:

1. every range is nonempty: $a_p < e_p$;
2. the first range starts at $r_1$ and the last ends at $r_1 + h$: $a_0 = 0$ and $e_{H-1} = h$;
3. next ranges leave no gap and share at most one row: $a_{p+1} \le e_p \le a_{p+1} + 1$;
4. the ranges cover $[r_1, r_1 + h)$, and their lengths sum to at most $h + H - 1$.

*Proof.* (1) Since $h \ge 1$, $(p + 1)h/H > p h / H$, so $e_p \ge (p + 1) h / H > p h / H \ge a_p$, and $a_p < e_p$ as both are integers. (2) $a_0 = \lfloor 0 \rfloor = 0$ and $e_{H-1} = \lceil h \rceil = h$. (3) Let $z = (p + 1) h / H$. Then $a_{p+1} = \lfloor z \rfloor$ and $e_p = \lceil z \rceil$, and $\lfloor z \rfloor \le \lceil z \rceil \le \lfloor z \rfloor + 1$. (4) By (3) range $p + 1$ starts no later than range $p$ ends, so by (2) the union of the ranges is $[r_1, r_1 + h)$ with no gap. For the lengths, $\sum_{p=0}^{H-1} (e_p - a_p) = (e_{H-1} - a_0) + \sum_{p=0}^{H-2} (e_p - a_{p+1}) \le h + (H - 1)$, by (2) and (3). $\square$

When $h < H$ a row can lie in more than two ranges; for $h = 1$ and $H = 3$ all three ranges are $[r_1, r_1 + 1)$. The sum in item 4 gives the cost bound of the page. The clipping of line L4 to $[0, h_F]$ intersects each range with the rows of the map, which can only shrink the ranges, and makes a range empty only when it lies outside the map.

**Claim 2 (forward).** For every channel $c$ and bin $(p, q)$ with a nonempty clipped range $R_p \times Q_q$, line L6 sets $Y[c][p][q] = \max_{(r, k) \in R_p \times Q_q} F[c][r][k]$ and $S[c][p][q]$ to the first cell in row-major order where the maximum is attained.

*Proof.* The loop visits the cells of the bin in row-major order and replaces the current best only on a strictly larger value. After the loop the best value is the maximum of the visited values, and since later equal values do not replace it, the switch is the first cell with that value. $\square$

**Claim 3 (backward).** Let $L = \sum_{c, p, q} dY[c][p][q] \, Y[c][p][q]$, a function of $F$. At any $F$ where every nonempty bin of every channel has exactly one cell with the largest value, $L$ is differentiable in $F$ and $\partial L / \partial F[c][r][k] = \sum dY[c][p][q]$ over the bins $(p, q)$ with $S[c][p][q] = (r, k)$, which is the value of line L8.

*Proof.* In a bin with a unique largest value at cell $x$, the gap $\delta$ between that value and the second largest is positive. If every cell changes by less than $\delta/2$, the largest value stays at $x$, so $Y[c][p][q] = F[c][x]$ on a neighborhood of $F$. Take the smallest $\delta$ over the finitely many bins. On that neighborhood $L$ is the linear function $\sum dY[c][p][q] \, F[c][S[c][p][q]]$, and its partial derivative in $F[c][r][k]$ is the sum of the $dY[c][p][q]$ whose switch is $(r, k)$. Empty bins add the constant 0. $\square$

When a bin has a tie, $L$ may not be differentiable there; line L8 then returns one subgradient, the one that sends the gradient to the first cell.

**Claim 4 (whole-cell shifts).** Let $G[c][r][k] = F[c][r - \Delta_r][k - \Delta_k]$ for integers $\Delta_r, \Delta_k$, and let $b'$ be the box $b$ moved by $\Delta_k / s$ pixels in $x$ and $\Delta_r / s$ in $y$. If both boxes have nonnegative coordinates and no clipping happens for either box, ROIPOOL(G, b') = ROIPOOL(F, b), and the switches move by $(\Delta_r, \Delta_k)$.

*Proof.* With $\operatorname{round}$ sending halves away from zero, $\operatorname{round}(t + n) = \operatorname{round}(t) + n$ for an integer $n$ whenever $t \ge 0$ and $t + n \ge 0$. Under the stated conditions line L1 adds $\Delta_k$ to $c_1$ and $c_2$ and $\Delta_r$ to $r_1$ and $r_2$, so $h$ and $w$ do not change, and every range of lines L4 and L5 moves by the same amount. Each bin of $G$ then holds the values of the same bin of $F$. $\square$

The same argument shows the rounding error: line L1 moves each side by at most half a cell, that is, by at most $1/(2s)$ pixels, and all boxes whose four sides round to the same cells give the same output.
